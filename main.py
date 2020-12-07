import os

from dotenv import load_dotenv
load_dotenv()

from telethon import TelegramClient, events, connection
import telethon

PROXY_URL = os.getenv('PROXY_URL')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_SECRET = os.getenv('PROXY_SECRET')
USE_PROXY = PROXY_URL and PROXY_PORT and PROXY_SECRET
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
TOKEN = os.getenv('BOT_TOKEN')
proxy = {'connection': connection.ConnectionTcpMTProxyRandomizedIntermediate,
         'proxy': (PROXY_URL, int(PROXY_PORT), PROXY_SECRET)} if USE_PROXY else {}

bot = TelegramClient('bot', API_ID, API_HASH, **proxy).start(bot_token=TOKEN)

class Cipher:
    def __init__(self, verb: str, replace: dict):
        self.replace = dict(replace)
        self.verb = verb
    
    def transform(self, s: str) -> str:
        new_s = list(s)
        for i, e in enumerate(new_s):
            new_s[i] = self.replace.get(e, e)
        return ''.join(new_s)
    
    def make_article(self, s: str, builder: telethon.tl.custom.InlineBuilder):
        res = self.transform(s)
        return builder.article(
            title = self.verb,
            text = res,
            description = res
        )

ciphers = []

def gen_lyfr_replace() -> dict:
    repl = dict([
        ('й', 'ф'), ('ц', 'ы'), ('у', 'в'), ('к', 'а'), ('е', 'п'), ('ё', 'п'), 
        ('н', 'р'), ('г', 'о'), ('ш', 'л'), ('щ', 'д'), ('з', 'ж'), ('х', 'э'), 
        ('q', 'a'), ('w', 's'), ('e', 'd'), ('r', 'f'), ('t', 'g'), ('y', 'h'), 
        ('u', 'j'), ('i', 'k'), ('o', 'l'), ('p', ';'), ('[', '\''), ('{', '"')
    ])
    it = list(repl.items())
    for f, t in it:
        repl[f.upper()] = t.upper()
    repl['P'] = ':'
    return repl

def gen_ctkl_replace() -> dict:
    repl = dict([
        ('й', 'q'), ('ц', 'w'), ('у', 'e'), ('к', 'r'), ('е', 't'), ('н', 'y'), 
        ('г', 'u'), ('ш', 'i'), ('щ', 'o'), ('з', 'p'), ('х', '['), ('ъ', ']'), 
        ('ф', 'a'), ('ы', 's'), ('в', 'd'), ('а', 'f'), ('п', 'g'), ('р', 'h'), 
        ('о', 'j'), ('л', 'k'), ('д', 'l'), ('ж', ';'), ('э', "'"), 
        ('я', 'z'), ('ч', 'x'), ('с', 'c'), ('м', 'v'), ('и', 'b'), 
        ('т', 'n'), ('ь', 'm'), ('б', ','), ('ю', '.')
    ])
    it = list(repl.items())
    for f, t in it:
        repl[f.upper()] = t.upper()
    

    repl['Х'] = '{'
    repl['Ъ'] = '}'
    repl['Ж'] = ':'
    repl['Э'] = '"'
    repl['Б'] = '<'
    repl['Ю'] = '>'
    
    it = list(repl.items())
    for f, t in it:
        repl[t] = f
        
    return repl

ciphers = [
    Cipher('Залифровать', gen_lyfr_replace()),
    Cipher('CTKL', gen_ctkl_replace())
]

@bot.on(events.InlineQuery)
async def inline(event):
    res = []
    for c in ciphers:
        res.append(c.make_article(event.text, event.builder))
    await event.answer(res)

if __name__ == '__main__':
    bot.run_until_disconnected()
