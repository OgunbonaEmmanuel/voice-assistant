import streamlit as st
from faster_whisper import WhisperModel
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI
import pyttsx3

load_dotenv('.env')
client = OpenAI()

st.header("AI ASSISTANT")

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# Keep the model loaded across Streamlit reruns
@st.cache_resource
def load_model():
    return WhisperModel(
        "base.en",
        device="cpu",
        compute_type="int8"
    )
model = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You're a friendly chatbot."}
    ]

messages = st.session_state.messages

audio = st.audio_input("Record your message", sample_rate=48000)
if audio is not None:
    st.audio(audio)

if st.button("Respond"):
    with st.spinner("Transcribing..."):
        segments, info = model.transcribe(
            BytesIO(audio.getvalue()),
            language="en",
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip() for segment in segments
        )
        messages.append({"role":"user", "content": text})
        st.write(text)

        response = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages = messages,
            temperature=0
        )

        asst_message = response.choices[0].message.content
        messages.append({"role": "assistant","content" : asst_message})

        if asst_message:
            st.write(asst_message)
            speak(asst_message)