import configparser as cp
import os
import re
from shutil import copyfile

from hyperopt import hp

import resourceAllocationOptimizer as resourceOptimization
#Módulos de SIMOD
from support_modules import support as sup
from support_modules.writers import assets_writer as assets_writer


def reformat_path(raw_path):
    """Provides path support to different OS path definition"""
    route = re.split(chr(92) + '|' + chr(92) + chr(92) + '|' +
                     chr(47) + '|' + chr(47) + chr(47), raw_path)
    return os.path.join(*route)

def read_settings(settings):
    """Catch parameters fron console or code defined"""
    config = cp.ConfigParser(interpolation=None)
    config.read("./config.ini")
    # Basic settings
    settings['input'] = config.get('FOLDERS', 'inputs')
    settings['file'] = config.get('EXECUTION', 'filename')
    settings['output'] = os.path.join(config.get('FOLDERS', 'outputs'), sup.folder_id())
    settings['timeformat'] = config.get('EXECUTION', 'timeformat')
    settings['simulation'] = config.get('EXECUTION', 'simulation')
    settings['analysis'] = config.get('EXECUTION', 'analysis')
    settings['role_optimization'] = config.get('EXECUTION', 'role_optimization')
    settings['resource_optimization'] = config.get('EXECUTION', 'resource_optimization')
    
    settings['flag'] = config.get('EXECUTION', 'flag')
    settings['cooperation_policy'] = config.get('EXECUTION', 'cooperation_policy')
    settings['preference_policy'] = config.get('EXECUTION', 'preference_policy')
    settings['ns_include'] = config.get('EXECUTION', 'ns_include')
    
    settings['k'] = config.get('EXECUTION', 'k')
    settings['sim_percentage'] = config.get('EXECUTION', 'sim_percentage')
    settings['quantity_by_cost'] = config.get('EXECUTION', 'quantity_by_cost')
    settings['reverse'] = config.get('EXECUTION', 'reverse')
    settings['happy_path'] = config.get('EXECUTION', 'happy_path')
    settings['graph_roles_flag'] = config.get('EXECUTION','graph_roles_flag')

    # Conditional settings
    settings['miner_path'] = reformat_path(config.get('EXTERNAL', 'splitminer'))
    if settings['alg_manag'] == 'repairment':
        settings['align_path'] = reformat_path(config.get('EXTERNAL', 'proconformance'))
        settings['aligninfo'] = os.path.join(settings['output'],
                                             config.get('ALIGNMENT', 'aligninfo'))
        settings['aligntype'] = os.path.join(settings['output'],
                                             config.get('ALIGNMENT', 'aligntype'))
    if settings['simulation']:
        settings['repetitions'] = config.get('EXECUTION', 'repetitions')
        settings['scylla_path'] = reformat_path(config.get('EXTERNAL', 'scylla'))
        settings['simulator'] = config.get('EXECUTION', 'simulator')
    if settings['role_optimization']:
        settings['objective'] = config.get('OPTIMIZATION', 'objective')
        settings['criteria'] = config.get('OPTIMIZATION', 'criteria')
        settings['graph_optimization'] = config.get('OPTIMIZATION', 'graph_optimization')
    if settings['resource_optimization']:
        settings['cost'] = config.get('OPTIMIZATION', 'cost')
        settings['workload'] = config.get('OPTIMIZATION', 'workload')
        settings['flow_time'] = config.get('OPTIMIZATION', 'flow_time')
        settings['waiting_time'] = config.get('OPTIMIZATION', 'waiting_time')
        settings['log'] = config.get('OPTIMIZATION', 'log')
        settings['non_repeated_resources'] = config.get('OPTIMIZATION', 'non_repeated_resources')
        settings['generations'] = config.get('OPTIMIZATION', 'generations')
        settings['initial_population'] = config.get('OPTIMIZATION', 'initial_population')
        settings['min_population'] = config.get('OPTIMIZATION', 'min_population')
        settings['max_population'] = config.get('OPTIMIZATION', 'max_population')
    return settings

params = {
        'epsilon': 1,
        'eta': 1,
        'alg_manag': hp.choice('alg_manag', ['replacement',
                                             'trace_alignment',
                                             'removal'])
    }

settings = read_settings(params)

resourceOptimization.read_parameters(settings['log'],settings['non_repeated_resources'],settings['cost'],
                                                    settings['workload'], settings['flow_time'],settings['waiting_time'], settings['preference_policy'], settings['cooperation_policy'])
resourceOptimization.main_NSGA2(settings['initial_population'],settings['max_population'],settings['min_population'],settings['generations'])
