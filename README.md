這是為你目前的專案 **Artale Channel Broadcast System（公共頻道外接系統）** 撰寫的繁體中文 `README.md`，可直接推上 GitHub 使用：

---

# Artale Channel Broadcast System（公共頻道外接系統）

🎮 用於楓之谷 Artale 伺服器的公共聊天訊息即時外接系統。透過封包分析，自動抓取 TCP 封包中的頻道、暱稱與訊息等欄位，並以 WebSocket 推播至前端介面，可用於網頁顯示、直播彈幕整合、AI 聊天串流等場景。

---

## ✅ 功能特色

* 📦 即時封包監聽（TCP port `32800`）
* 🧠 自動解析關鍵欄位：`Channel`、`Nickname`、`Text`、`UserId`、`ProfileCode` 等
* 🌐 WebSocket 廣播推播，方便接 Web UI
* 📅 訊息自動附加 `[YYYY-MM-DD HH:MM:SS]` 時間戳
* 🪶 無 GUI、極輕量，適合部署或整合第三方應用

---

## 🚀 安裝與啟動

### 1. 安裝相依套件

```bash
pip install scapy websockets
```

### 2. 啟動主程式

```bash
python main_chat_ws.py
```

你將會看到：

```
>> 🟢 啟動 Sniffer 中（tcp port 32800） ✅ 已啟動 MapleStory 聊天 WebSocket 推播器
✅ WebSocket 推播伺服器啟動於 ws://localhost:8765
```

---

## 🌐 前端 WebSocket 範例（HTML + JS）

```html
<script>
  const ws = new WebSocket("ws://localhost:8765");
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    console.log(`${msg.timestamp} ${msg.Channel} <${msg.Nickname}>: ${msg.Text}`);
  };
</script>
```

---

## 📂 專案結構

```
.
├── main_chat_ws.py    # 主程式：Sniffer + 封包解析 + WebSocket 廣播
└── README.md          # 本說明文件
```

---

## 🧪 範例輸出

```json
{
  "timestamp": "[2025-06-03 06:32:01]",
  "Channel": "CH4537",
  "Nickname": "PlayerOne",
  "Text": "Hello world!",
  "UserId": "abc123",
  "ProfileCode": "def456"
}
```

---

## 📌 注意事項

* 本程式需以管理員權限執行（封包監聽需要介面權限）
* 請搭配遊戲開啟使用，否則不會有封包輸出
* 本程式不會修改遊戲，也不注入任何 DLL，純被動封包擷取，安全穩定

---

## 📜 授權條款

MIT License
