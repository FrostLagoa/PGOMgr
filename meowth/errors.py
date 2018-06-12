
import discord
from discord.ext import commands
from discord.ext.commands.errors import CommandError
from inspect import signature, getfullargspec
import asyncio

class TeamSetCheckFail(CommandError):
    'Exception raised checks.teamset fails'
    pass

class WantSetCheckFail(CommandError):
    'Exception raised checks.wantset fails'
    pass

class WildSetCheckFail(CommandError):
    'Exception raised checks.wildset fails'
    pass

class ReportCheckFail(CommandError):
    'Exception raised checks.allowreport fails'
    pass

class RaidSetCheckFail(CommandError):
    'Exception raised checks.raidset fails'
    pass

class EXRaidSetCheckFail(CommandError):
    'Exception raised checks.exraidset fails'
    pass

class ResearchSetCheckFail(CommandError):
    'Exception raised checks.researchset fails'
    pass

class MeetupSetCheckFail(CommandError):
    'Exception raised checks.meetupset fails'
    pass

class ArchiveSetCheckFail(CommandError):
    'Exception raised checks.archiveset fails'
    pass

class InviteSetCheckFail(CommandError):
    'Exception raised checks.inviteset fails'
    pass

class CityChannelCheckFail(CommandError):
    'Exception raised checks.citychannel fails'
    pass

class WantChannelCheckFail(CommandError):
    'Exception raised checks.wantchannel fails'
    pass

class RaidChannelCheckFail(CommandError):
    'Exception raised checks.raidchannel fails'
    pass

class EggChannelCheckFail(CommandError):
    'Exception raised checks.eggchannel fails'
    pass

class NonRaidChannelCheckFail(CommandError):
    'Exception raised checks.nonraidchannel fails'
    pass

class ActiveRaidChannelCheckFail(CommandError):
    'Exception raised checks.activeraidchannel fails'
    pass

class ActiveChannelCheckFail(CommandError):
    'Exception raised checks.activechannel fails'
    pass

class CityRaidChannelCheckFail(CommandError):
    'Exception raised checks.cityraidchannel fails'
    pass

class RegionEggChannelCheckFail(CommandError):
    'Exception raised checks.cityeggchannel fails'
    pass

class RegionExRaidChannelCheckFail(CommandError):
    'Exception raised checks.allowexraidreport fails'
    pass

class ExRaidChannelCheckFail(CommandError):
    'Exception raised checks.cityeggchannel fails'
    pass

class ResearchReportChannelCheckFail(CommandError):
    'Exception raised checks.researchreport fails'
    pass

class MeetupReportChannelCheckFail(CommandError):
    'Exception raised checks.researchreport fails'
    pass

class WildReportChannelCheckFail(CommandError):
    'Exception raised checks.researchreport fails'
    pass

async def delete_error(message, error):
    try:
        await message.delete()
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        pass
    try:
        await error.delete()
    except (discord.errors.Forbidden, discord.errors.HTTPException):
        pass

def missing_arg_msg(ctx):
    prefix = ctx.prefix.replace(ctx.bot.user.mention, '@' + ctx.bot.user.name)
    command = ctx.invoked_with
    callback = ctx.command.callback
    sig = list(signature(callback).parameters.keys())
    (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults, annotations) = getfullargspec(callback)
    rq_args = []
    nr_args = []
    if defaults:
        rqargs = args[:(- len(defaults))]
    else:
        rqargs = args
    if varargs:
        if varargs != 'args':
            rqargs.append(varargs)
    arg_num = len(ctx.args) - 1
    sig.remove('ctx')
    args_missing = sig[arg_num:]
    msg = _("Miau! Preciso de mais detalhes! Uso: {prefix}{command}").format(prefix=prefix, command=command)
    for a in sig:
        if kwonlydefaults:
            if a in kwonlydefaults.keys():
                msg += ' [{0}]'.format(a)
                continue
        if a in args_missing:
            msg += ' **<{0}>**'.format(a)
        else:
            msg += ' <{0}>'.format(a)
    return msg

