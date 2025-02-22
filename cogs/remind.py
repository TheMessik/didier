import discord
from discord.ext import commands
from decorators import help
from enums.help_categories import Category
from functions.database import remind


class Remind(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Don't allow any commands to work when locked
    def cog_check(self, ctx):
        return not self.client.locked

    @commands.group(name="Remind", aliases=["Remindme"], usage="[Categorie]", case_insensitive=True, invoke_without_command=True)
    @help.Category(Category.Other)
    async def remind(self, ctx):
        """
        Command group to remind the user of a certain thing every day.
        :param ctx: Discord Context
        """
        rows = remind.getOrAddUser(ctx.author.id)

        # TODO use a loop for this when not lazy
        categories = [remind.getIcon(rows[1]) + " Nightly", remind.getIcon(rows[2]) + " Les"]

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Remind Categorieën")
        embed.description = "\n".join(sorted(categories))

        await ctx.send(embed=embed)

    @remind.command(name="Nightly")
    async def nightly(self, ctx):
        """
        Command to get a daily Nightly reminder
        """
        if remind.switchReminder(ctx.author.id, "nightly"):
            await ctx.send("Vanaf nu word je er dagelijks aan herinnerd om Didier Nightly te doen.")
        else:
            await ctx.send("Je zal er niet langer aan herinnerd worden om Didier Nightly te doen.")

    @remind.command(name="Les", aliases=["Class", "Classes", "Sched", "Schedule"])
    async def les(self, ctx):
        """
        Command to get a daily reminder with an embed of your schedule
        """
        if remind.switchReminder(ctx.author.id, "les"):
            await ctx.send("Vanaf nu krijg je dagelijks je lessenrooster toegestuurd.")
        else:
            await ctx.send("Je zal je lessenrooster niet langer toegestuurd krijgen.")


def setup(client):
    client.add_cog(Remind(client))
