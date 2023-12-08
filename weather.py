# 실행하는법,, streamlit run weather.py

import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title='20224조은경',
    page_icon='✨'
)

st.title('날씨 데이터 시각화⛅')
st.markdown('**대구강동고 소인수 20224 조은경**')

api_key = "8c8dac1c764bc38338e66379dfb82ae8"

# 사이트 내의 어느 도시든 가능!^^
st.markdown("""---""")
city = st.text_input('도시명을 입력하세요', 'Daegu')
st.markdown('*⚠️  OpenWeather에 없는 도시일 경우 그래프가 나타나지 않을 수도 있습니다*')
st.markdown("""---""")

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"

response = requests.get(url)
data = response.json()

df = pd.DataFrame({
    'Date': [entry['dt_txt'] for entry in data['list']],
    'Temperature (Celsius)': [entry['main']['temp'] - 273.15 for entry in data['list']],
})

tab1, tab2 = st.tabs(["선 그래프", "막대 그래프"])

with tab1:
    st.line_chart(df.set_index('Date'))

with tab2:
    st.bar_chart(df.set_index('Date'))
