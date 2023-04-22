import os 
import sys 
import asyncio
import discord 
from jishaku import Jishaku
from discord.ext import commands

logs = 1081237669171961866
tasks = []
intents = discord.Intents.all()

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

with open('tokens.txt') as f:
    tokens = f.read().splitlines()

if not tokens:
    print('[-] There are no tokens in tokens.txt')
    exit()

async def create_bot(token):
    bot = commands.Bot(command_prefix=".", intents=intents)
    bot.owner_ids = [1098527644993196042]
    await bot.load_extension("jishaku")

    @bot.event
    async def on_ready():
      print(f'{bot.user.name} Is Hosted')
      await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.competing,
          name=f"{len(bot.guilds)} Guilds"
        ),
        status=discord.Status.idle
    )
     
    @bot.event
    async def on_disconnect():
      os.system("kill 1 && python3 main.py")

    @bot.event 
    async def on_guild_join(guild):
      if guild.member_count < 5:
        await guild.leave()
      channel = bot.get_channel(logs)
      await channel.send(embed=discord.Embed(description=f"Joined a guild\nName -> {guild.name}\nMembers -> {guild.member_count}\nTotal Guilds -> {len(bot.guilds)}", color=0000))
     
    @bot.command()
    @commands.is_owner()
    async def restart(ctx):
      os.execl(sys.executable, sys.executable, *sys.argv)
      
    @bot.command()
    @commands.is_owner()
    async def guilds(ctx):
      await ctx.reply(embed=discord.Embed(description=f"{len(bot.guilds)}", color=0000))

    try:
        await bot.login(token)
        await bot.connect()
    except discord.errors.LoginFailure:
        print(f'{token} Is Invalid')

async def main():
    global tasks
    for token in tokens:
        task = asyncio.create_task(create_bot(token))
        tasks.append(task)
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())

    if all(task.done() and task.result() is None for task in tasks):
        print('[+] All Tokens Were Invalid')
