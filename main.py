# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 21:01:43 2023

@author: ACER
"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    
    Carbohydrate : float
    Protein: float
    Sodium: float
    Calcium: float

dietary_model = pickle.load(open('dietary_score.sav','rb'))

@app.post('/dietary_score')

def dietary_pred(input_parameters: model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    carb = input_dictionary['Carbohydrate']
    protein = input_dictionary['Protein']
    sodium = input_dictionary['Sodium']
    calcium = input_dictionary['Calcium']
    
   # input_list = [carb,protein,sodium,calcium]
    
   # prediction = dietary_model.predict([input_list])
   
    dietary_model.input['Carbohydrates'] = carb
    dietary_model.input['Protein'] = protein
    dietary_model.input['Sodium'] = sodium
    dietary_model.input['Calcium'] = calcium
    
    dietary_model.compute()
    
    return dietary_model.output['Score']