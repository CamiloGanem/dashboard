from email.policy import default
from operator import index
from optparse import Option
from turtle import width
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import random

st.set_page_config(
     page_title="DASHBOARD",
     page_icon="🐽",
     layout="wide",
     initial_sidebar_state="expanded"
 )

read_col = ['AÑO','DEPARTAMENTO','MUNICIPIO','APROBACIÓN', 'APROBACIÓN_TRANSICIÓN', 'APROBACIÓN_PRIMARIA', 'APROBACIÓN_SECUNDARIA', 'APROBACIÓN_MEDIA']
df = pd.read_csv("D:\Diplomado/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_POR_MUNICIPIO_LIMPIO.csv" , usecols=read_col)  


def request_api(tipo_aprobacion, years):
  request_data = {"tipo_aprobacion": tipo_aprobacion,
                     "years": years}    

  data_cleaned = str(request_data).replace("'", '"')

  url_api = "https://api-modelos-aprobacion.herokuapp.com/predict"

  pred = requests.post(url=url_api, data=data_cleaned).text

  pred_df = pd.read_json(pred)
  return pred_df

def procesar_request(dataframe):
    dataframe['years'] = pd.to_datetime(dataframe['years']).dt.year
    años = dataframe['years']
    aprobaciones = dataframe['aprobacion'].round(2)
    col1, col2, col3 = st.columns(3)
    resultado = ""
    for p in range(len(años)):
        if p == 0:
            col1.metric('Año '+str(años[0]), str(aprobaciones[0])+'%')
        elif p == 1:
            col2.metric('Año '+str(años[1]), str(aprobaciones[1])+'%')
        elif p == 2:
            col3.metric('Año '+str(años[2]), str(aprobaciones[2])+'%')
    return resultado

# Using object notation

st.sidebar.title('NAVEGACIÓN')
genre_bar = st.sidebar.radio(
            label = 'Seleccione',
            options = ('Homepage','Exploracion', 'Predicción')
            )


if genre_bar == 'Homepage':
    st.title("Estadísticas de aprobación escolar 📊 (DASHBOARD) 📊" ) 
    st.write('📌 ABOUT US')
    st.write('Este DASHBOARD fue elaborado con fines académicos, con el propósito de mostrar cual es la tasa de aprobación escolar en todos los departamentos de Colombia. Nuestro equipo está conformado por: Juan Ramos, Jeremías Palacio, Jesús Hoyos, Camilo Ganem y Yesica Durango')
    agree = st.checkbox('Display Data')

    if agree:
        st.dataframe(df)
    agree_columns = st.checkbox('Columns')
    if agree_columns:
        st.write(df.columns)

    genre = st.radio(
        "¿Qué dimensión quieres ver?",
        ('Filas', 'Columnas'))

    if genre == 'Row':
        st.write('Cantidad de filas del Dataframe')
        st.write(df.shape[0])
    else:
        st.write('Cantidad de columnas del Dataframe')
        st.write(df.shape[1])

    agree_describe = st.checkbox('📈 Estadísticas Generales 📈')
    if agree_describe: 
        st.write(df.describe())

elif genre_bar == 'Exploracion':

    st.sidebar.header('Ingrese los datos')
    DEPARTAMENTO = st.sidebar.multiselect("Selecciona departamento:", options=df['DEPARTAMENTO'].unique() , default =df['DEPARTAMENTO'].unique() )
    df_selection = df.query("DEPARTAMENTO == @DEPARTAMENTO")

    # st.dataframe(df_selection)
    st.title("🔍 Exploración de datos(graficas)") 

    

    dataframe_depatamento = (
    df_selection.groupby(by=['DEPARTAMENTO']).mean()[['APROBACIÓN']]
    )
    
    fig = px.bar(
        dataframe_depatamento,
        x = "APROBACIÓN",
        y = dataframe_depatamento.index,
        orientation = "h",
        height=700, width = 1200,
        title= "<b> Nivel de aprobación a nivel departamental </b>",
        color_discrete_sequence = ["#3EC6FF"] * len(dataframe_depatamento),
        template = "plotly_white"
        )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False)),
        yaxis={'categoryorder':'total ascending'}
        )

    fig.update_xaxes(automargin=True)

    dataframe_año = (
        df.groupby(by=['AÑO']).mean()[['APROBACIÓN','APROBACIÓN_TRANSICIÓN','APROBACIÓN_PRIMARIA','APROBACIÓN_SECUNDARIA', 'APROBACIÓN_MEDIA']]
        )
   #
   # 
   #  
   #
    def grafica_time(dataframe,x,y,title):
        fig_2 = px.line(
            dataframe,
            x = x,
            y = y,
            title= title,
            color_discrete_sequence = ["#3EC6FF"],
            template = "plotly_white"
        )
        
        fig_2.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(buttons = list([dict(step = 'year' , stepmode = "backward",count = 1,label = '1 año')])),
        )

        return fig_2
