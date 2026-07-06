# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
import streamlit as st

# load_dotenv()
# model = ChatOpenAI(model = "gpt-5.5")
# st.header("Research Tool")
# user_input = st.text_input("Enter your prompt")
# if st.button("Summarize"):
#     result = model.invoke(user_input)

#     st.write(result.content)

st.write("This runs every single time!")
name = st.text_input("What's your name?")

if name:
    st.write(f"Hello, {name}!")


col1, col2 = st.columns(2)

with col1:
    st.header("Left side")
    st.write("I live in column 1")

with col2:
    st.header("Right side")
    st.write("I live in column 2")


# option = st.sidebar.button("Choose a page", ["Home", "About"])

# st.title("Main content")
# st.write(f"You selected: {option}")

# st.header("Counter App")

# if "count" not in st.session_state:
#     st.session_state.count = 0
# if st.button("Increment"):
#     st.session_state.count += 1

# if st.button("Reset"):
#     st.session_state.count = 0

# st.write(f"Count = {st.session_state.count}")




if "count" not in st.session_state:
    st.session_state.count = 0

if st.sidebar.button("Increment"):
    st.session_state.count += 1

if st.sidebar.button("Reset"):
    st.session_state.count = 0

st.write(f"Count: {st.session_state.count}")
