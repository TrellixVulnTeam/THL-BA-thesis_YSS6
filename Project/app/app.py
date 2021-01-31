from flask import Flask, render_template, url_for, request, jsonify
from model.model import load_site_config, load_hero_mapping, load_pretrained_model, valid_input, data_to_feature
from model.model import combine_list, hero_ids
from itertools import product
import numpy as np

app = Flask(__name__,static_folder='./static')


@app.route('/')
def demo():
    return render_template("home.html",hero_mapping = hero_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    # do check to validate data input
    valid, res = valid_input(list(request.json))
    if not valid:
        return res
    else:
        feature = data_to_feature(res)
        prob = model.predict_proba(feature)[0]
        # prob: probabilities
        ret_val = dict()
        ret_val[0] = prob[0]
        ret_val[1] = prob[1]
        return ret_val

@app.route('/recommend', methods=['POST'])
def recommend():
    idx = -1
    raw_data = list(request.json)
    for i, id_str in enumerate(list(request.json)):
        if id_str == -1:
            idx = i
            break
    if idx == -1:
        return "ERROR: illegal input."
    
    predict_side = 0 if idx < 5 else 1
    hero_2_prob = dict()
    max_prob = 0
    recommended_hero_id = -1
    for hero_id in hero_ids:
        raw_data[idx] = str(hero_id)
        valid, current_data = valid_input(raw_data)
        if not valid:
            continue
        feature = data_to_feature(current_data)
        prob = model.predict_proba(feature)[0,predict_side]
        hero_2_prob[hero_id] = prob
        if prob > max_prob:
            recommended_hero_id = hero_id
            max_prob = prob
    ret_val = dict()
    ret_val['hero_id'] = recommended_hero_id
    ret_val['hero_name'] = inverse_hero_mapping[recommended_hero_id]
    return ret_val


if __name__ == '__main__':

    # site initialization
    config = load_site_config('App/model/site_config.json')
    hero_mapping, inverse_hero_mapping = load_hero_mapping(config['hero_mapping_path'])
    model = load_pretrained_model(config['model_path'])
    
    app.run(debug=True)