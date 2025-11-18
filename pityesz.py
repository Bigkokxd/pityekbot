import discord
from discord.ext import tasks
import os

# --- KONFIGURÁCIÓ ---
TOKEN = 'MTQ0MDQ0NTM4MDQwNjgwNDUzMw.GX3MV1.cNoT-KFjSkGewYz5gJjsHw_wwMXTY5d9NIoK4U'
CHANNEL_ID = 1290612739634499639  # Cseréld ki a saját számra!
MESSAGE_TEXT = "https://tenor.com/view/mcisti-selim-etkar-norbert-stu-k%C3%B6r%C3%B6sk%C3%A9nyi-istv%C3%A1n-k%C3%B6r%C3%B6sk%C3%A9nyi-gif-10597262277681601568"

# --- A BOT KÓDJA ---

class MyBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('--------------------------------------------------')
        print(f'BEJELENTKEZVE: {self.user} (ID: {self.user.id})')
        print('--------------------------------------------------')
        print('A bot jelenleg ezeken a szervereken van bent:')
        for guild in self.guilds:
            print(f"- {guild.name} (ID: {guild.id})")
        print('--------------------------------------------------')
        
        if not self.spam_loop.is_running():
            self.spam_loop.start()
            print("Az 5 perces időzítő elindult.")

    @tasks.loop(minutes=5)
    async def spam_loop(self):
        try:
            # A fetch_channel közvetlenül a Discord szerverét kérdezi le, biztosabb mint a get_channel
            channel = await self.fetch_channel(CHANNEL_ID)
            
            await channel.send(MESSAGE_TEXT)
            print(f'[SIKER] Üzenet elküldve ide: {channel.name} ({CHANNEL_ID})')

        except discord.NotFound:
            print(f"[HIBA] Nem található csatorna ezzel az ID-vel: {CHANNEL_ID}")
            print("Tipp: Biztos, hogy a bot be van lépve arra a szerverre, ahol ez a csatorna van?")
        except discord.Forbidden:
            print(f"[HIBA] A bot látja a csatornát ({CHANNEL_ID}), de NINCS JOGA írni bele.")
            print("Tipp: Adj a botnak 'Send Messages' és 'View Channel' jogot a szerveren!")
        except Exception as e:
            print(f"[HIBA] Váratlan hiba történt: {e}")

    @spam_loop.before_loop
    async def before_spam_loop(self):
        await self.wait_until_ready()

# Beállítjuk a jogosultságokat
intents = discord.Intents.default()
intents.messages = True

client = MyBot(intents=intents)

if __name__ == '__main__':
    try:
        if TOKEN == 'IDE_MÁSOLD_A_BOT_TOKEN_T':
            print("HIBA: Nem adtál meg Tokent a kód elején!")
        else:
            client.run(TOKEN)
    except Exception as e:
        print(f"Indítási hiba: {e}")