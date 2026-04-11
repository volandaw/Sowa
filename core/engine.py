import streamlit as st


def get_current_dilemma(dilemmas_data):
    dilemmas = dilemmas_data.get("dilemmas", [])
    idx = st.session_state.current_dilemma_index

    if 0 <= idx < len(dilemmas):
        return dilemmas[idx]
    return None


def save_answer(dilemma, answer):
    st.session_state.answers.append(
        {
            "dilemma_id": dilemma["id"],
            "axis_id": dilemma["axis_id"],
            "axis_left": dilemma["axis_left"],
            "axis_right": dilemma["axis_right"],
            "choice_value": answer["choice_value"],
            "cost_reflection": answer.get("cost_reflection", ""),
            "hidden_cost_left": dilemma.get("hidden_cost_left", ""),
            "hidden_cost_right": dilemma.get("hidden_cost_right", ""),
            "bias_warning_left": dilemma.get("bias_warning_left", ""),
            "bias_warning_right": dilemma.get("bias_warning_right", ""),
            "mentor_prompt": dilemma.get("mentor_prompt", ""),
            "mirror_line_left": dilemma.get("mirror_line_left", ""),
            "mirror_line_right": dilemma.get("mirror_line_right", ""),
        }
    )


def go_to_next_dilemma():
    st.session_state.current_dilemma_index += 1


def is_last_dilemma(dilemmas_data):
    dilemmas = dilemmas_data.get("dilemmas", [])
    return st.session_state.current_dilemma_index >= len(dilemmas) - 1


def build_mirror_data(answers, sages):
    if not answers:
        return None

    summary = []

    for answer in answers:
        axis_id = answer["axis_id"]
        score = answer["choice_value"]

        if score < 0:
            tendency = f"Bliżej Ci dziś ku biegunowi: {answer['axis_left']}."
            hidden_cost = answer["hidden_cost_left"]
            bias_warning = answer["bias_warning_left"]
            mirror_line = answer.get("mirror_line_left", "")
        elif score > 0:
            tendency = f"Bliżej Ci dziś ku biegunowi: {answer['axis_right']}."
            hidden_cost = answer["hidden_cost_right"]
            bias_warning = answer["bias_warning_right"]
            mirror_line = answer.get("mirror_line_right", "")
        else:
            tendency = "Pozostajesz dziś w samym środku napięcia, bez łatwego rozstrzygnięcia."
            hidden_cost = "Być może chronisz obie wartości, ale żadnej nie da się ocalić bez kosztu."
            bias_warning = "Czy zawieszenie decyzji nie jest także formą wyboru?"
            mirror_line = ""

        sage_comment = sages.get(axis_id, {}).get("default_comment", "")

        summary.append(
            {
                "axis_id": axis_id,
                "axis_label": f"{answer['axis_left']} ↔ {answer['axis_right']}",
                "tendency": tendency,
                "hidden_cost": hidden_cost,
                "bias_warning": bias_warning,
                "mentor_prompt": answer["mentor_prompt"],
                "sage_comment": sage_comment,
                "cost_reflection": answer["cost_reflection"],
                "mirror_line": mirror_line,
            }
        )

    return {"summary": summary}