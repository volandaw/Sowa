import streamlit as st


def render_welcome():
    st.title("Nowe granice odpowiedzialności")
    st.caption("Zmieniają się czasy, zmienia się świat. Jak wyznaczać granice odpowiedzialności w zmiennej rzeczywistości, nie naruszając własnych wartości?")
    st.caption("aplikacja edukacyjno-refleksyjna")
    st.caption("pierwszy moduł systemu mentorskiego")

    st.markdown(
        """
        To nie jest test.  
        To nie jest ankieta.  
        To jest krótka przestrzeń rozeznania.
        """
    )

    return st.button("wejdź")


def render_manifest(manifesto):
    st.title(manifesto["title"])
    st.subheader(manifesto["subtitle"])

    for paragraph in manifesto["paragraphs"]:
        st.markdown(paragraph)

    return st.button("czytaj dalej")


def render_dilemma(dilemma):
    st.title(dilemma["title"])
    st.caption(f"Oś: {dilemma['axis_left']} ↔ {dilemma['axis_right']}")

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
        placeholder="Kilka słów dla siebie. Możesz też zostawić puste.",
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