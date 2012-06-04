from mpi4py import MPI
from soma.workflow import scheduler, constants
from soma.workflow.client import Job
from soma.workflow.engine_types import EngineJob
import time
import threading
import subprocess
import atexit


def slave_loop(communicator, cpu_count=1):
    status = MPI.Status()
    to_send = True
    while True:
        processes = {}
        if to_send:
            communicator.send(cpu_count, dest=0,
                             tag=MPIScheduler.JOB_REQUEST)
            to_send = False
        communicator.Probe(source=MPI.ANY_SOURCE,
                           tag=MPI.ANY_TAG, status=status)
        print "job request slave " + repr(communicator.Get_rank())
        t = status.Get_tag()
        if t == MPIScheduler.job_sending:
            job_list = communicator.recv(source=0, tag=t)
            for j in job_list:
                process = scheduler.LocalScheduler.create_process(j)
                processes[j.job_id] = process
        elif t == MPIScheduler.NO_JOB:
            communicator.recv(source=0, tag=t)
            print "received no job " + repr(processes)
            time.sleep(1)
        elif t == MPIScheduler.EXIT_SIGNAL:
            communicator.send('STOP', dest=0, tag=MPIScheduler.EXIT_SIGNAL)
            print "STOP !!!!! received (slave %d)" % communicator.Get_rank()
            break
        else:
            raise Exception('Unknown tag')
        returns = {}
        for job_id, process in processes.iteritems():
            if process == None:
                returns[job_id] = None
            else:
                returns[job_id] = process.wait()
        if returns:
            communicator.send(returns, dest=0,
                              tag=MPIScheduler.job_result)


