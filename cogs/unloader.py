from discord import app_commands, Interaction
from discord.ext import commands 

class unload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def extension_autocomplete(self, intrc: Interaction, current: str):
        """Autocomplete function for extension names."""
        cogs = [extension.replace('cogs.', '') for extension in self.bot.extensions]

        return [
            app_commands.Choice(name=cog, value=cog)
            for cog in cogs if cog.startswith(current)
        ][:5]

    @app_commands.command(name='unload', description='Unload an extension')
    @app_commands.describe(extension='Specify the extension to unload')
    @app_commands.autocomplete(extension=extension_autocomplete)
    async def unload(self, intrc: Interaction, extension: str):
        """Unload a specific extension."""
        try:
            await self.bot.unload_extension(f'cogs.{extension}')
            await self.bot.tree.sync()
            await intrc.response.send_message(f'Unloaded `{extension}`.')
        except Exception as e:
            await intrc.response.send_message(f'Failed to unload `{extension}`: {str(e)}')

async def setup(bot):
    await bot.add_cog(unload(bot))
