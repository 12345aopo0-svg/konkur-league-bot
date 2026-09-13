const http = require("http");

const TOKEN = process.env.BOT_TOKEN;

async function sendMessage(chatId, text) {
  await fetch(`https://api.telegram.org/bot${TOKEN}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text
    })
  });
}

const server = http.createServer(async (req, res) => {
  if (req.method === "GET") {
    res.writeHead(200);
    return res.end("Konkur League Bot is running!");
  }

  if (req.method === "POST") {
    let body = "";

    req.on("data", chunk => {
      body += chunk;
    });

    req.on("end", async () => {
      try {
        const update = JSON.parse(body);
        const message = update.message;

        if (message && message.text) {
          const chatId = message.chat.id;
          const text = message.text.trim();

          if (text === "/start") {
            await sendMessage(
              chatId,
              "🎓 به لیگ کنکور خوش اومدی!\n\n📚 مطالعه\n🏆 رقابت\n🔥 استمرار\n📊 گزارش و رتبه‌بندی\n\nربات آماده است."
            );
          } else if (text === "/help") {
            await sendMessage(
              chatId,
              "📖 راهنمای ربات\n\n/start — شروع\n/profile — پروفایل\n/goal — هدف امروز\n/report — گزارش روزانه\n/stats — آمار\n/rank — رتبه‌بندی\n/team — تیم من\n/challenge — چالش‌ها\n/exam — آزمون‌ها\n/result — نتیجه آزمون\n/streak — زنجیره مطالعه"
            );
          } else {
            await sendMessage(
              chatId,
              "🤖 دستور دریافت شد.\nاز منوی ربات استفاده کن."
            );
          }
        }
      } catch (e) {
        console.error(e);
      }

      res.writeHead(200);
      res.end("OK");
    });

    return;
  }

  res.writeHead(200);
  res.end("OK");
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`Bot running on port ${PORT}`);
});
