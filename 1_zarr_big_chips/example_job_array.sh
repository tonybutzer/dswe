#!/bin/bash
#SBATCH --job-name=python_array_job    # Job name
#SBATCH --output=python_array_job.%A_%a.out    # Output file name with job ID (%A) and task ID (%a)
#SBATCH --error=python_array_job.%A_%a.err    # Error file name with job ID (%A) and task ID (%a)
#SBATCH --array=1-100    # Number of tasks in the array

# Load any necessary modules
# For example, if you need a specific Python environment:
# module load python/3.8.2

# Your Python script
PYTHON_SCRIPT="your_python_script.py"

# Assuming your Python script takes an argument to specify the run number
# The task ID (%a) will be passed as an argument to the Python script
python $PYTHON_SCRIPT $SLURM_ARRAY_TASK_ID


### run with sbatch submit_job_array.sh
