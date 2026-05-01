import streamlit as st


def init_session_state():
    defaults = {
        "screen": "welcome",
        "selected_set": None,
        "current_dilemma_index": 0,
        "answers": [],
        "mirror_data": None,
        "last_dilemma_completed": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_session():
    for key in [
        "screen",
        "selected_set",
        "current_dilemma_index",
        "answers",
        "mirror_data",
        "last_dilemma_completed",
    ]:
        if key in st.session_state:
            del st.session_state[key]

    init_session_state()