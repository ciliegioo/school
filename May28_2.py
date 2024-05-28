import streamlit as st
import os
import numpy as np
import collections
import math

# @@@@@@@@@
# One Time Pad 암호화 함수
# @@@@@@@@@


def one_time_pad_encrypt(message, key):
    return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key))


# @@@@@@@@@
# 엔트로피 계산 함수
# @@@@@@@@@
def calculate_entropy(text):
    # 각 문자의 빈도 계산
    frequency = collections.Counter(text)
    text_length = len(text)
    probabilities = [count/text_length for count in frequency.values()]

    # 엔트로피 계산
    entropy = -sum(p * math.log2(p) for p in probabilities)
    return entropy


# @@@@@@@@@
# 문자의 확률 분포 계산 함수
# @@@@@@@@@
def calculate_distribution(text):
    # 각 문자의 빈도 계산
    frequency = collections.Counter(text)
    text_length = len(text)

    # 각 문자의 확률 계산
    distribution = {char: count/text_length for char,
                    count in frequency.items()}
    return distribution

# @@@@@@@@@
# 몬테카를로 시뮬레이션 함수
# @@@@@@@@@


def simulate_one_time_pad(message_length, num_simulations):
    distributions = []
    for _ in range(num_simulations):
        message = os.urandom(message_length)
        key = os.urandom(message_length)
        message = ''.join(chr(b % 128) for b in message)
        key = ''.join(chr(b % 128) for b in key)
        ciphertext = one_time_pad_encrypt(message, key)
        distribution = calculate_distribution(ciphertext)
        distributions.append(distribution)
    return distributions


# @@@@@@@@@
# 페이지 세팅
# @@@@@@@@@
st.set_page_config(
    page_title='Entropy Simulation',
    page_icon='✨'
)

menu = st.sidebar.selectbox(
    'MENU', ['Introduction', 'Graph'])

if menu == 'Introduction':
    st.header('Introduction')
    tab1, tab2, tab3, tab4 = st.tabs(
        ['암호화 알고리즘', '원타임패드 알고리즘', '엔트로피와 암호화', '몬테카를로 시뮬레이션'])
    with tab1:
        st.header('암호화 알고리즘')
        st.write('데이터의 무결성 및 기밀성을 확보하기위해 정보를 쉽게 해독할 수 없도록 암호화하는 알고리즘')
        st.write("")
        img = Image.open('image2.png')
        st.image(img)
	    st.write("")
        st.write("**대칭키 암호화(암호화 알고리즘의 종류) :**")
        st.write("평문을 특정 대칭키로 암호화하고, 결과로 나온 암호문도 대칭키로 복호화할 수 있는 방식")
        st.write("")

        st.text("*평문 : 해독 가능한 형태의 메세지 (암호화 전)")
        st.text("*암호문 : 해독 불가능한 형태의 메세지")
        st.text("*암호화 : '평문 → 암호문' 변환  *복호화 : '암호문 → 평문' 변환")

    with tab2:
        st.header('원타임패드 알고리즘')
        st.write("평문과 같은 길이의 무작위 배열 문자열(패드)를 만들어서 평문에 더하는 방식 (대칭키 암호화)")
        st.markdown(
            "송신자가 평문과 패드를 XOR 연산하여 메세지 전송 → 수신자가 받은 메세지와 패드를 XOR 연산하여 평문 얻음 (XOR 연산의 'A XOR B = C → A XOR C = B, B XOR C = A' 특성 이용)")
        st.write("")

        st.text("*XOR 연산 (= 배타적 논리합)")
        st.text("주어진 두개의 명제 가운데 하나만 참일 경우를 판단하는 논리 연산")
        st.text("입력값이 서로 다르면 '1'출력, 같으면 '0'출력")

    with tab3:
        st.header("엔트로피와 암호화")
        st.write("엔트로피 : 확률분포의 무작위성을 측정하는 척도")
        st.write("엔트로피↑ → 확률분포 균일 & 불확실성↑")
        st.write("완벽하게 균일한 분포를 가진 8비트 데이터의 엔트로피는 8")

    with tab4:
        st.header("몬테카를로 시뮬레이션")
        st.write("무작위 추출된 난수를 이용하여 함수의 값을 계산하는 통계학 방법")
        st.write("예측에 불확실성 또는 무작위성을 포함할 수 있음")
        st.write("인공지능, 핵 및 입자물리학, 임상시험, 컴퓨터 시뮬레이터 등에서 이용")


else:
    st.title("원타임패드의 엔트로피")
    st.write("몬테카를로 시뮬레이션을 이용한 엔트로피의 시각화")

    message_length = st.slider("문자 길이", min_value=10, max_value=100, value=50)
    num_simulations = st.slider(
        "시뮬레이션 횟수", min_value=10, max_value=1000, value=50)

    # 몬테카를로 시뮬레이션 실행
    distributions = simulate_one_time_pad(message_length, num_simulations)

    # 평균 분포 계산
    average_distribution = {}
    unique_characters = set.union(*[set(distribution.keys())
                                  for distribution in distributions])
    for char in unique_characters:
        average_distribution[char] = 0
    for distribution in distributions:
        for char, value in distribution.items():
            average_distribution[char] += value
    for char in average_distribution:
        average_distribution[char] /= num_simulations

    # 분포 시각화
    characters = list(average_distribution.keys())
    probabilities = list(average_distribution.values())
    st.bar_chart(data=probabilities)

    st.subheader(":gray[설명]", divider='gray')
    st.write("X축 : 문자의 개수 ")
    st.write("Y축 :  암호화된 암호문에서 각 문자의 확률 밀도 ('암호화된' 암호문에서 각 문자가 나타날 확률)")
    st.write("그래프는 모든 시뮬레이션에 대한 문자의 평균 분포를 나타냄")
    st.write("")
    st.write("Q. 왜 x축 값이 127개일까?")
    st.text("아스키(컴퓨터의 문자 인코딩)는 총 128개")
    st.text("그중 0(널 문자)를 제외하면 사용가능한 문자의 개수는 127개")
    st.write("")

    st.write("Key Point")
    st.text("문자의 길이가 길 수록, 시뮬레이션 횟수가 많을 수록, 확률 분포가 균일하다!")
