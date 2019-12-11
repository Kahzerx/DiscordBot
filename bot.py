from discord.ext import commands
import discord
from mcstatus import MinecraftServer
import sys
import os

bot = commands.Bot(command_prefix='.')
client = discord.Client()
TOKEN = 'tutoken'
imagenLH = 'https://cdn.discordapp.com/icons/392285907195002880/6894fa91cf7c1d3559f260599d57c98f.png'
server = MinecraftServer.lookup("ipserver")
trusted = 'adminrolename'
rol_conect = 653623812343988248
rol_member = 654095858958336021
canal_welcome = 653656543685771304

print('Iniciando bot...')

bot.remove_command('help')


@bot.event
async def on_ready():
    print(bot.user.name + ' iniciado :D')


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {round(bot.latency * 1000)}ms')


@bot.command()
async def help(ctx):
    comandos = ['.clear[admin_only]', '.encuesta', '.member[admin_only]', '.online', '.ping', '.reload[admin_only]', '.removerole[admin_only]']
    msg = '\n'.join(comandos)
    embed = discord.Embed(
        title='Comandos disponibles:\n\n' + msg,
        color=discord.Colour.blue()
    )
    embed.set_author(name='LastHope Unity', icon_url=imagenLH)
    await ctx.send(embed=embed)


@bot.command()
async def encuesta(ctx, mensaje='nada'):
    if mensaje == 'nada':
        await ctx.send('Por favor, especifica un tema')
    else:
        subrayado = ''
        msg = mensaje
        for characters in msg:
            subrayado += '▔'

        if subrayado > '▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔':
            subrayado = '▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔'

        embed = discord.Embed(
            title='Pregunta:\n' + msg + '\n' + subrayado,
            color=discord.Colour.blue()
        )

        embed.set_author(name='LastHope Unity', icon_url=imagenLH)
        embed.add_field(name='opcion 1', value='1\u20e3 Si', inline=True)
        embed.add_field(name='opcion 2', value='2\u20e3 No', inline=True)

        sent = await ctx.send(embed=embed)
        await sent.add_reaction('1\u20e3')
        await sent.add_reaction('2\u20e3')


@bot.command()
async def clear(ctx, cantidad=0):
    verificado = False
    for a in ctx.author.roles:
        if str(a) == trusted:
            verificado = True
    if verificado:
        await ctx.channel.purge(limit=cantidad)
        if cantidad == 0:
            await ctx.send('Especifica una cantidad')

    else:
        await ctx.send('No estas verificado para ejecutar este comando')


@bot.command()
async def reload(ctx):
    verificado = False
    for a in ctx.author.roles:
        if str(a) == trusted:
            verificado = True
    if verificado:
        await ctx.send('Reiniciando...')
        python = sys.executable
        os.execl(python, python, * sys.argv)
    else:
        await ctx.send('No estas verificado para ejecutar este comando')


@bot.command()
async def online(ctx):
    status = server.status()
    query = server.query()
    msg = '\n'.join(query.players.names)
    if status.players.online == 0:
        embed = discord.Embed(
            title='No hay jugadores conectados :( ',
            color=discord.Colour.blue()
        )
        embed.set_author(name='LastHope Unity', icon_url=imagenLH)
    elif status.players.online == 1:
        embed = discord.Embed(
            title='Jugador conectado:',
            description=msg,
            color=discord.Colour.blue()
        )
        embed.set_author(name='LastHope Unity', icon_url=imagenLH)
    elif status.players.online > 1:
        embed = discord.Embed(
            title='Jugadores conectados:',
            description=msg,
            color=discord.Colour.blue()
        )
        embed.set_author(name='LastHope Unity', icon_url=imagenLH)

    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def member(ctx):
    verificado = False
    for a in ctx.author.roles:
        if str(a) == trusted:
            verificado = True
    if verificado:
        role = discord.utils.get(ctx.guild.roles, id=rol_member)
        await ctx.message.mentions[0].add_roles(role)
        await ctx.send('rol añadido a ' + ctx.message.mentions[0].mention)
    else:
        await ctx.send('No estas verificado para ejecutar este comando')


@bot.command(pass_context=True)
async def removerole(ctx):
    verificado = False
    for a in ctx.author.roles:
        if str(a) == trusted:
            verificado = True
    if verificado:
        role = discord.utils.get(ctx.guild.roles, id=rol_member)
        await ctx.message.mentions[0].remove_roles(role)
        await ctx.send('rol eliminado de ' + ctx.message.mentions[0].mention)
    else:
        await ctx.send('No estas verificado para ejecutar este comando')



@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, id=rol_conect)
    await member.add_roles(role)

    embed = discord.Embed(
        title='¿Quieres formar parte de LastHope?',
        description='Si te interesa formar parte de LastHope sigue estos pasos!',
        color=discord.Colour.blue()
    )
    embed.set_author(name='LastHope Unity', icon_url=imagenLH)
    embed.add_field(name='Entrevista',
                    value='Si quieres unirte al servidor de LastHope, tienes que comunicarte con un administrador y '
                          'preguntale cuando te podría hacer una entrevista para poder formar parte de LastHope',
                    inline=True)
    embed.add_field(name='Recomendación',
                    value='Pasate algunas veces de la semana para hablar con los miembros y que ellos tengan una '
                          'buena perspectiva sobre tí',
                    inline=True)
    embed.add_field(name='Requisitos',
                    value='Tener minecraft premium, tener twitter, tener microfono, pasarte de vez en cuando a '
                          'charlar con los otros miembros (En el caso de que entres al servidor)',
                    inline=True)

    await member.send(embed=embed)

    canal = bot.get_channel(canal_welcome)
    await canal.send('¡Bienvenido a LastHope ' + member.mention + ' esperemos que sea de tu agrado! **Revisa tus '
                                                                  'mensajes privados para más información.** '
                                                                  ':mailbox_with_mail: ')


bot.run(TOKEN)
