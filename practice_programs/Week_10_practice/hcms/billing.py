def calculate_bill(consult, meds, tax = 0.05):
    if consult < 0 or meds < 0:
        raise ValueError("Negative costs")
    return (consult + meds) * (1 + tax)