import pickle
from pathlib import Path
from streamlit_auth.authentification import *
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

def add_user(username,name,email,password):
    with open('./streamlit_auth/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    hashed_password = stauth.hasher(password)
    config['credentials'][username] = {'name' : name, 'email': email, 'password' : password, 'password' : hashed_password}
    with open('./streamlit_auth/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)