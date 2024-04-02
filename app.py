import streamlit as st
from openai import OpenAI

st.title("Seller ChatBox")

def translate_text(text,target_lang):
    client = OpenAI(api_key='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')
    response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt=f"Conver the following text into {target_lang} : {text}",
    temperature=0.7,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    answer = response.choices[0].text
    return answer

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key='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')

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

response=""

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


# Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
            max_tokens=100,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Language translator in sidebar
with st.sidebar:
  st.title("Chat Translator")
  st.write("Translate text from one language to another")
  languages = ["afrikaans","albanian","amharic","arabic","armenian","azerbaijani","basque","belarusian","bengali","bosnian","bulgarian","catalan","cebuano",
                "chichewa","chinese (simplified)","chinese (traditional)","corsican","croatian","czech","danish","dutch","english","esperanto","estonian",
                "filipino","finnish","french","frisian","galician","georgian","german","greek","gujarati","haitian creole","hausa","hawaiian","hebrew",
                "hindi","hmong","hungarian","icelandic","igbo","indonesian","irish","gujarati","bengali","kannada","malayalam","tamil","telugu"]
  target_lang = st.selectbox("select target language :",languages)

  st.markdown("""---""")

  user_input = st.text_input("Buyer Chat :", value=prompt)
  if user_input:
  # Call translation API here and display the translated text
    translation_response = translate_text(user_input,target_lang)
    st.write("Buyer input Translation :")
    st.write(translation_response)

  st.markdown("""---""")

  gpt_reply = st.text_input("Seller Chat :", value=response)
  if gpt_reply:
    translation_response = translate_text(gpt_reply,target_lang)
    st.write("Seller input Translation :")
    st.write(translation_response)


