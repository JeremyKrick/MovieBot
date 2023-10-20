import streamlit as st
from streamlit_chat import message
import openai

# Initialize OpenAI API key
openai.api_key = "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"

st.set_page_config(page_title="Chat with SimonGPT")
st.title("Chat with SimonGPT")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

model = "gpt-3.5-turbo"

def get_initial_message():
    messages = [
        {"role": "system", "content": """
        You are SimonGPT a strategy researcher based in the UK.
        “Researcher” means in the style of a strategy researcher with well over twenty years research in strategy and cloud computing.
        You use complicated examples from Wardley Mapping in your answers, focusing on lesser-known advice to better illustrate your arguments.
        Your language should be for a 12 year old to understand.
        If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context.
        Use a mix of technical and colloquial UK English language to create an accessible and engaging tone.
        Provide your answers using Wardley Mapping in a form of a sarcastic tweet.
        """},
        {"role": "user", "content": "I want to learn about Wardley Mapping"},
        {"role": "assistant", "content": "That's awesome, what do you want to know about Wardley Mapping?"}
    ]
    return messages

def get_chatgpt_response(messages, model=model):
    response = openai.Completion.create(
        model=model,
        prompt="\n".join([f"{message['role']}: {message['content']}" for message in messages]),
        max_tokens=150
    )
    return response.choices[0].text.strip()

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "What is Wardley Mapping?", key="input")

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

# Reverse the display order
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))
