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
st.image("assets/realistic_barred_owl_on_branch.png", width=180)

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
        color: #5a6170 !important;
    }

    label, .stMarkdown, .stTextArea, .stRadio, .stSlider {
        font-size: 1.02rem !important;
    }

    button[kind="primary"], button[kind="secondary"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stButton"] > button {
        border-radius: 10px;
        border: 1px solid #cfd6df;
    }

    .welcome-accent-line {
        width: 96px;
        height: 3px;
        border-radius: 999px;
        background: #5b6c8f;
        margin: 0.4rem 0 1.1rem 0;
    }

    .welcome-intro {
        border-left: 3px solid #5b6c8f;
        padding-left: 0.9rem;
        margin: 1rem 0 1.2rem 0;
    }

    .welcome-motto {
        border: 1px solid #dde3ea;
        border-radius: 12px;
        padding: 0.95rem 1rem;
        margin: 1rem 0 1.4rem 0;
        background: #fbfcfe;
    }

    .dilemma-title-line {
        width: 82px;
        height: 3px;
        border-radius: 999px;
        margin: 0.35rem 0 0.9rem 0;
    }

    .dilemma-box {
        border-left-width: 4px;
        border-left-style: solid;
        border-radius: 10px;
        padding: 0.9rem 1rem;
        margin: 0.9rem 0 1rem 0;
        background: #fcfcfd;
        white-space: pre-line;
    }

    .dilemma-accent-0 .dilemma-title-line,
    .dilemma-accent-0.dilemma-box {
        border-color: #5b6c8f;
        background: linear-gradient(to right, rgba(91,108,143,0.07), rgba(91,108,143,0.02));
    }
    .dilemma-accent-0 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-0 {
        background: #5b6c8f;
    }

    .dilemma-accent-1 .dilemma-title-line,
    .dilemma-accent-1.dilemma-box {
        border-color: #6b7d5c;
        background: linear-gradient(to right, rgba(107,125,92,0.07), rgba(107,125,92,0.02));
    }
    .dilemma-accent-1 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-1 {
        background: #6b7d5c;
    }

    .dilemma-accent-2 .dilemma-title-line,
    .dilemma-accent-2.dilemma-box {
        border-color: #9b7a4b;
        background: linear-gradient(to right, rgba(155,122,75,0.07), rgba(155,122,75,0.02));
    }
    .dilemma-accent-2 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-2 {
        background: #9b7a4b;
    }

    .dilemma-accent-3 .dilemma-title-line,
    .dilemma-accent-3.dilemma-box {
        border-color: #8a5f6b;
        background: linear-gradient(to right, rgba(138,95,107,0.07), rgba(138,95,107,0.02));
    }
    .dilemma-accent-3 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-3 {
        background: #8a5f6b;
    }

    .dilemma-accent-4 .dilemma-title-line,
    .dilemma-accent-4.dilemma-box {
        border-color: #5f7f8a;
        background: linear-gradient(to right, rgba(95,127,138,0.07), rgba(95,127,138,0.02));
    }
    .dilemma-accent-4 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-4 {
        background: #5f7f8a;
    }

    .dilemma-accent-5 .dilemma-title-line,
    .dilemma-accent-5.dilemma-box {
        border-color: #75688c;
        background: linear-gradient(to right, rgba(117,104,140,0.07), rgba(117,104,140,0.02));
    }
    .dilemma-accent-5 .dilemma-title-line,
    .dilemma-title-line.dilemma-accent-5 {
        background: #75688c;
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
    action, selected_set = render_set_selector(set_files)

    if action == "select":
        st.session_state.selected_set = selected_set
        st.session_state.current_dilemma_index = 0
        st.session_state.answers = []
        st.session_state.mirror_data = None
        st.session_state.last_dilemma_completed = False
        st.session_state.screen = "dilemma"
        st.rerun()

    elif action == "end":
        reset_session()
        st.rerun()

elif screen == "dilemma":
    dilemmas = load_dilemma_set("content/dilemma_sets", st.session_state.selected_set)
    dilemma = get_current_dilemma(dilemmas)

    if dilemma is None:
        st.session_state.screen = "silence"
        st.rerun()

    action, result = render_dilemma(dilemma)

    if action == "answer" and result is not None:
        save_answer(dilemma, result)

        last_answer = [st.session_state.answers[-1]]
        st.session_state.mirror_data = build_mirror_data(last_answer, sages)

        st.session_state.last_dilemma_completed = is_last_dilemma(dilemmas)
        st.session_state.screen = "mirror"
        st.rerun()

    elif action == "end":
        reset_session()
        st.rerun()

elif screen == "mirror":
    action = render_mirror(st.session_state.mirror_data)

    if action == "next":
        if st.session_state.last_dilemma_completed:
            st.session_state.screen = "silence"
        else:
            go_to_next_dilemma()
            st.session_state.screen = "dilemma"
        st.rerun()

    elif action == "end":
        reset_session()
        st.rerun()

elif screen == "silence":
    if render_silence():
        reset_session()
        st.rerun()