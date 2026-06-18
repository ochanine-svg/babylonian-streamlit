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

/* Reduce Streamlit's built-in top and bottom page padding */
.block-container,
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"] {
    padding-top: 0.25rem !important;
    padding-bottom: 0.25rem !important;
}

/* Remove extra space caused by hidden header */
[data-testid="stHeader"] {
    display: none !important;
    height: 0rem !important;
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
    value="100"
)

st.markdown("**Results below.**")

number_of_iterations = st.slider("# rows", 1, 50, 9)


def parse_positive_number(input_string, variable_name):
    input_string = input_string.strip()

    if not input_string:
        return None, f"Enter a value for {variable_name}."

    try:
        if "/" in input_string:
            value = float(Fraction(input_string))
        else:
            value = float(input_string)

        if not math.isfinite(value):
            return None, f"{variable_name} has to be a finite number."

        if value <= 0:
            return None, f"{variable_name} has to be positive."

        return value, None

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


a, a_error = parse_positive_number(a_string, "a")

if a_error:
    st.error(a_error)
    st.stop()

x0, x0_error = parse_positive_number(x0_string, "x0")

if x0_error:
    st.error(x0_error)
    st.stop()


rows = compute_iterations(a, x0, number_of_iterations)


st.markdown("**x**")

for row in rows:
    st.write(row)


st.subheader("Check")

st.write(f"$\\sqrt{{a}} \\approx {math.sqrt(a):.14f}$")
