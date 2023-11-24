#!/bin/sh

# We assume running this from the script directory
job_directory=$PWD/.job

for lizard in `cat dancecard.txt` ; do

    job_file="${job_directory}/${lizard}.job"
  
    echo "#!/bin/bash
#SBATCH --account=butzer
#SBATCH --time=00:20:00
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=butzer@contractor.usgs.gov
#SBATCH --job-name=${lizard}.job
#SBATCH --output=.out/${lizard}.out
#SBATCH --error=.out/${lizard}.err
source /home/ec2-user/mambaforge/bin/activate water
## source /home/ec2-user/tony/source_conda.src
## source /home/butzer/miniconda3/bin/activate nlcd2
python3 0_squirrel.py ${lizard}" > $job_file
    sbatch $job_file

done
