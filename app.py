# app.py (starter)
import streamlit as st

st.set_page_config(page_title="Tachi | AI Twin", layout="centered")

st.title("Tachi: Your AI Twin")
st.markdown("---")

prompt = st.text_input("Ask Tachi something:", "")

if st.button("Submit"):
    if prompt.strip():
        # Stub response until model is connected
        response = f"You said: '{prompt}'. Tachi will respond intelligently once the backend is live."
        st.success(response)
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.caption("This is a starter UI. Model, voice, and vision integration will be wired in next.")
