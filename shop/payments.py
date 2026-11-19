"""A stub payments client. Real calls are out of scope for the demo."""


class PaymentsClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key

    def charge(self, amount_cents: int) -> dict[str, object]:
        return {"status": "ok", "amount_cents": amount_cents}
