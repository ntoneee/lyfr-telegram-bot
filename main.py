import os

if os.getenv('PRODUCTION') is None:
    from dotenv import load_dotenv
    load_dotenv()

from telethon import TelegramClient, events, connection

PROXY_URL = os.getenv('PROXY_URL')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_SECRET = os.getenv('PROXY_SECRET')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
TOKEN = os.getenv('BOT_TOKEN')

proxy = (PROXY_URL, int(PROXY_PORT), PROXY_SECRET)

bot = TelegramClient('bot', API_ID, API_HASH, proxy=proxy, 
    connection=connection.ConnectionTcpMTProxyRandomizedIntermediate
    ).start(bot_token=TOKEN)


replace_lowers = [
    ('й', 'ф'), ('ц', 'ы'), ('у', 'в'), ('к', 'а'), ('е', 'п'), ('н', 'р'),
    ('г', 'о'), ('ш', 'л'), ('щ', 'д'), ('з', 'ж'), ('х', 'э')
]
replace_capitals = []
for f, t in replace_lowers:
    replace_capitals.append((f.upper(), t.upper()))
replace = dict(replace_lowers + replace_capitals)

async def lyfrize(text):
    text = list(text)

    for i, c in enumerate(text):
        text[i] = replace.get(c, c)

    return ''.join(text)

@bot.on(events.InlineQuery)
async def inline(event):
    builder = event.builder
    lyfred = await lyfrize(event.text)
    
    await event.answer([
        builder.article('Лифрировать', text=lyfred, description=lyfred[:10] + '...')
    ])

if __name__ == "__main__":
    bot.run_until_disconnected()