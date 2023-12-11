import base64
import streamlit as st

def set_bg_hack(main_bg):
    '''
    A function to unpack an image from root folder and set as bg.
 
    Returns
    -------
    The background.
    '''
    # set bg name
    main_bg_ext = "jpg"
        
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         [data-testid="stHeader"] {{
          background-color: rgba(0,0,0,0);
        }}
        [data-testid="baseButton-secondary"]{{
            border-radius:2rem;
            height: 47px;
            border-color: transparent;
            background-color: #fef8ff;
            font-family: 'Itim';
        }}
        [data-testid="baseButton-secondary"]:hover{{
            border-radius:2rem;
            height: 47px;
            border-color: transparent;
            background-color: #fdf4ff;
            color:black;
            font-family: 'Itim';
        }}
        .stChatFloatingInputContainer{{
            background-color: transparent;
        }}
         </style>
         """,
         unsafe_allow_html=True
     )
    
    

def set_page_container_style(
        max_width: int = 1400, max_width_100_percent: bool = False,
        padding_top: int = 2, padding_right: int = 0, padding_left: int = 1, padding_bottom: int = 1,
        # color: str = COLOR, background_color: str = BACKGROUND_COLOR,
    ):
    if max_width_100_percent:
        max_width_str = f'max-width: 100%;'
    else:
        max_width_str = f'max-width: {max_width}px;'
    st.markdown(
        f'''
        <style>
            
            [data-testid="block-container"]{{
                {max_width_str}
                padding-top: {padding_top}rem;
                padding-right: {padding_right}rem;
                padding-left: {padding_left}rem;
                padding-bottom: {padding_bottom}rem;
                
            }}
        </style>
            
        ''',
        unsafe_allow_html=True,
    )
    
def refresh(key:str):
    del st.session_state[key]
    st.rerun()