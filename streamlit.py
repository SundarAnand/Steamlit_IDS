# Required libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Introduction
st.write(""" 
# Interactive Data Science
## By Annie Johnson and Sundar Anand
## Interesting trends when pandemic happened""")

# Reading the file
country_df = pd.read_csv("vaccination dataset/country.csv")

# Getting only vaccination data
vaccine_df = country_df[(country_df['people_vaccinated'].notna())]
vaccine_df['date'] = pd.to_datetime(vaccine_df['date']).dt.date
vaccine_df = vaccine_df.sort_values(by='date')

# Getting the country list
country_list = sorted(vaccine_df['country'].unique())

# Getting country and date as input
option = st.selectbox('Pick a country', country_list)
country_vaccine_df = vaccine_df[(vaccine_df['country'] == option)]
date = st.select_slider("Pick a date", options = country_vaccine_df['date'].unique())

# Calculating the percentage of vaccination

vacc_info_df = country_vaccine_df[(country_vaccine_df['date'] == pd.to_datetime(str(date)))]
vacc = vacc_info_df['people_vaccinated'].iloc[0]
per = round(vacc*100/vacc_info_df['population'].iloc[0], 2)

# Displaying the results
st.write("The total vaccinated people are " + str(vacc) + " and the vaccination percentage as of " + str(date) + " is " + str(per) + "%")

# Country wise comparison bar graphs
vaccine_df['date'] = pd.to_datetime(vaccine_df['date']).dt.strftime('%Y-%m-%d')
countries = st.multiselect("Which country do you like to see?", country_list, ['United States'])
date = st.selectbox("Pick a date", options = ['autoplay'] + list(vaccine_df[vaccine_df['country'].isin(countries)]['date'].unique()))

# For a selected date
if date != 'autoplay':
    conditioned_df = vaccine_df[(vaccine_df['country'].isin(countries)) & (vaccine_df['date'] == pd.to_datetime(date))]
    fig = px.bar(conditioned_df, x='country', y='people_vaccinated', color='country')

# For all dates
else:
    conditioned_df = vaccine_df[(vaccine_df['country'].isin(countries))]
    #conditioned_df['date'] = pd.to_datetime(conditioned_df['date']).dt.strftime('%Y-%m-%d')
    fig = px.bar(conditioned_df, x='country', y='people_vaccinated', range_y=[0, max(conditioned_df['people_vaccinated'])], color='country', animation_frame='date', animation_group='country')
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 4
    fig.update_layout(width=1000)

# Displaying the graph
st.write(fig)