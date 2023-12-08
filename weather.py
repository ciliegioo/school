# 실행하는법,, streamlit run weather.py

import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title='20224조은경',
    page_icon='✨'
)

st.title('날씨 데이터 시각화')

api_key = "8c8dac1c764bc38338e66379dfb82ae8"

# 사이트 내의 어느 도시든 가능!^^
city = st.text_input('Enter City', 'Daegu')

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

response = requests.get(url)
data = response.json()

df = pd.DataFrame({
    'Date': [entry['dt_txt'] for entry in data['list']],
    'Temperature (Celsius)': [entry['main']['temp'] - 273.15 for entry in data['list']],
})

visualization_option = st.radio('Select Visualization Option', [
                                'Line Chart', 'Bar Chart'])

if visualization_option == 'Line Chart':
    st.line_chart(df.set_index('Date'))
else:
    st.bar_chart(df.set_index('Date'))

st.text('대구강동고 소인수 20224 조은경')
