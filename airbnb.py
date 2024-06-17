import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px




st.set_page_config(page_title='Airbnb Visualization and Price analysis',page_icon=':hotel:',layout='wide',initial_sidebar_state='expanded')
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlS1KlT786bUC9h1YuWPz4F50FGu7mh-y2BQ&s")
st.sidebar.header(":red[Airbnb]")

with st.sidebar:
    selected= option_menu(None,['Home','Overview','Explore'],
                         icons=['house','graph-up-arrow','bar-chart-line','exclamation-circle'],
                         default_index=0,
                         orientation='vertical',
                         styles={'nav-link': {'font-size':'15px','text-align':'centre','margin':'2px',
                                              "--hover-color": "#B73967"},
                                              'icon':{'font-size':'20px'},
                                               "nav-link-selected": {"background-color": "#B73967"}})
    
mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='airbnb')
mycursor=mydb.cursor(buffered=True)
engine=create_engine('mysql+mysqlconnector://root:''@localhost/airbnb')
table='airbnb1'
df=pd.read_sql_table(table,con=engine)

    
if selected=='Home':
    st.sidebar.image('https://media1.tenor.com/m/BAGbC68hRz8AAAAC/airbnb-globe.gif',width=280)
    st.image('https://miro.medium.com/v2/resize:fit:1358/0*ZrQXh9KUtHqsOiAy.gif',width=250)
    st.title(':red[Airbnb Data-visualization and Price analysis]')
    st.markdown('## :red[Domain]: Travel Industry, Property Management and Tourism')
    st.markdown('## :red[Overview]: To analyze Airbnb data using Python,Pandas , perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.')
    st.markdown('#  ')
    st.markdown("#  ")
    col1,col2=st.columns([4,3],gap='medium')
    with col1:
        st.write(' ')
        st.markdown('## :red[This app creates a bridge over user and hotels where they can explore the facilities,locations before planning a trip or plans. Thank you !]')
    with col2:
        st.write(' ')
        st.image("https://media1.tenor.com/m/rsSIoLjds9UAAAAC/airbnb-door.gif",width=400)
elif selected=='Overview':
    tab1,tab2 = st.tabs(['Reports','Management'])
    with tab1:
        st.title(':green[Some interesting reports]')
        col1,col2=st.columns([0.5,0.5],gap='small')
        with col1:
            plot=px.pie(df,values='Number_of_reviews',names='Cancellation_policy',hole=0.4,
            title='Reviews by Cancellation Policy')
            st.plotly_chart(plot,use_container_width=True)
            st.markdown('##  ')
            st.markdown('##  ')
            st.markdown('## :red[Top 10 Host names who has highest cleaning fees and their Country and Amenities]')

            mycursor.execute('Select Host_name, Amenities,Cleaning_fee,Country_code from airbnb.airbnb1 group by Host_name order by Cleaning_fee Desc limit 10 ')
            Table1=mycursor.fetchall()
            data=pd.DataFrame(Table1,columns=['Host_name','Amenities','Cleaning_fee','Country_code'])
            st.write(data)
        with col2:
            Price=df.groupby('Property_type',as_index=False)['Price'].mean()
            plot=px.bar(Price,x='Price',y='Property_type',title='Price distribution by Property',color_discrete_sequence=px.colors.sequential.Agsunset,color='Property_type')
            st.plotly_chart(plot,use_container_width=True)
    with tab2:
        country=st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop=st.sidebar.multiselect('Select a Property type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room_type=st.sidebar.multiselect('Select your Room type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price=st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        query = f'Country in {country} & Room_type in {room_type} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

        filtered_df = df[
                    (df['Country'].isin(country)) &
                    (df['Property_type'].isin(prop)) &
                    (df['Room_type'].isin(room_type)) &
                    (df['Price'] >= price[0]) &
                    (df['Price'] <= price[1])]
        st.write(filtered_df)

        col1,col2=st.columns(2,gap='medium')
        with col1:
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Host_total_listings_count").sort_values(by='Host_total_listings_count',ascending=False)[:10]
           
            table1=pd.DataFrame(df1,columns=['Property_type','Host_total_listings_count'])
            fig=px.bar(table1,title='Top 10 Property types',x='Host_total_listings_count',y='Property_type',
                       orientation='h',color='Property_type',color_continuous_scale=px.colors.sequential.Agsunset)
            
            st.plotly_chart(fig,use_container_width=True)

            df2=df.query(query).groupby(['Host_name']).size().reset_index(name='Host_total_listings_count').sort_values(by='Host_total_listings_count',ascending=False)[:10]
            fig=px.bar(df2,x='Host_total_listings_count',y='Host_name',title='Top 10 Hosts with Highest number of Listings',
                       orientation='h',color='Host_name',color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
        with col2:
            df1=df.query(query).groupby(['Room_type']).size().reset_index(name='Host_total_listings_count')
            fig=px.pie(df1,title='Total Listings in each Room type',names='Room_type',values='Host_total_listings_count',
                       color_discrete_sequence=px.colors.sequential.Rainbow)
            fig.update_traces(textposition='outside',textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)

            df2=df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name':'Total_listing'})
            fig=px.choropleth(df2,title='Total listings in each country',
                              locations='Country',
                              locationmode='country names',
                              color='Total_listing',
                              color_continuous_scale=px.colors.sequential.Plasma)
            st.plotly_chart(fig,use_container_width=True)

if selected=='Explore':
    st.markdown('## red[Explore more about Airbnb]')

    country=st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop=st.sidebar.multiselect('Select a Property type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room_type=st.sidebar.multiselect('Select your Room type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price=st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

    query=f'Country in {country} & Property_type in {prop} & Room_type in {room_type} & Price>={price[0]} & Price<={price[1]}'

    st.markdown('## :green[Price analysis]')

    col1,col2=st.columns(2,gap='medium')

    with col1:
        df1=df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        plot=px.bar(df1,x='Room_type',
                    y='Price',
                    color='Price',
                    title='Avg Price in each room type')
        st.plotly_chart(plot,use_container_width=True)

        st.markdown('## :red[Avilability analysis]')

        plot=px.box(df.query(query),
                    x='Room_type',
                    y='Availability_365',
                    color='Room_type',
                    title='Availability by room type')
        st.plotly_chart(plot,use_container_width=True)
    with col2:
        df1=df.query(query).groupby('Country',as_index=False)['Price'].mean()
        plot=px.scatter_geo(df1,
                            locations='Country',
                            color='Price',
                            hover_data=['Price'],
                            locationmode='country names',
                            size='Price',
                            title='Avg Price in each country',
                            color_continuous_scale='agsunset'
                            )
        st.plotly_chart(plot,use_container_width=True)

        st.markdown('# ')
        st.markdown('# ')

        df2=df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        df2.Availability_365= df2.Availability_365.astype(int)
        plot=px.scatter_geo(df2,
                            locations='Country',
                            color= 'Availability_365', 
                            hover_data=['Availability_365'],
                            locationmode='country names',
                            size='Availability_365',
                            title= 'Avg Availability in each Country',
                            color_continuous_scale='agsunset'
                            )   
        st.plotly_chart(plot,use_container_width=True)

    

       

    

        






       
          
           
        

