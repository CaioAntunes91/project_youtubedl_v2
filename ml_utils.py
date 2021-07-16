import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

mdl_rf = jb.load("./model/rf_20210620.pkl.z")
mdl_lgbm = jb.load("./model/lgbm_20210620.pkl.z")
title_vec = jb.load("./parameter/title_vec_opt_20210620.pkl.z")

def compute_features(data):

	features = pd.DataFrame(index=data.index)
	features['dias_desde_upload'] = data['dias_desde_upload']
	features['view_count'] = data['view_count']
	features['views_por_dia'] = features['view_count'] / features['dias_desde_upload']
	features.drop(['dias_desde_upload'], axis = 1, inplace = True)

	title = data['title'].copy()

	title_bow = title_vec.transform(title)
	feature_wtitle = hstack([features, title_bow])

	return feature_wtitle

def compute_predictions(data):
	
	p_rf = mdl_rf.predict_proba(data)[:,1]
	p_lgbm = mdl_lgbm.predict_proba(data)[:,1]

	p = 0.5*p_rf + 0.5*p_lgbm

	return p
