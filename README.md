以下是你更新後的 `README.md`，整合了：

1. ✅ Discord 機器人推播功能說明
2. ✅ Npcap 安裝必要提醒
3. ✅ 頻道權限錯誤的解法與注意事項

---

````markdown
# Artale Channel Broadcast System（公共頻道外接系統）

🎮 用於楓之谷 Artale 伺服器的公共聊天訊息外接系統。透過封包分析，自動解析 TCP 封包中的頻道、暱稱、訊息等資訊，並以 WebSocket 推播給網頁前端與 Discord 頻道同步顯示。可用於自動顯示聊天、建立好友、整合直播視覺化。

---

## ✅ 功能特色

- 📦 即時封包監聽（TCP port `32800`）
- 🔍 精準解析欄位：`Channel`、`Nickname`、`UserId`、`Text`、`ProfileCode`
- 🧠 自動產生好友標籤格式：`Nickname#UserId`
- 🕒 附加時間戳（`[YYYY-MM-DD HH:MM:SS]`）
- 🌐 WebSocket 即時推播至前端 UI 顯示
- 📣 整合 Discord 機器人自動轉貼聊天訊息
- ✨ 支援複製好友資訊、美化 UI、標記收購／販售

---

## 🔮 未來預計功能

- 💾 儲存聊天紀錄至本地或遠端資料庫
- 🔍 關鍵字快速搜尋（如：背包、賣、買）
- 📈 建立歷史價格紀錄與交易統計分析
- 🧭 前端整合搜尋列、時間範圍與排序工具
- 🔔 Discord bot 增加高亮通知與 tag 特定角色

---

## 🚀 安裝與啟動

### 1. 安裝 Python 套件（後端封包監聽）

```bash
pip install scapy websockets
````

> ❗ 若你是 Windows 用戶，**請務必安裝 [Npcap](https://nmap.org/npcap/) 並勾選 "WinPcap API-compatible mode"**，否則封包將無法擷取（`No libpcap provider available`）。

---

### 2. 啟動封包監聽 + WebSocket 廣播

```bash
python main_chat_ws.py
```

啟動後你將看到：

```
🟢 啟動 Sniffer 中（tcp port 32800）
✅ 已啟動 MapleStory 聊天 WebSocket 推播器
✅ WebSocket 伺服器啟動於 ws://localhost:8765
```

---

### 3. （可選）安裝與啟動 Discord Bot 推播功能

#### 3.1 安裝依賴：

```bash
npm install discord.js ws dotenv
```

#### 3.2 建立 `.env` 並填入以下資訊：

```env
DISCORD_TOKEN=你的 Discord Bot Token
DISCORD_CHANNEL_ID=要推播的頻道 ID
WS_URL=ws://localhost:8765
```

#### 3.3 執行 bot：

```bash
node bot.js
```

> 🔐 如果出現 `Missing Access` 錯誤：
>
> * 請重新產生 [OAuth2 URL](https://discord.com/developers/applications) 並邀請機器人
> * 確保 bot **已加入伺服器** 並在該文字頻道擁有「傳送訊息」權限
> * 建議開啟「開發者模式」，右鍵頻道 > 複製 ID，填入 `.env`

---

## 🌐 前端展示頁（index.html）

即時顯示聊天訊息、關鍵字高亮、複製好友 ID 的網頁前端。支援：

✔ 自動顯示訊息時間、頻道、暱稱、訊息內容
✔ 收／售／雙向標記背景色
✔ 點擊「複製好友」快速複製 `暱稱#UserId`
✔ 黑名單、關鍵字過濾、排序切換、推播通知

---

## 📂 專案結構

```
.
├── main_chat_ws.py       # 封包監聽 + WebSocket 廣播主程式（Python）
├── bot.js                # Discord 推播 bot 主程式（Node.js）
├── index.html            # 前端頁面（可直接開啟）
├── .env                  # Discord token 與頻道設定（需自行建立）
├── thumbnail.png         # UI 畫面預覽
├── .gitignore            # Git 忽略設定
└── README.md             # 專案說明文件
```

---

## 🧪 推播範例資料格式（WebSocket 傳送）

```json
{
  "timestamp": "[2025-06-03 06:57:03]",
  "Channel": "CH140",
  "Nickname": "企鵝",
  "UserId": "iuvOC",
  "ProfileCode": "iuvOC",
  "Text": "140自由賣背包：180w，只有17個要買的快來啊！",
  "FriendTag": "企鵝#iuvOC"
}
```

---

## 📌 注意事項

* ✅ 請用「系統管理員身份」啟動 Python 封包監聽程式
* ✅ 封包擷取僅在遊戲送出聊天訊息時觸發
* 🔒 本系統僅進行被動封包監聽，**不修改、不注入、不干涉遊戲行為**

---

## 📜 授權 License

MIT License

開源分享，歡迎交流與改作！

```

---

如果你還想加入影片教學連結、加入 Logo 或 Discord 社群連結，我也可以幫你補上。需要的話告訴我！
```
