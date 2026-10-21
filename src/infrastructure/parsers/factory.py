from .base import ChargesParser
from .xlsx_calls_parser import XlsxCallsParser
from .xml_parser import XmlChargesParser


_PARSERS: dict[str, type] = {
    "xml": XmlChargesParser,
    "xlsx_calls": XlsxCallsParser,
}


def get_parser(source_type: str) -> ChargesParser:
    parser_cls = _PARSERS.get(source_type.lower())
    if parser_cls is None:
        raise ValueError(f"Неподдерживаемый формат источника: {source_type}")
    return parser_cls()


def available_sources() -> list[str]:
    return sorted(_PARSERS)