from start_page import start_page
from app import main_app
import streamlit as st

if "questionType" not in st.session_state:
    st.session_state.questionType = None
    st.session_state.category = None
    start_page()
    
elif st.session_state.questionType!=None :
    main_app(questionType=st.session_state.questionType)

else:
    start_page()
    