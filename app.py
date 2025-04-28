import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Função para plotar histogramas 3D
def plotar_histogramas_3d(mapa_temperatura_etanol, mapa_temperatura_agua, mapa_temperatura_dec, bins, xinf, xsup, elev, azim, largura_barra):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Calculando os histogramas
    n_etanol, bins_etanol = np.histogram(mapa_temperatura_etanol, bins=bins, range=(xinf, xsup))
    n_agua, bins_agua = np.histogram(mapa_temperatura_agua, bins=bins, range=(xinf, xsup))
    n_dec, bins_dec = np.histogram(mapa_temperatura_dec, bins=bins, range=(xinf, xsup))

    # Definindo a largura das barras
    width = (bins_etanol[1] - bins_etanol[0])*largura_barra
    x_etanol = bins_etanol[:-1] + width / 2
    x_agua = bins_agua[:-1] + width / 2
    x_dec = bins_dec[:-1] + width / 2

    # Plota os histogramas 3D
    ax.bar3d(x_etanol, np.zeros_like(x_etanol), np.zeros_like(x_etanol), width, width, n_etanol, color='blue', edgecolor='black', alpha=0.6, label='Etanol')
    ax.bar3d(x_agua, np.ones_like(x_agua), np.zeros_like(x_agua), width, width, n_agua, color='yellow', edgecolor='black', alpha=0.6, label='Água')
    ax.bar3d(x_dec, np.full_like(x_dec, 2), np.zeros_like(x_dec), width, width, n_dec, color='red', edgecolor='black', alpha=0.6, label='DEC')

    # Etiquetas
    ax.set_xlabel('Temperatura')
    ax.set_zlabel('Frequência')
    ax.set_xlim(xinf, xsup)
    ax.set_ylim([-1, 3])

    # Remover ticks do eixo y
    ax.set_yticks([])

    ax.view_init(elev=elev, azim=azim)

    # Retorna a figura para o Streamlit
    return fig

# --- Streamlit App ---

st.title("Histograma 3D de Temperaturas")

# Carregar o arquivo CSV
uploaded_file = st.file_uploader("Escolha o arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Selecione as colunas no sidebar
    colunas = df.columns.tolist()
    col1 = st.sidebar.selectbox('Selecione a primeira coluna:', colunas)
    col2 = st.sidebar.selectbox('Selecione a segunda coluna:', colunas)
    col3 = st.sidebar.selectbox('Selecione a terceira coluna:', colunas)

    # Ajuste dos parâmetros no sidebar
    bins = st.sidebar.number_input('Número de bins', min_value=5, max_value=100, value=20)
    elev = st.sidebar.number_input('Elevação', min_value=0, max_value=360, value=30)
    azim = st.sidebar.number_input('Azimute', min_value=0, max_value=360, value=60)
  
    xinf = st.sidebar.number_input('Valor mínimo (xinf)', value=float(df[[col_etanol, col_agua, col_dec]].min().min()))
    xsup = st.sidebar.number_input('Valor máximo (xsup)', value=float(df[[col_etanol, col_agua, col_dec]].max().max()))

    largura_barra = st.sidebar.number_input('Largura da Barra', min_value=0.0, max_value=1.0, value=0.5)

    if st.sidebar.button('Gerar Histograma 3D'):
        fig = plotar_histogramas_3d(df[col1], df[col2], df[col3], bins, xinf, xsup, elev, azim, largura_barra)
        st.pyplot(fig)
