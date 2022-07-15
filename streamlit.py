from email.policy import default
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

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

def request_api(tipo_aprobacion, years):
  request_data = {"tipo_aprobacion": tipo_aprobacion,
                     "years": years}

  data_cleaned = str(request_data).replace("'", '"')

  url_api = "https://api-modelos-aprobacion.herokuapp.com/predict"

  pred = requests.post(url=url_api, data=data_cleaned).text

  pred_df = pd.read_json(pred)
  return pred_df


read_col = ['AÑO','DEPARTAMENTO','MUNICIPIO','APROBACIÓN', 'APROBACIÓN_TRANSICIÓN', 'APROBACIÓN_PRIMARIA', 'APROBACIÓN_SECUNDARIA', 'APROBACIÓN_MEDIA']
df = pd.read_csv("https://raw.githubusercontent.com/JJPC98/DiplomadoPython/main/MEN_ESTADISTICAS_EN_EDUCACION_EN_PREESCOLAR__B_SICA_Y_MEDIA_POR_MUNICIPIO_LIMPIO.csv" , usecols=read_col)  

# Using object notation
genre_bar = st.sidebar.radio(
            "Navigate",
            ('Homepage','Exploracion', 'Prediccion'))

#HOMEPAGE SELECCIONADO
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
        ('Row', 'Colomns'))

    if genre == 'Row':
        st.write('Cantidad de filas del Dataframe')
        st.write(df.shape[0])
    else:
        st.write('Cantidad de columnas del Dataframe')
        st.write(df.shape[1])

    agree_describe = st.checkbox('📈 Estadísticas Generales 📈')
    if agree_describe: 
        st.write(df.describe())

       
elif genre_bar == 'Prediccion':
    
    st.header('🔮Prediccion de aprobacion')
    st.sidebar.title('Selccione los datos para su prediccion')
    c1, c2= st.columns(2)
    aprobacion_options = c1.selectbox('Seleccione la aprobacion',('Aprobacion general', 'Aprobacion media', 'Aprobacion primaria', 'Aprobacion secundaria', 'Aprobacion transicion'))
    num_años = c2.selectbox('Seleccione numero de años', (1,2,3))
    btn_predecir = st.button('Predecir aprobacion')
    
    if btn_predecir:
        if aprobacion_options == 'Aprobacion general':
            pred = request_api(0, num_años)
            st.text('Para la Aprobacion general')
            st.text(procesar_request(pred))    

        elif aprobacion_options == 'Aprobacion media':
            pred = request_api(1, num_años)
            st.text('Para la Aprobacion en media')
            st.text(procesar_request(pred))

        elif aprobacion_options == 'Aprobacion primaria':
            pred = request_api(2, num_años)
            st.text('Para la Aprobacion en primaria')
            st.text(procesar_request(pred))

        elif aprobacion_options == 'Aprobacion secundaria':
            pred = request_api(3, num_años)
            st.text('Para la Aprobacion en secundaria')
            st.text(procesar_request(pred))

        elif aprobacion_options == 'Aprobacion transicion':
            pred = request_api(4, num_años)
            st.text('Para la Aprobacion en transicion')
            st.text(procesar_request(pred))

        st.snow()

else:
    st.sidebar.header('Ingrese los datos')
    DEPARTAMENTO = st.sidebar.multiselect("Selecciona departamento:", options=df['DEPARTAMENTO'].unique() , default =df['DEPARTAMENTO'].unique() )
    df_selection = df.query("DEPARTAMENTO == @DEPARTAMENTO")

    # st.dataframe(df_selection)
    st.title("Hello world!") 

    dataframe_depatamento = (
    df_selection.loc[:,['DEPARTAMENTO','APROBACIÓN']].groupby('DEPARTAMENTO').mean('APROBACIÓN')
    )

    fig = px.bar(
        dataframe_depatamento,
        x = "APROBACIÓN",
        y = dataframe_depatamento.index,
        orientation = "h",
        title= "<b> Hola </b>",
        color_discrete_sequence = ["#0083BB"] * len(dataframe_depatamento),
        template = "plotly_white"
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False))
    )

    AÑO = st.sidebar.multiselect("Selecciona los años:", options=df['AÑO'].unique() , default =df['AÑO'].unique() )
    df_selection_año = df.query("AÑO == @AÑO")

    dataframe_año = (
        df_selection_año.loc[:,['AÑO','APROBACIÓN']].groupby('AÑO').mean('APROBACIÓN')
        )

    fig_2 = px.line(
        dataframe_año,
        x = dataframe_año.index,
        y = "APROBACIÓN"
    )



    st.plotly_chart(fig)
    st.plotly_chart(fig_2)

    st.sidebar.title('📩 Contact us')
    st.wride('camiloganemortega@gmail.com')

























# option = st.sidebar.selectbox(
#      'Elija un departamento',
#      ('Amazonas', 'Antioquia', 'Arauca', 'Atlantico', 'Bogota DC', 'Bolivar', 'Boyaca', 
#      'Caldas', 'Caquetá', 'Casanare', 'Cauca', 'Cesar', 'Choco', 'Cordoba', 'Cundinamarca', 'Guainia', 
#      'Guaviare', 'Huila', 'La Guajira', 'Magdalena', 'Meta', 'Nariño', 'Norte de Santander', 'Putumayo', 
#      'Quindio', 'Risaralda', 'San Andres y Providencia', 'Santander', 'Sucre', 'Tolima', 'Valle del Cauca',
#      'Vaupés', 'Vichada'))

#     selected_year = st.sidebar.selectbox('AÑO', list(reversed(range(2011,2025))))
