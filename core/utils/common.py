import json

def encode_data(data: dict) -> bytes:
    return json.dumps(data).encode("utf-8")

def decode_data(data: bytes) -> dict:
    return json.loads(data.decode("utf-8"))
