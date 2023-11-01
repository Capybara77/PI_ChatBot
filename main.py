from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import logging
import streamlit as st

logging.set_verbosity_error()

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
step = 0

st.title("PI_ChatBot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "tokens" not in st.session_state:
    st.session_state.tokens = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Write something"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([st.session_state.tokens, new_user_input_ids], dim=-1) if st.session_state.tokens != None else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    st.session_state.tokens = chat_history_ids

    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
