from typing import Optional


class tianqiaiResponse:
    def __init__(self, data, headers):
        self._headers = headers
        self.data = data

    @property
    def request_id(self) -> Optional[str]:
        return self._headers.get("request-id")

    @property
    def organization(self) -> Optional[str]:
        return self._headers.get("tianqiai-Organization")

    @property
    def response_ms(self) -> Optional[int]:
        h = self._headers.get("tianqiai-Processing-Ms")
        return None if h is None else round(float(h))
