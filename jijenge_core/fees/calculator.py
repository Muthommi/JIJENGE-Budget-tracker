import json
from pathlib import Path
from typing import Optional

def load_tariffs(path: Optional[str] = None):
    if path is None:
        path = Path(__file__).resolve().parents[0] / "tariffs.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

class FeeCalculator:
    def __init__(self, tariffs=None):
        self.tariffs = tariffs or load tariffs()

    def calc_fee(self, amount_ksh: float, channel: str):
        try:
            amount = float(amount_ksh)
        except Exception:
            return None
        channel = (channel or "").lower()
        for band in self.tariffs:
            if band.get("channel") == channel and amount >= band.get("min", -1) and amount <= band.get("max", float('inf')):
                return float(band.get("fee", 0.0))
        return None
