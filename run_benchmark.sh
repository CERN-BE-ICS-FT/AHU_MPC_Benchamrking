#!/bin/bash

#SBATCH --job-name=mpc_job
#SBATCH --array=1-8
#SBATCH --cpus-per-task=1
#SBATCH --mem=500M      # Assuming each job requires 500Mb of memory, adjust as necessary
#SBATCH --output=out/job_%j.out
#SBATCH --error=err/job_%j.err
#SBATCH --time=00:01:05

/home/ubuntu/.pyenv/shims/python main.py $SLURM_ARRAY_TASK_ID
