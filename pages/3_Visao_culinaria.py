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

st.set_page_config(page_title="Visão Restaurantes", page_icon="👩‍🍳", layout="wide")

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

################### criando os cards dos melhores restaurantes por tipo de culinaria
def card_cuisines(df, type_food):
    df_aux = (df.loc[df1["cuisines"]==type_food, ["restaurant_id","restaurant_name","country_name","city",
                                                  "average_cost_for_two","currency","aggregate_rating"]]
               .groupby(["restaurant_id","restaurant_name","country_name","city","average_cost_for_two","currency"])
               .max().sort_values(["aggregate_rating", "restaurant_id"], ascending=[False,True]).reset_index())
    rest = df_aux.loc[0, "restaurant_name"]
    nota = df_aux.loc[0, "aggregate_rating"]
    pais = df_aux.loc[0, "country_name"]
    cidade = df_aux.loc[0, "city"]
    cf2 = df_aux.loc[0, "average_cost_for_two"]
    moeda = df_aux.loc[0, "currency"]
    multi = f'''Restaurante: {rest}  \nPaís: {pais}  \nCidade: {cidade}  \nMédia de preço para dois: {cf2} ({moeda})'''
    label = f"{type_food}:  \n{rest}"
    nota =f"{nota}/5.0"
    card = st.metric(label, nota, help=multi)
    return card

################### criando grafico de barras dos melhores tipos de culinaria
def barplot_bycuisines(df):
    df_aux = (df.loc[:, ["cuisines", "restaurant_id"]].groupby("cuisines").nunique()
              .sort_values("restaurant_id", ascending=False).reset_index().head(5))
    df_aux.columns = ["Tipos de culinária", "Quantidade de restaurantes"]
    fig = px.bar(df_aux, x="Tipos de culinária", y="Quantidade de restaurantes", text_auto=True, width=500, height=400,
                 template="plotly_white")
    fig.update_traces(marker_color="darkred")
    fig.update_layout(xaxis_title=None, yaxis_title=None, plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor="gray")
    return fig

################### criando grafico de setores sobre tipo de preco dos restaurantes
def pieplot_price(df):
    df_aux = (df.loc[:, ["price_type", "restaurant_id"]].groupby("price_type").nunique()
              .sort_values("restaurant_id", ascending=False).reset_index())
    df_aux.columns = ["Tipo de preço", "Quantidade de restaurantes"]
    fig = px.pie(df_aux, values="Quantidade de restaurantes", names="Tipo de preço", width=500, height=400, template="plotly_white",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

################### criando o histograma sobre avaliacao media dos restaurantes
def histogram_aggrating(df):
    df_aux = df.loc[:, ["aggregate_rating", "restaurant_id"]]
    df_aux.columns = ["Avaliação média", "Quantidade de restaurantes"]
    fig = px.histogram(df_aux, x="Avaliação média", nbins=30, text_auto=True, width=500, height=400, template="plotly_white")
    fig.update_traces(marker_color="darkred")
    fig.update_layout(yaxis_title="Quantidade de restaurantes", plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor="gray")
    return fig

################### criando uma tabela com os melhores restaurantes conforme avaliacao media
def best_restaurants(df):
    df_aux = (df.loc[:, ["restaurant_id", "restaurant_name", "country_name", "city", "cuisines", "average_cost_for_two",
                         "currency", "aggregate_rating", "votes", "price_type"]]
              .groupby(["restaurant_id", "restaurant_name", "country_name", "city", "cuisines", "average_cost_for_two",
                        "currency","votes", "price_type"]).mean()
              .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False,True]).reset_index().head(15))
    df_aux = df_aux.loc[df_aux["aggregate_rating"]==4.9, df_aux.columns != "restaurant_id"]
    df_aux.columns = ["Restaurante","País","Cidade","Culinária","Preço médio*","Moeda","Quantidade de Avaliações", 
                      "Tipo de Preço", "Avaliação Média"]
    df_aux[["Preço médio*", "Quantidade de Avaliações"]] = (df_aux[["Preço médio*", "Quantidade de Avaliações"]]
                                                            .applymap("{:,.0f}".format))
    df_aux["Avaliação Média"] = df_aux["Avaliação Média"].map("{:,.2f}".format)
    df_aux = (df_aux.style.set_table_styles([{"selector": "th","props": "background-color: #800000; color: white; font-size:10pt"}])
              .set_properties(**{'font-size': '10pt'}).hide(axis="index").to_html())
    return df_aux
    
