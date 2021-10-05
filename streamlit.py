import streamlit as st
st.write(""" 
# HELLO WORLD 
How are you? """)

number = st.slider("Pick a number", 0, 100)

date = st.date_input("Pick a date")

st.write("""
You have chosen """ + str(number) + """ number and """ + str(date) + """ date
""")