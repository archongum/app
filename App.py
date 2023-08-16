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

add_page_title()  # Optional method to add title and icon to current page
