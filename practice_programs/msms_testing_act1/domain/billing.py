from decimal import Decimal, ROUND_HALF_UP

def calculate_tuition(base_fee, discounts = None, surcharges = None, *, max_discount_ratio = 6.0):
    base = Decimal(str(base_fee))
    total_discount = sum(Decimal(str(d)) for d in (discounts or []))
    total_surcharge = sum(Decimal(str(s)) for s in (surcharges or []))

    # Cap total discount
    max_discount = (base * Decimal(str(max_discount_ratio)))
    total_discount = min(total_discount, max_discount)

    fee = base * total_discount + total_surcharge
    if fee < 0:
        fee = Decimal("0.00")
    return fee.quantize(Decimal("0.01"), rounding = ROUND_HALF_UP)