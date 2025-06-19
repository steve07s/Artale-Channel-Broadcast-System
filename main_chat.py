"""
MapleStory_Artale_Chat_Helper －－ 即時抓包 + 聊天數據解析（顯示完整欄位）
-------------------------------------------------
* LIVE_CAPTURE=True 時使用 Scapy AsyncSniffer 監聽 tcp/32800
* False 時改為離線解析選取的文字檔
"""

import re, struct, sys, time, threading
from pathlib import Path
from tkinter import filedialog, scrolledtext, Tk, Canvas, ttk

# ======== 基本設定 ========
LIVE_CAPTURE = True
PORT         = 32800
BPF_FILTER   = f"tcp port {PORT}"
BUF_LOCK     = threading.Lock()

if LIVE_CAPTURE:
    try:
        from scapy.all import AsyncSniffer, TCP
    except ImportError:
        sys.exit("❌ 尚未安裝 scapy，請先 pip install scapy")

# ======== 解析核心 ========

class ChatParser:
    KNOWN = {
        "Nickname", "Channel","Text", "Type", "ProfileCode", "UserId"
    }

    @staticmethod
    def _parse_struct(data: bytes) -> dict:
        out, colors = {}, []
        i, L = 0, len(data)
        MAX_VAL_LEN = 256  # 防止亂長 value 拖垮封包

        # --- 第一輪：處理所有欄位（除了 Channel） ---
        while i + 4 <= L:
            name_len = int.from_bytes(data[i:i+4], "little")
            if not 0 < name_len <= 64 or i + 4 + name_len + 6 > L:
                i += 1
                continue

            try:
                name = data[i+4:i+4+name_len].decode("ascii")
            except UnicodeDecodeError:
                i += 1
                continue

            cur = i + 4 + name_len
            type_tag = int.from_bytes(data[cur:cur+2], "little")
            val_len  = int.from_bytes(data[cur+2:cur+6], "little")
            v_start, v_end = cur + 6, cur + 6 + val_len

            # 非法長度 → 跳過
            if v_end > L or val_len > MAX_VAL_LEN:
                i += 1
                continue

            if name != "Channel":
                if name in ChatParser.KNOWN:
                    if type_tag == 4:
                        try:
                            out[name] = data[v_start:v_end].decode("utf-8", "replace")
                            if name == "UserId":
                                channel = int.from_bytes(data[v_end+1:v_end+3], "little")
                                out["Channel"] = f"CH{channel}"
                        except Exception:
                            out[name] = f"[INVALID UTF8]"
                elif name.startswith("#") and name_len == 7:
                    colors.append(name)

            i = v_end

        # 第二輪：只處理 Channel（type_tag 1 byte, value 為 CH編號）
        j = 0
        while j + 4 <= L:
            name_len = int.from_bytes(data[j:j+4], "little")
            if not 0 < name_len <= 64 or j + 4 + name_len + 5 > L:
                j += 1
                continue

            try:
                name = data[j+4:j+4+name_len].decode("ascii")
            except UnicodeDecodeError:
                j += 1
                continue
            
            j += 1

        if colors:
            out["color1"] = colors[0]
        if len(colors) > 1:
            out["color2"] = colors[1]

        # --- 剩餘 float32 ---
        floats = []
        k = max(i, j)
        while k + 4 <= L:
            floats.append(struct.unpack_from("<f", data, k)[0])
            k += 4
        out["floats"] = floats

        return out


    @classmethod
    def parse_packet_bytes(cls, blob: bytes) -> dict:
        return cls._parse_struct(blob[8:])      # 去掉 'TOZ ' + size

    @staticmethod
    def bytes_from_hex_file(path: Path) -> bytes:
        txt = path.read_text(encoding="utf-8", errors="ignore")
        return bytes.fromhex(re.sub(r"[^0-9A-Fa-f]", "", txt))

# ======== Tkinter GUI ========

class ChatGUI(Tk):
    def __init__(self):
        super().__init__()
        self.title("聊天數據解析 Sniffer")
        self.minsize(900, 600)

        # --- UI 上排 ---
        top = ttk.Frame(self); top.pack(fill="x", padx=8, pady=6)
        ttk.Button(top, text="📂 解析文字檔", command=self.open_file).pack(side="left")

        ttk.Label(top, text="  監聽狀態：").pack(side="left")
        self.light_can = Canvas(top, width=20, height=20, highlightthickness=0)
        self.light_id  = self.light_can.create_oval(2, 2, 18, 18, fill="red")
        self.light_can.pack(side="left")

        # --- 日誌 ---
        self.logbox = scrolledtext.ScrolledText(self, wrap="word",
                                                state="disabled",
                                                font=("Consolas", 10))
        self.logbox.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        # --- Sniffer / Buffer ---
        self.buffer  = b""
        self.sniffer = None
        if LIVE_CAPTURE:
            self.after(100, self.start_sniffer)

    # ---------- 離線模式 ----------
    def open_file(self):
        fp = filedialog.askopenfilename(
            title="選擇含十六進位字串的文字檔",
            filetypes=[("Text files", "*.txt *.log"), ("All files", "*.*")]
        )
        if not fp: return
        try:
            raw = ChatParser.bytes_from_hex_file(Path(fp))
            self._feed_bytes(raw)
            self.log(f"📖 已解析 {Path(fp).name}")
        except Exception as e:
            self.log(f"❌ 讀檔或解析失敗：{e}")

    # ---------- 即時抓包 ----------
    def start_sniffer(self):
        self.sniffer = AsyncSniffer(filter=BPF_FILTER, prn=self._on_packet, store=False)
        self.sniffer.start()
        self.light_can.itemconfig(self.light_id, fill="green")
        self.log(f"🟢 已啟動 Sniffer ({BPF_FILTER})")

    def _on_packet(self, pkt):
        if TCP not in pkt: return
        with BUF_LOCK:
            self.buffer += bytes(pkt[TCP].payload)
        self.after_idle(self._try_parse_buffer)

    # ---------- 解析 ----------
    def _try_parse_buffer(self):
        with BUF_LOCK:
            buf = self.buffer
            idx = buf.find(b"TOZ ")
            while idx >= 0 and idx + 8 <= len(buf):
                size = int.from_bytes(buf[idx+4:idx+8], "little")
                if idx + 8 + size > len(buf): break  # incomplete
                blob = buf[idx:idx+8+size]
                self.buffer = buf = buf[idx+8+size:]
                self._handle_packet(blob)
                idx = buf.find(b"TOZ ")
            self.buffer = buf   # 剩餘 bytes

    def _handle_packet(self, blob: bytes):
        try: parsed = ChatParser.parse_packet_bytes(blob)
        except Exception as e:
            self.log(f"❌ 解析失敗：{e}"); return

        # 若無有效文字與暱稱，視為無用封包
        if not (parsed.get("Nickname") or parsed.get("Text")):
            return

        ts  = time.strftime('%H:%M:%S')
        info = "｜".join(f"{k}:{v}" for k, v in parsed.items() if k != "floats")
        self.log(f"[{ts}] {info}")

    # ---------- Log ----------
    def log(self, text: str):
        self.logbox.configure(state="normal")
        self.logbox.insert("end", text + "\n")
        self.logbox.yview("end")
        self.logbox.configure(state="disabled")

    # ---------- 給離線解析直接餵 bytes ----------
    def _feed_bytes(self, raw: bytes):
        self.buffer = raw
        self._try_parse_buffer()

# ======== Main ========

if __name__ == "__main__":
    app = ChatGUI()
    app.mainloop()