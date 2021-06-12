import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

st.image("./data/RB.png")
st.title("RedBull Energy Graph")
"""
Этот граф построен на основе открытых данных с сайта RedBull. Давайте попробуем поиграться с ним.
Выбери, что ты хочешь.
"""
df = pd.read_csv("./data/RedBull_graph.csv")
#... columns=['name', 'sport', 'birth', 'naton']
df['origin'] = 'RedBull'
#не забыть df.dropna()
variants = ['Посмтореть все виды спорта','Посмотреть разбиение по странам']
what = st.selectbox('Что?', variants)
if what == variants[0]:
    nodes = list(df['sport'].unique())
    nodes.extend(df['name'])
    nodes.extend(["RedBull"])

    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)

    for _, row in df.iterrows():
        graph.add_edge(row['origin'], row['sport'])
        graph.add_edge(row['sport'], row['name'])

    net = Network(width='800px', notebook=True)
    net.from_nx(graph)
    net.show("./data/graph.html")
    HtmlFile = []
    with open("./data/graph.html", 'r', encoding='utf-8') as f:
        HtmlFile = f.read()
    components.html(HtmlFile, height=1200, width=1000)

else:
    countries = df['nation'].unique()

    nodes = list(countries)
    nodes.extend(df['name'].unique())
    nodes.extend(["RedBull"])


    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)

    for c in countries:
        sportsmen = df[df['nation'] == c]
        for s in sportsmen['name'].unique():
            graph.add_edge(c, s)

    net = Network(width='800px', notebook=True)
    net.from_nx(graph)
    net.show("./data/graph.html")
    HtmlFile = []
    with open("./data/graph.html", 'r', encoding='utf-8') as f:
        HtmlFile = f.read()
    components.html(HtmlFile, height=1200, width=1000)

'''
## Давайте посмторим на статистику:

Количесвто спортсменов:
'''
st.dataframe(df[['nation', 'name']].groupby('nation').count().rename(columns={'name': '#'}).sort_values(by='#', ascending=False))


df['age'] = 2021 - df['birth']
'''
Рейтинг по возрасту:
'''
st.dataframe(df[['age', 'nation']].groupby('nation').mean().rename(columns={'age':'mean age'}).sort_values(by='mean age'))

