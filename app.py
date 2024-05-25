import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import streamlit as st

# Carregar o dataset
file_path = 'ACIDENTES_FRANCA_2505.xlsx'
data = pd.read_excel(file_path)

# Verificar os nomes das colunas
st.write("Nomes das colunas no DataFrame:", data.columns)

# Corrigir nomes de colunas se necessário
data.columns = [col.strip() for col in data.columns]  # Remove leading/trailing spaces

# Verificar se a coluna 'Ano' existe e ajustar o nome se necessário
if 'Ano do BO' in data.columns:
    data.rename(columns={'Ano do BO': 'Ano'}, inplace=True)

# Adicionar colunas 'Ano' e 'Mês' se não existirem
if 'Ano' not in data.columns:
    data['Ano'] = pd.to_datetime(data['Data do Sinistro']).dt.year
if 'Mês' not in data.columns:
    data['Mês'] = pd.to_datetime(data['Data do Sinistro']).dt.month

# Filtros de ano
anos_disponiveis = sorted([ano for ano in data['Ano'].unique() if ano <= 2023])
ano_selecionado = st.sidebar.selectbox('Selecione o Ano', anos_disponiveis, index=len(anos_disponiveis)-1)
data_filtered = data[data['Ano'] == ano_selecionado]

# Tabs para diferentes seções da análise
tab1, tab2, tab3, tab4 = st.tabs(["Distribuição Temporal", "Análise de Vítimas", "Localização", "Dados Brutos"])

with tab1:
    st.header('Distribuição Temporal Detalhada')

    # Gráfico de linha para mostrar a tendência dos acidentes ao longo dos anos
    accidents_per_year = data.groupby('Ano')['Data do Sinistro'].count()
    st.subheader('Tendência dos Acidentes por Ano')
    fig, ax = plt.subplots()
    accidents_per_year.plot(kind='line', marker='o', color='skyblue', ax=ax)
    ax.set_title('Tendência dos Acidentes por Ano')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Número de Acidentes')
    st.pyplot(fig)

    # Gráfico de linha para mostrar a tendência dos acidentes ao longo dos meses
    accidents_per_month = data_filtered.groupby('Mês')['Data do Sinistro'].count()
    st.subheader('Tendência dos Acidentes por Mês')
    fig, ax = plt.subplots()
    accidents_per_month.plot(kind='line', marker='o', color='orange', ax=ax)
    ax.set_title('Tendência dos Acidentes por Mês')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Número de Acidentes')
    st.pyplot(fig)

    # Boxplot para a distribuição dos acidentes por dia da semana
    st.subheader('Distribuição dos Acidentes por Dia da Semana')
    fig, ax = plt.subplots()
    data_filtered.boxplot(column='Hora do Sinistro', by='Dia da Semana', grid=False, ax=ax)
    ax.set_title('Distribuição dos Acidentes por Dia da Semana')
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Hora do Sinistro')
    st.pyplot(fig)

    # Boxplot para a distribuição dos acidentes por turno
    st.subheader('Distribuição dos Acidentes por Turno')
    fig, ax = plt.subplots()
    data_filtered.boxplot(column='Hora do Sinistro', by='Turno', grid=False, ax=ax)
    ax.set_title('Distribuição dos Acidentes por Turno')
    ax.set_xlabel('Turno')
    ax.set_ylabel('Hora do Sinistro')
    st.pyplot(fig)

with tab2:
    st.header('Análise de Vítimas Detalhada')

    # Boxplot da idade das vítimas por sexo
    st.subheader('Distribuição da Idade das Vítimas por Sexo')
    fig, ax = plt.subplots()
    data_filtered.boxplot(column='Idade da v�tima', by='Sexo', grid=False, ax=ax)
    ax.set_title('Distribuição da Idade das Vítimas por Sexo')
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Idade da Vítima')
    st.pyplot(fig)

    # Análise cruzada de tipo de sinistro com faixa etária
    st.subheader('Análise Cruzada de Tipo de Sinistro com Faixa Etária')
    cross_tab_sinistro_faixa = pd.crosstab(data_filtered['Tipo de Sinistro'], data_filtered['Faixa et�ria'])
    st.dataframe(cross_tab_sinistro_faixa)

with tab3:
    st.header('Localização dos Acidentes')

    # Filtrar dados que têm latitude e longitude disponíveis
    location_data_filtered = data_filtered.dropna(subset=['latitude', 'longitude'])

    # Criar um mapa de folium
    mapa_acidentes_filtered = folium.Map(location=[-20.53, -47.4], zoom_start=12)

    # Adicionar pontos ao mapa
    for _, row in location_data_filtered.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(mapa_acidentes_filtered)

    # Exibir o mapa no Streamlit
    folium_static(mapa_acidentes_filtered)

with tab4:
    st.header('Dados Brutos')
    st.dataframe(data_filtered)
