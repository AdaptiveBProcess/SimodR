# ========================================================================================================================================
#                                   GENERATE TABLE STATS FROM DIFFERENT CONFIGURATIONS OF SIMODR
# ========================================================================================================================================

from unicodedata import decimal
from resourceAllocationOptimizer import read_parameters, main_NSGA2, calculate_fitness
import configparser as cp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

input_log = 'PurchasingExample'
input_nonrepeated_resources = False

"""
Parameters used to get the stats reported in the thesis.
generaciones = 100
individuos = 40000 
"""

def generate_stats(input_log, input_nonrepeated_resources):
    
    optimizer = { 
            'no policy': {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'workload':{'cost':  0, 'workload': 1, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 1, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':0}
                    },
            'preference' : {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'workload':{'cost':  0, 'workload': 1, 'flow_time':  0, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':1, 'cooperation':0},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':1, 'cooperation':0},
                    'multiobjective':{'cost': -1, 'workload': 1, 'flow_time': -1, 'waiting_time': -1, 'preference':1, 'cooperation':0}
                    },
            'cooperation' : {
                    'cost':{'cost': -1, 'workload': 0, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'workload':{'cost':  0, 'workload': 1, 'flow_time':  0, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'flow_time':{'cost':  0, 'workload': 0, 'flow_time': -1, 'waiting_time':  0, 'preference':0, 'cooperation':1},
                    'waiting_time':{'cost':  0, 'workload': 0, 'flow_time':  0, 'waiting_time': -1, 'preference':0, 'cooperation':1},
                    'multiobjective':{'cost': -1, 'workload': 1, 'flow_time': -1, 'waiting_time': -1, 'preference':0, 'cooperation':1}
                    }        
    }

    config = cp.ConfigParser(interpolation=None)
    config.read("./config.ini")

    generations = config.get('OPTIMIZATION', 'generations')
    initial_population = config.get('OPTIMIZATION', 'initial_population')
    min_population = config.get('OPTIMIZATION', 'min_population')
    max_population = config.get('OPTIMIZATION', 'max_population')

    data = []
    for policy in optimizer:
        for optimization in optimizer[policy]:
            params = optimizer[policy][optimization]
            read_parameters(input_log, input_nonrepeated_resources, params['cost'], params['workload'], params['flow_time'], params['waiting_time'], \
                             params['preference'],  params['cooperation'])
            print('Parametros leidos')
            solution, scores = main_NSGA2(initial_population, max_population, min_population, generations)
            print('Soluciones obtenidas')
            results = calculate_fitness(solution[0])
            print('Resultados obtenidos')
            row = [input_log, policy, optimization, results['cost_average'], results['flow_time_average'], results['waiting_time_average'], results['workload_average']]
            data.append(row)

    results_baseline = calculate_fitness('BASELINE')
    data.append([input_log, 'baseline', 'baseline', results_baseline['cost_average'], results_baseline['flow_time_average'], results_baseline['waiting_time_average'], results_baseline['workload_average']])
    
    data_df = pd.DataFrame(data = data, columns = ['Log', 'Policy', 'Optimization', 'Cost', 'Flow time', 'Waiting', 'Workload'])
    data_df[['Cost', 'Flow time', 'Waiting', 'Workload']] = data_df[['Cost', 'Flow time', 'Waiting', 'Workload']].astype(float)
    filename = r'C:\Users\DanielBaron\Desktop\CursosMaestria\AsistenciaGraduada\SimodR\stats\{}_estadisticas.csv'.format(input_log)
    data_df.to_csv(filename, sep='|', decimal=',', index=False)
    
    baseline_mat = data_df[data_df['Policy'] == 'baseline'][['Cost', 'Flow time', 'Waiting','Workload']]
    results_mat = data_df[data_df['Policy'] != 'baseline']
    
    multiobjective_mat = results_mat[results_mat['Optimization'] == 'multiobjective']
    norm_results_mat = results_mat
    
    def generate_graph(data, policy, optimize, include_baseline=False):
        n = len(data[0])
        X = np.arange(n)
        fig = plt.figure()
        
        ax = fig.add_axes([0,0,1,1])
    
        ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
        ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
        if include_baseline:
            ax.bar(X + 0.5, data[2], color = 'r', width = 0.25)
            ax.set_title('Optimize {} - {} Policy'.format(optimize.capitalize(), policy.capitalize()))
        else:
            ax.set_title('{} - {} Policy'.format(optimize.capitalize(), policy.capitalize()))
        
        ax.set_xticks([r + 0.25 for r in range(n)])
        ax.set_xticklabels(['Cost', 'Flow time', 'Waiting','Workload'])
        if include_baseline:
            ax.legend(labels=[optimize.capitalize(), 'Multiobjective', 'Baseline'], loc='best')
        else:
            ax.legend(labels=[optimize.capitalize(), 'Multiobjective'], loc='best')
        ax.grid()
        ax.set_ylim([0, 2])
        if include_baseline:
            fig.savefig('stats/Optimize_{}_{}.png'.format(optimize.capitalize(), policy.capitalize().replace(' ','_')), bbox_inches='tight', dpi=150)
        else:
            fig.savefig('stats/{}_{}.png'.format(optimize.capitalize(), policy.capitalize().replace(' ','_')), bbox_inches='tight', dpi=150)
    
    for col in baseline_mat.columns:
        baseline_value = float(baseline_mat[col].values[0])
        norm_results_mat[col] = norm_results_mat[col].apply(lambda x: x/max(x, baseline_value ))
    
    for policy in norm_results_mat['Policy'].unique():
        block = norm_results_mat[norm_results_mat['Policy']==policy]
        for optimize in norm_results_mat['Optimization'].unique():
            if optimize != 'multiobjective':
                minimize = block[norm_results_mat['Optimization']==optimize][['Cost', 'Flow time', 'Waiting','Workload']].values
                multiobjective = block[norm_results_mat['Optimization']=='multiobjective'][['Cost', 'Flow time', 'Waiting','Workload']].values
                data_min = [list(minimize[0]), list(multiobjective[0]), [1, 1, 1, 1]]
                generate_graph(data_min, policy, optimize, True)
    
    for policy in multiobjective_mat['Policy'].unique():
        block = multiobjective_mat[multiobjective_mat['Policy']==policy]
        baseline = []
        multiobjective = []
        for col in baseline_mat.columns:
            multiobjective_value = float(block[col].values[0])
            baseline.append(baseline_mat[col].values[0]/multiobjective_value)
            multiobjective.append(multiobjective_value/multiobjective_value)
        generate_graph([baseline, multiobjective], policy, 'Baseline', False)
        
generate_stats(input_log, input_nonrepeated_resources)





