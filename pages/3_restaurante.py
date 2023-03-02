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
image=Image.open('restaurante.png')
st.image('restaurante.png', width=150)
        
st.header( 'Visão Restaurante')

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
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Restaurantes com mais avaliações e nota media destes')
        #nome do restaurante que possui a maior quantidade de avaliações
        nome_aval = (df1[['votes','restaurant_id', 'restaurant_name','aggregate_rating']]
             .groupby(['restaurant_name','restaurant_id'])
             .sum()
             .sort_values('votes', ascending = False)
             .reset_index())
        nome_aval = nome_aval.loc[0:10,['restaurant_name', 'votes','aggregate_rating' ]]
        nome_aval 
        
    with col2:
        st.markdown('#### Restaurantes com maior nota media com mais de 1000 votos')
        #nome do restaurante com a maior nota média com mais de 1000 votos
        aux = df1[(df1['votes']>1000)]
        maior_nota_media = (aux[['aggregate_rating','restaurant_id', 'restaurant_name','votes']]
             .groupby(['restaurant_name','restaurant_id'])
             .max()             
             .sort_values(['aggregate_rating','restaurant_id'] , ascending = False)
             .reset_index())
        maior_nota_media = maior_nota_media.loc[0:10,['restaurant_name', 'aggregate_rating','votes' ]]
        maior_nota_media
        
with st.container():
    #nome do restaurante com o maior valor de uma prato para duas pessoas
    maior_valor_2 = (df1[['average_cost_for_two','restaurant_id', 'restaurant_name', 'country_code']]
             .groupby(['restaurant_name','country_code'])
             .max()
             .reset_index()
             .sort_values(['average_cost_for_two','restaurant_id'] ,   ascending = False))
    maior_valor_2 = maior_valor_2.head(20)
    fig = px.bar(maior_valor_2 ,
            x= 'restaurant_name' ,
            y= 'average_cost_for_two',
             color="country_code",
             text_auto='.2s',
             labels={
                     "restaurant_name": "Restaurante",
                     "average_cost_for_two": "Custo médio para 2 Pessoas"                    
                 },
            title=' Cidades Com Maior Valor de Alimentação Para 2 Pessoas')
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Comparativo de Avaliação Entre Restaurantes que Fazem ou Não Entrega') 
        # restaurantes que aceitam pedido online vs não. média de avaliações registradas

        med_av_online = df1[['has_online_delivery', 'aggregate_rating' ]].groupby(['has_online_delivery']).mean().reset_index()

        med_av_online['has_online_delivery'] = med_av_online['has_online_delivery'].replace([0, 1], ['Não Entrega online', 'Entrega online'])

        colors = ['gold', 'mediumturquoise']

        fig = go.Figure(data=[go.Pie(labels=med_av_online['has_online_delivery'],
                             values=med_av_online['aggregate_rating'])])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, use_container_width=True)

        
    with col2:
        st.markdown('#### Comparativo do Valor para 2 Entre Restaurantes que Fazem ou Não Reserva') 
        #restaurantes que fazem reservas são também, na média, os restaurantes que possuem o maior valor médio de um prato para duas pessoas

        med_preco2_reserva = df1[['has_table_booking', 'average_cost_for_two' ]].groupby(['has_table_booking']).mean().reset_index()

        med_preco2_reserva['has_table_booking'] = med_preco2_reserva['has_table_booking'].replace([0, 1], ['Não Faz Reserva', 'Faz Reserva'])



        colors = ['darkorange', 'lightgreen']

        fig = go.Figure(data=[go.Pie(labels=med_preco2_reserva['has_table_booking'],
                             values=med_preco2_reserva['average_cost_for_two'].round(2))])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        st.plotly_chart(fig, use_container_width=True)

    