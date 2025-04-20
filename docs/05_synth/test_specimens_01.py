import pytest
from params_01 import SpecimenParams
from specimens_01 import AllSnails


@pytest.mark.xfail
def test_defaults():
    params = SpecimenParams()
    fixture = AllSnails.generate(params, 3)
    assert all(len(s.genome) == params.genome_length for s in fixture.samples)
