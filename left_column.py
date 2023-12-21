import streamlit as st
from helper_functions import refresh
categories=["R", "Python", "Data Warehousing","Database","MySQL","Algorithms","Data Structure"]
questionTypes=["Technical", "Behavioural"]
# def onChange(option):
#     del option

def left_column():
    st.markdown("#")
    st.markdown("#")
    
    st.markdown(
            f"""
            <style>
            .st-b6{{
                color:rgb(61, 48, 96);
            }}
            .st-bb{{
                background-color:rgb(240, 233, 255);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown("""
        <style>
        .welcome-font {
            font-size:18px !important; 
            font-family: arial;
            font-weight:700;
            margin:0;
            color:rgb(38, 29, 69);
            # font-size:large;
        }
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="welcome-font">Try something new!</p>', unsafe_allow_html=True)
    st.markdown("#")
    
    # button to redirect to quiz page (currently does nothing)
    option = st.selectbox(
            "Type",
            options=(questionTypes),
            index=questionTypes.index(st.session_state.questionType),
            key="typeSelectBox",
            placeholder="Select type...",
            )
    if option=="Technical":
        category = st.selectbox("Category", 
                             options=("R", "Python", "Data Warehousing","Database","MySQL","Algorithms","Data Structure"),
                             key="categorySelectBox",
                             index=categories.index( st.session_state.category))
                # if "category" not in st.session_state:
        st.session_state.category = category
    else:
        st.session_state.category = "R"
    st.markdown("#")
    
    start=st.button("Start Learning!", use_container_width=True, key="quizbutton")
    if start:
        st.session_state.questionType = option
        del st.session_state.messages
        refresh("quizbutton")