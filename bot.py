import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

user_data = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name} 已连接')
    
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name}，和我们一起写出一个人工智障吧喵！'
    )
    
@bot.command(name='add')
async def add_data(ctx):
    # Get today's date
    today = datetime.date.today()

    # Send a message prompting the user to enter the date
    await ctx.send("主人的作业哪天due呢喵~? (YYYY-MM-DD)")

    # Define a check function to make sure the response is from the same user and the date is later than today
    def check(message):
        try:
            date_str = message.content.strip()
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            return message.author == ctx.author and date_obj > today
        except ValueError:
            return False

    # Wait for the user to enter the date as a separate message
    response = await bot.wait_for('message', check=check)

    # Convert the user's response to a date object
    date_str = response.content.strip()
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

    # Check if the user is already in the dictionary
    if str(ctx.author.id) not in user_data:
        user_data[str(ctx.author.id)] = []

    # Add the date to the user's list of dates
    user_data[str(ctx.author.id)].append(date_obj)

    # Print the user's data
    print(user_data)
    await ctx.send(date_str + " 已经添加了喵~")
    
@bot.command(name='remove')
async def remove_data(ctx):
    # Check if the user has any data stored
    if str(ctx.author.id) not in user_data:
        await ctx.send("已经一滴都不剩了喵。。。")
        return

    # Send a message prompting the user to choose a date to remove
    user_dates = user_data[str(ctx.author.id)]
    date_strs = [date.strftime("%Y-%m-%d") for date in user_dates]
    date_options = "\n".join([f"{i+1}. {date_strs[i]}" for i in range(len(date_strs))])
    await ctx.send(f"主人要去掉哪一个日期呢喵~?\n{date_options}")

    # Define a check function to make sure the response is from the same user and that it is a valid choice
    def check(message):
        return message.author == ctx.author and message.content.isdigit() and 0 < int(message.content) <= len(user_dates)

    # Wait for the user to choose a date to remove
    response = await bot.wait_for('message', check=check)

    # Remove the chosen date from the user's list of dates
    chosen_index = int(response.content) - 1
    chosen_date = user_dates.pop(chosen_index)

    # Print the user's data
    print(user_data)
    await ctx.send(f"{chosen_date.strftime('%Y-%m-%d')} 已移除喵~")

@bot.command(name='due')
async def calculate_due(ctx):
    # Check if the user has any data stored
    if str(ctx.author.id) not in user_data:
        await ctx.send("主人还没有存日期呢喵~")
        return

    # Calculate the remaining time from today to each stored date and send a message with the results
    today = datetime.datetime.today()
    user_dates = user_data[str(ctx.author.id)]
    results = []
    for date in user_dates:
        date_with_time = datetime.datetime.combine(date, datetime.time.min)
        delta = date_with_time - today
        days = delta.days
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        results.append(f"{date.strftime('%Y-%m-%d')}: 主人还剩 {days} 天 {hours} 小时 {minutes} 分钟喵~")
    message = "\n".join(results)
    await ctx.send(message)
    
bot.run(TOKEN)
