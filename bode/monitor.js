const { Telegraf } = require("telegraf");
require("dotenv").config();

const Token = process.env.TOKEN;

const bot = new Telegraf(Token);
bot.start((ctx) => ctx.reply("Welcome"));
bot.help((ctx) => ctx.reply("Send me a sticker"));
bot.on("sticker", (ctx) => ctx.reply("👍"));
bot.on(
  ["new_chat_members", "left_chat_member", "new_chat_photo", "voice"],
  (ctx) => console.log(ctx.message.new_chat_members)
);
bot.hears("hi", (ctx) => ctx.reply("Hey there"));
bot.on("message", (ctx) => console.log(ctx));

bot.launch();
