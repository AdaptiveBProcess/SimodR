import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os


def generate_graphs_exps():

  files = glob('stats/stats_files/*.csv')
  input_logs = list(set([x.split('\\')[-1].split('_')[0] for x in files]))

  for input_log in input_logs:
      
    print(input_log)
    
    if not os.path.exists('stats/graphs/'):
        os.mkdir('stats/graphs/')
    if not os.path.exists('stats/graphs/{}/'.format(input_log)):
        os.mkdir('stats/graphs/{}/'.format(input_log))
    files_log = [x for x in files if input_log in x]
    data_df = pd.read_csv(files_log[0], sep=',', decimal=',', index_col=False)
    for file_log in files_log[1:]:
        data_df_tmp = pd.read_csv(file_log, sep=',', decimal=',', index_col=False)
        data_df = pd.concat([data_df, data_df_tmp])

    id_vars, value_vars = ['Log', 'Policy', 'Optimization'], ['Cost', 'Flow time', 'Waiting','Workload']
    data_df['Optimization'] = data_df['Optimization'].str.replace('_', ' ').str.capitalize()
    data_df[value_vars] = data_df[value_vars].astype(float)

    results_mat = data_df[data_df['Policy'] != 'Baseline']
    multiobjective_mat = results_mat[results_mat['Optimization'] == 'Multiobjective']
    df_results = pd.melt(data_df, id_vars=id_vars, value_vars=value_vars, var_name = 'Performance Metric', value_name='Performance Metric Value')


    try:
        # Graphs for experiment 1
        fig = plt.figure(figsize=(20, 20))
        df_exp1 = df_results[df_results['Policy'].isin(['No policy', 'Baseline'])]
        df_exp1 = df_exp1.round({'Performance Metric Value':3})

        for j, metric in enumerate(df_exp1['Performance Metric'].drop_duplicates()):

            ax = fig.add_subplot(2, 2, j+1)

            df_exp1_tmp = df_exp1[df_exp1['Performance Metric'].isin([metric])]
            
            graph_title = '{} : Trade-Off in {} metric'.format(input_log, metric.capitalize().replace('_', ' '))
            ax = sns.barplot(ax=ax, x="Performance Metric", y="Performance Metric Value", hue="Optimization", data=df_exp1_tmp)
            for i in ax.containers:
                ax.bar_label(i,)
            plt.grid()
            plt.title(graph_title)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

        fig.savefig('stats/graphs/{}/Trade-Off in Optimizations.png'.format(input_log), bbox_inches='tight', dpi=150)
    except:
        pass

    try:
        # Graphs for experiment 2
        for col in ['Cost', 'Flow time', 'Waiting', 'Workload']:
            max_col = np.max(multiobjective_mat[col])
            multiobjective_mat[col] = multiobjective_mat[col]/max_col

        df_exp2 = pd.melt(multiobjective_mat, id_vars=id_vars, value_vars=value_vars, var_name = 'Performance Metric', value_name='Performance Metric Value')
        df_exp2 = df_exp2.round({'Performance Metric Value':3})

        fig = plt.figure(figsize=(10, 6))
        ax = sns.barplot(x="Performance Metric", hue="Policy", y="Performance Metric Value", data=df_exp2)
        for i in ax.containers:
                ax.bar_label(i,)
        plt.grid()
        plt.title('{} : Multiobjective Optimization by Allocation Policy'.format(input_log))
        plt.title('Normalized Metric Value')
        fig.savefig('stats/graphs/{}/Multiobjective optimization by Allocation Policy.png'.format(input_log), bbox_inches='tight', dpi=150)
    except:
        pass

    try:
        # Additional graphs for experiments
        df_exp3_ = data_df.copy()
        df_exp3_ = df_exp3_[df_exp3_['Policy'].isin(['No policy', 'Baseline'])]
        for col in ['Cost', 'Flow time', 'Waiting', 'Workload']:
            max_col = np.max(df_exp3_[col])
            df_exp3_[col] = df_exp3_[col]/max_col
            
        df_exp3 = pd.melt(df_exp3_, id_vars=['Log', 'Policy', 'Optimization'], value_vars=['Cost', 'Flow time', 'Waiting','Workload'], var_name = 'Metric', value_name='Normalized Metric Value')
        df_exp3 = df_exp3.round({'Performance Metric Value':3})
        df_exp3['Optimization'] = df_exp3['Optimization'].apply(lambda x: x + ' MO' if x == 'Multiobjective' else x + ' SO')

        for policy in df_exp3['Policy'].drop_duplicates():
            if policy != 'Baseline':
                df_policy = df_exp3[df_exp3['Policy'].isin([policy, 'Baseline'])]
                fig = plt.figure(figsize=(10, 6))
                graph_title = 'Comparison of metrics between Role-based allocation (Baseline) and Resource-based allocation (No policy)'.format(input_log, policy.capitalize().replace('_', ' '))
                ax = sns.barplot(x="Optimization", y="Normalized Metric Value", hue="Metric", data=df_policy)
                for i in ax.containers:
                    ax.bar_label(i,)
                plt.grid()
                plt.title(graph_title)
                plt.xlabel('Single-objective (SO) vs Multi-objective (MO) optimization')
                fig.savefig('stats/graphs/{}/Comparison of metrics between Baseline and No policy.png'.format(input_log), bbox_inches='tight', dpi=150)
    except:
        pass

generate_graphs_exps()