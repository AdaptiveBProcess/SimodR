import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
import os


def generate_graphs_exps():
    folder_path = '../stats/stats_files'
    files = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            files.append(os.path.join(folder_path, file))
    input_logs = list(set([x.split('\\')[-1].split('_')[0] for x in files]))
    exp1_df = []
    exp2_df = []
    for input_log in input_logs:
        if not os.path.exists('../stats/graphs/'):
            os.mkdir('../stats/graphs/')
        if not os.path.exists('../stats/graphs/{}/'.format(input_log)):
            os.mkdir('../stats/graphs/{}/'.format(input_log))
        files_log = [x for x in files if input_log in x]
        data_df = pd.read_csv(files_log[0], sep=',', decimal=',', index_col=False)
        for file_log in files_log[1:]:
            data_df_tmp = pd.read_csv(file_log, sep=',', decimal=',', index_col=False)
            data_df = pd.concat([data_df, data_df_tmp])

        id_vars, value_vars = ['Log', 'Policy', 'Optimization'], ['Cost', 'Flow time', 'Waiting', 'Workload']
        data_df['Optimization'] = data_df['Optimization'].str.replace('_', ' ').str.capitalize()
        data_df[value_vars] = data_df[value_vars].astype(float)

        results_mat = data_df[data_df['Policy'] != 'Baseline']
        multiobjective_mat = results_mat[results_mat['Optimization'] == 'Multiobjective']
        df_results = pd.melt(data_df, id_vars=id_vars, value_vars=value_vars, var_name='Performance Metric',
                             value_name='Performance Metric Value')

        # Graphs for experiment 1
        df_exp1 = df_results[df_results['Policy'].isin(['No policy', 'Baseline'])]
        df_exp1 = df_exp1.round({'Performance Metric Value': 3})
        exp1_df.append(df_exp1)

        for col in ['Cost', 'Flow time', 'Waiting', 'Workload']:
            max_col = np.max(multiobjective_mat[col])
            multiobjective_mat[col] = multiobjective_mat[col] / max_col
        # Data for experiment 1
        df_exp2 = pd.melt(multiobjective_mat, id_vars=id_vars, value_vars=value_vars, var_name='Performance Metric',
                          value_name='Performance Metric Value')
        df_exp2 = df_exp2.round({'Performance Metric Value': 3})
        exp2_df.append(df_exp2)

    exp2_df = pd.concat(exp2_df, axis=0)
    exp2_df.replace('ConsultaDataMining201618', 'ACR', inplace=True)
    exp2_df.replace('Production', 'MP', inplace=True)
    exp2_df.replace('PurchasingExample', 'P2P', inplace=True)
    exp2_df.rename(columns={'Performance Metric Value': 'Normalized Metric Value'}, inplace=True)

    exp2_df['Optimization'].replace('Multiobjective', 'Multi O.', inplace=True)
    sns.set(font_scale=1.4, style='white', palette="tab10")
    g = sns.catplot(data=exp2_df, col='Log', x="Performance Metric", hue="Policy",
                    y='Normalized Metric Value', kind='bar',
                    col_order=['ACR', 'MP', 'P2P'], legend_out=False, legend=False,
                    sharey=True, sharex=True)
    g.set(xlabel=None)
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(40)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

    for ax in g.axes.ravel():

        # add annotations
        for c in ax.containers:
            labels = [f'{v.get_height():.2f}' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge', size='xx-small')
        ax.margins(y=0.2)

    plt.tight_layout()
    plt.show()
    g.fig.savefig(
        '../stats/graphs/Multiobjective optimization by Allocation Policy.png', bbox_inches='tight', dpi=300)

generate_graphs_exps()
