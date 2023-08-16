import streamlit as st
from st_pages import Page, Section, add_page_title, show_pages

show_pages(
    [
        Page("App.py", "Home", "🏠"),
        Section(name="App", icon="🧨"),
        Page("pages/kubernetes_config.py", "Kubernetes Config", ":books:"),
        Page("pages/omymodels.py", "Omymodels Online", "📖"),
    ]
)

add_page_title()

st.markdown(
    r"""
## App

👉Click on Sidebar

## External App

- [SQL Parser](https://archongum.cn/static/filebeat_pg_parser.html)

"""
)
