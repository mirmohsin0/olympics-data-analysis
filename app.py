import streamlit as st
import pandas as pd 
import preprocessor, helper
import plotly.express as px
from matplotlib import pyplot as plt 
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv("athlete_events.csv")
region = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region)

st.sidebar.image("OlympicsLogo.jpg")

st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis', )

)


if user_menu == 'Medal Tally':
    st.sidebar.header('Medal Tally')

    years, country = helper.country_year_list(df)

    # display using dropdown
    selected_year = st.sidebar.selectbox('Select Year',years)
    selected_country = st.sidebar.selectbox('Select Country',country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title("Overall Tally")
    if selected_year != 'overall' and selected_country == 'overall':
        st.title(selected_country + ' overall performance')  
    if selected_year == 'overall' and selected_country != 'overall':
        st.title("Year Tally in "+ str(selected_year))
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " performamce in " + str(selected_year) + ' Olympics')     

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0] 
    sports = df['Sport'].unique().shape[0] 
    events = df['Event'].unique().shape[0] 
    athletes = df['Name'].unique().shape[0] 
    nations = df['region'].unique().shape[0] 

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)    

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)   

    # Region
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    # Events
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x ='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    # Athletes
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x ='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)   


    # Events Over time 
    st.title("NO of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', 
    aggfunc='count').fillna(0).astype(int), annot=True)
    st.pyplot(fig)

    # Most Decorated Players in every sport
    st.title("Most Successful Athletes")
    
    #Options
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    selected_sport = st.selectbox("Select a Sport", sport_list)

    x = helper.most_successful(df, selected_sport)
    st.table(x)


# Country wise
if user_menu == 'Country-wise Analysis':

    st.sidebar.title("Country-wise Analysis")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    
    # coutry-wise heatmap
    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    # most successful athlete countrywise
    st.title('Top 10 Athletes of ' + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)

# Athlete-wise Analysis
if user_menu == 'Athlete-wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False )
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)   


    # Age Distribution in famous sports
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming',
    'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
    'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving',
    'Canoeing' , 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 
    'Table Tennis', 'Baseball', 'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
    'Triathion', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()

        if not ages.empty:
            x.append(ages)
            name.append(sport)


    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports")
    st.plotly_chart(fig) 

    # Analysis on the basis of height, weight  and sex
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'overall')

    st.title("Height vs Weight")

    selected_sport = st.selectbox("Select a Sport", sport_list)

    temp_df = helper.weightHeight(df, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df)
    st.pyplot(fig)
    
    # men vs women 
    st.title("Men vs Women Participation over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)