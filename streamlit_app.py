def compute_iterations(a, x, use_fractions, number_of_iterations):
    rows = []
    current_mode = use_fractions
    switched_from_fraction_to_decimal = False

    if use_fractions:
        rows.append({"x": f"x0 = {x}"})
    else:
        rows.append({"x": f"x0 = {float(x):.14f}"})

    for k in range(1, number_of_iterations):
        if current_mode:
            x = Fraction(1, 2) * (x + a / x)

            if fraction_is_short_enough(x):
                rows.append({"x": f"x{k} = {x}"})
            else:
                rows.append({"x": f"x{k} ≈ {float(x):.14f}"})
                x = float(x)
                a = float(a)
                current_mode = False
                switched_from_fraction_to_decimal = True

        else:
            x = 0.5 * (x + a / x)

            if switched_from_fraction_to_decimal:
                rows.append({"x": f"x{k} ≈ {x:.14f}"})
            else:
                rows.append({"x": f"x{k} = {x:.14f}"})

    return rows
