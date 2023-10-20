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

st.set_page_config(page_title="Visão Cidades", page_icon="🌇", layout="wide")

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
def clean_code(df):
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

################### grafico de barras na visao cidade
def barplot_bycity(df):
    df_aux = (df.loc[:,["city", "country_name", "restaurant_id"]].groupby(["city", "country_name"]).nunique()
              .sort_values("restaurant_id", ascending=False).reset_index().head(10))
    df_aux.columns = ["Cidade", "País", "Quantidade de restaurantes"]
    fig = px.bar(df_aux, x="Cidade", y="Quantidade de restaurantes", color="País", text_auto=True, template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(title_text="Quantidade de restaurantes por Cidade (TOP10)", title_x=0.45, title_font_color="gray",
                      xaxis_title=None, yaxis_title=None, plot_bgcolor="white")
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor="gray")
    return fig

################### grafico de barras sobre avaliacao media na visao cidade
def rating_bycity(df, restricao, valor, title):
    if restricao == "maior":
        df_aux = (df.loc[df["aggregate_rating"]>valor, ["city","country_name","restaurant_id"]]
                  .groupby(["city", "country_name"]).nunique().sort_values("restaurant_id", ascending=False).reset_index().head(10))
    else:
        df_aux = (df.loc[df["aggregate_rating"]<valor, ["city", "country_name", "restaurant_id"]]
                  .groupby(["city", "country_name"]).nunique().sort_values("restaurant_id", ascending=False).reset_index().head(10))
    df_aux.columns = ["Cidade", "País", "Quantidade de restaurantes"]
    fig = px.bar(df_aux, y="Cidade", x="Quantidade de restaurantes", color="País", text_auto=True, template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.G10, width=300, height=450)
    fig.update_layout(title_text=title,title_font_color="gray",xaxis_title=None, yaxis_title=None, plot_bgcolor="white", 
                      title_x=0.5, yaxis={'categoryorder':'total ascending'}, 
                      legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="right",x=0.9))
    fig.update_yaxes(showline=True, linewidth=1.5, linecolor="gray")
    return fig

################### grafico de barras sobre entrega ou pedido online na visao cidade
def delivery_bycity(df, var_selecao, title):
    df_aux = (df.loc[df1[var_selecao]==1, ["city", "country_name", "restaurant_id"]].groupby(["city","country_name"])
              .nunique().sort_values("restaurant_id", ascending=False).reset_index().head(25))
    df_aux.columns = ["Cidade", "País", "Quantidade de restaurantes"]
    fig = px.bar(df_aux, x="Cidade", y="Quantidade de restaurantes", color="País", text_auto=True, template="plotly_white",
                 color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(title_text= title, title_font_color="gray",xaxis_title=None, yaxis_title=None, plot_bgcolor="white",
                      title_x=0.25, xaxis={'categoryorder':'total descending'})
    fig.update_xaxes(showline=True, linewidth=1.5, linecolor="gray")
    return fig

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

st.header("🌇 Visão de Negócios: Cidades")
with st.container():
    fig = barplot_bycity(df1)
    st.plotly_chart(fig, theme=None, use_container_width=True)
with st.container():
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        fig = rating_bycity(df1, restricao="maior", valor=4, 
                            title="Quantidade de restaurantes com avaliação<br>média acima de 4 por Cidade (TOP10)")
        st.plotly_chart(fig, theme=None, use_container_width=True)
    with col2:
        fig = rating_bycity(df1, restricao="menor", valor=2.5, 
                            title="Quantidade de restaurantes com avaliação<br>média abaixo de 2,5 por Cidade (TOP10)")
        st.plotly_chart(fig, theme=None, use_container_width=True)
with st.container():
    st.divider()
    fig = delivery_bycity(df1, var_selecao="is_delivering_now", 
                          title="Quantidade de restaurantes que fazem entrega por Cidade (TOP25)")
    st.plotly_chart(fig, theme=None, use_container_width=True)
with st.container():
    st.divider()
    fig = delivery_bycity(df1, var_selecao="has_online_delivery", 
                          title="Quantidade de restaurantes que aceitam pedidos online por Cidade (TOP25)")
    st.plotly_chart(fig, theme=None, use_container_width=True)