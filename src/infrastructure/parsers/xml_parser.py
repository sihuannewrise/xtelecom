from __future__ import annotations

import xml.etree.ElementTree as ET

from .schemas import ChargeEntrySchema, ChargesFile


_SKIP_TAGS = {"ctn", "ban", "ben", "periodStartDate", "periodEndDate",
              "offerDescription"}


def _entry_to_dict(el: ET.Element) -> dict:
    data: dict = {}
    for child in el:
        tag = child.tag
        text = (child.text or "").strip()
        if not text:
            continue
        if tag in _SKIP_TAGS:
            data[tag] = text
        else:
            # числовые поля — snake_case
            data[tag] = text
    return data


class XmlChargesParser:
    """Парсер исходного XML-формата (детализация оператора)."""

    source_type = "xml"

    def parse(self, content: bytes) -> ChargesFile:
        root = ET.fromstring(content)
        entries: list[ChargeEntrySchema] = []
        summary: ChargeEntrySchema | None = None

        for el in root.findall("entry"):
            data = _entry_to_dict(el)

            # алиасы тегов -> имена полей Pydantic
            mapped = {
                "ctn": data.get("ctn"),
                "ban": data.get("ban"),
                "ben": data.get("ben"),
                "period_start_date": data.get("periodStartDate"),
                "period_end_date": data.get("periodEndDate"),
                "offer_description": data.get("offerDescription"),
            }
            for f in (
                "usagIntlActvAmt", "usagNationalActvAmt", "usagAirActvAmt",
                "usagSmsActvAmt", "usagGprsActvAmt",
                "iromLocalActvAmt", "iromSmsActvAmt", "iromGprsActvAmt",
                "iromServerActvAmt",
                "nromLocalActvAmt", "nromSmsActvAmt", "nromGprsActvAmt",
                "nromServerActvAmt",
                "rcPpActvAmt", "rcSocActvAmt", "discActvAmt",
                "ocOtPrice", "latepym",
                "subtotalAmount", "trsLoRcUcAmt", "trsLoOcAmt",
                "vat", "totalAmount",
            ):
                if f in data:
                    # camelCase -> snake_case
                    snake = "".join(
                        ("_" + ch.lower()) if ch.isupper() else ch for ch in f
                    )
                    mapped[snake] = data[f]

            entry = ChargeEntrySchema.model_validate(mapped)
            if entry.ctn:
                entries.append(entry)
            else:
                summary = entry

        return ChargesFile(
            source_type=self.source_type, entries=entries, summary=summary
        )
