from __future__ import with_statement
import ConfigParser

cfg = ConfigParser.ConfigParser()

cfg.add_section('is2064645')
# jobs file directories
cfg.set('is2064645', 'job_examples_dir', "/home/soizic/svn/brainvisa/source/soma/soma-workflow/trunk/test/jobExamples")
cfg.set('is2064645', 'job_output_dir', "/home/soizic/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)


cfg.add_section('soizic-vaio')
# jobs file directories
cfg.set('soizic-vaio', 'job_examples_dir', "/home/soizic/projets/jobExamples/")
cfg.set('soizic-vaio', 'job_output_dir', "/home/soizic/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)
cfg.set('soizic-vaio', 'mode', 'local')
cfg.set('soizic-vaio', 'ressource_id', 'soizic_home_cluster')
cfg.set('soizic-vaio', 'python', 'python')

cfg.add_section('is143016')
# jobs file directories
cfg.set('is143016', 'job_examples_dir', "/home/sl225510/svn/brainvisa/soma/soma-pipeline/trunk/test/jobExamples/")
cfg.set('is143016', 'job_output_dir', "/home/sl225510/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)
cfg.set('is143016', 'mode', 'local')
cfg.set('is143016', 'ressource_id', 'neurospin_test_cluster')
# python: to avoid the site package error in the jobs standard error output
cfg.set('is143016', 'python', "python")#/i2bm/research/Mandriva-2008.0-i686/bin/python") 
 
#cfg.add_section('is143016')
## jobs file directories
#cfg.set('is143016', 'job_examples_dir', "/home/sl225510/svn/brainvisa/soma/soma-pipeline/trunk/test/jobExamples/")
#cfg.set('is143016', 'job_output_dir', "/home/sl225510/output/")
## mode: 'remote' or 'local' (the login and password will be asked in the remote case)
#cfg.set('is143016', 'mode', 'remote')
#cfg.set('is143016', 'ressource_id', 'DSV_cluster')
## python: to avoid the site package error in the jobs standard error output
#cfg.set('is143016', 'python', "/usr/bin/python") 
 
#cfg.add_section('is143016')
## jobs file directories
#cfg.set('is143016', 'job_examples_dir', "/home/sl225510/svn/brainvisa/soma/soma-pipeline/trunk/test/jobExamples/")
#cfg.set('is143016', 'job_output_dir', "/home/sl225510/output/")
## mode: 'remote' or 'local' (the login and password will be asked in the remote case)
#cfg.set('is143016', 'mode', 'remote')
#cfg.set('is143016', 'ressource_id', 'HiPiP_cluster')
## python: to avoid the site package error in the jobs standard error output
#cfg.set('is143016', 'python', "/home/cea/brainvisa/bin/python") 
 
 
#cfg.add_section('is206464')
## jobs file directories
#cfg.set('is206464', 'job_examples_dir',  "/home/soizic/svn/brainvisa/source/soma/soma-pipeline/trunk/test/jobExamples/")
#cfg.set('is206464', 'job_output_dir', "/home/soizic/output/")
## mode: 'remote' or 'local' (the login and password will be asked in the remote case)
#cfg.set('is206464', 'mode', 'remote')
#cfg.set('is206464', 'ressource_id', 'neurospin_test_cluster')
## python: to avoid the site package error in the jobs standard error output
#cfg.set('is206464', 'python', "/i2bm/research/Mandriva-2008.0-i686/bin/python")


cfg.add_section('is206464')
# jobs file directories
cfg.set('is206464', 'job_examples_dir',  "/home/soizic/svn/brainvisa/source/soma/soma-pipeline/trunk/test/jobExamples/")
cfg.set('is206464', 'job_output_dir', "/home/soizic/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)
cfg.set('is206464', 'mode', 'remote')
cfg.set('is206464', 'ressource_id', 'DSV_cluster')
# python: to avoid the site package error in the jobs standard error output
cfg.set('is206464', 'python', "python")


#cfg.add_section('is206464')
##jobs file directories
#cfg.set('is206464', 'job_examples_dir',  "/home/soizic/svn/brainvisa/source/soma/soma-pipeline/trunk/test/jobExamples/")
#cfg.set('is206464', 'job_output_dir', "/home/soizic/output/")
##mode: 'remote' or 'local' (the login and password will be asked in the remote case)
#cfg.set('is206464', 'mode', 'remote')
#cfg.set('is206464', 'ressource_id', 'HiPiP_cluster')
##python: to avoid the site package error in the jobs standard error output
#cfg.set('is206464', 'python', "python")


cfg.add_section('gabriel.intra.cea.fr')
# jobs file directories
cfg.set('gabriel.intra.cea.fr', 'job_examples_dir',  "/home/sl225510/jobExamples/")
cfg.set('gabriel.intra.cea.fr', 'job_output_dir', "/home/sl225510/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)
cfg.set('gabriel.intra.cea.fr', 'mode', 'local')
cfg.set('gabriel.intra.cea.fr', 'ressource_id', 'DSV_cluster')
# python: to avoid the site package error in the jobs standard error output
cfg.set('gabriel.intra.cea.fr', 'python', "/usr/bin/python")

cfg.add_section('hipip0')
# jobs file directories
cfg.set('hipip0', 'job_examples_dir',  "/home/cea/soma-jobs-test/jobExamples/")
cfg.set('hipip0', 'job_output_dir', "/home/cea/soma-jobs-test/output/")
# mode: 'remote' or 'local' (the login and password will be asked in the remote case)
cfg.set('hipip0', 'mode', 'local')
cfg.set('hipip0', 'ressource_id', 'HiPiP_cluster')
# python: to avoid the site package error in the jobs standard error output
cfg.set('hipip0', 'python', "/home/cea/brainvisa/bin/python")



with open('TestJobs.cfg', 'wb') as configfile:
    cfg.write(configfile)

