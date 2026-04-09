import streamlit as st

from core.loader import load_manifesto, load_dilemmas, load_sages
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
    render_dilemma,
    render_mirror,
    render_silence,
)

st.set_page_config(
    page_title="Nowe granice odpowiedzialności",
    page_icon="🦉",
    layout="centered",
)

manifesto = load_manifesto("content/manifesto.yaml")
dilemmas = load_dilemmas("content/dilemmas.yaml")
sages = load_sages("content/sages.yaml")

init_session_state()

screen = st.session_state.screen

if screen == "welcome":
    if render_welcome():
        st.session_state.screen = "manifest"
        st.rerun()

elif screen == "manifest":
    if render_manifest(manifesto):
        st.session_state.screen = "dilemma"
        st.rerun()

elif screen == "dilemma":
    dilemma = get_current_dilemma(dilemmas)

    if dilemma is None:
        st.session_state.mirror_data = build_mirror_data(
            st.session_state.answers, sages
        )
        st.session_state.screen = "mirror"
        st.rerun()

    result = render_dilemma(dilemma)

    if result is not None:
        save_answer(dilemma, result)

        if is_last_dilemma(dilemmas):
            st.session_state.mirror_data = build_mirror_data(
                st.session_state.answers, sages
            )
            st.session_state.screen = "mirror"
        else:
            go_to_next_dilemma()

        st.rerun()

elif screen == "mirror":
    if render_mirror(st.session_state.mirror_data):
        st.session_state.screen = "silence"
        st.rerun()

elif screen == "silence":
    if render_silence():
        reset_session()
        st.rerun()