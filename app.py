import streamlit as st
import requests
from chatbot import qa, chain
from pydantic import BaseModel


def main():

    st.sidebar.title("Product Recommendation App Demo")
    st.sidebar.markdown(
        """
        You can use the two methods listed below to use this application.
        """
    )

    def manual():
        st.header("🛍️ Product Recommendation App 🛍️")
        st.write("")
        st.write("Please fill in the fields below.")
        st.write("")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            department = st.text_input("Product Department: ")
        with col2:
            category = st.text_input("Product Category: ")
        with col3:
            brand = st.text_input("Product Brand: ")
        with col4:
            price = st.number_input("Maximum price: ", min_value=0, max_value=1000)
        if st.button("Get recommendations"):
            with st.spinner("Just a moment..."):

                response = chain.run(
                    department=department, category=category, brand=brand, price=price
                )

                try:
                    result = response

                    result_string = result

                    result_cleaned = (
                        result_string.replace("[", "")
                        .replace("0:", "")
                        .replace("]", "")
                    )
                    st.success(result_cleaned)
                except Exception as e:
                    st.error(f"Error fetching answer. Please try again. \n Error {e}")

    def chatbot():
        class Message(BaseModel):
            actor: str
            payload: str

        st.header("🤖 Product Recommendation Chatbot 🤖")

        user = "User"
        assistant = "Assistant"
        message = "Messages"

        if message not in st.session_state:
            st.session_state[message] = [
                Message(actor=assistant, payload="Hi!How can I help you? 😀")
            ]

        msg: Message
        for msg in st.session_state[message]:
            st.chat_message(msg.actor).write(msg.payload)

        prompt: str = st.chat_input("Enter a prompt here")

        if prompt:
            response = qa.run(query=prompt)
            result = response
            result_string = result
            result_cleaned = (
                result_string.replace("[", "").replace("0:", "").replace("]", "")
            )
            st.session_state[message].append(Message(actor=user, payload=prompt))
            st.chat_message(user).write(prompt)
            st.session_state[message].append(
                Message(actor=assistant, payload=result_cleaned)
            )
            st.chat_message(assistant).write(result_cleaned)

    mode = st.sidebar.radio(" ", ["Manual Input 🛍️", "ChatBot 🤖"])

    if mode == "Manual Input 🛍️":
        manual()
    elif mode == "ChatBot 🤖":
        chatbot()


if __name__ == "__main__":
    main()
