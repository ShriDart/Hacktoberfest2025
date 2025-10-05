import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('startup_clean.csv')

# Clean and process columns
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['month'] = df['date'].dt.month
df['invested_year'] = df['date'].dt.year
df['amount'] = df['amount'].fillna(0)

st.set_page_config(layout='wide', page_title='Startup Analysis')

# ---------------- INVESTOR DETAILS FUNCTION ----------------
def load_investor_details(investor):
    st.title(investor)

    inv_df = df[df['investors'].str.contains(investor, na=False)]

    # Last 5 investments
    last_5df = inv_df.sort_values('date', ascending=False)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']
    ].head(5)
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)

    # Biggest investments
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investments')
        big_invest = inv_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(5)
        fig, ax = plt.subplots()
        ax.bar(big_invest.index, big_invest.values)
        ax.set_ylabel('Total Amount (Cr)')
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors Invested In')
        sector = inv_df.groupby('vertical')['amount'].sum()
        if not sector.empty:
            fig1, ax1 = plt.subplots()
            ax1.pie(sector, labels=sector.index, autopct='%1.1f%%')
            st.pyplot(fig1)

    st.markdown('---')

    # Stages and Cities
    col3, col4 = st.columns(2)
    with col3:
        st.subheader('Stages Invested In')
        stage = inv_df.groupby('round')['amount'].sum()
        if not stage.empty:
            fig2, ax2 = plt.subplots()
            ax2.pie(stage, labels=stage.index, autopct='%1.1f%%')
            st.pyplot(fig2)

    with col4:
        st.subheader('Cities Invested In')
        city = inv_df.groupby('city')['amount'].sum()
        if not city.empty:
            fig3, ax3 = plt.subplots()
            ax3.pie(city, labels=city.index, autopct='%1.1f%%')
            st.pyplot(fig3)

    # Yearly trend
    st.subheader('Yearly Investment Trend')
    year_invest = inv_df.groupby('invested_year')['amount'].sum()
    if not year_invest.empty:
        fig4, ax4 = plt.subplots()
        ax4.plot(year_invest.index, year_invest.values, marker='o')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Investment Amount (Cr)')
        st.pyplot(fig4)


# ---------------- OVERALL ANALYSIS FUNCTION ----------------
def overall_analysis():
    st.title('Overall Startup Funding Analysis')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total Investment', f"{total} Cr")

    with col2:
        max_invest = round(df.groupby('startup')['amount'].max().max())
        st.metric('Maximum Single Investment', f"{max_invest} Cr")

    with col3:
        avg = round(df.groupby('startup')['amount'].sum().mean())
        st.metric('Average Funding per Startup', f"{avg} Cr")

    with col4:
        t_startup = df['startup'].nunique()
        st.metric('Total Startups Funded', str(t_startup))

    # Month-over-Month Trend
    st.header('Month-over-Month Investment Trend')
    select_op = st.selectbox('Select Type', ['Total Investment', 'Number of Investments'])

    if select_op == 'Total Investment':
        temp_df = df.groupby(['invested_year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['invested_year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['invested_year'].astype(str)
    fig1, ax1 = plt.subplots()
    ax1.plot(temp_df['x_axis'].values, temp_df['amount'].values, marker='o')
    plt.xticks(rotation=90)
    st.pyplot(fig1)

    # Sector Analysis
    st.header('Sector Analysis')
    col5, col6 = st.columns(2)
    with col5:
        st.subheader('Top 10 Sectors by Total Funding')
        sect_df = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig2, ax2 = plt.subplots()
        ax2.pie(sect_df, labels=sect_df.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    with col6:
        st.subheader('Top 10 Sectors by Number of Fundings')
        sect_df = df.groupby('vertical')['amount'].count().sort_values(ascending=False).head(10)
        fig3, ax3 = plt.subplots()
        ax3.pie(sect_df, labels=sect_df.index, autopct='%1.1f%%')
        st.pyplot(fig3)


# ---------------- SIDEBAR SETUP ----------------
st.sidebar.title('Startup Analysis Dashboard')
option = st.sidebar.selectbox('Select Option', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    overall_analysis()
elif option == 'Startup':
    st.title('Startup Analysis (Coming Soon)')
else:
    all_investors = sorted(set(sum((i.split(',') for i in df['investors'].dropna()), [])))
    invest = st.sidebar.selectbox('Select Investor', all_investors)
    btn2 = st.sidebar.button('Show Investor Details')
    if btn2:
        load_investor_details(invest)