#
#
#

    st.plotly_chart(fig)   
    
    col1, col2= st.columns(2)
    st.plotly_chart(grafica_time(dataframe_año,dataframe_año.index,dataframe_año['APROBACIÓN_MEDIA'],'APROBACIÓN MEDIA'))
    st.write('Aprobación Media: La grafica de aprobación estudiantil en el nivel educativo “Media” con respecto a los años (2011 – 2020) muestra su pico más alto en el año 2014 con un 95.4%, así mismo su punto más bajo fue en el 2020 con un 89.7%')
    
    with col1:
        st.plotly_chart(grafica_time(dataframe_año,dataframe_año.index,dataframe_año['APROBACIÓN'],'APROBACIÓN'))
        st.write('Aprobación: La grafica de aprobación estudiantil "General" con respecto a los años (2011 - 2020) muestra su pico mas alto en el año 2014 con un 95.3%, así mismo el punto más bajo fue en el 2020 con un 90.7%')
        st.plotly_chart(grafica_time(dataframe_año,dataframe_año.index,dataframe_año['APROBACIÓN_PRIMARIA'],'APROBACIÓN PRIMARIA'))
        st.write('Aprobación Primaria: La grafica de aprobación estudiantil en el nivel educativo “Primaria” con respecto a los años (2011 – 2020) muestra su pico más alto en el año 2014 con un 96.1%, así mismo su punto más bajo fue en el 2020 con un 93.3')
    with col2:
        st.plotly_chart(grafica_time(dataframe_año,dataframe_año.index,dataframe_año['APROBACIÓN_TRANSICIÓN'],'APROBACIÓN TRANSICIÓN'))
        st.write('Aprobación Transición: La grafica de aprobación estudiantil en el nivel educativo "Transición" con respecto a los años (2011 – 2020) muestra su pico más alto en el año 2014 con un 97.7%, así mismo su punto más bajo fue en el 2012 con un 95.8%')
        st.plotly_chart(grafica_time(dataframe_año,dataframe_año.index,dataframe_año['APROBACIÓN_SECUNDARIA'],'APROBACIÓN SECUNDARIA'))
        st.write('Aprobación Secundaria: La grafica de aprobación estudiantil en el nivel educativo “Secundaria” con respecto a los años (2011 – 2020) muestra su pico más alto en el año 2014 con un 93.6%, así mismo el punto más bajo fue en el 2020 con un 86.9% ')
        
    st.sidebar.title('📩 Contact us')


else: 
    st.sidebar.header('Ingrese los datos')  
    selectbox_aprobacion = st.sidebar.selectbox(
     'How would you like to be contacted?',
     ('Aprobacion general', 'Aprobacion media', 'Aprobacion primaria', 'Aprobacion secundaria','Aprobacion transicion'))
    

    selectbox_año = st.sidebar.selectbox(
     'How would you like to be contacted?',
     (1,2,3))

    # def random_emoji():
    #     st.session_state.emoji = random.choice(emojis)
        
    # if "emoji" not in st.session_state:
    #     st.session_state.emoji = "👌"

    # emojis = ["📈","📊","🔝","🍑","📸","😲"] 

    
    
    if st.sidebar.button('Predicción'):
        
        if selectbox_aprobacion == 'Aprobacion general':
            pred = request_api(0, selectbox_año)
            st.text('Para la Aprobacion general')
            st.text(procesar_request(pred))    

        elif selectbox_aprobacion == 'Aprobacion media':
            pred = request_api(1, selectbox_año)
            st.text('Para la Aprobacion en media')
            st.text(procesar_request(pred))

        elif selectbox_aprobacion == 'Aprobacion primaria':
            pred = request_api(2, selectbox_año)
            st.text('Para la Aprobacion en primaria')
            st.text(procesar_request(pred))

        elif selectbox_aprobacion == 'Aprobacion secundaria':
            pred = request_api(3, selectbox_año)
            st.text('Para la Aprobacion en secundaria')
            st.text(procesar_request(pred))

        elif selectbox_aprobacion == 'Aprobacion transicion':
            pred = request_api(4, selectbox_año)
            st.text('Para la Aprobacion en transicion')
            st.text(procesar_request(pred))

        st.snow()
   
    
