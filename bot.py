import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot

Bot = commands.Bot(command_prefix='$')
Bot.remove_command('help')


@Bot.event
async def on_ready():
    print('Logged on. Bot made by lyt1x💙#3824')
    await Bot.change_presence(activity=discord.Streaming(name='lyt1x', url='https://www.twitch.tv/lyt1x'))


@Bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild is None:
        return
    await Bot.process_commands(message)


@Bot.command()
async def привязать(ctx, member, role):

    role = role.replace('<', '')
    role = role.replace('>', '')
    role = role.replace('@', '')
    role = role.replace('&', '')
    with open('ids.json', 'r') as f:
        data = json.load(f)
    if str(ctx.guild.id) in data:
        if member in data[str(ctx.guild.id)]:
            await ctx.channel.send('Какая-то роль уже привязана к данному юзеру')
        if not member in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][f'{member}'] = int(role)
            guild = Bot.get_guild(ctx.guild.id)
            rolee = discord.utils.get(guild.roles, id=int(role))
            user = guild.get_member(int(member))
            await user.add_roles(rolee)
            await rolee.edit(name=f'{user}')
            await ctx.channel.send(f'<@&{role}> успешно привязана к <@!{member}>')
            with open('ids.json', 'w') as f:
                json.dump(data, f)
    if not str(ctx.guild.id) in data:
        data[str(ctx.guild.id)] = {}
        if member in data[str(ctx.guild.id)]:
            await ctx.channel.send('Какая-то роль уже привязана к данному юзеру')
        if not member in data[str(ctx.guild.id)]:
            data[str(ctx.guild.id)][f'{member}'] = int(role)
            guild = Bot.get_guild(ctx.guild.id)
            rolee = discord.utils.get(guild.roles, id=int(role))
            user = guild.get_member(int(member))
            await user.add_roles(rolee)
            await rolee.edit(name=f'{user}')
            await ctx.channel.send(f'<@&{role}> успешно привязана к <@!{member}>')
            with open('ids.json', 'w') as f:
                json.dump(data, f)


@Bot.command()
async def переименовать(ctx, name):
    with open('ids.json', 'r') as f:
        data = json.load(f)
    try:
        if str(ctx.author.id) in data[str(ctx.guild.id)]:
            roleid = data[str(ctx.guild.id)][str(ctx.author.id)]
            role = discord.utils.get(ctx.guild.roles, id=roleid)
            await role.edit(name=name)
            await ctx.channel.send(f'Ваша кастомная роль успешно переименована в {name}')
        if str(ctx.author.id) not in data[str(ctx.guild.id)]:
            await ctx.channel.send('К вам не привязана никакая роль')
    except KeyError:
        await ctx.channel.send('На вашем сервере не привязана ни одна роль')


@Bot.command()
async def цвет(ctx, color):
    with open('ids.json', 'r') as f:
        data = json.load(f)
    try:
        if str(ctx.author.id) in data[str(ctx.guild.id)]:
            roleid = data[str(ctx.guild.id)][str(ctx.author.id)]
            role = discord.utils.get(ctx.guild.roles, id=roleid)
            otvet = color
            color = color.replace('#', '0x')
            color = color.lower()
            try:
                colorr = int(color, 0)
                await role.edit(color=discord.Color(colorr))
                await ctx.channel.send(f'Цвет вашей кастомной роли успешно изменен на {otvet}')
            except ValueError:
                await ctx.channel.send('Вы походу немного не то скопировали, убедитесь что ваш строение вашего HEX кода примерно похоже на #BDA2F0 или #FC66D3')
        if str(ctx.author.id) not in data[str(ctx.guild.id)]:
            await ctx.channel.send('К вам не привязана никакая роль')
    except KeyError:
        await ctx.channel.send('На вашем сервере не привязана никакая роль')


@Bot.command()
async def отвязать(ctx, member):
    with open('ids.json', 'r') as f:
        data = json.load(f)
    if str(ctx.author.id) in data[str(ctx.guild.id)]:
        role = data[str(ctx.guild.id)][str(ctx.author.id)]
        member = member.replace('<', '')
        member = member.replace('>', '')
        member = member.replace('@', '')
        member = member.replace('!', '')
        guild = Bot.get_guild(ctx.guild.id)
        rolee = discord.utils.get(ctx.guild.roles, id=int(role))
        user = guild.get_member(int(member))
        await user.remove_roles(rolee)
        for element in data[str(ctx.guild.id)]:
            test = str(ctx.author.id)
            print(element) #378602408424767498
            print(type(element)) #<class 'str'>
            print(test) #378602408424767498
            print(type(test)) #<class 'str'>
            print(data[str(ctx.guild.id)]) #{'378602408424767498': 744509565025910805}
            if element == test:
                data.pop(element)
        await ctx.channel.send(f'<@!{member}> отвязан от кастомной роли <@&{role}>')
        with open('ids.json', 'w') as f:
            json.dump(data, f)
    if str(ctx.author.id) not in data[str(ctx.guild.id)]:
        await ctx.channel.send('Данный юзер не привязан ни к какой роли')


@Bot.command()
async def помощь(ctx):
    emb = discord.Embed(title="Как пользоваться ботом?", color=0xff0000)
    emb.add_field(name='Команды', value='''
    **$привязать <@человек> <@роль>** - привязывает кастомную роль к какому-то человеку (нужна роль модератора)
    **$переименовать <имя>** - переименовывает вашу роль в указанное вами слово. Чтобы написать в больше чем 1 слово используйте $переименовать "имя имя" (ковычки)
    **$цвет <цвет>** - зайдите на https://htmlcolorcodes.com , выберите цвет, скопируйте из поля HEX данные (например #DA7863) и напишите $цвет <то что вы скопировали>
    **$отвязать <@человек>** - отвязывает кастомную роль от какого-то человека (нужна роль модератора)''')
    await ctx.send(embed=emb)


Bot.run('token')
