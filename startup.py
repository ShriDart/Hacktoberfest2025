import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('startup_clean.csv')


df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['invested_year'] = df['date'].dt.year

st.set_page_config(layout='wide',page_title='startup analysis')
def load_investor_details(investor):
    st.title(investor)



    #load last 5 investments of invesotr
    last_5df = df[df['investors'].str.contains(investor)][['date','startup','vertical','city','round','amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)

    #biggest investment of investor
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('biggest investment')

        big_invest = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        fig, ax = plt.subplots()
        ax.bar(big_invest.index,big_invest.values)
        st.pyplot(fig)



    with col2:

        sector = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(sector,labels=sector.index,autopct='%1.1f%%')
        st.pyplot(fig1)


    st.write('-------------------------------------------------------------------------------------------------------------')
    col3,col4 = st.columns(2)

    with col3:

        stage = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('stages invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(stage, labels=stage.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    with col4:
        city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('invested in citys')
        fig3, ax3 = plt.subplots()
        ax3.pie(city, labels=city.index, autopct='%1.1f%%')
        st.pyplot(fig3)




    year_invest = df[df['investors'].str.contains(investor)].groupby('invested_year')['amount'].sum()
    st.subheader('invested in citys')
    fig4, ax4 = plt.subplots()
    ax4.plot(year_invest.index,year_invest.values)
    st.pyplot(fig4)



def overall_analysis():
    st.title('genreal analysis')

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        #total amount invested
        total = round(df['amount'].sum())
        st.metric('total' ,str(total) + ' CR')
    with col2:
        #max amount investe

        max = round(df.groupby('startup')['amount'].max().sort_values(ascending=False)).head(1).values[0]
        st.metric('maximum', str(max) + ' CR')

    with col3:
        # avg ticket size

        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('average funding', str(avg) + ' CR')

    with col4:
        t_startup = df['startup'].nunique()
        st.metric('Total Startup Funded', str(t_startup) + ' CR')


    st.header('MOM startup')

    select_op = st.selectbox('select type', ['Total','count'])

    if select_op == 'Total':

        temp_df = df.groupby(['invested_year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['invested_year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['invested_year'].astype('str')
    fig1, ax1 = plt.subplots()
    ax1.plot(temp_df['x_axis'].values, temp_df['amount'].values)
    st.pyplot(fig1)

    st.header('Sector Analysis')
    col5,col6 = st.columns(2)


    with col5:
        st.subheader('Total secotors funded')
        sect_df = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig2, ax2 = plt.subplots()
        ax2.pie(sect_df, labels=sect_df.index, autopct='%1.1f%%')
        st.pyplot(fig2)
    with col6:
        st.subheader('No of sectors')
        sect_df = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
        fig3, ax3 = plt.subplots()
        ax3.pie(sect_df, labels=sect_df.index, autopct='%1.1f%%')
        st.pyplot(fig3)




st.sidebar.title('Startup Analysis')
option = st.sidebar.selectbox('select option',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    overall_analysis()
elif option =='Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup',sorted(list(df['startup'].unique())))
    btn1 = st.sidebar.button('Startup Analysis')
else:
    invest = st.sidebar.selectbox('Select Startup',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Investors Analysis')
    if btn2:
        load_investor_details(invest)
