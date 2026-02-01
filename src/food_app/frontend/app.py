import sys
import os

# Add the parent directory (food_app) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import streamlit as st
from food_app.backend.infrastructure.logger import setup_logging, get_logger, trace_execution
from food_app.frontend.api_client import ApiClient
from food_app.frontend.constants import get_text
from food_app.frontend.views.dashboard import render_dashboard
from food_app.frontend.views.registry import render_registry
from food_app.frontend.views.kitchen import render_kitchen

# Configure logging
setup_logging()
logger = get_logger(__name__)

# 1. Setup & Architecture
@st.cache_resource
def get_api_client():
    return ApiClient()

api_client = get_api_client()

# Page Config
st.set_page_config(page_title=get_text("app_title"), layout="wide")

# 2. UI Structure (Sidebar Navigation)
st.sidebar.title(get_text("sidebar_title"))
nav_options = {
    get_text("nav_dashboard"): "dashboard",
    get_text("nav_registry"): "registry",
    get_text("nav_kitchen"): "kitchen"
}
selected_nav = st.sidebar.radio(get_text("sidebar_title"), options=list(nav_options.keys()))
page_id = nav_options[selected_nav]

# 3. Router
@trace_execution
def route_page(page_id, api_client):
    if page_id == "dashboard":
        render_dashboard(api_client)
    elif page_id == "registry":
        render_registry(api_client)
    elif page_id == "kitchen":
        render_kitchen(api_client)

route_page(page_id, api_client)
