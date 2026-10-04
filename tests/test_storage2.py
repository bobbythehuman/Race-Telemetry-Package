from types import SimpleNamespace

import pytest

from src.RaceTelemetry.storage import fetch, prepare


class TestPrepare:
    @pytest.mark.parametrize(
        ("text", "expected"),
        [
            ("speed", [["speed"]]),
            ("vehicle.speed", [["vehicle"], ["speed"]]),
            ("wheels[2].speed", [["wheels", 2], ["speed"]]),
            ("wheels[*].speed", [["wheels", "*"], ["speed"]]),
            ("telemetry[vehicle.gear].value", [["telemetry", [["vehicle"], ["gear"]]], ["value"]]),
        ],
    )
    def test_parses_supported_paths(self, text, expected):
        assert prepare(text) == expected

    @pytest.mark.parametrize(
        "text",
        [
            "",
            "speed-value",
            "wheels[",
            "wheels[2",
            "wheels[2].speed]",
            "speed..gear",
        ],
    )
    def test_rejects_invalid_paths(self, text):
        with pytest.raises(ValueError):
            prepare(text)


class TestFetch:
    def test_fetches_nested_attributes(self):
        root = SimpleNamespace(vehicle=SimpleNamespace(speed=123))

        assert fetch(root, prepare("vehicle.speed")) == 123

    def test_fetches_list_item_and_attribute(self):
        root = SimpleNamespace(wheels=[SimpleNamespace(speed=10), SimpleNamespace(speed=20)])

        assert fetch(root, prepare("wheels[1].speed")) == 20

    def test_resolves_dynamic_index_from_root(self):
        root = SimpleNamespace(
            currentWheel=1,
            wheels=[SimpleNamespace(speed=10), SimpleNamespace(speed=20)],
        )

        assert fetch(root, prepare("wheels[currentWheel].speed")) == 20

    def test_fetches_nested_dynamic_index_from_root(self):
        root = SimpleNamespace(
            selector=SimpleNamespace(wheel=0),
            wheels=[SimpleNamespace(speed=10), SimpleNamespace(speed=20)],
        )

        assert fetch(root, prepare("wheels[selector.wheel].speed")) == 10

    def test_wildcard_fetches_attribute_from_each_item(self):
        root = SimpleNamespace(
            wheels=[SimpleNamespace(speed=10), SimpleNamespace(speed=20), SimpleNamespace(speed=30)]
        )

        assert fetch(root, prepare("wheels[*].speed")) == [10, 20, 30]

    def test_wildcard_preserves_remaining_static_indices(self):
        root = SimpleNamespace(
            cars=[
                SimpleNamespace(wheels=[SimpleNamespace(speed=10), SimpleNamespace(speed=11)]),
                SimpleNamespace(wheels=[SimpleNamespace(speed=20), SimpleNamespace(speed=21)]),
            ]
        )

        assert fetch(root, prepare("cars[*].wheels[1].speed")) == [11, 21]

    def test_missing_attribute_returns_none(self):
        root = SimpleNamespace(vehicle=SimpleNamespace())

        assert fetch(root, prepare("vehicle.speed")) is None

    def test_negative_dynamic_index_raises(self):
        root = SimpleNamespace(currentWheel=-1, wheels=[SimpleNamespace(speed=10)])

        with pytest.raises(IndexError, match="Negative index -1"):
            fetch(root, prepare("wheels[currentWheel].speed"))