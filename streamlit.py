# Required libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

############################ COVID DATA ############################

# Introduction
st.write(""" 
# Interactive Data Science
### By Annie Johnson and Sundar Anand
### Interesting trends when pandemic happened""")

# Reading the file
country_df = pd.read_csv("vaccination dataset/country.csv")
country_df['date'] = pd.to_datetime(country_df['date'], format='%d/%m/%y').dt.date

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

# For all dates
else:

    # Getting only the countries and sorting it by time and country
    conditioned_df = vaccine_df[(vaccine_df['country'].isin(countries))]
    conditioned_df['date'] = pd.to_datetime(conditioned_df['date'])
    conditioned_df = conditioned_df.sort_values(by=['date'])
    conditioned_df['date'] = conditioned_df['date'].dt.strftime('%Y-%m-%d')
    conditioned_df = conditioned_df.sort_values(by=['percentage_vaccinated', 'date', 'country'])

    # Plotting the graph and animating it
    fig = px.bar(conditioned_df, x='country', y=['percentage_active', 'percentage_vaccinated'], animation_frame='date', barmode='group')

    # Increasing the animation speed
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 10
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 4

# Displaying the graph
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

# Vaccination vs Active rate graph for multiple countries
countries = st.multiselect("Which countries do you like to see?", country_list, ['United States', 'India', 'Brazil', 'Germany', 'United Kingdom', 'Russia', 'France', 'Malaysia', 'Japan'])
vaccine_df['date'] = pd.to_datetime(vaccine_df['date']).dt.strftime('%Y-%m-%d')
vaccine_df = vaccine_df[(vaccine_df['country'].isin(countries))]

# Plotting the graph
figcovid = px.scatter(vaccine_df, x="percentage_vaccinated", y="percentage_active", animation_frame="date", 
    animation_group="country", range_x=[-5,max(vaccine_df['percentage_vaccinated'])], range_y=[-1,max(vaccine_df['percentage_active'])], color='country', size='population')

# Increasing the animation speed
figcovid.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 30
figcovid.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 15

# Displaying the graph
figcovid.update_layout(width=800)
st.plotly_chart(figcovid, use_container_width=False)

############################ STOCK DATA ############################

# Reading the global file
global_df = pd.read_csv("vaccination dataset/global.csv")
global_df = global_df[global_df['moderna_stock'].notna()]

# Generating stock graphs for different companies against active cases and vaccination rate
company_list = ['fb_stock', 'zoom_stock', 'ubereats_stock', 'moderna_stock']
graph_list = ['active_cases', 'people_vaccinated']
covid_rate_stocks_list = []

# For each country
for i in company_list:

    # For each metric
    for j in graph_list:

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add traces
        fig.add_trace(
            go.Scatter(x=global_df['date'], y=global_df[j], name=j),
            secondary_y=False,
        )

        fig.add_trace(
            go.Scatter(x=global_df['date'], y=global_df[i], name=i),
            secondary_y=True,
        )

        # Set x-axis title
        fig.update_xaxes(title_text="Date", showgrid=False)

        # Set y-axes titles
        fig.update_yaxes(title_text=j, secondary_y=False, showgrid=False)
        fig.update_yaxes(title_text=i, secondary_y=True, showgrid=False)

        # Storing the graph
        covid_rate_stocks_list.append(fig)


# Counter to keep track of the plots
counter = 0

st.write("""
#### Sad times. But how the big companies delt with this? Was there any segment that got beaten up or flourished in this pandemic?
#### Let's consider each compnay from each sector and see how they have done
""")

# Plotting social media stocks
st.write ("""
#### 1. Social Media
##### Ofcourse the choice of company will be Facebook which owns Facebook, WhatsApp and Instagram.
##### Let's see their stock value over this period of time along with COVID count across the globe.
""")

# Plotting the first graph
st.write(covid_rate_stocks_list[counter])

st.write ("""
##### We can see that the Facebook stocks increased the COVID count which kind of explains that once lockdowns 
##### have been announced people started to stay in side their house and hence social media became their only entertainment.

##### Let's look at their stock price against the vaccination count.
""")

# Plotting the second graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
###### Vaccination didn't really affect FB's stock by a lot which shows that the FB shares were highly influenced by the lockdown
###### and not exactly but the COVID count.

#### 2. Video Communication
##### Video Communication have become one of the inevitable parts of our life in today's normal.
##### Right from education to team meets and even family or friends get together was hosted on video communication platforms.

##### In recent days, even though Apple and Google have up their game in this domain, it has always been ZOOM that dominated it
##### Let's see how Zoom's stocks flew in the last couple of years.
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
##### It is evident enough to show that Zoom has been through a drastic financial growth during this period of uncertainty.

##### Let's look at their stock price against the vaccination count.
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
###### Vaccination didn't really become a factor in Zoom's stocks.
###### Zoom just enabled people to meet irrespective of the physical meeting guidlines mandated.

