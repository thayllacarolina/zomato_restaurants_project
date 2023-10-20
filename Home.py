################### bibliotecas necessarias (libraries)
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from haversine import haversine
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime
import numpy as np
import inflection
from streamlit_extras.metric_cards import style_metric_cards
from folium.plugins import MarkerCluster
import locale

st.set_page_config(page_title="Home", page_icon="📈", layout="wide")

#----------------------------------------------------------------------------------------------------------------------------#
#                                                     DICIONARIOS                                                            #
#----------------------------------------------------------------------------------------------------------------------------#

################### dicionario com os codigos dos paises
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

################### dicionario com os codigos das cores
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

#----------------------------------------------------------------------------------------------------------------------------#
#                                                        FUNCOES                                                             #
#----------------------------------------------------------------------------------------------------------------------------#

################### fazendo a limpeza no dataset
def clean_code (df):
    df = df.dropna().drop_duplicates()
    df.drop("Switch to order menu", inplace=True, axis=1)
    df.drop(df.loc[df["Average Cost for two"] == 25000017,:].index.item(), inplace=True, axis=0)
    df["Cuisines"] = df["Cuisines"].astype(str).apply(lambda x: x.split(",")[0])
    return df

################### criando a variavel com o nome dos paises com base nos codigos
def country_name(country_id):
    return COUNTRIES[country_id]

################### criando a categoria do tipo de preco de comida com base no range de valores
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

################### criando a variavel com o nome das cores com base nos codigos
def color_name(color_code):
 return COLORS[color_code]

################### renomeando as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

################### criando mapa dos restaurantes
def map_restaurants(df):
    columns = ["city", "aggregate_rating", "currency", "cuisines", "color_name", "restaurant_id", "restaurant_name",
               "average_cost_for_two","latitude", "longitude"]
    columns_groupby = ["city", "cuisines", "color_name", "currency", "restaurant_id", "restaurant_name"]
    df_aux = df1.loc[:, columns].groupby(columns_groupby).median().reset_index()
    map = folium.Map(zoom_start=11)
    marker_cluster = folium.plugins.MarkerCluster().add_to(map)
    for i in range (len(df_aux)):
        popup_html = f'<div style="width: 250px;">' \
                     f"<b>{df_aux.loc[i, 'restaurant_name']}</b><br><br>" \
                     \
                     f"Preço para dois: {df_aux.loc[i, 'average_cost_for_two']:.2f} ( {df_aux.loc[i, 'currency']})<br> " \
                     f"Tipo de culinária: {df_aux.loc[i, 'cuisines']}<br>" \
                     f"Avaliação média: {df_aux.loc[i, 'aggregate_rating']}/5.0" \
                     f'</div>'
        folium.Marker ([df_aux.loc[i, 'latitude'], df_aux.loc[i, 'longitude']], popup=popup_html, width=500, height=500, 
                       tooltip='Ver informações', parse_html=True, zoom_start=30, tiles= 'Stamen Toner',
                       icon=folium.Icon(color=df_aux.loc[i, 'color_name'] , icon='home')).add_to(marker_cluster)
    return map

#-----------------------------------------------------------------------------------------------------------------------------#
#                                      INICIO DA ESTRUTURA LOGICA DO CODIGO                                                   #
#-----------------------------------------------------------------------------------------------------------------------------#

################### importando o dataset
df = pd.read_csv("dataset/zomato.csv")

################### limpando o dataset e aplicando as funcoes criadas para preparar o dataset para analise
df1 = clean_code(df)
df1["Country Name"] = df1["Country Code"].apply(lambda x: country_name(x))
df1["Price type"] = df1["Price range"].apply(lambda x: create_price_type(x))
df1["Color name"] = df1["Rating color"].apply(lambda x: color_name(x))
df1 = rename_columns(df1)

#============================#
# Barra Lateral do Streamlit #
#============================#

image = Image.open("zomato.jpg")
st.sidebar.image(image, width=210)
st.sidebar.markdown("# Zomato Restaurants")
st.sidebar.markdown("### Food Delivery")
st.sidebar.divider()
st.sidebar.markdown("## Filtros:")
# filtro dos paises:
country_options = st.sidebar.multiselect("Selecione os países:", df1["country_name"].unique(), default = ["Philippines", "Brazil",
                        "United States of America", "Canada", "United Arab Emirates", "India", "England", "Turkey"])
# filtro dos tipos de preco:
price_options = st.sidebar.multiselect("Selecione os tipos de preço:", df1["price_type"].unique(), 
                                       default = ["expensive", "gourmet", "normal", "cheap"])
# ativando os filtros:
select_country_filter = df1["country_name"].isin(country_options)
df1 = df1.loc[select_country_filter, :]
select_price_filter = df1["price_type"].isin(price_options)
df1 = df1.loc[select_price_filter, :]
st.sidebar.divider()
st.sidebar.markdown(":gray[Developed by Thaylla Alves]")

#=====================#
# Layout do Streamlit #
#=====================#

st.markdown(""" <style> [data-testid="stMetricValue"] {font-size: 25px;}</style>""", unsafe_allow_html=True,)

st.header("📈 Zomato Restaurants Dashboard")
with st.container():
    st.markdown("<h2 style='text-align: left; font-size:14pt; color: gray'>Principais métricas do dashboard com base nos filtros:</h2>",
                unsafe_allow_html=True)
    style_metric_cards(border_left_color="#800000", box_shadow=False)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Restaurantes cadastrados", df1["restaurant_id"].nunique())
    with col2:
        st.metric("Países cadastrados", df1["country_code"].nunique())
    with col3:
        st.metric("Cidades cadastradas", df1["city"].nunique())
    with col4:
        metrica = df1["votes"].sum()
        st.metric("Total de avaliações", "{0:,}".format(metrica).replace(',','.'))
    with col5:
        st.metric("Tipos de culinária cadastrados", df1["cuisines"].nunique())
with st.container():
    st.markdown("<h2 style='text-align: left; font-size:14pt; color: gray'>Mapa com a localização dos restaurantes:</h2>",
                unsafe_allow_html=True)
    map = map_restaurants(df1)
    folium_static(map)
