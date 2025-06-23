# Artale Channel Broadcast System（公共頻道外接系統）

🎮 適用於楓之谷 Artale 伺服器的公共聊天訊息外接系統。透過封包分析自動解析 TCP 封包中頻道、暱稱、訊息等資訊，並即時推送至：

- 🌐 Web 前端頁面（index.html）
- 🤖 Discord 頻道（透過 Discord Bot）

適合直播整合、朋友自動加入、收購通知、資訊視覺化等應用場景。

---

## ✅ 功能特色

- 📦 即時封包監聽（監聽 TCP 32800 port）
- 🔍 自動解析欄位：`Channel`, `Nickname`, `UserId`, `Text`, `ProfileCode`
- 🧠 自動組合好友標籤：`Nickname#UserId`
- 🕒 附加時間戳格式 `[YYYY-MM-DD HH:MM:SS]`
- 🌐 WebSocket 推播給網頁（靜態 index.html）
- 🤖 Discord Bot 自動推送到指定頻道
- 🔔 支援買/賣關鍵字通知、訊息高亮、自動標記
- 📋 一鍵複製好友資訊、黑名單、訊息排序、快速關鍵字過濾
- 🚀 npm script 一鍵啟動 bot 與前端（免 Live Server）

---

## 📦 安裝與使用

### 1. Python 封包擷取（main_chat_ws.py）

#### 📥 安裝必要套件

```bash
pip install scapy websockets
````

#### ⚠ Windows 用戶注意：

請先安裝 [Npcap](https://nmap.org/npcap/)，安裝時記得勾選：

* ✅ WinPcap-compatible mode
* ✅ 安裝為開機服務

否則你將遇到 `No libpcap provider available` 錯誤，無法擷取封包。

#### ▶ 啟動封包擷取 + WebSocket 廣播

```bash
python main_chat_ws.py
```

啟動成功會顯示：

```
🟢 Sniffer 啟動中（tcp port 32800）
✅ WebSocket 推播啟動於 ws://localhost:8765
```

---

### 2. Node.js Discord Bot + Web 前端

#### 📥 安裝依賴

```bash
npm install
```

#### ⚙ 設定 `.env`

請建立 `.env` 檔，填入以下內容：

```env
DISCORD_TOKEN=你的 Discord Bot Token
DISCORD_CHANNEL_ID=推播目標的文字頻道 ID
WS_URL=ws://localhost:8765
```

> 開啟 Discord 開發者模式 → 右鍵頻道 → 複製 ID
> 邀請 bot 進入伺服器請使用含 `bot` 權限的 OAuth2 URL

#### ▶ 啟動 Discord Bot

```bash
npm start
```

---

### 3. 網頁前端展示（index.html）

#### 📂 內建靜態頁面功能（無需 Live Server）

使用以下指令即可啟動本地瀏覽器展示：

```bash
npm run view
```

預設將自動開啟瀏覽器並啟動於：[http://localhost:5500](http://localhost:5500)

支援功能：

* ✅ 訊息高亮分類（力量/智力/買/賣）
* ✅ 自動捲動、排序切換、推播通知
* ✅ 黑名單、交集/聯集關鍵字過濾
* ✅ 固定釘選訊息、顯示時間、頻道與暱稱

---

## 📂 專案結構

```
.
├── main_chat_ws.py         # 封包監聽 + WebSocket 廣播主程式（Python）
├── bot.js                  # Discord Bot 主程式（Node.js）
├── index.html              # 前端頁面（即時聊天室顯示）
├── .env.example            # 環境變數範本（建議使用 .env 建立設定）
├── .gitignore              # 忽略 .env 與 node_modules
├── package.json            # npm 套件與 script 管理
└── README.md               # 本說明文件
```

---

## 🧪 WebSocket 推播格式範例

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

## 🛡️ 安全性與注意事項

* ✅ 本系統純為封包監聽工具，不修改、不注入、不干擾遊戲運作
* ✅ 執行 Python 抓包時請以「系統管理員」身份執行
* ✅ 確保防火牆允許 Python 存取 port `32800`

---

## 📜 授權 License

MIT License

開源分享，歡迎貢獻與改作！

---

## 🙋‍♀️ 有問題？

如需協助設定、整合 Discord bot、加入歷史資料分析或前端 UI 擴充，歡迎發 Issue 或來信交流 🙌