#!usr/bin/python3

from datetime import datetime, timedelta, date
import os
import asyncio
import discord
from discord.ext import commands

TOKEN = 'token'
bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
adminChatId = 706096301045055580
adminRole = 608608975981903873
channelId = 607849606532956161
subRole = 739058520955289650

fileName = 'subs.txt'
subs = {}


async def ripSub(userId):
    await bot.get_channel(adminChatId).send(f'La sub de {bot.get_user(int(userId))} ha caducado')
    await bot.get_guild(channelId).get_member(int(userId)).remove_roles(discord.utils.get(bot.get_guild(channelId).roles, id=subRole))
    updateFileRemove(userId)
    updateDict()


async def timeLeft():
    with open(fileName, 'r') as f:
        list1 = f.read().split('\n')

    for line in list1:
        if line != '':
            d1 = date(int(line.split()[1].split('-')[0]), int(line.split()[1].split('-')[1]), int(line.split()[1].split('-')[2]))
            d2 = date(int(str(datetime.today()).split()[0].split('-')[0]), int(str(datetime.today()).split()[0].split('-')[1]), int(str(datetime.today()).split()[0].split('-')[2]))
            if (d2 - d1).days * -1 <= 0:
                await ripSub(line.split()[0])


def updateFileAdd(userId, date1):
    with open(fileName, 'a') as f:
        f.write(f'\n{userId} {date1}')


def updateFileRemove(userId):
    updatedList = ''

    with open(fileName, 'r') as f:
        list1 = f.read().split('\n')

    for line in list1:
        if line != '':
            if line.split()[0] != userId:
                updatedList += line

    with open(fileName, 'w') as f:
        f.write(updatedList)


def updateDict():
    subs.clear()
    with open(fileName, 'r') as f:
        list1 = f.read().split('\n')

    if list1 != ['']:
        for line in list1:
            if line != '':
                subs[line.split()[0]] = line.split()[1]


@bot.event
async def on_ready():
    print(bot.user.name + ' iniciado :D')
    if not os.path.isfile(fileName):
        with open(fileName, 'w') as f:
            f.write('')

    else:
        updateDict()


@bot.command()
async def add(ctx, user='', subTime=''):
    if str(adminRole) in (', '.join(str(role.id) for role in ctx.author.roles)):
        if user == '' or subTime == '' or len(ctx.message.content.split(' ')) > 3:
            await ctx.send('Uso: .add @mencion meses\nej: .add @Kahzerx 1', delete_after=5)

        else:
            try:
                if not isinstance(int(subTime), int):
                    await ctx.send('Introduce un número ;-;', delete_after=3)

                else:
                    new_date = str(datetime.today() + timedelta(int(subTime) * 30)).split(' ')[0]
                    if user[3:-1] in subs:
                        await ctx.send('Ya tenía el rol, sobreescribiendo fecha...', delete_after=3)
                        await bot.get_channel(adminChatId).send(
                            f'Fecha de {bot.get_user(int(user[3:-1]))} sobreescrita, su rol caduca el {new_date}')
                        updateFileRemove(user[3:-1])
                    else:
                        await ctx.message.mentions[0].add_roles(discord.utils.get(ctx.guild.roles, id=subRole))
                        await ctx.send('Rol añadido', delete_after=3)
                        await bot.get_channel(adminChatId).send(
                            f'{bot.get_user(int(user[3:-1]))} añadido, su rol caduca el {new_date}')
                    updateFileAdd(user[3:-1], new_date)
                    updateDict()

            except:
                await ctx.send('No ha sido posible asignar el rol, revisa el comando :(', delete_after=3)

    else:
        await ctx.send(f'{ctx.author.mention} necesitas ser admin :P', delete_after=2)

    await ctx.message.delete()


@bot.command()
async def remove(ctx, user=''):
    if str(adminRole) in (', '.join(str(role.id) for role in ctx.author.roles)):
        if user == '' or len(ctx.message.content.split(' ')) > 3:
            await ctx.send('Uso: .remove @mencion\nej: .remove @Kahzerx', delete_after=5)

        else:
            try:
                if user[3:-1] in subs:
                    updateFileRemove(user[3:-1])
                    await ctx.message.mentions[0].remove_roles(discord.utils.get(ctx.guild.roles, id=subRole))
                    await ctx.send('Rol eliminado', delete_after=3)
                    await bot.get_channel(adminChatId).send(f'{bot.get_user(int(user[3:-1]))} eliminado')
                    updateDict()

                else:
                    await ctx.send('No tenía el rol', delete_after=3)

            except:
                await ctx.send('No ha sido posible eliminar el rol, revisa el comando :(', delete_after=3)

    else:
        await ctx.send(f'{ctx.author.mention} necesitas ser admin :P', delete_after=2)

    await ctx.message.delete()


@bot.event
async def on_message(ctx):

    if ctx.author == bot.user:
        return

    await bot.process_commands(ctx)


async def checkDate():
    await bot.wait_until_ready()
    await asyncio.sleep(2)
    while not bot.is_closed():
        print(subs)
        await timeLeft()
        await asyncio.sleep(10)


bot.loop.create_task(checkDate())
bot.run(TOKEN)

