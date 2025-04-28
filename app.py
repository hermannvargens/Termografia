import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Função para plotar histogramas 3D
def plotar_histogramas_3d(mapa1, mapa2, mapa3, bins, xinf, xsup, elev, azim, largura_barra, comprimento_barra, alpha1, alpha2, alpha3, col1, col2, col3):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    n_col1, bins_col1 = np.histogram(mapa1, bins=bins, range=(xinf, xsup))
    n_col2, bins_col2 = np.histogram(mapa2, bins=bins, range=(xinf, xsup))
    n_col3, bins_col3 = np.histogram(mapa3, bins=bins, range=(xinf, xsup))

    width = (bins_col1[1] - bins_col1[0]) * largura_barra
    x_col1 = bins_col1[:-1] + width / 2
    x_col2 = bins_col2[:-1] + width / 2
    x_col3 = bins_col3[:-1] + width / 2

    ax.bar3d(x_col1, np.zeros_like(x_col1), np.zeros_like(x_col1), width*comprimento_barra, width, n_col1, color='blue', edgecolor=None, alpha=alpha1, label=col1)
    ax.bar3d(x_col2, np.ones_like(x_col2), np.zeros_like(x_col2), width*comprimento_barra, width, n_col2, color='yellow', edgecolor=None, alpha=alpha2, label=col2)
    ax.bar3d(x_col3, np.full_like(x_col3, 2), np.zeros_like(x_col3), width*comprimento_barra, width, n_col3, color='red', edgecolor=None, alpha=alpha3, label=col3)

    ax.set_xlabel('Temperatura')
    ax.set_zlabel('Frequência')
    ax.set_xlim(xinf, xsup)
    ax.set_ylim([-1, 3])

    ax.set_yticks([])

    ax.view_init(elev=elev, azim=azim)
    ax.legend([col1, col2, col3], loc='upper left', fontsize=10)

    return fig

# Função para plotar gráficos 2D
def plotar_histogramas_2d(df, colunas, bins, xinf, xsup, alpha):
    fig, ax = plt.subplots(figsize=(10, 6))
    for coluna in colunas:
        ax.hist(df[coluna], bins=bins, range=(xinf, xsup), alpha=alpha, label=coluna, edgecolor="black")
    ax.set_xlabel('Temperatura')
    ax.set_ylabel('Frequência')
    ax.legend()
    return fig

# --- Streamlit App ---
st.set_page_config(page_title="App de Histogramas", layout="wide")

# Sidebar para escolha de página
pagina = st.sidebar.selectbox("Selecione a Página", ["Gráfico 3D", "Gráfico 2D"])

# Upload do arquivo
uploaded_file = st.sidebar.file_uploader("Escolha o arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    colunas = df.columns.tolist()

    if pagina == "Gráfico 3D":
        st.title("Histograma 3D de Temperaturas")

        col1 = st.sidebar.selectbox('Selecione a primeira coluna:', colunas, key='col1_3d')
        col2 = st.sidebar.selectbox('Selecione a segunda coluna:', colunas, key='col2_3d')
        col3 = st.sidebar.selectbox('Selecione a terceira coluna:', colunas, key='col3_3d')

        bins = st.sidebar.number_input('Número de bins', min_value=5, max_value=100, value=20, key='bins_3d')
        elev = st.sidebar.number_input('Elevação', min_value=0, max_value=360, value=30, key='elev_3d')
        azim = st.sidebar.number_input('Azimute', min_value=0, max_value=360, value=60, key='azim_3d')
        xinf = st.sidebar.number_input('Valor mínimo (xinf)', value=float(df[[col1, col2, col3]].min().min()), key='xinf_3d')
        xsup = st.sidebar.number_input('Valor máximo (xsup)', value=float(df[[col1, col2, col3]].max().max()), key='xsup_3d')
        largura_barra = st.sidebar.number_input('Largura da Barra', min_value=0.0, max_value=1.0, value=0.5, key='largura_barra')
        comprimento_barra = st.sidebar.number_input('Comprimento da Barra', min_value=0.0, max_value=10.0, value=1.0, key='comprimento_barra')
        alpha1 = st.sidebar.number_input('Alpha 1', min_value=0.0, max_value=1.0, value=0.5, key='alpha1')
        alpha2 = st.sidebar.number_input('Alpha 2', min_value=0.0, max_value=1.0, value=0.5, key='alpha2')
        alpha3 = st.sidebar.number_input('Alpha 3', min_value=0.0, max_value=1.0, value=0.5, key='alpha3')

        if st.sidebar.button('Gerar Histograma 3D'):
            fig = plotar_histogramas_3d(df[col1], df[col2], df[col3], bins, xinf, xsup, elev, azim, largura_barra, comprimento_barra, alpha1, alpha2, alpha3, col1, col2, col3)
            st.pyplot(fig)

    elif pagina == "Gráfico 2D":
        st.title("Histograma 2D de Temperaturas")

        colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas:', colunas)
        bins = st.sidebar.number_input('Número de bins', min_value=5, max_value=100, value=20, key='bins_2d')
        alpha = st.sidebar.number_input('Alpha', min_value=0.0, max_value=1.0, value=0.5, key='alpha')

        if colunas_selecionadas:
            xinf = st.sidebar.number_input('Valor mínimo (xinf)', value=float(df[colunas_selecionadas].min().min()), key='xinf_2d')
            xsup = st.sidebar.number_input('Valor máximo (xsup)', value=float(df[colunas_selecionadas].max().max()), key='xsup_2d')

            if st.sidebar.button('Gerar Histograma 2D'):
                fig = plotar_histogramas_2d(df, colunas_selecionadas, bins, xinf, xsup, alpha)
                st.pyplot(fig)
