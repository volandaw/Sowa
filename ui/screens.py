import html
import streamlit as st


def render_welcome():
    st.title("Moje granice odpowiedzialności")
    st.caption("aplikacja edukacyjno-refleksyjna")
    st.markdown('<div class="welcome-accent-line"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="welcome-intro">
            W świecie, który przyspiesza, człowiek coraz częściej działa odruchowo — pod wpływem presji, emocji, zmęczenia albo lęku.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="welcome-motto">
            Ta aplikacja powstała po to, by odzyskać choćby chwilę namysłu między bodźcem a reakcją.<br>
            Nie po to, by oceniać. Po to, by nie być obojętnym.
        </div>
        """,
        unsafe_allow_html=True
    )

    return st.button("Rozpocznij")


def render_manifest(manifesto):
    st.title(manifesto["title"])
    st.subheader(manifesto["subtitle"])

    for paragraph in manifesto["paragraphs"]:
        st.markdown(paragraph)

    return st.button("Przejdź dalej")


def render_set_selector(set_files):
    st.title("Która z tych sytuacji jest Ci dziś najbliższa?")

    set_map = {
        "podstawowe.yaml": "Codzienne granice odpowiedzialności",
        "slad.yaml": "Silny stres, milczenie i odpowiedź",
        "szkola.yaml": "Hejt w szkole",
    }
    options = [set_map.get(name, name) for name in set_files]
    reverse_map = {set_map.get(name, name): name for name in set_files}

    selected_label = st.radio(
        "Wybierz obszar, który najmocniej dotyka dziś Twojej uwagi:",
        options=options,
        index=0
    )

    st.markdown(
        """
        Każdy obszar dotyka innego rodzaju napięcia.  
        Wybierz ten, który jest Ci dziś najbliższy.
        """
    )

    if st.button("Wybieram ten obszar"):
        return "select", reverse_map[selected_label]

    if st.button("Zakończ teraz"):
        return "end", None

    return None, None


def render_dilemma(dilemma):
    accent_index = st.session_state.get("current_dilemma_index", 0) % 6
    safe_title = html.escape(dilemma["title"])
    safe_axis_left = html.escape(dilemma["axis_left"])
    safe_axis_right = html.escape(dilemma["axis_right"])
    safe_scenario = html.escape(dilemma["scenario"])

    st.markdown(
        f"""
        <div class="dilemma-accent-{accent_index}">
            <h1>{safe_title}</h1>
            <div class="dilemma-title-line dilemma-accent-{accent_index}"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(f"Oś: {dilemma['axis_left']} ↔ {dilemma['axis_right']}")

    st.markdown(
        """
        Przed Tobą jeden z sześciu dylematów.  
        Zaznacz, gdzie jest Ci dziś bliżej.  
        Skala nie ocenia. Pomaga tylko zobaczyć kierunek.
        """
    )

    st.markdown(
        f"""
        <div class="dilemma-box dilemma-accent-{accent_index}">
            {safe_scenario}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"**{dilemma['choice_prompt']}**")

    choice_value = st.slider(
        f"{safe_axis_left} ↔ {safe_axis_right}",
        min_value=-2,
        max_value=2,
        value=0,
        step=1
    )

    cost_reflection = st.text_area(
        dilemma["cost_question"],
        placeholder="Jeśli chcesz, zostaw krótką notatkę dla siebie. Co w tej sytuacji porusza Cię najmocniej? Możesz też zostawić puste.",
        height=120
    )

    if st.button("Zobacz odbicie"):
        return "answer", {
            "choice_value": choice_value,
            "cost_reflection": cost_reflection,
        }

    if st.button("Zakończ teraz"):
        return "end", None

    return None, None


def render_mirror(mirror_data):
    st.title("Lustro")

    for item in mirror_data["summary"]:
        st.markdown(f"## {item['axis_label']}")

        st.markdown("### Rozpoznanie")
        st.markdown(item["tendency"])

        st.markdown("### Cena")
        st.markdown(item["hidden_cost"])

        if item.get("mirror_line"):
            st.markdown(item["mirror_line"])

        st.markdown("### Łagodne ostrzeżenie")
        st.markdown(item["bias_warning"])

        st.markdown("### Pytanie")
        st.markdown(item["mentor_prompt"])

        if item.get("cost_reflection"):
            st.markdown("### Twój zapis")
            st.markdown(item["cost_reflection"])

        if item.get("sage_comment"):
            st.markdown("### Co powiedziałaby Sowa?")
            st.info(item["sage_comment"])

        if item.get("help_hint"):
            st.markdown("### Dalej")
            st.markdown(item["help_hint"])

        st.markdown("---")

    if st.button("Idź dalej"):
        return "next"

    if st.button("Zakończ teraz"):
        return "end"

    return None


def render_silence():
    st.markdown("## ")
    st.markdown(
        """
        Zostaw to ze sobą.

        Nie wszystko domaga się natychmiastowej odpowiedzi.
        """
    )

    return st.button("Wróć na początek")