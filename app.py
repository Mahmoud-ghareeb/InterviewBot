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
import time
from dotenv import load_dotenv


config = yaml.load(open('./configs/config.star.yaml', 'r'),
                   Loader=yaml.FullLoader)

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    api_key=API_KEY
)

df = pd.read_csv('./data/star_questions.csv')


st.set_page_config(layout="wide")

set_bg_hack("assets/images/pastel3.jpg")

set_page_container_style()

titlecol1, titlecol2, titlecol3 = st.columns([8,5,3])

with titlecol1:
    st.markdown('#')

with titlecol2:
    st.title('Mentor Bot')
    
with titlecol3:
    st.markdown('#')  

def get_evaluation(content: str) -> dict:
    """
    Evaluate if the provided answer follows the STAR methodology

    :param content: {'question': the question, 'answer': the answer}
    :return: {"eval": your detailed evaluation of the answer}
    """
    key = generate()
    
    st.session_state.messages.append(
            {"role": "assistant", "content": "", "key": "assistant-"+key.get_key()})
        
    st.session_state.response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system",
              "content": config['prompts']['evaluation_prompt']},
            {"role": "user", "content": content}
        ],
        stream=True 
    )
    
    st.session_state.rateAnswer=False
    
    st.session_state.responding = True
    
    refresh("chatcontainer")


def get_random_question():
    """
    get a random question from the csv file

    :return: question 
    """
    random_question_idx = np.random.randint(0, 60)
    data = df.iloc[random_question_idx]

    return data['Question']



def messageFromChatBot():
    """
    get each chunk streamed from the API and add it to the message then refresh except for the first
    4 and last 2 chunks which are these token {eval:" "}

    :return: nothing 
    """
    for chunk in st.session_state.response:
        if chunk.choices[0].delta.content is not None:
            if st.session_state.skip>4:
                st.session_state.messages[-1]["content"]+=chunk.choices[0].delta.content
                time.sleep(0.005)
                refresh("chatcontainer")
            else:
                st.session_state.skip+=1
    st.session_state.messages[-1]["content"]=st.session_state.messages[-1]["content"][:-1]
    st.session_state.messages[-1]["content"]=st.session_state.messages[-1]["content"][:-1]



# Initialize session variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "rateAnswer" not in st.session_state:
    st.session_state.rateAnswer = False
    
if "getQuestion" not in st.session_state:
    st.session_state.getQuestion = False
    
if "userAnswer" not in st.session_state:
    st.session_state.userAnswer = ""
    
if "responding" not in st.session_state:
    st.session_state.responding = False
    
if "skip" not in st.session_state:
    st.session_state.skip = 0

# get a question to ask the user
new_question = get_random_question()

# if there are no messages in the session add
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
    
    key = generate()
    
    # check if the agent is still streaming
    if st.session_state.responding:
        
        # call function that recieves the agent stream
        messageFromChatBot()
        
        # after the streaming is done reset the responding falg
        st.session_state.responding = False
        
        # change the flag to true to make the agent ask a new question
        st.session_state.getQuestion = True
        
        #reset the number of tokens to skip
        st.session_state.skip = 0
        
    # check if the user submitted an answer to review
    elif st.session_state.rateAnswer:
        
        # prepare the prompt for the agent
        content = '{question: '+new_question+', answer: '+st.session_state.userAnswer+'}'
        
        # call the function that sends the prompt to the agent
        get_evaluation(content)
        
        # reset user answer
        st.session_state.userAnswer=""
        
        # reset rate flag
        st.session_state.rateAnswer = False
        
        # make the question flag true to fetch a new question
        st.session_state.getQuestion = True
        
        refresh('chatcontainer')
        
    # check if a new question should be displayed
    if st.session_state.getQuestion:
        
        # call function to get a new question
        new_question = get_random_question()
        
        # add the new question to the session state
        st.session_state.messages.append(
            {"role": "assistant", "content": new_question, "key": "assistant-"+key.get_key()})
        
        # reset question flag
        st.session_state.getQuestion = False
        
        refresh('chatcontainer')
        
    # recieve input from the user
    if answer := ChatInput(initialValue="", key="inputButton"):
        
        # add user message to chat history
        st.session_state.messages.append(
            {"role": "user", "content": answer, "key": "user-"+key.get_key()})
        
        st.session_state.userAnswer = answer
        
        # make the rate flag true to send the question to the agent
        st.session_state.rateAnswer = True
        
        # reset question and responding flags
        st.session_state.getQuestion = False
        st.session_state.responding = False
        
        refresh('inputButton')

       