def custom_error_handling(bot, logger):

    @bot.event
    async def on_command_error(ctx, error):
        channel = ctx.channel
        prefix = ctx.prefix.replace(ctx.bot.user.mention, '@' + ctx.bot.user.name)
        if isinstance(error, commands.MissingRequiredArgument):
            error = await ctx.channel.send(missing_arg_msg(ctx))
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, commands.BadArgument):
            formatter = commands.formatter.HelpFormatter()
            page = await formatter.format_help_for(ctx, ctx.command)
            error = await ctx.channel.send(page[0])
            await asyncio.sleep(20)
            await delete_error(ctx.message, error)
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CheckFailure):
            pass
        elif isinstance(error, TeamSetCheckFail):
            msg = _('Miau! Gerenciamento de times não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, WantSetCheckFail):
            msg = _('Miau! Notificação de Pokémon não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, WildSetCheckFail):
            msg = _('Miau! Aviso de Pokémon selvagem não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ReportCheckFail):
            msg = _('Miau! Aviso não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, RaidSetCheckFail):
            msg = _('Miau! Gerenciamento de raid não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, EXRaidSetCheckFail):
            msg = _('Miau! Gerenciamento de raid EX não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ResearchSetCheckFail):
            msg = _('Miau! Aviso de missões não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, MeetupSetCheckFail):
            msg = _('Miau! Aviso de encontros não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ArchiveSetCheckFail):
            msg = _('Miau! Arquivamento de canais não está disponível nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, InviteSetCheckFail):
            msg = _('Miau! Convite para raid EX não está habilitado nesse servidor. **{prefix}{cmd_name}** está indisponível para uso.').format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, CityChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('em um dos seguintes canais de região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, WantChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um dos seguintes canais:').format(cmd_name=ctx.invoked_with, prefix=prefix)
            want_channels = bot.guild_dict[guild.id]['configure_dict']['want']['report_channels']
            counter = 0
            for c in want_channels:
                channel = discord.utils.get(guild.channels, id=c)
                if counter > 0:
                    msg += '\n'
                if channel:
                    msg += channel.mention
                else:
                    msg += '\n#deleted-channel'
                counter += 1
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, RaidChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de raid. Use **{prefix}lista** em qualquer ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += _('canal de raid de região para ver as raids ativas.')
            else:
                msg += _('dos seguintes canais de raid para ver as raids ativas:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, EggChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de ovo de raid. Use **{prefix}lista** em qualquer ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += _('canal de aviso de raid para ver as raids ativas.')
            else:
                msg += _('dos seguintes canais de região para ver as raids ativas:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, NonRaidChannelCheckFail):
            msg = _("Miau! **{prefix}{cmd_name}** não pode ser usado em um canal de raid.").format(cmd_name=ctx.invoked_with, prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ActiveRaidChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de raid ativa. Use **{prefix}lista** em qualquer ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            try:
                egg_check = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('type',None)
                meetup = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('meetup',{})
            except:
                egg_check = ""
                meetup = False
            if len(city_channels) > 10:
                msg += _('canal de aviso por região para ver os canais ativos.')
            else:
                msg += _('dos seguintes canais por região para ver os canais ativos:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            if egg_check == "egg" and not meetup:
                msg += _('\nEsse é um canal de ovo de raid. O canal precisa ficar ativo usando o comando **{prefix}raid <pokemon>** antes de eu aceitar comandos!').format(prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ActiveChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal ativo. Use **{prefix}lista** em qualquer ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            try:
                egg_check = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('type',None)
                meetup = bot.guild_dict[guild.id]['raidchannel_dict'][ctx.channel.id].get('meetup',{})
            except:
                egg_check = ""
                meetup = False
            if len(city_channels) > 10:
                msg += _('canal de aviso por região para ver as raids ativas')
            else:
                msg += _('dos seguintes canais por região para ver as raids ativas:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            if egg_check == "egg" and not meetup:
                msg += _('\nEsse é um canal de ovo de raid. O canal precisa ficar ativo usando o comando **{prefix}raid <pokemon>** antes de eu aceitar comandos!').format(prefix=prefix)
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, CityRaidChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de raid ou ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += _('em um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, RegionEggChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de ovo de raid ou ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['raid']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, RegionExRaidChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** raid EX em um dos seguintes canais por região:').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['exraid']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ExRaidChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em um canal de raid EX. Use **{prefix}lista** em qualquer um dos seguintes canais por região:').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['exraid']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, ResearchReportChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['research']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error, MeetupReportChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['meetup']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        elif isinstance(error,WildReportChannelCheckFail):
            guild = ctx.guild
            msg = _('Miau! Por favor use **{prefix}{cmd_name}** em ').format(cmd_name=ctx.invoked_with, prefix=prefix)
            city_channels = bot.guild_dict[guild.id]['configure_dict']['wild']['report_channels']
            if len(city_channels) > 10:
                msg += _('um canal de aviso por região.')
            else:
                msg += _('um dos seguintes canais por região:')
                for c in city_channels:
                    channel = discord.utils.get(guild.channels, id=c)
                    if channel:
                        msg += '\n' + channel.mention
                    else:
                        msg += '\n#deleted-channel'
            error = await ctx.channel.send(msg)
            await asyncio.sleep(10)
            await delete_error(ctx.message, error)
        else:
            logger.exception(type(error).__name__, exc_info=error)
