# main.py
from gui.main_dashboard import launch
# TODO: Import the new admin utilities.
from app.admin_utils import init_logger, backup_data

import streamlit as st



if __name__ == "__main__":
    # TODO: Initialize the logger as the very first step.
    if "initlog" not in st.session_state:
        init_logger()
        st.session_state.initlog = True

    # TODO: Perform a data backup before starting the application session.
    if "backup" not in st.session_state:
        backup_data()
        st.session_state.backup = True

    # TODO: Launch the GUI as before.
    launch()