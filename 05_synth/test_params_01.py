import pytest
from params_01 import SpecimenParams


def test_not_defaults():
    fixture = SpecimenParams(
        mass_mean=20.0,
        mass_sd=0.3,
        genome_length=50,
        mut_mass_scale=3.0,
        mut_prob=0.01,
    )
    assert fixture.mass_mean == 20.0
    assert fixture.genome_length == 50
    assert fixture.mut_mass_scale == 3.0
    assert fixture.mass_sd == 0.3
    assert fixture.mut_prob == 0.01


def test_defaults():
    fixture = SpecimenParams()
    for name in SpecimenParams.model_fields:
        assert getattr(fixture, name) == SpecimenParams.model_fields[name].default


@pytest.mark.parametrize(
    ("name", "value"),
    (
        ("mass_mean", -1.0),
        ("mass_sd", -0.5),
        ("genome_length", "string"),
        ("mass_sd", [0.5]),
        ("mut_prob", 100.0),
    ),
)
def test_invalid(name, value):
    with pytest.raises(ValueError):
        SpecimenParams(**{name: value})
