#!/bin/bash

#SBATCH --job-name=mpc_job
#SBATCH --array=0-44999
#SBATCH --cpus-per-task=1
#SBATCH --ntasks=1               
#SBATCH --mem=1G
#SBATCH --output=out/output_%A_%a.out
#SBATCH --error=err/error_%A_%a.err 
#SBATCH --time=00:01:30

/home/ubuntu/.pyenv/shims/python main.py $SLURM_ARRAY_TASK_ID

