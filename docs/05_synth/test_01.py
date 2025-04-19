import pytest

from synth_01 import SpecimenParams


def test_not_defaults():
    fixture = SpecimenParams(
        mean_mass=20.0,
        genome_length=50,
        mut_mass_scale=3.0,
        mass_rel_sd=0.3,
        p_mutation=0.01,
    )
    assert fixture.mean_mass == 20.0
    assert fixture.genome_length == 50
    assert fixture.mut_mass_scale == 3.0
    assert fixture.mass_rel_sd == 0.3
    assert fixture.p_mutation == 0.01


def test_defaults():
    fixture = SpecimenParams()
    for name in SpecimenParams.model_fields:
        assert getattr(fixture, name) == SpecimenParams.model_fields[name].default


@pytest.mark.parametrize(
    ("name", "value"),
    (
        ("mean_mass", -1.0),
        ("genome_length", "string"),
        ("mut_mass_scale", 0.5),
        ("mass_rel_sd", [0.5]),
        ("p_mutation", 100.0),
    ),
)
def test_invalid(name, value):
    with pytest.raises(ValueError):
        SpecimenParams(**{name: value})
