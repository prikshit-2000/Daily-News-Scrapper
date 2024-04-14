import streamlit as st
from scrapper import scrapper




st.write("<h1 style='text-align: center;'>Daily News Post</h1>", unsafe_allow_html=True)


news_data = scrapper()

for i in range(len(news_data)):
    with st.expander(f"**{news_data[i]['title']}**"):
        
        with st.columns(3)[1]:
            st.image(news_data[i]['image_link'])
        st.write(news_data[i]['story_detail'])