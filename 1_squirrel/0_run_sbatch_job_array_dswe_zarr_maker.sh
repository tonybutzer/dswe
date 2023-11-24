#! /bin/bash

len=$(wc -l dancecard.txt | awk '{print $1}')
echo $len

#SBATCH --account=butzer
#SBATCH --job-name=myarrayjob
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --array=1-$(len)

# Specify the path to the config file
config=/path/to/config.txt

# Extract the sample name for the current $SLURM_ARRAY_TASK_ID
sample=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $2}' $config)

# Extract the sex for the current $SLURM_ARRAY_TASK_ID
sex=$(awk -v ArrayTaskID=$SLURM_ARRAY_TASK_ID '$1==ArrayTaskID {print $3}' $config)

# Print to a file a message that includes the current $SLURM_ARRAY_TASK_ID, the same name, and the sex of the sample
echo "This is array task ${SLURM_ARRAY_TASK_ID}, the sample name is ${sample} and the sex is ${sex}." >> output.txt
