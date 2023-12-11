import streamlit as st
# from custom_chat_bubble import CustomChatBubble
# from streamlit_custom_chat import ChatContainer
# from custom_chat_bubble import updateMessages
from streamlit_custom_input import ChatInput
from key_generator.key_generator import generate
from streamlit_js_eval import streamlit_js_eval
from helper_functions import set_bg_hack, set_page_container_style, refresh
  
st.set_page_config(layout="wide")
  
set_bg_hack("assets/images/pastel3.jpg") 

set_page_container_style()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    

st.sidebar.header("header")
# st.sidebar.subheader(‘1.please chose which app you want to operate’)

    
if len(st.session_state.messages) ==0:
    st.session_state.messages.append({"role":"assistant","content":"Hello! How may I help you?","key":0})
   
col1, col2 = st.columns([2,13]) 
        
with col1:
    st.markdown("#")
    st.markdown("#")
    st.markdown("#")
    st.button("Take a Quiz", use_container_width=True)
    
with col2:
    ChatContainer(messages=st.session_state.messages, key=str(55))

    # if st.button(label="assistant", key="assistant"):
    #     key = generate()
    #     st.session_state.messages.append({"role": "assistant", "content": "whatever","key":"assistant-"+key.get_key()})
    #     refresh('assistant')
        

    if prompt:= ChatInput(initialValue="",key="inputButton"):
        key = generate()
       
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt,"key":"user-"+key.get_key()})
        # st.session_state.messages.append({"role": "assistant", "content": prompt,"key":"assistant-"+key.get_key()})

        refresh('inputButton')