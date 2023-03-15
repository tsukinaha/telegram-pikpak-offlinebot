import logging
import json
from pikpakapi import PikPakApi
from telegram import Update
from urllib.parse import quote
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def geturl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    magnet_name = ' '.join(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="请求正在发送中，请耐心等待")
    try:
        client: PikPakApi = PikPakApi(
            username="username",
            password="password",
        )
        await client.login()
        offline_data = json.dumps(
            await client.offline_download(
                magnet_name
            ),
            indent=4,
        )
        file_name_uni = json.loads(offline_data)['task']['file_name']
        file_name_url = quote(file_name_uni, 'utf-8')
        text = '请求发送成功。\nUrl: rooturl' + file_name_url
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="请求失败，请检查你的magnet链接")


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()
    geturl_handler = CommandHandler('magnet', geturl)

    application.add_handler(geturl_handler)

    application.run_polling()
