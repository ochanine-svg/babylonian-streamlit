import streamlit as st
from fractions import Fraction
import math
import pandas as pd

st.markdown("""
<style>
[data-testid="stSlider"] [role="slider"] {
    background-color: #2ecc71 !important;
    border-color: #2ecc71 !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] [data-testid="stThumbValue"] *,
[data-testid="stSlider"] div[class*="ThumbValue"],
[data-testid="stSlider"] div[class*="thumbValue"] {
    display: none !important;
    visibility: hidden !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

html, body, [class*="css"] {
    font-family: 'Merriweather', serif;
    font-size: 18px;
}

.stTextInput input {
    font-size: 18px !important;
}

[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p {
    font-size: 18px !important;
}

[data-testid="stSlider"] label,
[data-testid="stSlider"] label p {
    font-size: 18px !important;
}

[data-testid="stDataFrame"] * {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)


st.write("This app computes successive updates of the value of $x$ using")

st.latex(r"\frac12\left(x+\frac{a}{x}\right)")

st.write("The value of $x$ converges fast to $\sqrt{a}$.")


a_string = st.text_input("Enter a positive number $a$", value="5")

x0_string = st.text_input(
    "Enter a positive initial guess for the square root of $a$. This is the initial value of $x$.",
    value="100"
)

st.markdown(
    """
    <p style="font-size:20px; font-weight:bold;">
    Results below.
    </p>
    """,
    unsafe_allow_html=True,
)

number_of_iterations = st.slider("# rows", 1, 50, 11)


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

    first_row = {
        "n": 0,
        "decimal approximation": f"{float(x):.14f}",
    }

    if use_fractions:
        first_row["exact value"] = str(x)

    rows.append(first_row)

    for k in range(1, number_of_iterations):
        if current_mode:
            x = Fraction(1, 2) * (x + a / x)

            row = {
                "n": k,
                "decimal approximation": f"{float(x):.14f}",
            }

            if fraction_is_short_enough(x):
                row["exact value"] = str(x)
            else:
                x = float(x)
                a = float(a)
                current_mode = False
                row["exact value"] = "too long to display"

            rows.append(row)

        else:
            x = 0.5 * (x + a / x)

            row = {
                "n": k,
                "decimal approximation": f"{x:.14f}",
            }

            if use_fractions:
                row["exact value"] = ""

            rows.append(row)

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

df = pd.DataFrame(rows)

if use_fractions:
    st.markdown(
        """
        <p style="font-size:18px;">
        Exact values are shown when they are not too long to display.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "n": st.column_config.NumberColumn("n", width="small"),
            "decimal approximation": st.column_config.TextColumn("decimal approximation", width="medium"),
            "exact value": st.column_config.TextColumn("exact value", width="large"),
        },
    )
else:
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "n": st.column_config.NumberColumn("n", width="small"),
            "decimal approximation": st.column_config.TextColumn("decimal approximation", width="medium"),
        },
    )

st.subheader("Check")

st.write(f"$\\sqrt{{a}} \\approx {math.sqrt(float(a)):.14f}$")
