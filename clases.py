# -*- coding: utf-8 -*-
"""clases.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UXNczs17jnrs9V8svZ8IwxtfAHm_Q4gq
"""

from pydantic import BaseModel as BM
from pydantic import Field
from datetime import date
import joblib
import pandas as pd

#general = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_media.pklaprobacion_general.pkl")
#media = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_media.pkl")
#primaria = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_primaria.pkl")
#secundaria = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_secundaria.pkl")
#transicion = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_transicion.pkl")

class InputModelo(BM):
    """
    Clase que define las entradas del modelo según las verá el usuario.
    """
    tipo_aprobacion: int = Field(ge = 0, le = 4)
    years: int = Field(
        ge=1, le=3, description="Años futuros"
    )

    class Config:
        schema_extra = {
            "example": {
                "tipo_aprobacion": 1,
                "years": 1
            }
        }

class OutputModelo(BM):
    """
    Clase que define la salida del modelo según la verá el usuario.
    """

    fecha: date = Field()
    aprobacion: float = Field(ge=0, le=1)

    class Config:
        scheme_extra = {
            "example": {
                "year": 2021-1-1,
                "aprobacion": 90.374421
            }
        }

class APIModelBackEnd:
    def __init__(
        self,
        years,
        tipo_aprobacion,
    ):
        self.tipo_aprobacion = tipo_aprobacion
        self.years = years

    def _cargar_modelo(self, tipo_apro:int):
        if tipo_apro == 0:#Aprobacion general
          self.model = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_general.pkl")

        elif tipo_apro == 1:#Aprobacion media
          self.model = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_media.pkl")

        elif tipo_apro == 2:#Aprobacion primaria
           self.model = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_primaria.pkl")

        elif tipo_apro == 3:#Aprobacion secundaria
           self.model = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_secundaria.pkl")

        else:#Aprobacion transicion
          self.model = joblib.load("./drive/MyDrive/Diplomado/Modulo 5/aprobacion_transicion.pkl")

    def _preparar_datos(self):
        years = self.years
        return years
    
    def predecir(self, y_name="aprobacion"):
        self._cargar_modelo()
        x = self._preparar_datos()
        prediction = pd.DataFrame(self.model.predict_proba(x)[:, 1]).rename(
            columns={0: y_name}
        )
        return prediction.to_dict(orient="records")