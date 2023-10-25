# Importando Bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import inflection
import plotly.graph_objs as go
import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(page_title = 'Países', layout='wide', page_icon = '🌎')
# Importando Dataframe

file_path = 'dataset/zomato.csv'
dados = pd.read_csv(file_path)

#Criando um dicionário com os códigos de países

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

#Criando um dicionário com os códigos de cores

COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

#Funçao para mostrar as dimensoes do dataframe
def show_dataframe_dimensions(dataframe):
    print(f"Number of Rows: {dataframe.shape[0]}")
    print(f"Number of Columns: {dataframe.shape[1]}")
    
    return None

show_dataframe_dimensions(dados)

#Funçao para identificar os atributos(variaveis) numericos
def get_numerical_attributes(dataframe):
    return dataframe.select_dtypes(include=['int64', 'float64'])

get_numerical_attributes(dados)

#Funcao para calcular estatídticas básicas a partir dos dados numericos
def get_first_order_statistics(dataframe):
    # Central Tendency Metrics
    mean = pd.DataFrame(dataframe.apply(np.mean)).T
    median = pd.DataFrame(dataframe.apply(np.median)).T

    # Dispersion Metrics
    min_ = pd.DataFrame(dataframe.apply(min)).T
    max_ = pd.DataFrame(dataframe.apply(max)).T
    range_ = pd.DataFrame(dataframe.apply(lambda x: x.max() - x.min())).T
    std = pd.DataFrame(dataframe.apply(np.std)).T
    skew = pd.DataFrame(dataframe.apply(lambda x: x.skew())).T
    kurtosis = pd.DataFrame(dataframe.apply(lambda x: x.kurtosis())).T

    # Metrics Concatenation
    m = pd.concat([min_, max_, range_, mean, median, std, skew, kurtosis]).T.reset_index()
    m.columns = ['attributes', 'min', 'max', 'range', 'mean', 'median', 'std', 'skew', 'kurtosis']
    
    return m

#Funçao para renomear as variaveis
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

# Funçao para substituir os códigos dos países por seus nome de acordo com o dicionário COUNTRIES
def country_name(country_id):
    return COUNTRIES[country_id]

#Funçao para substituir os códigos das cores por seus nomes de acordo com o dicionário COLORS
def color_name(color_code):
    return COLORS[color_code]

#Funçao para criar categorias de preços
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#Funçao para reordenar as colunas
def adjust_columns_order(dataframe):
    df = dataframe.copy()
    new_cols_order = [
        "restaurant_id",
        "restaurant_name",
        "country",
        "city",
        "address",
        "locality",
        "locality_verbose",
        "longitude",
        "latitude",
        "cuisines",
        "price_type",
        "price_range",
        "average_cost_for_two",
        "currency",
        "has_table_booking",
        "has_online_delivery",
        "is_delivering_now",
        "aggregate_rating",
        "rating_color",
        "color_name",
        "rating_text",
        "votes",
    ]
    return df.loc[:, new_cols_order]

#Funçao para aplicar todas as funçoes criadas e  tratar os dados de uma única vez
def process_data(file_path):
    df = pd.read_csv(file_path) #Lendo o CSV

    df = df.dropna() #Removendo as linhas com NAs

    df = rename_columns(df) #Renomeando as colunas

    df["price_type"] = df.loc[:, "price_range"].apply(lambda x: create_price_tye(x)) #Criando as categorias de preços

    df["country"] = df.loc[:, "country_code"].apply(lambda x: country_name(x)) #Trocando códigos por nomes de países

    df["color_name"] = df.loc[:, "rating_color"].apply(lambda x: color_name(x)) #Trocando códigos por nomes de cores

    df["cuisines"] = df.loc[:, "cuisines"].astype(str).apply(lambda x: x.split(",")[0]) #Dividindo a coluna de 'cuisines'

    df = df.drop_duplicates() #Removendo as duplicatas

    df = adjust_columns_order(df) #Arrumando a ordem das colunas

    df.to_csv("processed_data.csv", index=False) #Salvando de volta os dados processdos

    return df

data = process_data(file_path)

#Verificando estatísticas básicas dos dadosS
get_first_order_statistics(get_numerical_attributes(data))

# -----------------------------------------
# Barra Lateral
# -----------------------------------------

st.sidebar.image('pages/Zomato_logo.png', width=100, )

st.sidebar.markdown('# Fartura Restaurantes')
st.sidebar.markdown('##### *Trazendo a melhor experiência culinária!*')
st.sidebar.markdown("""---""")

paises_selec = st.sidebar.multiselect(label='Selecione os países', 
                       options=['Philippines', 'Brazil', 'Australia', 'United States of America',
       'Canada', 'Singapure', 'United Arab Emirates', 'India',
       'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
       'Sri Lanka', 'Turkey'],
                       default = ['Brazil', 'England','Qatar', 'South Africa', 'Canada', 'Australia'])


#Vinculando os widgets aos dados
linhas_selecionadas = data['country'].isin(paises_selec)
data = data.loc[linhas_selecionadas, :]
#linhas_selecionadas = (data['aggregate_rating'] >= nota_inicial) & (data['aggregate_rating'] <= nota_final)
#data = data.loc[linhas_selecionadas, :]

st.sidebar.markdown('##### Powered by Camillo Lepore')

# -------------------------------------------
# Layout
# -------------------------------------------
st.markdown("# :earth_americas: Visão de Países")

with st.container():
         # st.markdown('### Quantidade de restaurantes por país')
        df_aux = (data[['country', 'restaurant_name']]
        .groupby('country')
        .nunique()
        .sort_values(by='restaurant_name', ascending=False)
        .reset_index())

        fig = px.bar(x=df_aux.country, 
            y=df_aux.restaurant_name,
            title='Quantidade de restaurantes por país',
            labels={'x':'Países', 'y':'Número de restaurantes registrados'},
            color=df_aux.country)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

with st.container():
    # st.markdown('### Quantidade de cidades por país')
    df_aux = (data[['country', 'city']]
    .groupby('country')
    .nunique()
    .sort_values(by='city', ascending=False)
    .reset_index())
    
    fig = px.bar(x=df_aux.country, 
        y=df_aux.city,
        title='Quantidade de cidades por país',
        labels={'x':'Países', 'y':'Número de cidades registradas'},
        color=df_aux.country)
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    st.markdown('## Avaliações', )
    col1, col2 = st.columns(2)
    
    with col1:
        # st.markdown('### Média de notas por país')
        df_aux = (data[['country', 'aggregate_rating']]
        .groupby('country')
        .mean()
        .round(2)
        .sort_values(by='aggregate_rating', ascending=False)
        .reset_index())

        fig = px.bar(x=df_aux.country, 
            y=df_aux.aggregate_rating,
            title='Nota média dos restaurantes por país',
            labels={'x':'Países', 'y':'Nota média dos restaurantes'},
            color=df_aux.country)
        # fig = go.Figure(fig, layout_yaxis_range = [3, 5])
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # st.markdown('### Média de avaliaçoes por restaurante em cada país')
        df_aux = (data[['country', 'votes']]
        .groupby('country')
        .mean()
        .round(2)
        .sort_values(by='votes', ascending=False)
        .reset_index())

        fig = px.bar(x=df_aux.country, 
            y=df_aux.votes,
            title='Quantidade média de avaliaçoes por país',
            labels={'x':'Países', 'y':'Quantidade média de avaliaçoes'},
            color=df_aux.country)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)














