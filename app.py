import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Função para plotar histogramas 3D
def plotar_histogramas_3d(mapa1, mapa2, mapa3, bins, xinf, xsup, elev, azim, largura_barra):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Calculando os histogramas
    n_col1, bins_col1 = np.histogram(mapa1, bins=bins, range=(xinf, xsup))
    n_col2, bins_col2 = np.histogram(mapa2, bins=bins, range=(xinf, xsup))
    n_col3, bins_col3 = np.histogram(mapa3, bins=bins, range=(xinf, xsup))

    # Definindo a largura das barras
    width = (bins_col1[1] - bins_col1[0])*largura_barra
    x_col1 = bins_col1[:-1] + width / 2
    x_col2 = bins_col2[:-1] + width / 2
    x_col3 = bins_col3[:-1] + width / 2

    # Plota os histogramas 3D
    ax.bar3d(x_col1, np.zeros_like(x_col1), np.zeros_like(x_col1), width, width, n_col1, color='blue', edgecolor='black', alpha=0.6, label=col1)
    ax.bar3d(x_col2, np.ones_like(x_col2), np.zeros_like(x_col2), width, width, n_col2, color='yellow', edgecolor='black', alpha=0.6, label=col2)
    ax.bar3d(x_col3, np.full_like(x_col3, 2), np.zeros_like(x_col3), width, width, n_col3, color='red', edgecolor='black', alpha=0.6, label=col3)

    # Etiquetas
    ax.set_xlabel('Temperatura')
    ax.set_zlabel('Frequência')
    ax.set_xlim(xinf, xsup)
    ax.set_ylim([-1, 3])

    # Remover ticks do eixo y
    ax.set_yticks([])

    ax.view_init(elev=elev, azim=azim)

    # Adicionar a legenda
    ax.legend([col1, col2, col3], loc='upper left', fontsize=10)

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
  
    xinf = st.sidebar.number_input('Valor mínimo (xinf)', value=float(df[[col1, col2, col3]].min().min()))
    xsup = st.sidebar.number_input('Valor máximo (xsup)', value=float(df[[col1, col2, col3]].max().max()))

    largura_barra = st.sidebar.number_input('Largura da Barra', min_value=0.0, max_value=1.0, value=0.5)

    if st.sidebar.button('Gerar Histograma 3D'):
        fig = plotar_histogramas_3d(df[col1], df[col2], df[col3], bins, xinf, xsup, elev, azim, largura_barra)
        st.pyplot(fig)
