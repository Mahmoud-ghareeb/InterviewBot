import streamlit as st
from streamlit_custom_chat import ChatContainer
from streamlit_custom_input import ChatInput
from key_generator.key_generator import generate
from helper_functions import set_bg_hack, set_page_container_style, refresh
import numpy as np
import pandas as pd
from openai import OpenAI
import yaml
import json
import os
from dotenv import load_dotenv


config = yaml.load(open('./configs/config.star.yaml', 'r'),
                   Loader=yaml.FullLoader)

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=API_KEY
)

df = pd.read_csv('./data/star_questions.csv')


def get_evaluation(content: str) -> dict:
    """
    Evaluate if the provided answer follows the STAR methodology

    :param content: {'question': the question, 'answer': the answer}
    :return: {"eval": your detailed evaluation of the answer}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
              "content": config['prompts']['evaluation_prompt']},
            {"role": "user", "content": content}
        ]
    )

    return json.loads(response.choices[0].message.content)


def get_random_question():
    """
    get a random question from the csv file

    :return: question 
    """
    random_question_idx = np.random.randint(0, 60)
    data = df.iloc[random_question_idx]

    return data['Question']


st.set_page_config(layout="wide")

set_bg_hack("assets/images/pastel3.jpg")

set_page_container_style()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# after getting response from bot, add it to session and refresh


def messageFromChatBot(message):
    key = generate()
    st.session_state.messages.append(
        {"role": "assistant", "content": message, "key": "assistant-"+key.get_key()})
    refresh('assistant')

# st.sidebar.header("header")
# st.sidebar.subheader(‘1.please chose which app you want to operate’)


new_question = get_random_question()

# if there are no messages in the session add this one
if len(st.session_state.messages) == 0:
    st.session_state.messages.append(
        {"role": "assistant", "content": config['openning_message'], "key": 0})
    st.session_state.messages.append(
        {"role": "assistant", "content": new_question, "key": 1})

col1, col2 = st.columns([2, 13])

with col1:
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")
    # button to redirect to quiz page (currently does nothing)
    st.button("Take a Quiz", use_container_width=True)

with col2:
    # component that displays the messages
    ChatContainer(messages=st.session_state.messages, key="chatcontainer")

    # if st.button(label="assistant", key="assistant"):
    #     key = generate()
    #     st.session_state.messages.append({"role": "assistant", "content": "whatever","key":"assistant-"+key.get_key()})
    #     refresh('assistant')

    if answer := ChatInput(initialValue="", key="inputButton"):
        key = generate()

        # Add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": answer, "key": "user-"+key.get_key()})

        content = '{question: '+new_question+', answer: '+answer+'}'
        evaluation = get_evaluation(content)
        st.session_state.messages.append(
            {"role": "assistant", "content": evaluation['eval'], "key": "assistant-"+key.get_key()})

        new_question = get_random_question()
        st.session_state.messages.append(
            {"role": "assistant", "content": new_question, "key": "assistant-"+key.get_key()})

        refresh('inputButton')
