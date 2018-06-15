import asyncio

import discord
from discord.ext import commands


from meowth import utils
from meowth import checks

class Tutorial:
    def __init__(self, bot):
        self.bot = bot

    async def wait_for_cmd(self, tutorial_channel, newbie, command_name):

        # build check relevant to command
        def check(c):
            if not c.channel == tutorial_channel:
                return False
            if not c.author == newbie:
                return False
            if c.command.name == command_name:
                return True
            return False

        # wait for the command to complete
        cmd_ctx = await self.bot.wait_for(
            'command_completion', check=check, timeout=300)

        return cmd_ctx

    def get_overwrites(self, guild, member):
        return {
            guild.default_role: discord.PermissionOverwrite(
                read_messages=False),
            member: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_channels=True),
            guild.me: discord.PermissionOverwrite(
                read_messages=True)
            }

    async def want_tutorial(self, ctx, config):
        report_channels = config['want']['report_channels']
        report_channels.append(ctx.tutorial_channel.id)

        await ctx.tutorial_channel.send(
            f"Esse servidor utiliza o comando **{ctx.prefix}quero** para ajudar "
			"os membros a receberem notificações sobre o Pokémon que eles querem! "
			"Eu crio cargos para cada Pokémon que as pessoas querem, "
			"e @mencionando esses cargos irá enviar uma notificação para "
			f"qualquer um que usou o comando **{ctx.prefix}quero** para aquele Pokémon!\n"
			f"Teste o comando {ctx.prefix}quero!\n"
			f"Ex: `{ctx.prefix}quero unown`")

        try:
            await self.wait_for_cmd(ctx.tutorial_channel, ctx.author, 'quero')

            # acknowledge and wait a second before continuing
            await ctx.tutorial_channel.send("Excelente!")
            await asyncio.sleep(1)

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await ctx.tutorial_channel.send(
				f"Você demorou demais para completar o comando **{ctx.prefix}quero**!"
				"Esse canal será deletado em dez secundos.")
            await asyncio.sleep(10)
            await ctx.tutorial_channel.delete()

            return False

        # clean up by removing tutorial from report channel config
        finally:
            report_channels.remove(ctx.tutorial_channel.id)

        return True

    async def wild_tutorial(self, ctx, config):
        report_channels = config['wild']['report_channels']
        report_channels[ctx.tutorial_channel.id] = 'test'

        await ctx.tutorial_channel.send(
			f"Esse servidor utiliza o comando **{ctx.prefix}selvagem** para "
			"avisar sobre Pokémon selvagens! Quando você usa isso, irei enviar uma mensagem "
			"resumindo o aviso e contendo um link para o melhor palpite sobre a localização "
			"do Pokémon. Se o Pokémon tem um cargo associado a ele no servidor, então irei "
			"@mencionar o cargo na minha mensagem! Seu aviso precisa conter o nome do Pokémon "
			"seguido de sua localização. "
			"Teste o aviso de Pokémon selvagem!\n"
			f"Ex: `{ctx.prefix}selvagem magikarp algum parque`")

        try:
            await self.wait_for_cmd(ctx.tutorial_channel, ctx.author, 'selvagem')

            # acknowledge and wait a second before continuing
            await ctx.tutorial_channel.send("Excelente!")
            await asyncio.sleep(1)

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await ctx.tutorial_channel.send(
				f"Você demorou demais para completar o comando **{ctx.prefix}selvagem**!"
				"Esse canal será deletado em dez secundos.")
            await asyncio.sleep(10)
            await ctx.tutorial_channel.delete()
            return False

        # clean up by removing tutorial from report channel config
        finally:
            del report_channels[ctx.tutorial_channel.id]

        return True

    async def raid_tutorial(self, ctx, config):
        report_channels = config['raid']['report_channels']
        category_dict = config['raid']['category_dict']
        tutorial_channel = ctx.tutorial_channel
        prefix = ctx.prefix
        raid_channel = None

        # add tutorial channel to valid want report channels
        report_channels[tutorial_channel.id] = 'test'

        if config['raid']['categories'] == "region":
            category_dict[tutorial_channel.id] = tutorial_channel.category_id

        async def timeout_raid(cmd):
            await tutorial_channel.send(
                f"Você demorou demais para completar o comando **{prefix}{cmd}**!"
				"Esse canal será deletado em dez secundos.")
            await asyncio.sleep(10)
            await tutorial_channel.delete()
            del report_channels[tutorial_channel.id]
            del category_dict[tutorial_channel.id]
            if raid_channel:
                await raid_channel.delete()
                ctx.bot.loop.create_task(self.bot.expire_channel(raid_channel))
            return

        await tutorial_channel.send(
			f"Esse servidor utiliza o comando **{prefix}raid** para "
			"avisar as raids! Quando você usa isso, irei enviar uma mensagem "
			"resumindo o aviso e criarei um canal de texto para organização. \n"
			"A aviso deve conter, nessa ordem: O Pokémon (se for uma raid ativa) ou "
			"o level (se ainda vai chocar) e a localização.\n"
			"O aviso deve opcionalmente conter o clima (veja "
			f"**{prefix}help clima** para opções disponíveis) e o tempo restante até "
			"o ovo chocar ou expirar (no final do aviso) \n\n"
			"Teste avisar uma raid!\n"
			f"Ex: `{prefix}raid magikarp igreja local nublado 42`\n"
			f"`{prefix}raid 3 igreja local ensolarado 27`")

        try:
            while True:
                raid_ctx = await self.wait_for_cmd(
                    tutorial_channel, ctx.author, 'raid')

                # get the generated raid channel
                raid_channel = raid_ctx.raid_channel

                if raid_channel:
                    break

                # acknowledge failure and redo wait_for
                await tutorial_channel.send(
					"Parece que não funcionou. Tenha certeza que você não está "
					"esquecendo nenhum argumento no comando de raid e "
					"tente novamente.")

            # acknowledge and redirect to new raid channel
            await tutorial_channel.send(
                "Excelente! Vamos lá pro canal de raid que você acabou "
                f"de criar: {raid_channel.mention}")
            await asyncio.sleep(1)

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('raid')
            return False

        # post raid help info prefix, avatar, user
        helpembed = await utils.get_raid_help(
            ctx.prefix, ctx.bot.user.avatar_url)

        await raid_channel.send(
            f"Esse é um canal de raid de exemplo. Aqui uma lista dos comandos "
            "que podem ser usados aqui:", embed=helpembed)

        await raid_channel.send(
            f"Teste expressar interesse na raid!\n\n"
            f"Ex: `{prefix}interessado 5 m3 i1 v1` significaria 5 treinadores: "
            "3 Mystic, 1 Instinct, 1 Valor")

        # wait for interested status update
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'interessado')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('interessado')
            return False

        # acknowledge and continue with pauses between
        await asyncio.sleep(1)
        await raid_channel.send(
            f"Excelente! Para agilizar, você também pode usar **{prefix}i** "
            f"como uma abreviatura para **{prefix}interessado**.")

        await asyncio.sleep(1)
        await raid_channel.send(
            "Agora teste mostrar às pessoas que você está a caminho!\n\n"
            f"Ex: `{prefix}acaminho`")

        # wait for coming status update
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'acaminho')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('acaminho')
            return False

        # acknowledge and continue with pauses between
        await asyncio.sleep(1)
        await raid_channel.send(
			"Ótimo! Veja que se você já especificou "
			"seu grupo em um comando anterior, você não precisa fazer novamente "
			"para a raid atual a menos que você esteja mudando isso. Também, "
			f"**{prefix}ac** é uma abreviatura para **{prefix}acaminho**.")

        await asyncio.sleep(1)
        await raid_channel.send(
            "Agora tente mostrar as pessoas que você chegou na raid!\n\n"
            f"Ex: `{prefix}cheguei`")

        # wait for here status update
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'cheguei')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('cheguei')
            return False

        # acknowledge and continue with pauses between
        await asyncio.sleep(1)
        await raid_channel.send(
            f"Bom! Saiba que **{prefix}c** é uma abreviatura para "
            f"**{prefix}cheguei**")

        await asyncio.sleep(1)
        await raid_channel.send(
			"Agora teste checar para ver o status de todos que pretendem ir a raid!\n\n"
            f"Ex: `{prefix}lista`")

        # wait for list command completion
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'lista')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('lista')
            return False

        # acknowledge and continue with pauses between
        await asyncio.sleep(1)
        await raid_channel.send(
			"Incrível! Já que ninguém mais está a caminho, tente usar o "
			f"comando **{prefix}iniciar** para mover todo mundo na lista "
			"'cheguei' para a sala!")

        # wait for starting command completion
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'iniciar')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('iniciar')
            return False

        # acknowledge and continue with pauses between
        await asyncio.sleep(1)
        await raid_channel.send(
			f"Ótimo! Agora você está listado como 'na sala', onde "
			"você ficará por dois minutos até a raid começar. Nesse tempo, "
			"qualquer um pode solicitar a saída através do comando "
			f"**{prefix}sair**. Se a pessoa requisitando está na sala, "
			"a saída é automática. Se for alguém que chegou na raid depois, "
			"será solicitada uma confirmação de um membro da sala. Quando a saída é confirmada, "
			"todos os membros retornarão para a lista de 'cheguei'.")

        await asyncio.sleep(1)
        await raid_channel.send(
			"Algumas informações sobre os canais de raid. "
			"O Miau tem parceria com o Pokebattler para te informar os melhores atacantes "
			"para cada chefe de raid em qualquer situação. Você pode definir o "
			"clima no aviso inicial da raid ou com o comando "
			f"**{prefix}clima**. Você pode selecionar a combinação de golpes "
			"usando as reações na mensagem inicial dos atacantes. Se "
			f"você tem uma conta no Pokebattler, você pode usar **{prefix}definir "
			"pokebattler <id>** para vincular a sua conta! Depois disso, o comando "
			f"**{prefix}atacantes** vai te mandar uma mensagem direta com seus próprios "
			"atacantes da sua Pokebox.")

        await asyncio.sleep(1)
        await raid_channel.send(
			"Última coisa: se você precisa atualizar o tempo de expiração, use "
			f"**{prefix}tempo <minutos restantes>**\n\n"
			"Fique a vontade para testar os comandos aqui por um tempo. "
			f"Quando você terminar, digite `{prefix}tempo 0` e a raid irá expirar.")

        # wait for timerset command completion
        try:
            await self.wait_for_cmd(
                raid_channel, ctx.author, 'tempo')

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await timeout_raid('tempo')
            return False

        # acknowledge and direct member back to tutorial channel
        await raid_channel.send(
			f"Ótimo! Agora volte ao canal {tutorial_channel.mention} para "
			"continuar o tutorial. Esse canal será deletado em "
			"dez segundos.")

        await tutorial_channel.send(
			f"Ei {ctx.author.mention}, assim que eu terminar de limpar o "
			"canal de raid, o tutorial vai continuar aqui!")

        await asyncio.sleep(10)

        # remove tutorial raid channel
        await raid_channel.delete()
        raid_channel = None
        del report_channels[tutorial_channel.id]

        return True

    async def research_tutorial(self, ctx, config):
        report_channels = config['research']['report_channels']
        report_channels[ctx.tutorial_channel.id] = 'test'

        await ctx.tutorial_channel.send(
			f"Esse servidor utiliza o comando **{ctx.prefix}missao** para "
			"avisar sobre missões! Existem duas maneiras para usar esse comando: "
			f"**{ctx.prefix}missao irá iniciar uma sessão interativa "
			"na qual irei te perguntar sobre a missão, localização e recompensa "
			"da missão. Você também pode usar "
			f"**{ctx.prefix}missao <pokestop>, <missão>, <recompensa>** para "
			"enviar o aviso todo de uma vez.\n\n"
			f"Teste-o digitando `{ctx.prefix}missao`")

        # wait for research command completion
        try:
            await self.wait_for_cmd(
                ctx.tutorial_channel, ctx.author, 'missao')

            # acknowledge and wait a second before continuing
            await ctx.tutorial_channel.send("Excelente!")
            await asyncio.sleep(1)

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await ctx.tutorial_channel.send(
                f"Você demorou demais para completar o comando **{ctx.prefix}missao**!"
				"Esse canal será deletado em dez secundos.")
            await asyncio.sleep(10)
            await ctx.tutorial_channel.delete()
            return False

        # clean up by removing tutorial from report channel config
        finally:
            del report_channels[ctx.tutorial_channel.id]

        return True

    async def team_tutorial(self, ctx):
        await ctx.tutorial_channel.send(
			f"Esse servidor utiliza o comando **{ctx.prefix}time** para "
			"permitir membros selecionarem a qual time de Pokémon GO eles "
			f"pertencem! Digite `{ctx.prefix}time mystic`, por exemplo, se você é "
			" do Time Mystic.")

        # wait for team command completion
        try:
            await self.wait_for_cmd(
                ctx.tutorial_channel, ctx.author, 'time')

            # acknowledge and wait a second before continuing
            await ctx.tutorial_channel.send("Excelente!")
            await asyncio.sleep(1)

        # if no response for 5 minutes, close tutorial
        except asyncio.TimeoutError:
            await ctx.tutorial_channel.send(
                f"Você demorou demais para completar o comando **{ctx.prefix}time**!"
				"Esse canal será deletado em dez secundos.")
            await asyncio.sleep(10)
            await ctx.tutorial_channel.delete()
            return False

        return True

    @commands.group(invoke_without_command=True)
    async def tutorial(self, ctx):
        """Launches an interactive tutorial session for Meowth.

        Meowth will create a private channel and initiate a
        conversation that walks you through the various commands
        that are enabled on the current server."""

        newbie = ctx.author
        guild = ctx.guild
        prefix = ctx.prefix

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        # get tutorial settings
        cfg = self.bot.guild_dict[guild.id]['configure_dict']
        enabled = [k for k, v in cfg.items() if v.get('enabled', False)]

        await ctx.tutorial_channel.send(
			f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:

            # start want tutorial
            if 'want' in enabled:
                completed = await self.want_tutorial(ctx, cfg)
                if not completed:
                    return

            # start wild tutorial
            if 'wild' in enabled:
                completed = await self.wild_tutorial(ctx, cfg)
                if not completed:
                    return

            # start raid
            if 'raid' in enabled:
                completed = await self.raid_tutorial(ctx, cfg)
                if not completed:
                    return

            # start exraid
            if 'exraid' in enabled:
                invitestr = ""

                if 'invite' in enabled:
                    invitestr = (
						"Os canais de texto criados com esse comando "
						"são somente leitura até que os membros utilizem o comando "
						f"**{prefix}convite**.")

                await ctx.tutorial_channel.send(
					f"Esse servidor utiliza o comando **{prefix}raidex** para "
					"avisar sobre raids EX! Quando você usa ele, irei enviar uma mensagem "
					"resumindo o aviso e criarei um canal de texto para organização. "
					f"{invitestr}\n"
					"O aviso precisa conter apenas a localização da raid EX.\n\n"
					"Devido a longa duração dos canais de raid EX, não iremos "
					"testar esse comando agora.")

            # start research
            if 'research' in enabled:
                completed = await self.research_tutorial(ctx, cfg)
                if not completed:
                    return

            # start team
            if 'team' in enabled:
                completed = await self.team_tutorial(ctx)
                if not completed:
                    return

            # finish tutorial
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em trinta segundos.")
            await asyncio.sleep(30)

        finally:
            await ctx.tutorial_channel.delete()

    @tutorial.command()
    @checks.feature_enabled('want')
    async def want(self, ctx):
        """Launches an tutorial session for the want feature.

        Meowth will create a private channel and initiate a
        conversation that walks you through the various commands
        that are enabled on the current server."""

        newbie = ctx.author
        guild = ctx.guild

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        # get tutorial settings
        cfg = self.bot.guild_dict[guild.id]['configure_dict']

        await ctx.tutorial_channel.send(
            f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:
            await self.want_tutorial(ctx, cfg)
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em dez segundos.")
            await asyncio.sleep(10)
        finally:
            await ctx.tutorial_channel.delete()

    @tutorial.command()
    @checks.feature_enabled('wild')
    async def wild(self, ctx):
        """Launches an tutorial session for the wild feature.

        Meowth will create a private channel and initiate a
        conversation that walks you through wild command."""

        newbie = ctx.author
        guild = ctx.guild

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        # get tutorial settings
        cfg = self.bot.guild_dict[guild.id]['configure_dict']

        await ctx.tutorial_channel.send(
            f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:
            await self.wild_tutorial(ctx, cfg)
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em dez segundos.")
            await asyncio.sleep(10)
        finally:
            await ctx.tutorial_channel.delete()

    @tutorial.command()
    @checks.feature_enabled('raid')
    async def raid(self, ctx):
        """Launches an tutorial session for the raid feature.

        Meowth will create a private channel and initiate a
        conversation that walks you through the raid commands."""

        newbie = ctx.author
        guild = ctx.guild

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        # get tutorial settings
        cfg = self.bot.guild_dict[guild.id]['configure_dict']

        await ctx.tutorial_channel.send(
            f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:
            await self.raid_tutorial(ctx, cfg)
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em dez segundos.")
            await asyncio.sleep(10)
        finally:
            await ctx.tutorial_channel.delete()

    @tutorial.command()
    @checks.feature_enabled('research')
    async def research(self, ctx):
        """Launches an tutorial session for the research feature.

        Meowth will create a private channel and initiate a
        conversation that walks you through the research command."""

        newbie = ctx.author
        guild = ctx.guild

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        # get tutorial settings
        cfg = self.bot.guild_dict[guild.id]['configure_dict']

        await ctx.tutorial_channel.send(
            f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:
            await self.research_tutorial(ctx, cfg)
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em dez segundos.")
            await asyncio.sleep(10)
        finally:
            await ctx.tutorial_channel.delete()

    @tutorial.command()
    @checks.feature_enabled('team')
    async def team(self, ctx):
        """Launches an tutorial session for the team feature.

        Meowth will create a private channel and initiate a
        conversation that walks you through the team command."""

        newbie = ctx.author
        guild = ctx.guild

        # get channel overwrites
        ows = self.get_overwrites(guild, newbie)

        # create tutorial channel
        name = utils.sanitize_channel_name(newbie.display_name+"-tutorial")
        ctx.tutorial_channel = await guild.create_text_channel(
            name, overwrites=ows)
        await ctx.message.delete()
        await ctx.send(
            ("Miau! Criei um canal de tutorial privado pra você! "
             f"Entre em {ctx.tutorial_channel.mention} para continuar"),
            delete_after=20.0)

        await ctx.tutorial_channel.send(
            f"Oi {ctx.author.mention}! Eu sou Miau, um bot de Discord ajudante para "
			"comunidades de Pokémon GO! Eu criei um canal para te ensinar tudo "
			"sobre as coisas com as quais eu posso te ajudar nesse servidor! Você pode "
			"abandonar esse tutorial a qualquer momento e eu irei deletar esse canal "
			"depois de cinco minutos. Vamos começar!")

        try:
            await self.team_tutorial(ctx)
            await ctx.tutorial_channel.send(
				f"Isso conclui o tutorial do Miau! "
				"Esse canal será deletado em dez segundos.")
            await asyncio.sleep(10)
        finally:
            await ctx.tutorial_channel.delete()

def setup(bot):
    bot.add_cog(Tutorial(bot))
