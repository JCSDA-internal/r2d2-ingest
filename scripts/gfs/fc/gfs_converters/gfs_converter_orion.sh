#!/usr/bin/bash
#SBATCH --job-name=convert_gfs
#SBATCH -p orion
#SBATCH -A da-cpu
#SBATCH -q batch
#SBATCH --ntasks=24
#SBATCH --cpus-per-task=1
#SBATCH --time=0:30:00

source /work/noaa/da/$USER/jedi/setup.sh

ulimit -s unlimited
ulimit -v unlimited

export SLURM_EXPORT_ENV=ALL
export HDF5_USE_FILE_LOCKING=FALSE

# This path must not be jedipara because the fv3jedi_convertstate.x executable must write a log file in order to
# complete successfully. It does this in the cwd which is $JEDI_TEST.
export JEDI_BIN=/work/noaa/da/$USER/jedi/jedi-bundle/build/bin
export JEDI_TEST=/work/noaa/da/$USER/jedi/jedi-bundle/build/fv3-jedi/test
export OOPS_TRACE=0
export OOPS_DEBUG=0

# Change dir to $JEDI_TEST so that the relative paths in the YAML template are correct.
cd $JEDI_TEST

# Call the fv3jedi_convertstate.x executable using the YAML file path passed to this bash script.
srun --ntasks=24 --cpu_bind=core --distribution=block:block $JEDI_BIN/fv3jedi_convertstate.x $1

exit 0