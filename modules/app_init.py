import streamlit as st 

def init():  
    if not st.session_state.get("configured", False):  
        st.set_page_config(  
            page_title="Azure OpenAI Assistant",  
            page_icon="🤖",  
            layout="wide",  
            initial_sidebar_state="expanded",  
            menu_items={"Get help": "https://learn.microsoft.com/en-us/azure/?product=popular"},  
        )  
        st.session_state.configured = True