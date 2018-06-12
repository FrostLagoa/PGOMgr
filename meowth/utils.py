import re

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import discord

def get_match(word_list: list, word: str, score_cutoff: int = 60):
    """Uses fuzzywuzzy to see if word is close to entries in word_list

    Returns a tuple of (MATCH, SCORE)
    """
    result = process.extractOne(
        word, word_list, scorer=fuzz.ratio, score_cutoff=score_cutoff)
    if not result:
        return (None, None)
    return result

def colour(*args):
    """Returns a discord Colour object.

    Pass one as an argument to define colour:
        `int` match colour value.
        `str` match common colour names.
        `discord.Guild` bot's guild colour.
        `None` light grey.
    """
    arg = args[0] if args else None
    if isinstance(arg, int):
        return discord.Colour(arg)
    if isinstance(arg, str):
        colour = arg
        try:
            return getattr(discord.Colour, colour)()
        except AttributeError:
            return discord.Colour.lighter_grey()
    if isinstance(arg, discord.Guild):
        return arg.me.colour
    else:
        return discord.Colour.lighter_grey()

def make_embed(msg_type='', title=None, icon=None, content=None,
               msg_colour=None, guild=None, title_url=None,
               thumbnail='', image=''):
    """Returns a formatted discord embed object.

    Define either a type or a colour.
    Types are:
    error, warning, info, success, help.
    """
    embed_types = {
        'error':{
            'icon':'https://i.imgur.com/juhq2uJ.png',
            'colour':'red'
        },
        'warning':{
            'icon':'https://i.imgur.com/4JuaNt9.png',
            'colour':'gold'
        },
        'info':{
            'icon':'https://i.imgur.com/wzryVaS.png',
            'colour':'blue'
        },
        'success':{
            'icon':'https://i.imgur.com/ZTKc3mr.png',
            'colour':'green'
        },
        'help':{
            'icon':'https://i.imgur.com/kTTIZzR.png',
            'colour':'blue'
        }
    }
    if msg_type in embed_types.keys():
        msg_colour = embed_types[msg_type]['colour']
        icon = embed_types[msg_type]['icon']
    if guild and not msg_colour:
        msg_colour = colour(guild)
    else:
        if not isinstance(msg_colour, discord.Colour):
            msg_colour = colour(msg_colour)
    embed = discord.Embed(description=content, colour=msg_colour)
    if not title_url:
        title_url = discord.Embed.Empty
    if not icon:
        icon = discord.Embed.Empty
    if title:
        embed.set_author(name=title, icon_url=icon, url=title_url)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    return embed

def bold(msg: str):
    """Format to bold markdown text"""
    return f'**{msg}**'

def italics(msg: str):
    """Format to italics markdown text"""
    return f'*{msg}*'

def bolditalics(msg: str):
    """Format to bold italics markdown text"""
    return f'***{msg}***'

def code(msg: str):
    """Format to markdown code block"""
    return f'```{msg}```'

def pycode(msg: str):
    """Format to code block with python code highlighting"""
    return f'```py\n{msg}```'

def ilcode(msg: str):
    """Format to inline markdown code"""
    return f'`{msg}`'

def convert_to_bool(argument):
    lowered = argument.lower()
    if lowered in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
        return True
    elif lowered in ('no', 'n', 'false', 'f', '0', 'disable', 'off'):
        return False
    else:
        return None

def sanitize_channel_name(name):
    """Converts a given string into a compatible discord channel name."""
    # Remove all characters other than alphanumerics,
    # dashes, underscores, and spaces
    ret = re.sub('[^a-zA-Z0-9 _\\-]', '', name)
    # Replace spaces with dashes
    ret = ret.replace(' ', '-')
    return ret

async def get_raid_help(prefix, avatar, user=None):
    helpembed = discord.Embed(colour=discord.Colour.lighter_grey())
    helpembed.set_author(name="Ajuda na Organização de Raid", icon_url=avatar)
    helpembed.add_field(
        name="Chave",
        value="<> denota argumentos obrigatórios, [] denota argumentos opcionais",
        inline=False)
    helpembed.add_field(
        name="Comando",
        value=(
            f"`{prefix}raid <espécies>`\n"
            f"`{prefix}clima <clima>`\n"
            f"`{prefix}tempo <minutos>`\n"
            f"`{prefix}comeca <time>`\n"
            "`<link do google maps>`\n"
            "**Confirmação de presença**\n"
            f"`{prefix}(i/ac/c)...\n"
            "[total]...\n"
            "[contagem por time]`\n"
            "**Listas**\n"
            f"`{prefix}lista [status]`\n"
            f"`{prefix}lista [status] tags`\n"
            f"`{prefix}lista times`\n\n"
            f"`{prefix}comeca [time]`"))
    helpembed.add_field(
        name="Descrição",
        value=(
            "`Abre canal de raid ou ovo`\n"
            "`Define o clima atual no jogo`\n"
            "`Define o tempo pro ovo chocar ou pra raid acabar`\n"
            "`Define o início da raid`\n"
            "`Atualiza a localização da raid`\n\n"
            "`interessado/acaminho/cheguei`\n"
            "`quantidade de treinadores`\n"
            "`quantidade de cada time (ex. 3m para 3 Mystic)`\n\n"
            "`Listas de treinadores por status`\n"
            "`@menciona os treinadores por status`\n"
            "`Listas de treinadores por time`\n\n"
            "`Move os treinadores da lista de 'cheguei' para a sala.`"))
    if not user:
        return helpembed
    await user.send(embed=helpembed)