class MPIScheduler(scheduler.Scheduler):
    '''
    Allow to submit, kill and get the status of jobs.
    '''
    parallel_job_submission_info = None

    logger = None

    is_sleeping = None

    _proc_nb = None

    _queue = None

    _jobs = None

    _processes = None

    _status = None

    _exit_info = None

    _loop = None

    _interval = None

    _lock = None

    JOB_REQUEST = 11
    job_sending = 12
    EXIT_SIGNAL = 13
    job_kill = 14
    job_result = 15
    NO_JOB = 16

    def __init__(self, communicator, interval=1):
        super(MPIScheduler, self).__init__()

        self._communicator = communicator
        self.parallel_job_submission_info = None
        # self._proc_nb = proc_nb
        self._queue = []
        self._jobs = {}
        # self._processes = {}
        self._status = {}
        self._exit_info = {}
        self._lock = threading.RLock()
        self.stop_thread_loop = False
        self._interval = interval

        def master_loop(self):
            self._stopped_saves = 0
            while not self.stop_thread_loop:
                with self._lock:
                    self._master_iteration()
                # time.sleep(self._interval)

        self._loop = threading.Thread(name="scheduler_loop",
                                      target=master_loop,
                                      args=[self])
        self._loop.setDaemon(True)
        self._loop.start()

        #atexit.register(MPIScheduler.end_scheduler_thread, self)

    def end_scheduler_thread(self):
        with self._lock:
            self.stop_thread_loop = True
            self._loop.join()
            print "Soma scheduler thread ended nicely."

    def _master_iteration(self):
        print "master iteration"
        MPIStatus = MPI.Status()
        #if not self._queue:
        #    return
        self._communicator.Probe(source=MPI.ANY_SOURCE,
                                     tag=MPI.ANY_TAG,
                                     status=MPIStatus)
        t = MPIStatus.Get_tag()
        if t == MPIScheduler.JOB_REQUEST:
            print "Master received the JOB_REQUEST signal"
            s = MPIStatus.Get_source()
            if not self._queue:
                print "No job for now"
                self._communicator.recv(source=s, 
                                        tag=MPIScheduler.JOB_REQUEST)
                self._communicator.send("No job for now", 
                                        dest=s,
                                        tag=MPIScheduler.NO_JOB)            
                time.sleep(self._interval)
            else:
                self._communicator.recv(source=s, tag=MPIScheduler.JOB_REQUEST)
                job_id = self._queue.pop(0)
                job_list = [self._jobs[job_id]]
                self._communicator.send(job_list, dest=s,
                                      tag=MPIScheduler.job_sending)
                for j in job_list:
                    self._status[j.job_id] = constants.RUNNING
        elif t == MPIScheduler.job_result:
            print "Master received the job_result signal"
            s = MPIStatus.Get_source()
            results = self._communicator.recv(source=s,
                                              tag=MPIScheduler.job_result)
            for job_id, ret_value in results.iteritems():
                if ret_value != None:
                    self._exit_info[job_id] = (
                                           constants.FINISHED_REGULARLY,
                                           ret_value, None, None)
                    self._status[job_id] = constants.DONE
                else:
                    self._exit_info[job_id] = (constants.EXIT_ABORTED,
                                           None, None, None)
                    self._status[job_id] = constants.FAILED
        elif t == MPIScheduler.EXIT_SIGNAL:
            print "Master received the EXIT_SIGNAL"
            self._stopped_slaves = self._stopped_slaves + 1
            if self._stopped_slaves == self._communicator.size -1:
              self.stop_thread_loop = True
        else:
          print "Unknown tag"
        #else:
        #    print "sleep"
        #    time.sleep(self._interval)

    def sleep(self):
        self.is_sleeping = True

    def wake(self):
        self.is_sleeping = False

    def clean(self):
        pass

    def job_submission(self, job):
        '''
        * job *EngineJob*
        * return: *string*
        Job id for the scheduling system (DRMAA for example)
        '''
        if not job.job_id or job.job_id == -1:
            raise Exception("Invalid job: no id")
        with self._lock:
            #print "job submission " + repr(job.job_id)
            self._queue.append(job.job_id)
            self._jobs[job.job_id] = job
            self._status[job.job_id] = constants.QUEUED_ACTIVE
            self._queue.sort(key=lambda job_id: self._jobs[job_id].priority,
                             reverse=True)
        return job.job_id

    def get_job_status(self, scheduler_job_id):
        '''
        * scheduler_job_id *string*
        Job id for the scheduling system (DRMAA for example)
        * return: *string*
        Job status as defined in constants.JOB_STATUS
        '''
        if not scheduler_job_id in self._status:
            raise Exception("Unknown job.")
        status = self._status[scheduler_job_id]
        return status

    def get_job_exit_info(self, scheduler_job_id):
        '''
        * scheduler_job_id *string*
        Job id for the scheduling system (DRMAA for example)
        * return: *tuple*
        exit_status, exit_value, term_sig, resource_usage
        '''
        with self._lock:
            exit_info = self._exit_info[scheduler_job_id]
            del self._exit_info[scheduler_job_id]
        return exit_info

    def kill_job(self, scheduler_job_id):
        '''
        * scheduler_job_id *string*
        Job id for the scheduling system (DRMAA for example)
        '''
        # TODO
        pass

if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.size
    

print rank
# master code
if rank == 0:
    # on initie les differents process Engine, etc...
    sch = MPIScheduler(comm, interval=1)
    # a partir d'ici on gere le schedeling (ie. soumission, stop, status)
    import numpy as np
    max_elt = 10
    r_param = abs(np.random.randn(max_elt))
    tasks = []
    for r in r_param:
        mon_job = EngineJob(Job(command=['echo', '%f' % r], name="job"),
                            queue='toto')
        mon_job.job_id = '%s ' % mon_job.command
        tasks.append(mon_job)
        sch.job_submission(mon_job)
    ## status = MPI.Status()

    ## for task in tasks:
    ##     # print 'ask me.'
    ##     send_task = False
    ##     while send_task == False:
    ##         comm.Probe(source=MPI.ANY_SOURCE, tag=11, status=status)
    ##         s = status.Get_source()
    ##         data = comm.recv(source=s, tag=11)
    ##         # print "receive %s from %d " % (data, s)
    ##         if data == 'JOB_PLEASE':
    ##             comm.send(task, dest=s, tag=12)
    ##         else:
    ##             print 'bad message from %d' % s
    ##         send_task = True
    time.sleep(20)
    for slave in range(1, comm.size):
        print "STOP STOP STOP STOP STOP STOP STOP STOP slave " + repr(slave)
        comm.send('STOP', dest=slave, tag=MPIScheduler.EXIT_SIGNAL)
    while not sch.stop_thread_loop:
        time.sleep(1)
    print "### master ends ###"
# slave code
else:
    slave_loop(comm)
