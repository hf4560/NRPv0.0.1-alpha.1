import asyncio
from core.utils.common import decode_data, encode_data
from core.crypto.hashing import identify_peer

async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info("peername")
    print(f"[QNode] Connection from {addr}")

    try:
        data = await reader.read(1024)
        if not data:
            return

        message = decode_data(data)
        peer_id = identify_peer(message.get("hash", ""))

        print(f"[QNode] Received from {peer_id}: {message}")
        response = {"status": "ok", "received": message}
        writer.write(encode_data(response))
        await writer.drain()

    except Exception as e:
        print(f"[Error] {e}")
    finally:
        writer.close()
        await writer.wait_closed()
