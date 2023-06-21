import streamlit as st  
from dotenv import load_dotenv  
import os
import pytz
import tiktoken
from langchain.chat_models import ChatOpenAI  
from langchain.chat_models import AzureChatOpenAI  
from langchain.schema import (  
    SystemMessage,  
    HumanMessage,  
    AIMessage  
)  
from datetime import datetime  
from urllib.parse import unquote  
from datetime import datetime, timedelta
from modules.app_helpers import set_background_image  
from modules.app_helpers import get_prompt_system_message
from modules.app_helpers import set_azurechatopenai
from modules.app_init import init
  
def main():  

    # Load the Environment Vars
    load_dotenv()  

    init()  
    st.header("GPT4-Powered Assistant 🌐")

    now = datetime.now(pytz.utc)  # Get the current time in UTC  
    aest = pytz.timezone('Australia/Sydney')  # Define the AEST timezone  
    now_aest = now.astimezone(aest)  # Convert the time to AEST  
    current_datetime_str = now_aest.strftime("%Y-%m-%d %H:%M:%S")  
    print("Current Date and Time in AEST =", current_datetime_str)

    # Sidebar UI
    with st.sidebar:  

        if "personality" not in st.session_state:  
            st.session_state.personality_state = "Professional"

        if "character" not in st.session_state:
            st.session_state.character_state = "an A.I. Assitant"

        # Generate Default System Prompt
        prompt_system_message = get_prompt_system_message('General Knowledge', 'Professional', st.session_state.character_state, current_datetime_str)
        
        with st.expander("__System Settings__"):             
            token_limit = int(os.environ.get("OPENAI_TOKEN_LIMIT"))
            temperature_slider = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01, key="temperature")
            max_tokens_input = st.number_input("Max Response Tokens", min_value=1, max_value=8000, value=800, step=10, key="max_tokens")             
        
            # Multi-select for prompt template: Used for Assistant System Role
            options = ['General Knowledge','Financial Advise', 'Australia Taxation', 'Azure Integration','Human Resources']
            selected_options = st.multiselect("Select Expertise", options, key="selected_options", default=['General Knowledge'])

            # Custom user-provided 'Expertise' string input
            custom_option = st.text_input("Custom Expertise (comma separated)", key="custom_option")
            if custom_option:  
                if custom_option not in options:  
                    options.append(custom_option)  
                if custom_option not in selected_options:  
                    selected_options.append(custom_option)
            
            # Convert selected_options list to a string  
            selected_options_str = ', '.join(selected_options)  
            
            # Concatenate to another variable string  
            selected_expertise = ""  
            final_selected_expertise = selected_expertise + selected_options_str 

            # Select the personality
            personality = st.selectbox("Select Personality", ["Entertainer", "Friendly", "Humorous", "Perky", "Professional"], key="personality", index=1)
            st.session_state.personality_state = personality
            
            # Select Character Style
            character = st.selectbox("Select Writer Style", ["an A.I. Assistant", "Adam Sandler", "Eminem", "Shakespeare",  "Snoop Dogg", "Spock",  "Yoda"], key="character", index=0)
            st.session_state.character_state = character

            # Apply the settings via this button
            apply_button = st.button("Apply", key="apply")
            if apply_button:
                # Generate the System Prompt
                prompt_system_message = get_prompt_system_message(final_selected_expertise, st.session_state.personality_state, st.session_state.character_state, current_datetime_str)    
                st.session_state.messages = [  
                    SystemMessage(content=prompt_system_message)                  
                    ]  

            if "messages" not in st.session_state:  
                st.session_state.messages = [  
                    SystemMessage(content=prompt_system_message)                  
                    ]  

            if "total_token_count" not in st.session_state:  
                st.session_state.total_token_count = 0  
        
        st.divider()  

        # TODO: Find a way to clear the user_input text area


        # User input text area where users types their questions
        user_input = st.text_area("Chat with Savi: ", key="user_input", height=200)    

        # This will clear the chat history, but not the user input text area.
        clear_chat_button = st.button("Clear Chat")  
        if clear_chat_button:  
            st.session_state.messages = [  
                SystemMessage(content=prompt_system_message)  
                ]
            st.session_state.total_token_count = 0     

        # Call the Azure Chat API
        chat=set_azurechatopenai(temperature_slider, max_tokens_input)

        # Process the user input        
        if user_input and st.session_state.total_token_count < token_limit: 
            st.session_state.messages.append(HumanMessage(content=user_input)) 
            with st.spinner("Thinking..."):  
                try:                
                    response = chat(st.session_state.messages)
                    st.session_state.messages.append(AIMessage(content=response.content))   
                    token_count = chat.get_num_tokens_from_messages(st.session_state.messages)
                    st.session_state.total_token_count = token_count
                except Exception as error:
                    response = "Looks like something went wrong: " + str(error)    
                    st.session_state.messages.append(AIMessage(content=response))   
                    
        if st.session_state.total_token_count >= token_limit:
            st.error(f"❌ You have reached the token limit! Please clear the chat session now. {st.session_state.total_token_count}/{token_limit} tokens used.")    
        elif st.session_state.total_token_count >= 0.8 * token_limit:  
            st.warning(f"⚠️ You are nearing the token limit! {st.session_state.total_token_count}/{token_limit} tokens used.")        
        
    messages = st.session_state.get('messages', [])  
    for i, msg in enumerate(messages[1:]):  
        if i % 2 == 0:  
            # User message  
            with st.container():  
                col1, col2 = st.columns([1, 9])  
                with col1:  
                    st.write("")  
                with col2:  
                    st.markdown(f'<div style="background-color: rgba(7,25,51,0.5); border-radius: 5px; padding: 10px; margin-bottom: 10px; color: #FFFFFF; text-align: left;">🗨️&nbsp;{msg.content}<span style="margin-left: 5px;"></span></div>', unsafe_allow_html=True)  
        else:  
            # AI message  
            with st.container():  
                col1, col2 = st.columns([9, 1])  
                with col1:  
                    st.markdown(f'<div style="background-color: rgba(96,105,117,0.5); border-radius: 5px; padding: 10px; margin-bottom: 10px; color: #FFFFFF;"><span style="margin-right: 5px;"></span>💡{msg.content}<div style="font-size: 0.8rem; text-align: right; margin-top: 5px;">Tokens used: {st.session_state.total_token_count}/{token_limit}</div></div>',  
            unsafe_allow_html=True,  
        )  
                with col2:  
                    st.write("")  

  
    VERSION = "[Build.Id]"  
  
    footer = f"""<div style="position: fixed; bottom: 10px; right: 10px; font-size: 0.8rem; font-weight: bold; color: #aaa;">Version: {VERSION}</div>"""  
    st.markdown(footer, unsafe_allow_html=True)  

if __name__ == '__main__':  
    main()  

