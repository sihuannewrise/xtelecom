from litestar import Controller, post
from litestar.datastructures import UploadFile
from litestar.params import Parameter

from src.application.services.import_charges import ImportChargesService
from src.infrastructure.parsers.factory import get_parser


class ChargesController(Controller):
    path = "/charges"

    @post("/import")
    async def import_file(
        self,
        data: UploadFile,
        import_service: ImportChargesService,
        source_type: str = Parameter(query="source_type", default="xlsx_calls"),
    ) -> dict:
        content = await data.read()
        payload = get_parser(source_type).parse(content)
        report_id = await import_service.import_file(payload, source_file=data.filename)
        return {"report_id": report_id, "source_type": source_type}
