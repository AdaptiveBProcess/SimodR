#!/bin/bash

# ###### Zona de Parámetros de solicitud de recursos a SLURM  ############################
#
#SBATCH --job-name=SimodRProd
#SBATCH -p long
#SBATCH -N 1
#SBATCH	-n 1
#SBATCH	--cpus-per-task=32
#SBATCH	--mem-per-cpu=16000
#SBATCH	--time=144:00:00
#SBATCH -o logs_job_%j.txt
#
# ########################################################################################

############################## Zona de carga de Módulos ################################
module load anaconda/python3.9 
module load jdk/11.0.14
module load java/1.8.0_311
module load r/4.2.1

########################################################################################

# ################## Zona de ejecución de código #######################################
source activate SimodR
python generateStatsTests.py
########################################################################################