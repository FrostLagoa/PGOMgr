import json
from functools import partial

from discord.ext import commands
from meowth import utils
from meowth import checks

class DataHandler:
    """Carregamento e salvamento de dados."""

    def __init__(self, bot):
        self.bot = bot
        self.raid_info = bot.raid_info
        self.pkmn_info = bot.pkmn_info
        self.pkmn_match = partial(utils.get_match, self.pkmn_info['pokemon_list'])

    def __local_check(self, ctx):
        return checks.is_owner_check(ctx) or checks.is_dev_check(ctx)

    def get_name(self, pkmn_number):
        pkmn_number = int(pkmn_number) - 1
        try:
            name = self.pkmn_info['pokemon_list'][pkmn_number]
        except IndexError:
            name = None
        return name

    def get_number(self, pkm_name):
        try:
            number = self.pkmn_info['pokemon_list'].index(pkm_name) + 1
        except ValueError:
            number = None
        return int(number)

    @commands.group(invoke_without_command=True)
    async def raiddata(self, ctx, level=None):
        """Mostra todos os Pokémon de raid disponíveis, mostrando apenas o nível da raid, se solicitado."""
        data = []
        title = None
        if level:
            title = f"Dados de Pokémon para raid {level}"
            try:
                for pkmnno in self.raid_info['raid_eggs'][level]["pokemon"]:
                    data.append(f"#{pkmnno} - {self.get_name(pkmnno)}")
            except KeyError:
                return await ctx.send('Nível de raid especificado é inválido.')
        else:
            title = f"Dados de Pokémon para todas as raids"
            data = []
            for pkmnlvl, vals in self.raid_info['raid_eggs'].items():
                if not vals["pokemon"]:
                    continue
                leveldata = []
                for pkmnno in vals["pokemon"]:
                    leveldata.append(f"#{pkmnno} - {self.get_name(pkmnno)}")
                leveldata = '\n'.join(leveldata)
                data.append(f"**Raid {pkmnlvl} Pokemon**\n{leveldata}\n")
        data_str = '\n'.join(data)
        await ctx.send(f"**{title}**\n{data_str}")

    def in_list(self, pokemon_no):
        for pkmnlvl, vals in self.raid_info['raid_eggs'].items():
            if int(pokemon_no) in vals["pokemon"]:
                return pkmnlvl
        return None

    @raiddata.command(name='remover', aliases=['rm', 'del', 'delete'])
    async def remove_rd(self, ctx, *raid_pokemon):
        """Remove todos os Pokémon fornecidos como argumentos da lista de raids.

        Nota: Se for usado um Pokémon com nome composto, envolva-o com aspas duplas:
        Exemplo: !raiddata remover "Mr Mime" Jynx
        """
        results = []
        for pokemon in raid_pokemon:
            if not pokemon.isdigit():
                match = self.pkmn_match(pokemon)[0]
                if not match:
                    return await ctx.send('Nome de Pokémon inválido')
                pokemon = self.get_number(match)
            hit_key = []
            for k, v in self.raid_info['raid_eggs'].items():
                if pokemon in v['pokemon']:
                    hit_key.append(k)
                    self.raid_info['raid_eggs'][k]['pokemon'].remove(pokemon)
            hits = '\n'.join(hit_key)
            results.append(f"#{pokemon} {self.get_name(pokemon)} from {hits}")
        results_st = '\n'.join(results)
        await ctx.send(f"**Pokémon removida dos dados de raid**\n{results_st}")

    def add_raid_pkmn(self, level, *raid_pokemon):
        """Adiciona um Pokémon a um determinado nível."""
        added = []
        failed = []
        raid_list = self.raid_info['raid_eggs'][level]['pokemon']
        for pokemon in raid_pokemon:
            if not pokemon.isdigit():
                match = self.pkmn_match(pokemon)[0]
                if not match:
                    failed.append(pokemon)
                    continue
                pokemon = self.get_number(match)
            in_level = self.in_list(pokemon)
            if in_level:
                if in_level == level:
                    continue
                self.raid_info['raid_eggs'][in_level]['pokemon'].remove(pokemon)
            raid_list.append(pokemon)
            added.append(f"#{pokemon} {self.get_name(pokemon)}")
        return (added, failed)

    @raiddata.command(name='adicionar')
    async def add_rd(self, ctx, level, *raid_pokemon):
        """Adiciona os Pokémon fornecidos ao nível determinado
        nos dados da raid.

        Nota: Se for usado um Pokémon com nome composto, envolva-o com aspas duplas:
        Exemplo: !raiddata remover "Mr Mime" Jynx
        """

        if level not in self.raid_info['raid_eggs'].keys():
            return await ctx.send("O nível de raid especificado é inválido.")

        added, failed = self.add_raid_pkmn(level, *raid_pokemon)

        result = []

        if added:
            result.append(
                f"**{len(added)} Pokémon adicionado as raids de nível {level}:**\n"
                f"{', '.join(added)}")

        if failed:
            result.append(
                f"**{len(failed)} registros falharam ao serem adicionados:**\n"
                f"{', '.join(failed)}")

        await ctx.send('\n'.join(result))

    @raiddata.command(name='trocar', aliases=['tr'])
    async def replace_rd(self, ctx, level, *raid_pokemon):
        """Todos os Pokémon fornecidos irão substituir o nível de raid
        nos dados de raid.

        Nota: Se for usado um Pokémon com nome composto, envolva-o com aspas duplas:
        Exemplo: !raiddata remover "Mr Mime" Jynx
        """
        if level not in self.raid_info['raid_eggs'].keys():
            return await ctx.send("Nível de raid especificado é inválido.")
        if not raid_pokemon:
            return await ctx.send("Nenhum Pokémon fornecido.")
        old_data = tuple(self.raid_info['raid_eggs'][level]['pokemon'])
        self.raid_info['raid_eggs'][level]['pokemon'] = []
        added, failed = self.add_raid_pkmn(level, *raid_pokemon)
        if not added:
            self.raid_info['raid_eggs'][level]['pokemon'].extend(old_data)

        result = []

        if added:
            result.append(
                f"**{len(added)} Pokémon adicionado as raids de nível {level}:**\n"
                f"{', '.join(added)}")

        if failed:
            result.append(
                f"**{len(failed)} registros falharam ao serem adicionados:**\n"
                f"{', '.join(failed)}")

        await ctx.send('\n'.join(result))

    @raiddata.command(name='salvar', aliases=['commit'])
    async def save_rd(self, ctx):
        """Salva os dados de raid atuais no arquivo json."""
        for pkmn_lvl in self.raid_info['raid_eggs']:
            data = self.raid_info['raid_eggs'][pkmn_lvl]["pokemon"]
            pkmn_ints = [int(p) for p in data]
            self.raid_info['raid_eggs'][pkmn_lvl]["pokemon"] = pkmn_ints

        with open(ctx.bot.raid_json_path, 'w') as fd:
            json.dump(self.raid_info, fd, indent=4)
        await ctx.message.add_reaction('\u2705')

def setup(bot):
    bot.add_cog(DataHandler(bot))
