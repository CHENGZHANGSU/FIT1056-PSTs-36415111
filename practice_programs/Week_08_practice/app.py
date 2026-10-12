import streamlit as st

st.title("Hello World")

name = st.text_input("Enter your name: ")

if st.button("Greet"):
    st.write(f"Hello, {name}! Hi~ o(*￣▽￣*)ブ Welcome!")