#-----------------------------------------------------------------------------------------------------------------------------#
#                                      INICIO DA ESTRUTURA LOGICA DO CODIGO                                                   #
#-----------------------------------------------------------------------------------------------------------------------------#

################### importando o dataset
df = pd.read_csv("../dataset/zomato.csv")

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
country_options = st.sidebar.multiselect("Selecione os países:", df1["country_name"].unique(), default = ["Philippines", "Brazil",
                        "United States of America", "Canada", "United Arab Emirates", "India", "England", "Turkey"])
price_options = st.sidebar.multiselect("Selecione os tipos de preço:", df1["price_type"].unique(), 
                                       default = ["expensive", "gourmet", "normal", "cheap"])
cuisines_options = st.sidebar.multiselect("Selecione os tipos de culinária:", df1["cuisines"].unique(), default = ["North Indian", "BBQ",
                        "American", "Cafe", "Italian", "Pizza", "Brazilian", "Home-made"])
select_country_filter = df1["country_name"].isin(country_options)
df1 = df1.loc[select_country_filter, :]
select_price_filter = df1["price_type"].isin(price_options)
df1 = df1.loc[select_price_filter, :]
select_cuisines_filter = df1["cuisines"].isin(cuisines_options)
df1 = df1.loc[select_cuisines_filter, :]
st.sidebar.divider()
st.sidebar.markdown(":gray[Developed by Thaylla Alves]")

#=====================#
# Layout do Streamlit #
#=====================#

st.header("👩‍🍳 Visão de Negócios: Restaurantes")
with st.container():
    st.markdown("<h2 style='text-align: center; font-size:14pt; color: gray'>Melhores restaurantes do TOP5 tipos de culinária</h2>",
                unsafe_allow_html=True)
    style_metric_cards(border_left_color="#800000", box_shadow=False) 
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        metricas = card_cuisines(df1, type_food="North Indian")
    with col2:
        metricas = card_cuisines(df1, type_food="American")
    with col3:
        metricas = card_cuisines(df1, type_food="Cafe")
    with col4:
        metricas = card_cuisines(df1, type_food="Italian")
    with col5:
        metricas = card_cuisines(df1, type_food="Pizza")  
with st.container():
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2 style='text-align: center; font-size:15pt; color: gray'>TOP5 - Quantidade de restaurantes por Tipo de Culinária</h2>", unsafe_allow_html=True)
        fig = barplot_bycuisines(df1)
        st.plotly_chart(fig, theme=None, use_container_width=True)
    with col2:
        st.markdown("<h2 style='text-align: center; font-size:15pt; color: gray'>Distribuição do tipo de preço dos restaurantes</h2>",
                    unsafe_allow_html=True)
        fig = pieplot_price(df1)
        st.plotly_chart(fig, theme=None, use_container_width=True)
with st.container():
    st.divider()
    st.markdown("<h2 style='text-align: center; font-size:15pt; color: gray'>Distribuição das avaliações médias dos restaurantes</h2>",
                unsafe_allow_html=True)
    fig = histogram_aggrating(df1)
    st.plotly_chart(fig, theme=None, use_container_width=True)
with st.container():
    st.divider()
    st.markdown("<h2 style='text-align: center; font-size:15pt; color: gray'>TOP 15 Restaurantes com a maior avaliação média</h2>",
                unsafe_allow_html=True)
    df_aux = best_restaurants(df1)
    st.markdown(df_aux, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: right; font-size:9pt; color: gray'>* Preço médio para duas pessoas", unsafe_allow_html=True)