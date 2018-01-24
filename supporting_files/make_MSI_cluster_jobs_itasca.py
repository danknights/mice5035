#!/usr/bin/env python 

"""A simple qsub based cluster submission script."""

__author__ = "Jens Reeder"
__copyright__ = "Copyright 2011, The QIIME Project" 
__credits__ = ["Jens Reeder", "Rob Knight", "Hu Huang"]#remember to add yourself if you make changes
__license__ = "GPL"
__version__ = "1.7.0"
__maintainer__ = "Jens Reeder"
__email__ = "jens.reeder@gmail.com"
__status__ = "Release"

from os.path import exists
from os import remove, rename, rmdir, makedirs
from subprocess import Popen, PIPE, STDOUT
import math

from cogent.util.misc import app_path, create_dir
from cogent.app.util import ApplicationNotFoundError
from qiime.util import get_tmp_filename

# qsub template
#requires format string (walltime, nodes, ncpus, mem, queue, job_name, keep_output, command)
QSUB_TEXT = """# Walltime Limit: hh:nn:ss 
#PBS -l walltime=%s 

# Node Specification:
#PBS -l nodes=%d:ppn=%d
#PBS -l mem=%dgb

# Queue: Defaults to friendlyq 
#PBS -q %s 

# Mail: options are (a) aborted, (b) begins execution, (e) ends execution
# use -M <email> for additional recipients
# supress email notification

# Job Name:
#PBS -N %s 

# Keep output
#PBS -k %s

echo ------------------------------------------------------
echo PBS: qsub is running on $PBS_O_HOST
echo PBS: originating queue is $PBS_O_QUEUE
echo PBS: executing queue is $PBS_QUEUE
echo PBS: working directory is $PBS_O_WORKDIR
echo PBS: execution mode is $PBS_ENVIRONMENT
echo PBS: job identifier is $PBS_JOBID
echo PBS: job name is $PBS_JOBNAME
echo PBS: node file is $PBS_NODEFILE
echo PBS: current home directory is $PBS_O_HOME
echo PBS: PATH = $PBS_O_PATH
echo ------------------------------------------------------
# start time
date

cd $PBS_O_WORKDIR
module load qiime/1.8.0

# set up nodefile
uniq $PBS_NODEFILE pbs_nodefile.txt

module load parallel
cat %s | parallel --jobs %d --joblog %s

%s

# end time
date
""" 

def make_jobs(commands, job_prefix, queue, jobs_dir="jobs/",
              walltime="06:00:00", nodes=1, ncpus=16, mem=16, keep_output="oe"):
    """prepare qsub text files.
    
    command: list of commands
    
    job_prefix: a short, descriptive name for the job.

    queue: name of the queue to submit to
    
    jobs_dir: path to directory where job submision scripts are written

    walltime: the maximal walltime 
    
    ncpus: number of cpus
    
    nodes: number of nodes
    
    keep_output: keep standard error, standard out, both, or neither
                 o=std out, e=std err, oe=both, n=neither
    """

    filenames=[]
    create_dir(jobs_dir)
    job_list_name = get_tmp_filename(tmp_dir=jobs_dir, prefix=job_prefix+"_joblist_", suffix = ".txt")
    
    job_log_name = get_tmp_filename(tmp_dir=jobs_dir, prefix=job_prefix+"_prallel_job_log", suffix = ".txt")
    
    out_fh_list = open(job_list_name,"w")
    
    for command in commands[0:len(commands)-1]:
        out_fh_list.write(command+"\n")

    out_fh_list.close()

    job_name = get_tmp_filename(tmp_dir=jobs_dir, prefix=job_prefix+"_", suffix = ".txt")

    out_fh = open(job_name,"w")

    #num_nodes = int(math.ceil((len(commands)-1)/8.0))
    # If you use the lab queue, then change the num_nodes and ncpus as:
    num_nodes = 1
    ncpus = len(commands) - 1
    
    out_fh.write(QSUB_TEXT % (walltime, num_nodes, ncpus, mem, queue, job_prefix, keep_output, job_list_name, len(commands)-1, job_log_name, commands[-1]))

    out_fh.close()

    filenames.append(job_name)

    return filenames

def submit_jobs(filenames, verbose=False):
    """Submit jobs in filenames.

    filenames: list of prepared qsub job scripts, ready to be submitted

    verbose: a binary verbose flag
    """
    if(not app_path("qsub")):
        raise ApplicationNotFoundError,"qsub not found. Can't submit jobs."
    
    for file in filenames:        
        command = 'qsub %s' % file
        result = Popen(command, shell=True, universal_newlines=True,\
                           stdout=PIPE, stderr=STDOUT).stdout.read()
        if verbose:
            print result
