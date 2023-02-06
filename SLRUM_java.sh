#!/bin/bash

# ###### Zona de Parámetros de solicitud de recursos a SLURM  ############################
#
#SBATCH --job-name=SimodRPurchasing
#SBATCH -p bigmem
#SBATCH -N 1
#SBATCH	-n 1
#SBATCH	--cpus-per-task=32
#SBATCH	--mem-per-cpu=16000
#SBATCH	--time=96:00:00
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
java -jar external_tools/ScyllaNew/Scylla_V6.jar --config=inputs/PurchasingExampleScyllaGlobalConfig.xml --bpmn=inputs/PurchasingExample.bpmn --sim=inputs/PurchasingExampleScyllaSimuConfig.xml --output=scylla_results_baseline/ --enable-bps-logging

java -jar external_tools/ScyllaNew/Scylla_V6.jar --config=inputs/ProductionScyllaGlobalConfig.xml --bpmn=inputs/Production.bpmn --sim=inputs/ProductionScyllaSimuConfig.xml --output=scylla_results_baseline/ --enable-bps-logging

java -jar external_tools/ScyllaNew/Scylla_V6.jar --config=inputs/ConsultaDataMining201618ScyllaGlobalConfig.xml --bpmn=inputs/ConsultaDataMining201618.bpmn --sim=inputs/ConsultaDataMining201618ScyllaSimuConfig.xml --output=scylla_results_baseline/ --enable-bps-logging

python generateStats.py
########################################################################################