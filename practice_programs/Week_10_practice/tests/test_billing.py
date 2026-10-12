import pytest
import coverage
from hcms.billing import calculate_bill

def test_normal_case():
    assert calculate_bill(100, 50) == 157.5 
    
@pytest.mark.parametrize("consult, meds, tax, expected", [
    (100, 0, 0.00, 100.0),
    (80, 20, 0.05, 105.0),
])
def test_parameterized(consult, meds, tax, expected):
    assert calculate_bill(consult, meds, tax) == expected

def test_raise_on_negative():
    with pytest.raises(ValueError):
        calculate_bill(-1, 50)