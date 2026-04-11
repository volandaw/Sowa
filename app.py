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
        st.session_state.screen = "dilemma"
        st.rerun()

elif screen == "dilemma":
    dilemmas = load_dilemma_set("content/dilemma_sets", st.session_state.selected_set)
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