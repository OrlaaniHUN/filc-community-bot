import json
import discord
from discord import Intents, app_commands
import LaTex
import horoscope
import catto


horoszkop_csatorna = 994215263551623198 #992771006403985429
rangok_csatorna = 994215312604012605 #993630780532199536

MyGuild = discord.Object(id=994215181691392051) #991399821850202172
class aclient(discord.Client):
    def __init__(self, *, intents: Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MyGuild)
        await self.tree.sync(guild=MyGuild)




intents = Intents.all()
intents.members = True
intents.message_content = True


client = aclient(intents=intents)
token = open("token.txt", "r").read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

async def rossz_csatorna(aktualis_csatorna, jo_csatorna):
    await aktualis_csatorna.send_message(f"Kérlek használd a megfelelő csatornát: <#{jo_csatorna}> :)")

def rangok():
    rangok_fajl = open("roles.json", "r")
    tartalom = rangok_fajl.read()
    rangok_fajl.close()

    return json.loads(tartalom)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#parancsok

@client.tree.command()
@app_commands.describe(csillagkep="Lehetőségek: kos, bika, ikrek, rak, oroszlan, szuz, merleg, skorpio, nyilas, bak, vizonto, halak")
async def horoszkop(interaction: discord.Interaction, csillagkep: str):
    if interaction.channel_id == horoszkop_csatorna:
        try:
            await interaction.response.send_message(horoscope.fetch(csillagkep))
        except Exception:
            await interaction.response.send_message("Nem létező horoszkóp!")
    else:
            await rossz_csatorna(interaction.response, horoszkop_csatorna)

@client.tree.command()
@app_commands.describe(cat="http kód vagy random")
async def cat(interaction: discord.Interaction, cat: str):
    catto.fetch(cat)
    await interaction.response.send_message(file=discord.File("images/cat.gif"))

@client.tree.command(description="Publikus rangok felvétele!")
@app_commands.describe(rang="help vagy rang neve")
async def rang(interaction: discord.Interaction, rang: str):
    if interaction.channel_id == rangok_csatorna:
        if rang == "help":
            await interaction.response.send_message("Elérhető rangok:\n")
            await interaction.channel.send("\n\n".join(
                map(
                    lambda rang: 
                    f"Rang: {rang['name']}\n"
                    f"Leírás: {rang['description']}\n"
                    f"Parancs: `!rang {rang['role']}`\n",
                    rangok()
                )
            ))
        else:
            elerheto_rangok = rangok()
            if rang in map(lambda rang: rang["role"], elerheto_rangok):
                await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name=rang))
                await interaction.response.send_message(f"Megkaptad a {rang} rangot!",ephemeral=True)
            else:
                await interaction.response.send_message("Nincs ilyen rang!", ephemeral=True)

    else:
        await rossz_csatorna(interaction.response, rangok_csatorna)

@client.tree.command(description="Publikus rangok levétele!")
@app_commands.describe(rang="Rangod neve")
async def derang(interaction: discord.Interaction, rang: str):
    if interaction.channel_id == rangok_csatorna:
        if rang in map(lambda rang: rang.name, interaction.user.roles):
            await interaction.user.remove_roles(discord.utils.get(interaction.user.roles, name=rang))
            await interaction.response.send_message(f"Levetted magadról a {rang} rangot!",ephemeral=True)   
        else:
            await interaction.response.send_message("Nincs ilyen rangod!")
    else:
        await rossz_csatorna(interaction.response, rangok_csatorna)

@client.tree.context_menu(name="Conver to Latex")
async def convert_latex(interaction: discord.Interaction, message: discord.Message):
    try:
        LaTex.save_image_from_latex(message.content)
        await interaction.response.send_message(file=discord.File("images/compiled_latex.png"))
    except Exception as e:
        await interaction.response.send_message(f"Érvénytelen Latex! error: {e}")


@client.tree.command(description="Szöveg LaTex-é alakítása!")
@app_commands.describe(text="latex-é alakítandó szöveg")
async def latex(interaction: discord.Interaction, text: str):
    try:
        LaTex.save_image_from_latex(text)
        await interaction.response.send_message(file=discord.File("images/compiled_latex.png"))
    except Exception as e:
        await interaction.response.send_message(f"Érvénytelen Latex! error: {e}")

client.run(token)