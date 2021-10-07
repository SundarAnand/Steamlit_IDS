# Required libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Introduction
st.write(""" 
# Interactive Data Science
### By Annie Johnson and Sundar Anand
### Interesting trends when pandemic happened""")

# Reading the file
country_df = pd.read_csv("vaccination dataset/country.csv")
country_df['date'] = pd.to_datetime(country_df['date']).dt.date

# Getting only vaccination data
vaccine_df = country_df[(country_df['percentage_vaccinated'].notna()) & (country_df['percentage_active'].notna())]
vaccine_df = vaccine_df.sort_values(by='date')

# Getting the country list
country_list = sorted(vaccine_df['country'].unique())

st.write("""
#### Let's compare the vaccination timeseries data between countries at once...
""")

# Country wise comparison bar graphs
countries = st.multiselect("Which countries do you like to see?", country_list, ['United States', 'India', 'Brazil'])
date = st.selectbox("Pick a date", options = ['autoplay'] + list(vaccine_df[vaccine_df['country'].isin(countries)]['date'].unique()))

# For a selected date
if date != 'autoplay':
    conditioned_df = vaccine_df[(vaccine_df['country'].isin(countries)) & (vaccine_df['date'] == pd.to_datetime(date))]
    fig = px.bar(conditioned_df, x='country', y=['percentage_vaccinated', 'percentage_active'], barmode='group')
    st.plotly_chart(fig, use_container_width=False)

# For all dates
else:
    conditioned_df = vaccine_df[(vaccine_df['country'].isin(countries))]
    conditioned_df['date'] = pd.to_datetime(conditioned_df['date']).dt.strftime('%Y-%m-%d')
    
    # # Vaccination plot
    # fig1 = px.bar(conditioned_df, x='country', y='percentage_vaccinated', color='country', range_y=[0,100], animation_frame='date', animation_group='country')
    # fig1.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    # fig1.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 4

    # # Count plot
    # fig2 = px.bar(conditioned_df, x='country', y='percentage_active', color='country', range_y=[0,10], animation_frame='date', animation_group='country')
    # fig2.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    # fig2.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 4

    # # Displaying the graph
    # fig1.update_layout(width=800)
    # st.plotly_chart(fig1, use_container_width=False)
    # fig2.update_layout(width=800)
    # st.plotly_chart(fig2, use_container_width=False)

    df_long = pd.wide_to_long(conditioned_df, stubnames='percentage', i=['country','date'],j='param',sep='_', suffix='\w+').reset_index()
    df_long = df_long.sort_values(by='date')
    fig = px.bar(df_long, x='country', y='percentage', animation_frame='date', color='param', barmode='group', range_y=[0,60])
    #fig = px.bar(conditioned_df, x='country', y=['percentage_active', 'percentage_vaccinated'], animation_frame='date', barmode='group')
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 4
    fig.update_layout(width=800)
    st.plotly_chart(fig, use_container_width=False)

st.write("""
#### Take turns to see the vaccination percentage and active case count across countries at different dates
""")
# Getting country and date as input
default = country_list.index('United States')
option = st.selectbox('Pick a country', country_list, index=default)
country_vaccine_df = vaccine_df[(vaccine_df['country'] == option)]
date = st.select_slider("Pick a date", options = country_vaccine_df[country_vaccine_df['active_cases'].notna()]['date'].unique())

# Calculating the percentage of vaccination

vacc_info_df = country_vaccine_df[(country_vaccine_df['date'] == pd.to_datetime(str(date)))]
vacc = vacc_info_df['people_vaccinated'].iloc[0]
per = round(vacc_info_df['percentage_vaccinated'].iloc[0], 2)
count = country_df[(country_df['country'] == option) & (country_df['date'] == pd.to_datetime(str(date)))]['active_cases'].iloc[0]

# Displaying the results
st.write("The total vaccinated people are " + str(vacc) + ", the vaccination percentage as of " + str(date) + " is " + str(per) + "% yet the active cases count is " + str(count))


vaccine_df['date'] = pd.to_datetime(vaccine_df['date']).dt.strftime('%Y-%m-%d')
vaccine_df = vaccine_df[(vaccine_df['country'].isin(countries))]
figcovid = px.scatter(vaccine_df, x="percentage_vaccinated", y="percentage_active", animation_frame="date", 
    animation_group="country", range_x=[0,70], range_y=[0,10], color='country')
st.plotly_chart(figcovid, use_container_width=False)