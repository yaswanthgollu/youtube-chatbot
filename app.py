import streamlit as st
import os
from dotenv import load_dotenv

from youtube import get_transcript_from_url
from vectorstore import create_vectorstore
from rag import build_rag_chain

# -----------------------
# ENV SETUP
# -----------------------
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="centered"
)

# -----------------------
# TITLE
# -----------------------
st.title("🎥 YouTube Chatbot")
st.caption("Chat with any YouTube video using AI (RAG)")

# -----------------------
# SESSION STATE
# -----------------------
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------
# YOUTUBE INPUT (FORM - FIXES ENTER ISSUE)
# -----------------------
with st.form("video_form"):
    video_url = st.text_input("Paste YouTube URL")
    submitted = st.form_submit_button("🚀 Process Video")

if submitted:
    if not video_url:
        st.warning("Please enter a YouTube URL")
    else:
        with st.spinner("Fetching transcript & building knowledge base..."):
            transcript = get_transcript_from_url(video_url)

            if not transcript:
                st.error("Could not fetch transcript for this video.")
            else:
                vector_store = create_vectorstore(transcript)
                rag_chain = build_rag_chain(vector_store)

                st.session_state.rag_chain = rag_chain
                st.session_state.chat_history = []

                st.success("✅ Video processed successfully! Start chatting below.")

# -----------------------
# STATUS
# -----------------------
if st.session_state.rag_chain:
    st.success("🟢 Ready to chat")
else:
    st.info("ℹ️ Process a YouTube video to start chatting")

# -----------------------
# CHAT HISTORY DISPLAY
# -----------------------
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# -----------------------
# CHAT INPUT (MODERN UI)
# -----------------------
user_input = st.chat_input("Ask a question about the video...")

if user_input:
    if not st.session_state.rag_chain:
        st.warning("Please process a video first.")
    else:
        # User message
        st.session_state.chat_history.append(("user", user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag_chain.invoke(user_input)
                st.markdown(response)

        # Save response
        st.session_state.chat_history.append(("assistant", response))

        # Refresh UI
        st.rerun()

# -----------------------
# CLEAR CHAT BUTTON
# -----------------------
if st.session_state.rag_chain:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()