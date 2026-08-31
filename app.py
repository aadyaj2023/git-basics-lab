import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Country Development Dashboard",layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("life_expectancy_gdp.csv")
    df = df.rename(columns={"Entity":"country","Year":"year","Life expectancy at birth":"lifeExp","GDP per capita":"gdpPercap","Population":"pop","World region according to OWID":"continent"})
    df = df.dropna(subset=["country","year","lifeExp","gdpPercap","pop","continent"])
    return df

df = load_data()
st.title("Country Development Dashboard")

st.sidebar.header("Filters")
years = sorted(df["year"].unique())
selected_year = st.sidebar.select_slider("Year",options=years,value=years[-1])
continents = sorted(df["continent"].unique())
selected_continents = st.sidebar.multiselect("Continent",continents,default=continents)
min_population = st.sidebar.slider("Minimum Population",min_value=0,max_value=int(df["pop"].max()),value=0,step=1_000_000)

filtered = df[(df["year"]==selected_year)&(df["continent"].isin(selected_continents))&(df["pop"]>=min_population)]

col1,col2,col3 = st.columns(3)
col1.metric("Countries Shown",filtered["country"].nunique())
col2.metric("Median Life Expectancy",f"{filtered['lifeExp'].median():.1f} yrs")
col3.metric("Total Population",f"{filtered['pop'].sum()/1e9:.2f} B")

fig = px.scatter(filtered,x="gdpPercap",y="lifeExp",size="pop",color="continent",hover_name="country",log_x=True,size_max=60,title=f"GDP per Capita vs Life Expectancy - {selected_year}")
st.plotly_chart(fig,use_container_width=True)

st.subheader("Drill Down into a Country")
country_pick = st.selectbox("Choose a country",sorted(filtered["country"].unique()))
country_hist = df[df["country"]==country_pick]
fig2 = px.line(country_hist,x="year",y="lifeExp",markers=True,title=f"Life Expectancy Over Time - {country_pick}")
st.plotly_chart(fig2,use_container_width=True)
