import streamlit as st
from helper_functions import refresh, set_bg_hack
categories=["R", "Python", "Data Warehousing","Database","MySQL","Algorithms","Data Structure"]

def start_page():
    set_bg_hack("assets\images\pastel3.jpg")
    with st.container():
        # label = "Enter text here"
        # st.text_input(label)

        
        st.markdown(
            f"""
            <style>
            .st-b6{{
                color:rgb(43, 21, 120);
            }}
            .st-bb{{
                background-color:rgb(218, 226, 255);
            }}
            [data-testid="baseButton-secondary"]{{
                background-color:#dfe6ff
                
            }}
            [data-testid="baseButton-secondary"]{{
                width:100px;
            }}
            [data-testid="stVerticalBlockBorderWrapper"]{{
                justify-content:center;
                display:flex;
                # padding-right:10px;
                # padding-bottom:10px;
                # padding-left:10px;
            }} 
            [data-testid="stMarkdownContainer"]{{
                font-family: arial;
                # font-weight:700;
                font-size:large;
                color:rgb(43, 21, 120);
            }}
            [data-testid="stVerticalBlock"]{{
                border-radius:2rem;
                background-color:#f0efff;
                padding-left:25px;
                padding-right:25px;
                padding-top:5px;
                padding-bottom:25px;
            }}
            [data-testid="element-container"]{{
                width: auto;
                text-align:center;
            }}
            [data-testid="stSelectbox"]{{
                padding-bottom: 25px;
            }}
            [data-testid="block-container"]{{
                width:750px;
                display:flex;
                justify-content:center;

            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        col1, col2 =st.columns([11,1])
        with col1:
            
            st.markdown("""
            <style>
            .welcome-font {
                font-size:35px !important; 
                font-family: arial;
                font-weight:700;
                margin:0;
                color:rgb(88, 67, 159);
                # font-size:large;
            }
            .select-font {
                font-size:25px !important; 
                font-family: arial;
                font-weight:700;
                margin:0;
                padding-bottom:20px;
                color:rgb(88, 67, 159);
                
                # font-size:large;
            }
            </style>
            """, unsafe_allow_html=True)

            st.markdown('<p class="welcome-font">Welcome!</p>', unsafe_allow_html=True)
            st.markdown('<p class="select-font">Please select the type of questions</p>', unsafe_allow_html=True)
            option = st.selectbox(
            "Question type",
            options=("Technical", "Behavioural"),
            index=None,
            key="typeSelectBox",
            placeholder="Select type...",
                )
            if st.session_state["typeSelectBox"]=="Technical":
                category = st.selectbox("Category", 
                             options=(categories),
                             key="categorySelectBox1")
                # if "category" not in st.session_state:
                st.session_state.category=category
            # st.write('You selected:', option)
            start=st.button(label="Submit", key="start")
            
            if option!=None and start:
                st.session_state.questionType=option
                refresh("start")
        col2

    