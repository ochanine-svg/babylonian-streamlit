import streamlit as st
from fractions import Fraction
import math

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Merriweather', serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="Babylonian Square Root", page_icon="√")

st.title("The Babylonian Method")



a_string = st.text_input("Enter a positive number a", value="5")
x0_string = st.text_input("Enter a positive starting guess x0 for the square root of $a$", value="5/2")
number_of_iterations = st.slider("Number of iterations", 1, 50, 5)

st. write("This app repeatedly updates the value of x with the value of ")



st.latex(r"\frac12\left(x+\frac{a}{x}\right)")

st.write(
    "Try both a close starting guess and a far starting guess for $x_0$. "
    "Notice how rapidly the sequence approaches $\\sqrt{a}$."
)




def fraction_is_short_enough(frac, max_chars=50):
    return len(str(frac)) <= max_chars


def parse_a(a_string):
    a_string = a_string.strip()

    if not a_string:
        return None, None, "Enter a value for a."

    try:
        if "/" in a_string:
            a = Fraction(a_string)

            if a <= 0:
                return None, None, "a has to be positive."

            return a, True, None

        a_float = float(a_string)

        if a_float <= 0:
            return None, None, "a has to be positive."

        if a_float.is_integer():
            return Fraction(int(a_float)), True, None

        return a_float, False, None

    except ValueError:
        return None, None, "That was not a valid number."

    except ZeroDivisionError:
        return None, None, "A fraction cannot have 0 in the denominator."


def parse_x0(x0_string, force_float_mode):
    x0_string = x0_string.strip()

    if not x0_string:
        return None, None, "Enter a value for x0."

    try:
        if force_float_mode:
            if "/" in x0_string:
                x0 = float(Fraction(x0_string))
            else:
                x0 = float(x0_string)

            if x0 <= 0:
                return None, None, "x0 has to be positive."

            return x0, False, None

        if "/" in x0_string:
            x0 = Fraction(x0_string)

            if x0 <= 0:
                return None, None, "x0 has to be positive."

            return x0, True, None

        x0_float = float(x0_string)

        if x0_float <= 0:
            return None, None, "x0 has to be positive."

        if x0_float.is_integer():
            return Fraction(int(x0_float)), True, None

        return x0_float, False, None

    except ValueError:
        return None, None, "That was not a valid number."

    except ZeroDivisionError:
        return None, None, "A fraction cannot have 0 in the denominator."


def compute_iterations(a, x, use_fractions, number_of_iterations):
    rows = []
    current_mode = use_fractions

    for k in range(1, number_of_iterations + 1):
        if current_mode:
            x = Fraction(1, 2) * (x + a / x)

            if fraction_is_short_enough(x):
                rows.append(
                    {
                        "n": k,
                        "decimal approximation": f"{float(x):.14f}",
                        "exact value": str(x),
                    }
                )
            else:
                x = float(x)
                a = float(a)
                current_mode = False
                rows.append(
                    {
                        "n": k,
                        "decimal approximation": f"{x:.14f}",
                        "exact value": "fraction too long to display",
                    }
                )

        else:
            x = 0.5 * (x + a / x)
            rows.append(
                {
                    "n": k,
                    "decimal approximation": f"{x:.14f}",
                    "exact value": "",
                }
            )

    return rows


a, a_can_use_fractions, a_error = parse_a(a_string)

if a_error:
    st.error(a_error)
    st.stop()

x0, x0_can_use_fractions, x0_error = parse_x0(
    x0_string,
    force_float_mode=not a_can_use_fractions,
)

if x0_error:
    st.error(x0_error)
    st.stop()

use_fractions = a_can_use_fractions and x0_can_use_fractions

rows = compute_iterations(
    a,
    x0,
    use_fractions,
    number_of_iterations,
)

st.subheader("Iterations")

st.dataframe(
    rows,
    hide_index=True,
    use_container_width=True,
    column_config={
        "n": st.column_config.NumberColumn("n", width=20),
        "decimal approximation": st.column_config.TextColumn(
            "decimal approximation",
            width=150,
        ),
        "exact value": st.column_config.TextColumn(
            "exact value",
            width="large",
        ),
    },
)

st.subheader("Check")

st.write(f"$\\sqrt{{a}} \\approx {math.sqrt(float(a)):.14f}$")


