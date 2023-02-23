# ========================================================================================================================================
#                                   GENERATE TABLE STATS FROM DIFFERENT CONFIGURATIONS OF SIMODR
# ========================================================================================================================================

from unicodedata import decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from support_modules import generate_graphs as gg
from glob import glob

"""
iterations = [{ 'input_log' : 'PurchasingExample', 'time_format' : '%Y-%m-%dT%H:%M:%S.000', 'ns_include' : True},
              { 'input_log' : 'Production', 'time_format' : '%Y-%m-%dT%H:%M:%S', 'ns_include' : False},
              { 'input_log' : 'ConsultaDataMining201618', 'time_format' : '%Y-%m-%dT%H:%M:%S', 'ns_include' : False}]
"""

iterations = [{ 'input_log' : 'Production', 'time_format' : '%Y-%m-%dT%H:%M:%S', 'ns_include' : False}]

"""
Parameters used to get the stats reported in the thesis.
generaciones = 100
individuos = 40000 
"""

def generate_stats(input_log, time_format, ns_include):

    #""" Flowtime y cost
    
    optimizer = { 
            'preference' : {
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':1, 'cooperation':0},
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':1, 'cooperation':0}
                    },
            
            'no policy': {
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':0},
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':0}
                    },
            'cooperation' : {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':1},
                    'multiobjective':{'cost': -1, 'workload': 0, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':1}
                    }     
    }
    
    generations = 100
    initial_population = 20
    min_population = 20
    max_population = 40000
    
    """
     
    optimizer = { 
            'preference' : {
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    }  
    } 
    
    generations = 3
    initial_population = 5    
    min_population = 5
    max_population = 10
    
    #"""
    
    for policy in optimizer:
        for optimization in optimizer[policy]:

            params = optimizer[policy][optimization]
            
            with open('config_gen.ini', 'r') as file:
                text = file.read()
                
            text = text.replace('{filename}', input_log)
            text = text.replace('{log}', input_log)
            text = text.replace('{log}', str(params['preference'])).replace('{time_format}', time_format)
            text = text.replace('{preference}', str(params['preference'])).replace('{cooperation}', str(params['cooperation']))
            text = text.replace('{cost}', str(params['cost'])).replace('{workload}', str(params['workload']))
            text = text.replace('{flowtime}', str(params['flow_time'])).replace('{waitingtime}', str(params['waiting_time']))
            text = text.replace('{generations}', str(generations)).replace('{initialpopulation}', str(initial_population))
            text = text.replace('{minpopulation}', str(min_population)).replace('{maxpopulation}', str(max_population))
            text = text.replace('{ns_include}', str(ns_include))

            with open('config.ini', 'w') as file:
                file.write(text)
                
            files = [x for x in glob('inputs/*') if x.split('.')[-1] not in ['bpmn', 'json', 'xes', 'csv']]
            for file in files:
                os.remove(file)

            os.system('python3 main.py')
    
for iteration in iterations:
  input_log = iteration['input_log']
  time_format = iteration['time_format'] 
  ns_include = iteration['ns_include']  
  generate_stats(input_log, time_format, ns_include)

print('Generating graphs for experiments')
gg.generate_graphs_exps()





