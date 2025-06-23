// bot.js
require("dotenv").config();
const { Client, GatewayIntentBits } = require("discord.js");
const WebSocket = require("ws");

// ==== 環境變數設定 ====
const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const CHANNEL_ID = process.env.DISCORD_CHANNEL_ID;
const WS_URL = process.env.WS_URL;
// ====================

// 建立 Discord bot client
const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages],
});

// 登入成功後建立 WebSocket 連線
client.once("ready", () => {
  console.log(`🤖 已登入 Discord：${client.user.tag}`);

  const ws = new WebSocket(WS_URL);

  ws.onopen = () => console.log("📡 WebSocket 已連線");
  ws.onclose = () => console.log("🔌 WebSocket 已斷線");

  ws.onmessage = async (event) => {
    try {
      const raw = JSON.parse(event.data);
      const messages = Array.isArray(raw) ? raw : [raw];

      for (const msg of messages) {
        const text = msg.Text || msg.text || "";
        const channelName = msg.Channel || msg.channel || "未知頻道";
        const nickname =
          msg.Nickname || msg.username || "匿名";
        const profileCode = msg.ProfileCode || "";
        const timestamp = msg.timestamp?.replace(/^\[|\]$/g, "") || "";

        const formatted = `📢 [${channelName}] ${nickname}${profileCode ? `#${profileCode}` : ""}: ${text}\n🕒 ${timestamp}`;

        const discordChannel = await client.channels.fetch(CHANNEL_ID);
        if (discordChannel?.isTextBased()) {
          await discordChannel.send(formatted);
        }
      }
    } catch (err) {
      console.error("❌ 處理 WebSocket 訊息錯誤：", err);
    }
  };
});

client.login(DISCORD_TOKEN);
