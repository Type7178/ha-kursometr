from unittest.mock import patch

import pytest

from custom_components.kursometr.api import CbrApi, CbrInvalidResponseError, CbrRates

PAYLOAD = {
    "Date": "2026-11-19T11:30:00+03:00",
    "Valute": {
        "USD": {
            "CharCode": "USD",
            "Nominal": 1,
            "Name": "Доллар США",
            "Value": 82.2281,
        },
        "JPY": {
            "CharCode": "JPY",
            "Nominal": 100,
            "Name": "Иен",
            "Value": 51.5246,
        },
        "BROKEN": {"CharCode": "BROKEN", "Nominal": 0, "Name": "Брак", "Value": 1},
    },
}


class FakeResponse:
    def raise_for_status(self):
        pass

    async def json(self, content_type=None):
        return PAYLOAD

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc_info):
        return False


class FakeSession:
    def get(self, *args, **kwargs):
        return FakeResponse()


def make_api():
    return CbrApi(FakeSession())


async def test_async_get_rates_normalizes_nominal():
    rates = await make_api().async_get_rates()

    assert isinstance(rates, CbrRates)
    assert rates.date == PAYLOAD["Date"]
    assert rates.currencies["USD"].rate == pytest.approx(82.2281)
    assert rates.currencies["JPY"].rate == pytest.approx(0.515246)
    assert rates.currencies["JPY"].nominal == 100
    assert rates.currencies["JPY"].value == pytest.approx(51.5246)
    assert "BROKEN" not in rates.currencies


async def test_async_get_currencies():
    assert await make_api().async_get_currencies() == {
        "USD": "Доллар США",
        "JPY": "Иен",
    }


async def test_missing_valute_raises():
    api = make_api()
    with patch.object(api, "async_get_payload", return_value={"Date": "x"}):
        with pytest.raises(CbrInvalidResponseError):
            await api.async_get_rates()
