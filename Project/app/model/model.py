from itertools import product
import numpy as np
import pickle
import json

# static data
# hero combo list used during training time, as part of features.
combine_list = [(86, 8), (86, 96), (86, 106), (51, 11), (91, 19), (91, 72), (86, 11), (86, 39), (86, 17), (86, 46)]
hero_ids = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,121,126,128,129]

def load_site_config(site_config_file_folder):
    with open(site_config_file_folder, 'r') as fp:
        config = json.load(fp)
    return config

def load_hero_mapping(mapping_file_folder):
    with open(mapping_file_folder, 'r') as fp:
        hero_meta = json.load(fp)
        hero_mapping = dict()
        inverse_hero_mapping = dict()
    for hero in hero_meta:
        hero_id = hero['id']
        hero_name = hero['localized_name']
        hero_mapping[hero_name] = hero_id
        inverse_hero_mapping[hero_id] = hero_name
    return hero_mapping, inverse_hero_mapping

def load_pretrained_model(model_file_folder):
    lr_model_without_ban = pickle.load(open(model_file_folder, 'rb'))
    return lr_model_without_ban

def data_to_feature(raw_data):
    data_dim = len(raw_data)
    if not data_dim in [10, 20]:
        return None
    elif data_dim == 10:
        # generate hero combine
        team0_combine = list(product(raw_data[:5], raw_data[:5]))
        team1_combine = list(product(raw_data[5:], raw_data[5:]))
        feature = np.zeros(len(hero_ids) + 2 * len(combine_list))
        for i, hero_id in enumerate(hero_ids):
            if hero_id in raw_data[:5]:
                feature[i] = 1
            elif hero_id in raw_data[5:]:
                feature[i] = -1
        for i, hero_combine in enumerate(combine_list):
            if hero_combine in team0_combine:
                feature[i + len(hero_ids)] = 1
            elif hero_combine in team1_combine:
                feature[i + len(hero_ids) + len(combine_list)] = 1
        return feature.reshape(1, -1)
    else:
        # TODO
        return None

def valid_input(raw_data):
    try:
        raw_data = [int(hero_id) for hero_id in raw_data]
    except:
        return False, 'ERROR: hero id must be digit.'
    if not len(set(raw_data)) in [10, 20]:
        return False, 'ERROR: duplicate hero id.'
    for h in raw_data:
        if not h in hero_ids:
            return False, 'ERROR: invalid hero id.'
    return True, raw_data