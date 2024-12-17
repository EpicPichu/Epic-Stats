import discord, asyncio, time
from discord import app_commands, Interaction as inter
from discord.ext import commands
from main.tebex_req import req


class money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="money", description="Verify coupon codes for pika store")
    async def money(self, intr: inter,
    basket: str,
    coupon1: str,
    coupon2: str,
    coupon3: str
    ):
        await intr.response.send_message("Fetching...")
        start = time.time()

        basket_id = basket[21:-13]

        #combinations 
        c1 = (f"{coupon1}-{coupon2}-{coupon3}")
        c2 = (f"{coupon1}-{coupon3}-{coupon2}")
        c3 = (f"{coupon2}-{coupon1}-{coupon3}") 
        c4 = (f"{coupon2}-{coupon3}-{coupon1}") 
        c5 = (f"{coupon3}-{coupon1}-{coupon2}") 
        c6 = (f"{coupon3}-{coupon2}-{coupon1}") 

        combinations = [c1, c2, c3, c4, c5, c6]

        async def asyncrun(basket, codes):
            results = await asyncio.gather(*[req(basket, code) for code in codes])
            return results


        result = await asyncrun(basket_id, combinations)

        output = '''Result:
        '''

        for code, details in result:
            output += (f"{details}\n```{code}```\n")

        end = time.time()
        taim = round(end - start, 3)

        await intr.edit_original_response(content=f"Fetching took {taim} seconds\n{output}")



async def setup(bot):
    await bot.add_cog(money(bot))
