from discord.ext import commands
import discord
from googletrans import Translator
 
bot = commands.Bot(command_prefix='.')
TOKEN = 'Your Token Here'
translator = Translator()
 
bot.remove_command('help')
 
@bot.event
async def on_ready():
    print(bot.user.name + ' online :D')
 
 
@bot.event
async def on_message(ctx):
    if str(ctx.content).startswith('t '):
        msg = str(ctx.content)[2:]
 
        translation = translator.translate(msg, dest='en')
 
        if translation.src == 'es':
 
            traen = translator.translate(msg, dest='en')
            traja = translator.translate(msg, dest='ja')
 
            embed = discord.Embed(
                title='Spanish detected',
                description = msg,
                color=discord.Colour.gold()
            )
            embed.add_field(name='english', value=traen.text, inline=False)
            embed.add_field(name='japanese', value=traja.text)
            await ctx.channel.send(embed = embed)
 
        elif translation.src == 'en':
 
            traes = translator.translate(msg, dest='es')
            traja = translator.translate(msg, dest='ja')
 
            embed = discord.Embed(
                title='English detected',
                description = msg,
                color=discord.Colour.blue()
            )
            embed.add_field(name='spanish', value=traes.text, inline=False)
            embed.add_field(name='japanese', value=traja.text)
            await ctx.channel.send(embed = embed)
 
        elif translation.src == 'ja':
 
            traes = translator.translate(msg, dest='es')
            traen = translator.translate(msg, dest='en')
 
            embed = discord.Embed(
                title='Japanese detected',
                description = msg,
                color=discord.Colour.red()
            )
            embed.add_field(name='spanish', value=traes.text, inline=False)
            embed.add_field(name='english', value=traen.text)
            await ctx.channel.send(embed = embed)