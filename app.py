import streamlit as st

from core.loader import (
    load_manifesto,
    load_sages,
    list_dilemma_sets,
    load_dilemma_set,
)
from core.session import init_session_state, reset_session
from core.engine import (
    get_current_dilemma,
    save_answer,
    go_to_next_dilemma,
    is_last_dilemma,
    build_mirror_data,
)
from ui.screens import (
    render_welcome,
    render_manifest,
    render_set_selector,
    render_dilemma,
    render_mirror,
    render_silence,
)

st.set_page_config(
    page_title="Moje granice odpowiedzialności",
    page_icon="🦉",
    layout="centered",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 18px;
    }

    p, li, div {
        font-size: 1.05rem;
        line-height: 1.7;
    }

    h1 {
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.3;
    }

    h2 {
        font-size: 1.6rem;
        font-weight: 700;
        line-height: 1.4;
    }

    h3 {
        font-size: 1.2rem;
        font-weight: 700;
        line-height: 1.5;
    }

    .stCaption {
        font-size: 0.98rem !important;
        color: #444 !important;
    }

    label, .stMarkdown, .stTextArea, .stRadio, .stSlider {
        font-size: 1.02rem !important;
    }

    button[kind="primary"], button[kind="secondary"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

manifesto = load_manifesto("content/manifesto.yaml")
sages = load_sages("content/sages.yaml")
set_files = list_dilemma_sets("content/dilemma_sets")

init_session_state()

screen = st.session_state.screen

if screen == "welcome":
    if render_welcome():
        st.session_state.screen = "manifest"
        st.rerun()

elif screen == "manifest":
    if render_manifest(manifesto):
        st.session_state.screen = "set_selector"
        st.rerun()

elif screen == "set_selector":
    selected_set = render_set_selector(set_files)
    if selected_set is not None:
        st.session_state.selected_set = selected_set
        st.session_state.current_dilemma_index = 0
        st.session_state.answers = []
        st.session_state.mirror_data = None
        st.session_state.last_dilemma_completed = False
        st.session_state.screen = "dilemma"
        st.rerun()

elif screen == "dilemma":
    dilemmas = load_dilemma_set("content/dilemma_sets", st.session_state.selected_set)
    dilemma = get_current_dilemma(dilemmas)

    if dilemma is None:
        st.session_state.screen = "silence"
        st.rerun()

    result = render_dilemma(dilemma)

    if result is not None:
        save_answer(dilemma, result)

        last_answer = [st.session_state.answers[-1]]
        st.session_state.mirror_data = build_mirror_data(last_answer, sages)

        st.session_state.last_dilemma_completed = is_last_dilemma(dilemmas)
        st.session_state.screen = "mirror"
        st.rerun()

elif screen == "mirror":
    if render_mirror(st.session_state.mirror_data):
        if st.session_state.last_dilemma_completed:
            st.session_state.screen = "silence"
        else:
            go_to_next_dilemma()
            st.session_state.screen = "dilemma"
        st.rerun()

elif screen == "silence":
    if render_silence():
        reset_session()
        st.rerun()