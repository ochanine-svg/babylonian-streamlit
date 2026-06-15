import streamlit as st
from fractions import Fraction
import math

st.markdown("""
<style>


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

[data-testid="stSlider"] [role="slider"] {
    background-color: #2ecc71 !important;
    border-color: #2ecc71 !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #2ecc71 !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
    background-color: #2ecc71 !important;
}

[data-testid="stDataFrame"] * {
    font-size: 18px !important;
}
</style>
""", unsafe_allow_html=True)



a_string = st.text_input("Enter a positive number $a$", value="5")

x0_string = st.text_input(
    "Enter an initial guess for the square root of $a$",
    value="5/2"
)

st.markdown(
    """
    <p style="font-size:18px;">
    (Try both a close guess and a terrible guess to see fast convergence.)
    </p>
    """,
    unsafe_allow_html=True,
)

st.write("This app repeatedly updates the value of $x$ using")

st.latex(r"\frac12\left(x+\frac{a}{x}\right)")

number_of_iterations = st.slider("Number of iterations", 1, 50, 5)

st.markdown(
    """
    <p style="font-size:20px; font-weight:bold;">
    Results appear below. You can adjust the adjust the slider for more rows of results.
    </p>
    """,
    unsafe_allow_html=True,
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
                        "exact value": "fraction now too long to display",
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

st.table(
    rows
)



st.subheader("Check")

st.write(f"$\\sqrt{{a}} \\approx {math.sqrt(float(a)):.14f}$")
