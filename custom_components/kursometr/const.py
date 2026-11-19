"""Константы интеграции Курсометр."""

from __future__ import annotations

DOMAIN = "kursometr"
CONF_CURRENCY = "currency"

CBR_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"

DEFAULT_SCAN_INTERVAL = 3600
MIN_SCAN_INTERVAL = 10
MAX_SCAN_INTERVAL = 86400

PLATFORMS = ["sensor"]

ATTR_CURRENCY = "currency"
ATTR_NAME = "currency_name"
ATTR_NOMINAL = "nominal"
ATTR_VALUE = "official_rate"
ATTR_DATE = "date"
