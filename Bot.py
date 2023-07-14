
import discord
import random

TOKEN = 'Enter_token_here'
client = discord.Client(intents=discord.Intents.default())
GUILD = os.getenv('DISCORD_GUILD')

target_number = random.randint(1, 100)
current_game = None


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global target_number
    global current_game

    if message.author == client.user:
        return

    if message.content.startswith('!start'):
        if current_game is not None:
            await message.channel.send('A game is already in progress. Finish the current game first.')
            return

        target_number = random.randint(1, 100)
        current_game = {
            'player': message.author,
            'score': 0
        }
        await message.channel.send(f'A new game has started! Guess a number between 1 and 100.')

    elif message.content.startswith('!guess'):
        if current_game is None or current_game['player'] != message.author:
            await message.channel.send('No game in progress. Start a new game with !start.')
            return

        try:
            guess = int(message.content.split()[1])
        except (ValueError, IndexError):
            await message.channel.send('Invalid guess. Please provide a valid number.')
            return

        current_game['score'] += 1

        if guess < target_number:
            await message.channel.send('Too low! Guess higher.')
        elif guess > target_number:
            await message.channel.send('Too high! Guess lower.')
        else:
            await message.channel.send(f'Congratulations! You guessed the number in {current_game["score"]} attempts.')
            current_game = None


client.run(TOKEN)
