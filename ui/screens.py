import streamlit as st


def render_welcome():
    st.title("Moje granice odpowiedzialności")
    st.caption("aplikacja edukacyjno-refleksyjna")
    st.caption("pierwszy moduł systemu mentorskiego")

    st.markdown(
        """
        Czy zdarza Ci się pomyśleć, że zrobiłeś coś zbyt szybko?  
        Powiedziałeś coś, czego nie da się już cofnąć?

        To nie jest test.  
        To nie są cudze badania.  
        To chwila, w której możesz spokojniej przyjrzeć się własnym wyborom.
        """
    )

    return st.button("wejdź")

def render_manifest(manifesto):
    st.title(manifesto["title"])
    st.subheader(manifesto["subtitle"])

    for paragraph in manifesto["paragraphs"]:
        st.markdown(paragraph)

    return st.button("czytaj dalej")

def render_set_selector(set_files):
    st.title("Która z tych sytuacji jest Ci dziś najbliższa?")

    set_map = {
        "podstawowe.yaml": "Codzienne granice odpowiedzialności",
        "slad.yaml": "Silny stres, milczenie i odpowiedź",
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

    if st.button("otwórz ten obszar"):
        return reverse_map[selected_label]

    return None

def render_dilemma(dilemma):
    st.title(dilemma["title"])
    st.caption(f"Oś: {dilemma['axis_left']} ↔ {dilemma['axis_right']}")

    st.markdown(
        """
        Przed Tobą jeden z sześciu dylematów.  
        Zaznacz, gdzie jest Ci dziś bliżej.  
        Skala nie ocenia. Pomaga tylko zobaczyć kierunek.
        """
    )

    st.markdown("---")
    st.markdown(dilemma["scenario"])
    st.markdown(f"**{dilemma['choice_prompt']}**")    

    choice_value = st.slider(
        f"{dilemma['axis_left']} ↔ {dilemma['axis_right']}",
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

    if st.button("zobacz lustro"):
        return {
            "choice_value": choice_value,
            "cost_reflection": cost_reflection,
        }

    return None

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
            st.markdown("### Głos obok")
            st.info(item["sage_comment"])

        st.markdown("---")

    return st.button("zamknij")


def render_silence():
    st.markdown("## ")
    st.markdown(
        """
        Zostaw to ze sobą.

        Nie wszystko domaga się natychmiastowej odpowiedzi.
        """
    )

    return st.button("wróć do początku")