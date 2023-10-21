import os
import json
import openai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import textwrap

load_dotenv()

os.environ['OPENAI_KEY'] = "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"
openai.api_key = os.getenv('OPENAI_KEY')

def prepare_data_for_finetuning(csv_file, jsonl_output):
    data = pd.read_csv(csv_file).head(500)
    new_df = pd.DataFrame({'Completion': data['Text'].iloc[::2].values, 'Prompt': data['Text'].iloc[1::2].values})
    output = []
    for index, row in new_df.iterrows():
        line = {'prompt': row['Prompt'], 'completion': row['Completion']}
        output.append(line)

    with open(jsonl_output, 'w') as outfile:
        for i in output:
            json.dump(i, outfile)
            outfile.write('\n')

def generate_response(input_text, fine_tuned_model="ft:davinci-002:personal::8BsA3Pz3"):
    response = openai.Completion.create(
        engine=fine_tuned_model,
        prompt=f"The following is a conversation with MovieBot, an AI assistant. "
               f"MovieBot is a movie lines bot who is very helpful and knowledgeable in movies.\n\n"
               f"Prompt: Hello, who are you?\n"
               f"Completion: I am MovieBot, a movie chatbot assistant. How can I help you today?\n"
               f"Prompt: {input_text}\nMovieBot:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Prompt:", " Completion:"]
    )
    return response.choices[0].text.strip()

st.title("🤖 MovieBot - The Movie Chatbot")
st.write("Hello! I am MovieBot, a movie chatbot assistant.")
st.write("I can help you find lines from movies and provide answers based on them.")
st.write("BTW, my favorite movie is The Avengers (2012) Avengers: Age of Ultron (2015)!")
st.write("What is your favorite movie? Who is your favorite character?")
st.write("You can enter 'exit', 'bye', or 'quit' at any time to quit the chatbot.")

# New button for data preparation:
if st.button("Prepare Data for Fine-tuning"):
    prepare_data_for_finetuning('movie_lines.csv', 'processed_movie_lines.jsonl')
    st.write("Data has been prepared and saved to processed_movie_lines.jsonl!")

# Initializing chat history and user input if they don't exist in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# User input
user_input = st.text_input("You:", value=st.session_state.user_input)

# Check if the button is pressed or Enter is pressed in the text input
if st.button("Submit") or user_input != st.session_state.user_input:
    st.session_state.user_input = user_input
    if user_input.lower() in ["exit", "bye", "quit"]:
        st.write("Moviebot: Goodbye! 👋")
    else:
        response = generate_response(user_input)
        st.session_state.chat_history.insert(0, {"user": user_input, "bot": response})

        # Clear the text input field after processing
        st.session_state.user_input = ""

# Display chat history in reverse order
for chat in st.session_state.chat_history:
    if chat["user"]:
        st.image("avatar.png", use_column_width=False, width=50)
        st.write("You: " + chat["user"])
    if chat["bot"]:
        st.image("bot.png", use_column_width=False, width=50)
        st.write("Moviebot:", chat["bot"])