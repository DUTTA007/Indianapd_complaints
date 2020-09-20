import streamlit as st
import numpy as np 
import pandas as pd 
import plotly.express as px

st.markdown("""
<style>
body {
    background-color: #cce6ff;
}
</style>
    """, unsafe_allow_html=True)


# Path to dataset
path = 'Indianapolis_PD_clean.csv'

# Loading in and cleaning the data
@st.cache
def load_data():
    df = pd.read_csv(path, index_col=0)
    # print(df.head(2))
    return df

# Run our function and save the cleaned df to 'df_nyc'
df_force = load_data()

st.sidebar.title('Welcome to ___ !')
st.sidebar.write('Take a look at the number of "Use of Force" events by PD and District.')
st.sidebar.markdown('-------')
st.sidebar.write('Year(s)')

min_year = int(df_force['year_received'].min())
max_year = int(df_force['year_received'].max())

year_filter_min, year_filter_max = st.sidebar.slider('(Select a range or single year)', min_year, max_year, [max_year-1, max_year])

df_exp = df_force[(df_force['year_received'] <= year_filter_max) & (df_force['year_received'] >= year_filter_min)]
df_exp = df_exp.groupby(['district','subjectRace','subjectSex']).size().rename('cases').reset_index()

df_mos = df_force[(df_force['year_received'] <= year_filter_max) & (df_force['year_received'] >= year_filter_min)]
df_mos = df_mos.groupby(['district','officerRace','officerSex']).size().rename('cases').reset_index()

st.sidebar.markdown('-------')
st.sidebar.write('Select a District')

# Creating the selectbox and giving the dropdown options to choose from
district_most_to_least = df_exp.groupby(['district']).sum().sort_values(by='cases', ascending=False).index
selected_district = st.sidebar.selectbox('(Sorted from most to least cases)', district_most_to_least)

df_tot = df_exp[df_exp['district']==selected_district]


# f'''
# # NYPD #
# # :oncoming_police_car: Disctrict {selected_disctrict} :oncoming_police_car: 
# ## Total Excessive Force Reports: **{df_tot['cases'].sum()}**
# '''

st.sidebar.markdown('-------')
st.sidebar.write('Would you like to group the cases by the race of the Subjects or Officers?')
side = st.sidebar.selectbox("", ('Subjects', 'Officers'))
st.sidebar.markdown('-------')
st.sidebar.write('Would you like to see a breakdown of the cases by gender?')
option = st.sidebar.selectbox("", ('No', 'Yes'))
st.sidebar.markdown('-------')

if option == 'No':

    if side == 'Subjects':
    
        df_complainant = df_exp[df_exp['district']==selected_district].groupby(['subjectRace']).sum().reset_index().sort_values(by='cases', ascending=False)
        df_complainant['Percentage'] = df_complainant['cases']/(df_complainant['cases'].sum())*100

        fig = px.bar(df_complainant, y ='subjectRace', x='Percentage', orientation='h', text='cases', width=800, height=600)

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Subject Ethnicity",
            xaxis_title="Percentage of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), 
        )

        fig.update_traces(marker_color='white')
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)

    if side == 'Officers':

        df_officers = df_mos[df_mos['district']==selected_district].groupby(['officerRace']).sum().reset_index().sort_values(by='cases', ascending=False)
        df_officers['Percentage'] = df_officers['cases']/(df_officers['cases'].sum())*100

        fig = px.bar(df_officers, y ='officerRace', x='Percentage', orientation='h', text='cases', width=800, height=600)

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Officer Ethnicity",
            xaxis_title="Percentage of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), 
        )

        fig.update_traces(marker_color='white')
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)


if option == 'Yes':

    if side == 'Subjects':

        df_complainant = df_exp[df_exp['district']==selected_district].groupby(['subjectRace','subjectSex']).sum()
        df_complainant['Percentage'] = df_complainant.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_complainant = df_complainant.reset_index().sort_values(by='cases', ascending=False)

        fig = px.bar(df_complainant, x="cases", y="subjectRace",
                    color='subjectSex', orientation='h', text='subjectSex', 
                    hover_data=["subjectSex", "Percentage"])

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Cases by subject ethnicity",
            xaxis_title="Number of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), showlegend=False
        )

        fig.update_traces(textfont_size=12)
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)    

    if side == 'Officers':

        df_officers = df_mos[df_mos['district']==selected_district].groupby(['officerRace','officerSex']).sum()
        df_officers['Percentage'] = df_officers.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
        df_officers = df_officers.reset_index().sort_values(by='cases', ascending=False)

        fig = px.bar(df_officers, x="cases", y="officerRace",
                    color='officerSex', orientation='h', text='officerSex', 
                    hover_data=["officerSex", "Percentage"])

        fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
            title="Officer Ethnicity",
            xaxis_title="Number of Cases",
            yaxis_title="",
            font=dict(family="Arial Black",
                size=18,
                color="white"
            ), showlegend=False
        )

        fig.update_traces(textfont_size=12)
        fig.update_xaxes(showgrid=True, zeroline=False, gridcolor='white')
        fig.update_yaxes(showgrid=False, zeroline=False, ticklen=10, ticks="outside", tickcolor='rgba(0,0,0,0)')

        st.plotly_chart(fig)


# if st.sidebar.checkbox(f'Precinct {selected_precinct} Case Details'):

#     st.markdown('-------')
#     st.title(f'Precinct {selected_precinct} Cases')

#     st.dataframe(df_force[df_force['precinct'] == selected_precinct])
