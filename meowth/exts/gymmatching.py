import os
import json

from discord.ext import commands

from meowth import utils

class GymMatching:
    def __init__(self, bot):
        self.bot = bot
        self.gym_data = self.init_json()

    def init_json(self):
        with open(os.path.join('data', 'gym_data.json')) as fd:
            return json.load(fd)

    def get_gyms(self, guild_id):
        return self.gym_data.get(str(guild_id))

    def gym_match(self, gym_name, gyms):
        return utils.get_match(list(gyms.keys()), gym_name)

    @commands.command(hidden=True)
    async def gym_match_test(self, ctx, gym_name):
        gyms = self.get_gyms(ctx.guild.id)
        if not gyms:
            await ctx.send('Correspondência de ginásios não foi definida para esse servidor.')
            return
        match, score = self.gym_match(gym_name, gyms)
        if match:
            gym_info = gyms[match]
            coords = gym_info['coordinates']
            gym_info_str = (f"**Coordenadas:** {coords}")
            await ctx.send(f"Correspondência bem-sucedida `{match}` "
                           f"com uma pontuação de `{score}`\n{gym_info_str}")
        else:
            await ctx.send("Nenhuma correspondência encontrada.")

def setup(bot):
    bot.add_cog(GymMatching(bot))
