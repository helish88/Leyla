import disnake
from disnake.ext import commands


class CapsLockAutoMod(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.content) == 0:
            return
        else:
            percent = (len(list(filter(lambda i: i.isupper(), message.content))) / len(message.content)) * 100

            if await self.bot.config.DB.automod.count_documents({"_id": message.guild.id}) == 0:
                return
            else:
                data = dict(await self.bot.config.DB.automod.find_one({"_id": message.guild.id}))
                
                if message.author.bot:
                    return

                if percent >= data['percent']:
                    if data['admin_ignore']:
                        return

                    match data['action']:
                        case "warn":
                            await self.bot.config.DB.warns.insert_one({"guild": message.guild.id, "member": message.author.id, "reason": "Выключи caps lock! | (Автомодерация)", "warn_id": __import__('random').randint(10000, 99999)})
                        
                        case "ban":
                            await message.author.ban(reason="Caps lock")

                        case "timeout":
                            await message.author.timeout(duration=data['action']['duration'])

                    if not data['message']:
                        pass

                    else:
                        await message.channel.send(data['message'])
                        
                    await message.delete()

def setup(bot):
    bot.add_cog(CapsLockAutoMod(bot))
