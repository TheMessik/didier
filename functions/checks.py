import math

import discord
from discord import utils, Member, User
from discord.ext import commands
from data import constants
import requests
from functions.database import currency


# Checks if caller of a command is me
def isMe(ctx):
    return str(ctx.author.id) == constants.myId


# Checks if the caller of a command is an admin
def isMod(ctx):
    if ctx.guild is None:
        return isMe(ctx)

    return ctx.author.id in constants.mods[ctx.guild.id]


# Checks if a command is allowed to be used in this channel
def allowedChannels(ctx):
    return isMe(ctx) or ctx.channel.type == discord.ChannelType.private or int(ctx.channel.id) in constants.allowedChannels.values()


# TODO find a better way to check for legit links because reddit posts return a 502
def freeGamesCheck(ctx):
    if str(ctx.channel.id) != str(constants.allowedChannels["freegames"]):
        return True

    # Replace newlines with spaces
    noNewLines = ctx.content.replace("\n", " ")

    link = ""
    for word in noNewLines.split(" "):
        if "http" in word and "://" in word:
            link = word.strip()
            break

    if link == "":
        return False
    request = requests.get(link)
    if request.status_code != 200:
        return False

    return True


# Checks if a user can invest/gamble/... [amount]
def isValidAmount(ctx, amount):
    if not amount:
        return [False, "Geef een geldig bedrag op."]
    dinks = float(currency.dinks(ctx.author.id))
    if amount == "all":
        if dinks > 0:
            return [True, dinks]
        else:
            return [False, "Je hebt niet genoeg Didier Dinks om dit te doen."]
    # Check if it's a number <= 0 or text != all
    if (all(char.isalpha() for char in str(amount)) and amount != "all") or \
            (all(char.isdigit() for char in str(abs(int(amount)))) and int(amount) <= 0):
        return [False, "Geef een geldig bedrag op."]
    if int(amount) > dinks:
        return [False, "Je hebt niet genoeg Didier Dinks om dit te doen."]
    return [True, amount]


def pluralS(amount):
    return "s" if round(float(amount)) != 1 else ""