#### 3. Online Food Ordering
##### Once lockdown was established, going out for daily routines like grocery shopping, restaurents and vacation became tedious.
##### Many companies emerged in this period to address this issue. But one company that has always had an solution was UberEATS.

##### UberEats focuses on online food ordering and delivery as its primary goal.
##### Let's see COVID did to UberEats's stocks.
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
##### As mentioned earlier, the COVID just increased the demand for the service that UberEATS was already providing with high robustness.
##### It was kind of obvious to predict that the UberEATs stocks will increase along with the COVID rate and lockdowns.

##### Did vaccination rate make any imapct?
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
###### Seems like the vaccination rate didn't really domainate any field. But we are not done with the analysis yet...

#### 4. Medical department
##### Several medical companies across the globe made generating COVID vaccine as their primary goal in 2020.
##### Many companies succeed it but one company that was fast enough to push their success to a production level was Moderna.

##### Many people in today's work have taken/taking Moderna vaccines to protect themselves from the deadly virus.
##### Did the raise in COVID numbers make any impact to their stocks as well?
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
##### That's a YES!! The raise in COVID numbers also trigger the Moderna stocks.
##### We can see that the Moderna stock value increased along with the COVID active cases number expressing 
##### that people started to believe that Moderna will be their saviour in this battle.

##### But why is there a sudden spike at the end? Was it because the vaccination got released?
""")

# Plotting the third graph
counter = counter + 1
st.write(covid_rate_stocks_list[counter])

st.write ("""
###### That's a bingo!! We can see that the successful vaccination production by Moderna has made their Stocks hit their peak value in the last two years.
""")

st.write ("""
###### These are the four domains that we wanted to present in this article to understand how each department changed their game to make use of this pandemic period.
""")

st.write (""" 
#### Here is the final graph will all the stock values of the companies we saw together 
""")

# Meting the dataframe to get all the values
df_stock = global_df.melt(id_vars='date', value_vars=company_list)

# For active cases and vaccination count
for i in graph_list:

    # Plot for covid rate
    fig1 = px.line(global_df, x='date', y=i, color='param' + str(graph_list.index(i) + 1))

    # Plot for stock values
    fig2 = px.line(df_stock, x='date', y='value', color='variable')
    fig2.update_traces(yaxis="y2")

    # Making Subplots
    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    # Naming the axes
    subfig.add_traces(fig1.data + fig2.data)
    subfig.layout.xaxis.title="Date"
    subfig.layout.xaxis.showgrid = False
    subfig.layout.yaxis.title="COVID Rate"
    subfig.layout.yaxis.showgrid = False
    subfig.layout.yaxis2.title="Stock value"
    subfig.layout.yaxis2.showgrid = False
    
    # Recoloring
    subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    # Displaying the chart
    st.write(subfig)

st.write("""
### Some questions that we can answer from this analysis are...
""")


# Getting the bubble comparison for percentage_active

# Removing the outliers
country_df = country_df[(country_df['percentage_active'] >= 0) & (country_df['percentage_active'] < 70) & (country_df['percentage_vaccinated'] >= 0) & (country_df['percentage_vaccinated'] < 75)]

st.write("""
####1. Let's see which countries did the best and worst in controlling the pandemic
""")
# Grouping by country to get percentage active min and max
df = country_df.groupby('country').agg({'percentage_active':'max'})[['percentage_active']].reset_index()
df.columns = ['country', 'active_max']

# Plotting the top 10 countries with max and min
# Max
st.write("""
##### Lets look at top 10 countries that haven't done good
""")
max_df = df.sort_values(by='active_max', ascending=False).head(10)
fig = px.scatter(max_df, x="country", y="active_max", size="active_max")
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.write(fig)

# Min
st.write("""
##### Lets look at top 10 countries that have done good
""")
min_df = df.sort_values(by='active_max').head(10)
fig = px.scatter(min_df, x="country", y="active_max", size="active_max")
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.write(fig)

# Getting the bubble comparison for percentage_vaccinated
st.write("""
####2. Let's see which countries did the best and worst in getting vaccinated
""")
# Grouping by country to get percentage vaccinated min and max
df = country_df.groupby('country').agg({'percentage_vaccinated':'max'})[['percentage_vaccinated']].reset_index()
df.columns = ['country', 'vacc_max']

# Plotting the top 10 countries with max and min
# Max
st.write("""
##### Lets look at top 10 countries that haven't done good
""")
max_df = df.sort_values(by='vacc_max').head(10)
fig = px.scatter(max_df, x="country", y="vacc_max", size="vacc_max")
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.write(fig)

# Min
st.write("""
##### Lets look at top 10 countries that have done good
""")
min_df = df.sort_values(by='vacc_max', ascending=False).head(10)
fig = px.scatter(min_df, x="country", y="vacc_max", size="vacc_max")
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.write(fig)