import streamlit as st
import home, application, account
from streamlit_option_menu import option_menu

st.set_page_config(page_title="EnhanceAI",)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='EnhanceAI',
                options=['Home','Account','Enhancement'],
                icons=['house-fill','person-circle','cpu'],
                menu_icon='robot',
                default_index=0,
                styles={"container": {"padding": "5!important","background-color":'#000000'},
                        "icon": {"color": "white", "font-size": "23px"}, 
                        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "#14213D"},
                        "nav-link-selected": {"background-color": "#FCA311"},}
                )
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()
        if app == "Enhancement":
            application.app()

    run()
            
