import streamlit as st
from fractions import Fraction
import math


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

.result-row {
    font-size: 18px;
    margin-bottom: 0.25rem;
}
</style>
""", unsafe_allow_html=True)

st.write(r"Start with an initial guess for $\sqrt{a}$, which will be stored in a variable $x$.")
st.write("This app computes successive updates of the value of $x$ using")

st.latex(r"\frac12\left(x+\frac{a}{x}\right)")

st.write(r"The value of $x$ converges fast to $\sqrt{a}$.")


a_string = st.text_input("Enter a positive number $a$.", value="5")

x0_string = st.text_input(
    r"Enter a positive initial guess for $\sqrt{a}$.",
    value="3"
)

st.markdown(
    """
    <p style="font-size:20px; font-weight:bold;">
    Results below.
    </p>
    """,
    unsafe_allow_html=True,
)

number_of_iterations = st.slider("# rows", 1, 50, 6)


def parse_a(a_string):
    a_string = a_string.strip()

    if not a_string:
        return None, "Enter a value for a."

    try:
        if "/" in a_string:
            a = float(Fraction(a_string))
        else:
            a = float(a_string)

        if a <= 0:
            return None, "a has to be positive."

        return a, None

    except ValueError:
        return None, "That was not a valid number."

    except ZeroDivisionError:
        return None, "A fraction cannot have 0 in the denominator."


def parse_x0(x0_string):
    x0_string = x0_string.strip()

    if not x0_string:
        return None, "Enter a value for x0."

    try:
        if "/" in x0_string:
            x0 = float(Fraction(x0_string))
        else:
            x0 = float(x0_string)

        if x0 <= 0:
            return None, "x0 has to be positive."

        return x0, None

    except ValueError:
        return None, "That was not a valid number."

    except ZeroDivisionError:
        return None, "A fraction cannot have 0 in the denominator."


def compute_iterations(a, x, number_of_iterations):
    rows = []

    rows.append(f"x0 = {x:.14f}")

    for k in range(1, number_of_iterations):
        x = 0.5 * (x + a / x)
        rows.append(f"x{k} = {x:.14f}")

    return rows


a, a_error = parse_a(a_string)

if a_error:
    st.error(a_error)
    st.stop()

x0, x0_error = parse_x0(x0_string)

if x0_error:
    st.error(x0_error)
    st.stop()

rows = compute_iterations(
    a,
    x0,
    number_of_iterations,
)

st.markdown("**x**")

for row in rows:
    st.markdown(
        f"""
        <div class="result-row">
        {row}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.subheader("Check")

st.write(f"$\\sqrt{{a}} \\approx {math.sqrt(a):.14f}$")
