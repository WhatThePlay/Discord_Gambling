import time
from random import Random

from discord.ext import commands
from discord.ext.commands import CommandNotFound

from blackJack import DeckList
from blackJack import count_value
from blackJack import deal_card
from blackJack import reset_game
from blackJack import tostring

random = Random()

# client = discord.Client()
TOKEN = ""
GUILD = ""
CHANNEL_ID = 0

# give the bot it's designated prefix for commands
client = commands.Bot(command_prefix='$')


# prints the servers its connected to to the console and sends a "welcome" message to the intended channel
@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Hello friends. My name is Doug. I am your dealer for today.\nIf you want to start a round of "
                       "Blackjack simply type \"$blackjack\"")

# creates both hands and the deck for the methods to use
player_hand = []
dealer_hand = []
random_deck_list = random.sample(DeckList, len(DeckList))


# starts the game
@client.command()
async def blackjack(ctx):
    deal_card(random_deck_list, dealer_hand)
    deal_card(random_deck_list, player_hand)
    deal_card(random_deck_list, player_hand)
    await ctx.send("Your game will now begin")
    await ctx.send("Dealer Hand = " + tostring(dealer_hand)
                   + "\nPlayer Hand = " + tostring(player_hand)
                   + "\nDealer Value = " + str(count_value(dealer_hand))
                   + "\nPlayer Value = " + str(count_value(player_hand))
                   + "\nDo you want to hit ($h) or do you want to stand ($s)?")


# allows you to pull a card and then decide again
@client.command()
async def h(ctx):
    if player_hand:
        deal_card(random_deck_list, player_hand)
        await ctx.send("Player Hand = " + tostring(player_hand)
                       + "\nPlayer Value = " + str(count_value(player_hand)))
        await ctx.send("Do you want to hit ($h) or do you want to stand ($s)?")
        if count_value(player_hand) > 21:
            await ctx.send("You bust!\nGame Over!")
            reset_game(player_hand, dealer_hand, random_deck_list, (random.sample(DeckList, len(DeckList))))
    else:
        await ctx.send("You haven't started a game yet!\nType \"$blackjack\" to start a game!")


# let's the game play out after your hand is fixed
@client.command()
async def s(ctx):
    if player_hand:
        await ctx.send("You stand with:\nPlayer Hand = " + tostring(player_hand) + "\nPlayer Value = " + str(
            count_value(player_hand)))
        await ctx.send("Doug is now drawing!")
        while count_value(dealer_hand) < 17:
            deal_card(random_deck_list, dealer_hand)
            time.sleep(1)
            await ctx.send("Dealer Hand = " + tostring(dealer_hand)
                           + "\nDealer Value = " + str(count_value(dealer_hand)))
            if count_value(dealer_hand) > 21:
                await ctx.send("Doug bust!\nYou Win!")
                reset_game(player_hand, dealer_hand, random_deck_list, (random.sample(DeckList, len(DeckList))))
                return
                # Both the dealer and player have a valid Hand and stand
        if count_value(player_hand) < count_value(dealer_hand):
            await ctx.send("Doug has the better hand!\nYou Lose!")
        elif count_value(player_hand) > count_value(dealer_hand):
            await ctx.send("You have the better hand!\nYou Win!")
        else:
            await ctx.send("Your hands are equally good!\nIt's a Tie!")
        reset_game(player_hand, dealer_hand, random_deck_list, (random.sample(DeckList, len(DeckList))))
    else:
        await ctx.send("You haven't started a game yet!\nType \"blackjack\" to start a game!")


# some simple methods to get the different variables that are used
@client.command()
async def dealer(ctx):
    await ctx.send("Dealer Hand = " + tostring(dealer_hand))
    await ctx.send("Dealer Value = " + str(count_value(dealer_hand)))


@client.command()
async def player(ctx):
    await ctx.send("Player Hand = " + tostring(player_hand))
    await ctx.send("Player Value = " + str(count_value(player_hand)))


@client.command()
async def deck(ctx):
    await ctx.send(str(len(random_deck_list)) + " " + str(random_deck_list[0]))


# catches the error when a command is entered that doesn't exist and sends a message
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send("That must have been a mistake my friend.\nThat command doesn't exist!")
        return
    raise error


client.run(TOKEN)
