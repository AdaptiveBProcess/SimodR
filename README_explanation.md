
# Configuration

## System Prerequisites

- Python 3.x
- Java SDK 1.8
- R 4.x
- RTools 4.x
- Anaconda Distribution
- Git

## Configuration of the environment

Clone the github repository.
```
git clone https://github.com/AdaptiveBProcess/SimodR_V2.git
```

Enter to the folder created when you clone the repository.
```
cd SimodR_V2
```

Create an environment using .yml file.
```
conda env create -f SimodResourcesEnv.yml
```
Activate the environment created.
```
conda activate SimodR
```

Install the python modules needed to execute SimodR using requirements file.
```
pip install -r requirements.txt
```

## Parameters specification

Once the environment is configured, you can run SimodR but you need to specify certain parameters such as log name, policy, optimization target, time format of event log traces, etc.

To configure a single run of SimodR, you need to specify all the parameters included in the config.ini file. Once all parameters are specified, it is only necessary to run the main.py script.
```
python main.py
```

However, if you want to run optimization of multiple event logs with different optimization targets, you can use generateStats.py. In this script you need to specify the different optimization targets and policy as follows:

```
optimizer = { 
            'no policy': {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':0}
                    },
            'preference' : {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':1, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':1, 'cooperation':0}
                    },
            'cooperation' : {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':1},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':1}
                    }     
    }
```
Each key in that dictionary corresponds to a certain policy to be executed in SimodR. Within the value of each key, there is a dictionary where each key corresponds to a certain optimization objective and the value specifies the parameters needed to run the simulation with the specified optimization objective. In addition, you need to specify which policy you want to apply in the execution. 

For example, if you want to optimize the cost using the Cooperation policy, assign the following values.

```
cost : {'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':1}
```

In addition, if you want to execute multiobjective optimization, you assign to cost -1, to flow_time -1 and waiting_time -1.

```
multiobjective : {'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':1, 'cooperation':0}
```

Additionally, you can optimize different logs using the generateStats.py script. If you want to optimize more than one Log, you must modify the iteration list. This list contains the dictionary of parameters needed to run the simulation. These parameters are the log name, the time format of the event log file, and the ns_include parameter that specifies the version of the event log format. For example, if you want to run the Production and PurchasingExample logs you must specify the following items:

```python 
iterations = [{ 'input_log' : 'PurchasingExample', 'time_format' : '%Y-%m-%dT%H:%M:%S.000', 'ns_include' : True},
              { 'input_log' : 'Production', 'time_format' : '%Y-%m-%dT%H:%M:%S', 'ns_include' : False}]
```

Finally, you have to specify the generations, initial_population, min_population and max_population related to the NSGA2 algorithm.

Once you have all the settings in the script, run the script as follows.

```
python generateStats.py
```

The above run generates the performance metrics and generates graphs of those metrics. You can find those graphs in the stats folder. There, you are going to find a folder for each log run.
