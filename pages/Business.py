import streamlit as st
def app():
    st.sidebar.title('Business Need')
    with open('README.md', 'r') as file:
        readme_content = file.read()

    st.markdown(readme_content)  

  