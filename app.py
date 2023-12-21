import streamlit as st
from streamlit_custom_chat import ChatContainer
from streamlit_custom_input import ChatInput
from key_generator.key_generator import generate
from helper_functions import set_bg_hack, set_page_container_style, refresh
import json
from backend_functions import get_evaluation, get_random_question, get_technichal_question, get_technichal_evaluation, messageFromChatBot, config
from left_column import left_column


def main_app(questionType="Behavioural"):
    st.set_page_config(layout="wide")

    set_bg_hack("assets/images/pastel3.jpg")

    set_page_container_style()

    titlecol1, titlecol2, titlecol3 = st.columns([8, 5, 3])

    with titlecol1:
        st.markdown('#')

    with titlecol2:
        st.title('Mentor Bot')

    with titlecol3:
        # st.markdown(st.session_state.category)
        st.markdown('#')

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

    if "questionType" not in st.session_state:
        st.session_state.questionType = questionType

    if st.session_state.questionType == 'Technical':

        # get a question to ask the user
        new_question = get_technichal_question(st.session_state.category)

        # if there are no messages in the session add
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append(
                {"role": "assistant", "content": config['technical_message'], "key": 0})

            st.session_state.messages.append(
                {"role": "assistant", "content": new_question, "key": 1})

        col1, col2 = st.columns([2, 13])

        with col1:
            left_column()

        with col2:
            # component that displays the messages
            ChatContainer(messages=st.session_state.messages,
                          key="chatcontainer")

            key = generate()

            # check if the agent is still streaming
            if st.session_state.responding:

                # call function that recieves the agent stream
                messageFromChatBot()

                # after the streaming is done reset the responding falg
                st.session_state.responding = False

                # change the flag to true to make the agent ask a new question
                st.session_state.getQuestion = True

                # reset the number of tokens to skip
                st.session_state.skip = 0

            # check if the user submitted an answer to review
            elif st.session_state.rateAnswer:

                # prepare the prompt for the agent
                content = '{question: '+new_question + \
                    ', answer: '+st.session_state.userAnswer+'}'

                # call the function that sends the prompt to the agent
                get_technichal_evaluation(content)

                # reset user answer
                st.session_state.userAnswer = ""

                # reset rate flag
                st.session_state.rateAnswer = False

                # make the question flag true to fetch a new question
                st.session_state.getQuestion = True

                refresh('chatcontainer')

            # check if a new question should be displayed
            if st.session_state.getQuestion:

                # call function to get a new question
                new_question = get_technichal_question(
                    st.session_state.category)

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

    else:

        new_question = get_random_question()

        # if there are no messages in the session add
        if len(st.session_state.messages) == 0:
            st.session_state.messages.append(
                {"role": "assistant", "content": config['openning_message'], "key": 0})

            st.session_state.messages.append(
                {"role": "assistant", "content": new_question, "key": 1})

        col1, col2 = st.columns([2, 13])

        with col1:
            left_column()

        with col2:
            # component that displays the messages
            ChatContainer(messages=st.session_state.messages,
                          key="chatcontainer")

            key = generate()

            # check if the agent is still streaming
            if st.session_state.responding:

                # call function that recieves the agent stream
                messageFromChatBot()

                # after the streaming is done reset the responding falg
                st.session_state.responding = False

                # change the flag to true to make the agent ask a new question
                st.session_state.getQuestion = True

                # reset the number of tokens to skip
                st.session_state.skip = 0

            # check if the user submitted an answer to review
            elif st.session_state.rateAnswer:

                # prepare the prompt for the agent
                content = '{question: '+new_question + \
                    ', answer: '+st.session_state.userAnswer+'}'

                # call the function that sends the prompt to the agent
                get_evaluation(content)

                # reset user answer
                st.session_state.userAnswer = ""

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


main_app()
