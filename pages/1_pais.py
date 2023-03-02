# bibliotecas necessárias
import pandas as pd
import io
import inflection
import streamlit as st
#from haversine import haversine
import numpy as np
import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px
from PIL import Image

#---------------------Funções-------------------------
#Preenchimento do nome dos países

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
def country_name(country_id):
    return COUNTRIES[country_id]

#-------------------------------------------------------

# Criação do Tipo de Categoria de Comida

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

#-------------------------------------------------------

# Criação do nome das Cores

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

#------------------------------------------------------

# Renomear as colunas do DataFrame

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

#------------------------------------------------------

# mais valores em uma coluna por pais
def registros(df, column):
    aux = df[[column,'country_code']].groupby('country_code').nunique().reset_index().sort_values(column, ascending = False)
    return aux

#-----------------------------------------------------

#mais contagem por coluna por pais

def count_pais(df, column):
    aux = df[[column,'country_code']].groupby('country_code').count().reset_index().sort_values(column, ascending = False)
    return aux

#-----------------------------------------------------

# mais valores em uma coluna por cidade
def registros_city(df, column):
    aux = df[[column,'city', 'country_code']].groupby(['city', 'country_code']).nunique().reset_index().sort_values(column, ascending = False)
    return aux

#-----------------------------------------------------

#mais contagem por coluna por cidade

def count_city(df, column):
    aux = df[[column,'country_code']].groupby('country_code').count().reset_index().sort_values(column, ascending = False)
    return aux

#-----------------------------------------------------

# mais valores em uma coluna por restaurante
def registros_rest(df, column):
    aux = (df[[column,'restaurant_id', 'restaurant_name']]
         .groupby(['restaurant_name','restaurant_id'])
         .nunique()
         .reset_index()
         .sort_values(column, ascending = False))
    return aux

#------------------------------------------------------

#tipo culinaria e avaliação
def registros_culinaria(df, cuisines, ord):
    df_aux = df[(df['cuisines'] == cuisines)]
    aux = (df_aux[['restaurant_id', 'restaurant_name', 'aggregate_rating']]
         .groupby(['restaurant_name','restaurant_id'])
         .max()
         .reset_index()
         .sort_values(['aggregate_rating', 'restaurant_id'], ascending = ord))
  
    return aux

#_______________________________________Inicio da estrutura lógica do código_____________________________________
#import data set

df = pd.read_csv('zomato.csv')

df1 = df.copy()


#-------------------------------Tratando DF-------------
#retirando colunas irrelevantes

df1 = df1.drop("Switch to order menu", axis='columns')

# Arrumando nome dos paises
df1['Country Code'] = df1['Country Code'].apply(lambda x: country_name(x))
# Arrumando price tag
df1['Price range'] = df1['Price range'].apply(lambda x: create_price_tye(x))

# Criação do nome das Cores
df1['Rating color'] = df1['Rating color'].apply(lambda x: color_name(x))

# Renomear as colunas do DataFrame
df1 = rename_columns(df1)

# Somente um tipo de culinária
df1 = df1[df1['cuisines'].notnull()]
df1["cuisines"] = df1["cuisines"].apply(lambda x: x.split(",")[0])

df1 = df1.drop_duplicates()
df1 = df1.reset_index(drop = True)

#substituindo dado errado
df1 = df1.replace(25000017, 25)


#========================================
#Barra lateral
#========================================
image=Image.open('mundo.png')
st.image('mundo.png', width=50)
        
st.header( 'Visão Paises')

#image_path = 'C:/Users/Leonardo Paz/Documents/Repos/fundamentos_ftc/ciclo 6/alvo.png'
st.sidebar.markdown('# Fome Zero!!')
image=Image.open('logo.png')
st.sidebar.image('logo.png', width=120)


st.sidebar.markdown('## O Seu Favorito Novo Restaurante')
st.sidebar.markdown("""---""")

st.sidebar.markdown('# Filtros')


country_options=st.sidebar.multiselect(
    'Selecione os Países que Deseja Vizualizar',
    ["India","Australia","Brazil",
     "Canada", "Indonesia", "New Zeland",
     "Philippines", "Qatar", "Singapure",
     "South Africa", "Sri Lanka","Turkey",
     "United Arab Emirates", "England","United States of America"],
    default=["India", "United States of America" ,"Philippines", "South Africa","England", "New Zeland" ])

st.sidebar.markdown("""---""")



st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by CDS')


#Filtro de país

linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]


#========================================
#Layout no Streamlit
#========================================
with st.container():
    # pais com mais cidade reguistrada 
           
     
    df_cidades_pais = registros(df1, 'city')

    fig = px.bar(df_cidades_pais, y='city', x='country_code', text_auto='.2s',
             labels={
                     "city": "N° de Cidades",
                     "country_code": "País"                    
                 },
            title="N° de Cidades por País",
                )
        
    st.plotly_chart(fig, use_container_width=True)
   
    
with st.container():
    # pais com mais restaurante reguistrado

    df_rest_pais = registros(df1,'restaurant_id' )




    fig = px.bar(df_rest_pais, y='restaurant_id', x='country_code', text_auto='.2s',
             labels={
                     "restaurant_id": "N° de Restaurantes",
                     "country_code": "País"                    
                 },
            title="N° de Restaurantes por País")
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns (2)
    with col1:
       # mais avaliações feitas
        pais_mais_ava = df1[['votes','country_code']].groupby('country_code').sum().reset_index().sort_values('votes', ascending = False)

        fig = px.bar(pais_mais_ava, y='votes', x='country_code', text_auto='.2s',
             labels={
                     "votes": "N° Votos",
                     "country_code": "País"                    
                 },
            title="N° de Avaliações por País") 
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
       # pais com maior valor médio de avaliações 

        pais_avaliacoes = df1[['aggregate_rating','country_code']].groupby('country_code').mean().reset_index().sort_values('aggregate_rating', ascending = False)



        fig = px.bar(pais_avaliacoes, y='aggregate_rating', x='country_code', text_auto='.2s',
             labels={
                     "aggregate_rating": "Nota Média",
                     "country_code": "País"                    
                 },
            title="Avaliação Media por País") 
        st.plotly_chart(fig, use_container_width=True)