import streamlit as st
import pandas as pd
import datetime
import json
import requests


# App description
st.markdown('''
# Global Holidays App

- Source Code: https://github.com/steven-ngo/Stock-Price-App
- Language: `Python`
- Libraries: `streamlit` `pandas`
''')
st.write('---')





# Retrieving countries code
retrieveCountries = requests.get('https://date.nager.at/api/v3/AvailableCountries')

countries = json.loads(retrieveCountries.content)

countriesDict = {}

for country in countries:
    countriesDict[country['name']] = country['countryCode']


# Select country and year
countryOption = st.selectbox('Choose a Country:', countriesDict, index=104)

todayYear = datetime.datetime.now().year

year = st.slider('Select Year:', 2000, todayYear+50, datetime.datetime.now().year)


# Retrieving holidays
retrieveHolidays = requests.get('https://date.nager.at/api/v3/publicholidays/' + str(year) +'/'+ countriesDict[countryOption])
holidays = json.loads(retrieveHolidays.content)

# format the holidays data
holidaysList= []

for holiday in holidays:
    del holiday['fixed']
    del holiday['launchYear']

    holiday ['states/provinces'] = holiday.pop('counties')
    holiday['national'] = holiday.pop('global')

    holidaysList.append(holiday)

holidasTable = pd.DataFrame(holidaysList)

st.write(holidasTable)
