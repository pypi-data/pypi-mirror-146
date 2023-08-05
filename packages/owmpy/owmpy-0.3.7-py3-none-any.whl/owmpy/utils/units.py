from typing import NamedTuple as _NamedTuple
from ._classes import Number, ShortLong


class Units(_NamedTuple):
    temp: ShortLong = ShortLong("K", "Kelvin")
    speed: ShortLong = ShortLong("m/s", "meter/sec")
    api_name: str = "standard"

    time = ("unix", "UTC")
    pressure = "hPa"
    cloudiness = "%"
    precipitation = ShortLong("mm", "millimeters")
    degrees = ShortLong("°", "degrees (meteorological)")


class StandardUnits:
    STANDARD = Units()
    METRIC = Units(temp=ShortLong("°C", "Celsius"), api_name="metric")
    IMPERIAL = Units(temp=ShortLong("°F", "Fahrenheit"), speed=ShortLong("mph", "miles/hour"), api_name="imperial")


def convert_temp(temp: Number, __from: Units = StandardUnits.STANDARD, __to: Units = StandardUnits.IMPERIAL) -> Number:
    """Converts temperature between different units, with up to six significant digits"""
    if __from == __to:
        return temp

    match (__from, __to):
        case (StandardUnits.STANDARD, StandardUnits.METRIC):
            return temp - 273.15
        case (StandardUnits.STANDARD, StandardUnits.IMPERIAL):
            return 1.8 * temp - 459.67
        case (StandardUnits.METRIC, StandardUnits.STANDARD):
            return temp + 273.15
        case (StandardUnits.METRIC, StandardUnits.IMPERIAL):
            return 1.8 * temp + 32
        case (StandardUnits.IMPERIAL, StandardUnits.STANDARD):
            return temp / 1.8 + 255.372222
        case (StandardUnits.IMPERIAL, StandardUnits.METRIC):
            return (temp - 32) / 1.8
        case _:
            raise NotImplementedError(
                f"Conversion between types '{__from.__class__}' and '{__to.__class__}' is not defined"
            )


_MPS_PER_MPH = 0.44704


def convert_speed(
    speed: Number, __from: Units = StandardUnits.STANDARD, __to: Units = StandardUnits.IMPERIAL
) -> Number:
    if __from in {StandardUnits.STANDARD, StandardUnits.METRIC} and __to in {
        StandardUnits.STANDARD,
        StandardUnits.METRIC,
    }:
        return speed

    match (__from, __to):
        case (StandardUnits.STANDARD | StandardUnits.METRIC, StandardUnits.IMPERIAL):
            return speed / _MPS_PER_MPH
        case (StandardUnits.IMPERIAL, StandardUnits.STANDARD | StandardUnits.METRIC):
            return _MPS_PER_MPH * speed
        case _:
            raise NotImplementedError(
                f"Conversion between types '{__from.__class__}' and '{__to.__class__}' is not defined"
            )
