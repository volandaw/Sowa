import streamlit as st


def init_session_state():
    defaults = {
        "screen": "welcome",
        "current_dilemma_index": 0,
        "answers": [],
        "mirror_data": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session():
    for key in ["screen", "current_dilemma_index", "answers", "mirror_data"]:
        if key in st.session_state:
            del st.session_state[key]

    init_session_state()