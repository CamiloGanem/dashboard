# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JuCYX0skbamFscjzouBZOlkMq1pIoySZ
"""



import requests
import pandas as pd

def hacer_request_api(tipo_aprobacion, years):
    request_data = [{"tipo_aprobacion": tipo_aprobacion,
                     "years": years}]

    data_cleaned = str(request_data).replace("'", '"')

    url_api = "https://apiaprobacion.herokuapp.com/predict"

    pred = requests.post(url=url_api, data=data_cleaned).text

    pred_df = pd.read_json(pred)
    return pred_df
