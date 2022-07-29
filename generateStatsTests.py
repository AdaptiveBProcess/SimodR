import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


input_log = 'PurchasingExample'
filename = r'C:\Users\DanielBaron\Desktop\CursosMaestria\AsistenciaGraduada\SimodR\stats\{}_estadisticas.csv'.format(input_log)
data_df = pd.read_csv(filename, sep='|', decimal=',')

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