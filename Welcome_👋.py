import streamlit as st

st.set_page_config(
    page_title="Algoritma Demo - Python Beginner Specialization",
    page_icon="👋",
)

st.write("# Welcome to Algoritma Python Beginner Specialization! 👋")

st.sidebar.success("Select a demo above.")

# Copyright notice
st.sidebar.write("© Product Team Algoritma, 2024")

st.markdown(
    """
    🏢Algoritma is a data science education center based in Jakarta. 
    We organize workshops and training programs to help working professionals 
    and students gain mastery in various data science sub-fields: 
    data visualization, machine learning, data modeling, statistical inference etc.
    
    **👈 Explore the demos listed in the sidebar** 
    to discover various examples showcasing what we can learn 
    together using Python with **Algoritma Data Science School**!
    
    ### 💻 Want to learn more?
    - Check out [https://algorit.ma/](https://algorit.ma/)
    - Ask a question in our [community
        forums](https://github.com/teamalgoritma/community/discussions)
    ### 👩🏻‍🏫 Authors
    - Develop by [Algoritma](https://algorit.ma/)'s product division and instructors team
"""
)