from scapy.all import AsyncSniffer, TCP
from typing import Optional

import struct
import threading
import time

PORT = 32800
BPF_FILTER = f"tcp port {PORT}"
BUF_LOCK = threading.Lock()
buffer = b""

def parse_channel_from_packet(data: bytes) -> Optional[int]:
    if not data.startswith(b'TOZ '):
        return None
    payload = data[8:]
    L = len(payload)
    i = 0
    while i + 11 <= L:
        try:
            name_len = int.from_bytes(payload[i:i+4], "little")
            name = payload[i+4:i+4+name_len].decode("ascii")
            if name == "Channel":
                cur = i + 4 + name_len
                type_tag = payload[cur]
                val_len = int.from_bytes(payload[cur+1:cur+5], "little")
                if type_tag == 2 and 0 < val_len < 9999:
                    return val_len
        except:
            pass
        i += 1
    return None

def process_buffer():
    global buffer
    with BUF_LOCK:
        buf = buffer
        idx = buf.find(b"TOZ ")
        while idx >= 0 and idx + 8 <= len(buf):
            size = int.from_bytes(buf[idx+4:idx+8], "little")
            if idx + 8 + size > len(buf): break
            blob = buf[idx:idx+8+size]
            buffer = buf = buf[idx+8+size:]
            ch = parse_channel_from_packet(blob)
            if ch:
                ts = time.strftime('%H:%M:%S')
                print(f"[{ts}] ✅ 你目前在頻道：CH{ch}")
            idx = buf.find(b"TOZ ")
        buffer = buf

def handle_packet(pkt):
    global buffer
    if TCP in pkt:
        with BUF_LOCK:
            buffer += bytes(pkt[TCP].payload)
        process_buffer()

if __name__ == "__main__":
    print("📡 正在監聽 TCP 32800，等待頻道封包出現...")
    sniffer = AsyncSniffer(filter=BPF_FILTER, prn=handle_packet, store=False)
    sniffer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 已手動中止偵測")
