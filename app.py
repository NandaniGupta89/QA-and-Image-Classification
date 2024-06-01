from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
## function to load Gemini Pro model and get repsonses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])
## Function to load OpenAI model and get respones


def main():
    st.set_page_config(page_title="QA and Image classification")


    # Add navigation options
    navigation = st.sidebar.radio("Navigation", ["QA Application", "Image Classification"])

    if navigation == "QA Application":



        def get_gemini_response(question):
            response = chat.send_message(question, stream=True)
            return response

        ##initialize our streamlit app



        st.header("QA Application")

        # Initialize session state for chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        input = st.text_input("Input: ", key="input")
        submit = st.button("Ask the question")

        if submit and input:
            response = get_gemini_response(input)
            # Add user query and response to session state chat history
            st.session_state['chat_history'].append(("You", input))
            st.subheader("The Response is")
            for chunk in response:
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
        st.subheader("The Chat History is")

        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")




    elif navigation == "Image Classification":
        def get_gemini_response(input, image):
            model = genai.GenerativeModel('gemini-pro-vision')
            if input != "":
                response = model.generate_content([input, image])
            else:
                response = model.generate_content(image)
            return response.text

        ##initialize our streamlit app



        st.header("Image Classification")
        input = st.text_input("Input Prompt: ", key="input")
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image = ""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)

        submit = st.button("Tell me about the image")

        ## If ask button is clicked

        if submit:
            response = get_gemini_response(input, image)
            st.subheader("The Response is")
            st.write(response)


if __name__ == "__main__":
    main()


