import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout='wide')

# Import and Clear Data
df = pd.read_csv('numberofinternetusers.csv')
df = df[df['Number of Internet users'] > 0]
df = df.drop(['Code'], axis=1)

# Creating groups
entities_to_exclude = ['High-income countries', 'World']
continents = ['Europe', 'Asia']

world_users = df[df['Entity'] == 'World']
df = df[~df['Entity'].isin(entities_to_exclude)]
df_continents_users = df[df['Entity'].isin(continents)]
df_countrys_users = df[~df['Entity'].isin(continents)]

# Import and Clear Data
dfUrban = pd.read_csv('urban_total.csv')
dfUrban = dfUrban.drop(['Country Code', 'Indicator Name',
                       'Indicator Code', 'Unnamed: 65'], axis=1)
dfUrban = dfUrban.dropna()


with st.sidebar:
    st.title('Functions')
    general = st.checkbox(label='General Countries')
    compare = st.checkbox(label='Comparison Countries')
    top_10_chk = st.checkbox(label='Top 10')
    map_viz = st.checkbox(label='Map Visualization')
    if top_10_chk == True or map_viz == True:
        with st.container(border=1):
            yearSelected = st.slider(label='Select a year',
                                     min_value=1990, max_value=2020)
    if compare:
        with st.container(border=1):
            year_options = df_countrys_users['Year'].unique()
            year_comparison = st.selectbox(label='Year', options=year_options)
            entity_options = df_countrys_users['Entity'].unique()
            entity_comparison = st.multiselect(
                label='Comparation', options=entity_options)

if general == True:
    st.markdown("""<center><h1>General Data</h1></center>""",
                unsafe_allow_html=True)
    gph_world_users = px.bar(
        world_users,
        x='Year',
        y='Number of Internet users',
        labels={'x': 'Year', 'y': 'Users'})
    st.plotly_chart(gph_world_users, use_container_width=True)

if compare == True:
    st.markdown(f"""<center><h1>Compare Country</h1></center>""",
                unsafe_allow_html=True)

    filtered_df = df_countrys_users[df_countrys_users['Entity'].isin(
        entity_comparison) & (df_countrys_users['Year'] == year_comparison)].sort_values('Number of Internet users')

    fig = px.bar(filtered_df, x='Entity', y='Number of Internet users',
                 title=f"{year_comparison} - Comparison of Entities", color='Entity', barmode='relative')
    st.plotly_chart(fig, use_container_width=True)


if top_10_chk == True:
    st.markdown(f"""<center><h1>Top 10 in Year</h1></center>""",
                unsafe_allow_html=True)

    top_10 = px.bar(df_countrys_users[df_countrys_users['Year'] == yearSelected].sort_values('Number of Internet users', ascending=False)[:10],
                    x='Number of Internet users',
                    y='Entity',
                    text_auto='Entity',
                    color='Entity',
                    height=600,
                    labels={'Entity': '', 'Number of Internet users': ''},
                    )
    st.plotly_chart(top_10, use_container_width=True)

if map_viz == True:
    fig = px.choropleth(df_countrys_users[df_countrys_users['Year'] == yearSelected].sort_values('Number of Internet users', ascending=False),
                        locations='Entity',
                        locationmode='country names',
                        color='Number of Internet users',
                        color_continuous_scale='plasma',
                        fitbounds=False,
                        height=700
                        )

    st.plotly_chart(fig, use_container_width=True)

if map_viz and top_10_chk:
    fig, top_10 = st.columns(2)
