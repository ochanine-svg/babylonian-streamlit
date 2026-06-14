import streamlit as st
from fractions import Fraction
import math

st.set_page_config(page_title="Babylonian Square Root", page_icon="√")

st.title("Babylonian Method for Square Roots")

st.write(
    "Enter a positive number $a$ and a positive starting guess $x_0$. "
    "The app computes iterations of"
)

st.latex(r"x_{n+1}=\frac12\left(x_n+\frac{a}{x_n}\right)")

st.write("The sequence should approach $\\sqrt{a}$.")


def fraction_is_short_enough(frac, max_chars=60):
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

            # Fraction mode is still possible.
            return a, True, None

        a_float = float(a_string)

        if a_float <= 0:
            return None, None, "a has to be positive."

        if a_float.is_integer():
            # Treat whole-number inputs exactly.
            return Fraction(int(a_float)), True, None

        # Decimal a forces decimal mode.
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
                        "exact value": str(x),
                        "decimal approximation": f"{float(x):.14f}",
                        "mode": "fraction",
                    }
                )
            else:
                x = float(x)
                a = float(a)
                current_mode = False
                rows.append(
                    {
                        "n": k,
                        "exact value": 
                        "decimal approximation": f"{x:.14f}",
                        "mode": "switched to decimal",
                    }
                )

        else:
            x = 0.5 * (x + a / x)
            rows.append(
                {
                    "n": k,
                    "exact value": "",
                    "decimal approximation": f"{x:.14f}",
                    "mode": "decimal",
                }
            )

    return rows

with st.sidebar:
    st.header("Inputs")
    a_string = st.text_input("a", value="5")
    x0_string = st.text_input("x0", value="5/2")
    number_of_iterations = st.slider("Number of iterations", 1, 50, 10)
    

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

if use_fractions:
    st.info("Treating a and x0 as fractions.")
else:
    st.info("Using decimal/float mode.")

rows = compute_iterations(
    a,
    x0,
    use_fractions,
    number_of_iterations,
    
)

st.subheader("Iterations")

phone_friendly = st.checkbox("Phone-friendly display. ", value=True)

if phone_friendly:
    for row in rows:
        st.markdown(f"**x_{row['n']}**")

        if row["exact value"]:
            st.write("Exact value:")
            st.code(row["exact value"])

        st.write(f"Decimal approximation: `{row['decimal approximation']}`")
        st.caption(f"Mode: {row['mode']}")
        st.divider()

else:
    st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        column_config={
            "exact value": st.column_config.TextColumn(
                "exact value",
                width=350,
            ),
        },
    )

st.subheader("Check")
st.write(f"Decimal value of $\\sqrt{{a}}$: `{math.sqrt(float(a)):.14f}`")
