import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Título da aplicação
st.write('Preços Placas de Video RTX 4060')

# Criar conexão com o banco de dados SQLite
engine = create_engine('sqlite:///../0_bases_originais/Placa_de_Video.db')

# Leitura da tabela do banco de dados
df = pd.read_sql('SELECT * FROM Placa_de_Video', con=engine)

# Conversão de colunas para numérico e preenchimento de valores nulos
df["Preco_a_vista"] = pd.to_numeric(df["Preco_a_vista"], errors="coerce").fillna(0)
df["Valor_parcelado"] = pd.to_numeric(df["Valor_parcelado"], errors="coerce").fillna(0)

# Criando a coluna 'Faixa_parcelado' com faixas de preço
df['Faixa_parcelado'] = pd.cut(
    df['Valor_parcelado'],
    bins=[0, 1000, 2000, 3000, 4000, 5000, float('inf')],
    labels=['0-1k', '1k-2k', '2k-3k', '3k-4k', '4k-5k', '5k+']
)

# Boxplot - Preço à vista
fig_box = px.box(df, y='Preco_a_vista', title='Boxplot - Preço à Vista')
st.plotly_chart(fig_box)

# Histograma - Preço à vista
fig_hist = px.histogram(df, x='Preco_a_vista', nbins=20, title='Histograma - Preço à Vista')
st.plotly_chart(fig_hist)

# Contando os valores por faixa de preço parcelado
faixa_counts = df['Faixa_parcelado'].value_counts().reset_index()
faixa_counts.columns = ['Faixa_de_Preco', 'Quantidade']  # Renomeando colunas

# Criando o gráfico de pizza
fig_pizza = px.pie(
    faixa_counts,
    names='Faixa_de_Preco',  # Nome das fatias
    values='Quantidade',     # Tamanho das fatias
    title='Distribuição por Faixa de Preço Parcelado',  # Título do gráfico
    color_discrete_sequence=px.colors.sequential.RdBu  # Opcional: paleta de cores
)

# Exibindo o gráfico de pizza no Streamlit
st.plotly_chart(fig_pizza)

# Exibindo a tabela de faixas e quantidades para verificação
st.write(faixa_counts)

# Gráfico de dispersão com relação entre Preço à Vista e Valor Parcelado
fig_scatter = px.scatter(
    df,
    x='Preco_a_vista',
    y='Valor_parcelado',
    color='Faixa_parcelado',  # Diferencia por faixa de preço parcelado
    size='Valor_parcelado',   # Tamanho dos pontos baseado no valor parcelado
    hover_data=['Preco_a_vista', 'Valor_parcelado'],  # Informações ao passar o mouse
    labels={
        'Preco_a_vista': 'Preço à Vista',
        'Valor_parcelado': 'Valor Parcelado',
        'Faixa_parcelado': 'Faixa de Preço'
    },
    title='Relação entre Preço à Vista, Valor Parcelado e Faixa de Preço'
)

# Exibindo o gráfico no Streamlit
st.plotly_chart(fig_scatter)

# Histograma Multivariado: Preço à Vista por Faixa de Preço Parcelado
fig_hist_mult = px.histogram(
    df,
    x='Preco_a_vista',
    color='Faixa_parcelado',  # Categorização por faixa de preço parcelado
    nbins=20,
    labels={
        'Preco_a_vista': 'Preço à Vista',
        'Faixa_parcelado': 'Faixa de Preço Parcelado'
    },
    title='Distribuição de Preço à Vista por Faixa de Preço Parcelado',
    barmode='overlay',  # Sobreposição das barras para comparar distribuições
    opacity=0.7         # Ajusta a transparência para facilitar a visualização
)
st.plotly_chart(fig_hist_mult)

# Gráfico de Barras: Média de Preço à Vista por Faixa de Preço Parcelado
media_preco = df.groupby('Faixa_parcelado')['Preco_a_vista'].mean().reset_index()
fig_bar_mult = px.bar(
    media_preco,
    x='Faixa_parcelado',
    y='Preco_a_vista',
    labels={
        'Faixa_parcelado': 'Faixa de Preço Parcelado',
        'Preco_a_vista': 'Média de Preço à Vista'
    },
    title='Média de Preço à Vista por Faixa de Preço Parcelado',
    color='Faixa_parcelado',  # Opcional: pode usar uma paleta de cores
    text='Preco_a_vista'  # Exibe os valores no topo das barras
)
fig_bar_mult.update_traces(texttemplate='%{text:.2f}', textposition='outside')  # Formata os valores

st.plotly_chart(fig_bar_mult)
