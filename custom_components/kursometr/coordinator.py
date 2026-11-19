"""Координатор обновления курсов."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import CbrApi, CbrApiError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclass
class RateData:
    rate: float
    name: str
    nominal: int
    value: float
    date: str


class KursometrCoordinator(DataUpdateCoordinator):
    def __init__(
        self,
        hass: HomeAssistant,
        api: CbrApi,
        currency: str,
        scan_interval: int,
    ):
        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN} {currency}",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api = api
        self.currency = currency

    async def _async_update_data(self) -> RateData:
        try:
            rates = await self.api.async_get_rates()
        except CbrApiError as err:
            raise UpdateFailed(str(err)) from err

        item = rates.currencies.get(self.currency)
        if item is None:
            raise UpdateFailed(f"ЦБ больше не публикует {self.currency}")

        return RateData(
            rate=item.rate,
            name=item.name,
            nominal=item.nominal,
            value=item.value,
            date=rates.date,
        )
