import json
import os
from dotenv import load_dotenv
import datetime
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

courses = {
    "Professional Computing Practic": ["2023-05-12", "2023-05-26"],
    "Further Programming": ["N/A"],
    "Foundations of Artificial Intelligence for STEM": ["2023-04-07", "2023-05-12", "2023-06-02"],
    "Introduction to Cybersecurity": ["N/A"]
}

user_data = {}

# Load user data from file if exists
if os.path.isfile('user_data.json'):
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)

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
    # Check if the user is already in the dictionary
    if str(ctx.author.id) not in user_data:
        user_data[str(ctx.author.id)] = []

    # Prompt the user to select a course
    course_options = "\n".join([f"{i+1}. {course}" for i, course in enumerate(courses)])
    await ctx.send(f"主人，请选择要添加的课程喵：\n{course_options}")

    # Define a check function to make sure the response is from the same user and that it is a valid choice
    def check(message):
        return message.author == ctx.author and message.content.isdigit() and 0 < int(message.content) <= len(courses)

    # Wait for the user to choose a course
    response = await bot.wait_for('message', check=check)

    # Get the chosen course and add it to the user's list of courses
    chosen_index = int(response.content) - 1
    chosen_course = list(courses.keys())[chosen_index]
    user_data[str(ctx.author.id)].append(chosen_course)

    # Print the user's data
    print(user_data)

    # Write updated user data to file
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    await ctx.send(f"{chosen_course} 已经添加了喵~")
    
@bot.command(name='remove')
async def remove_data(ctx):
    # Check if the user is in the dictionary and has added any courses
    if str(ctx.author.id) not in user_data or not user_data[str(ctx.author.id)]:
        await ctx.send("你还没有添加过课程喵~")
        return

    # Show the user's current list of courses
    current_courses = "\n".join([f"{i+1}. {course}" for i, course in enumerate(user_data[str(ctx.author.id)])])
    await ctx.send(f"主人，以下是您当前添加的课程喵：\n{current_courses}")

    # Define a check function to make sure the response is from the same user and that it is a valid choice
    def check(message):
        return message.author == ctx.author and message.content.isdigit() and 0 < int(message.content) <= len(user_data[str(ctx.author.id)])

    # Wait for the user to choose a course
    response = await bot.wait_for('message', check=check)

    # Get the chosen course and remove it from the user's list of courses
    chosen_index = int(response.content) - 1
    chosen_course = user_data[str(ctx.author.id)][chosen_index]
    user_data[str(ctx.author.id)].remove(chosen_course)

    # Print the user's data
    print(user_data)

    # Write updated user data to file
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

    await ctx.send(f"{chosen_course} 已经从您的课程列表中移除了喵~")

@bot.command(name='due')
async def show_due_dates(ctx):
    # Check if the user has added any courses
    if str(ctx.author.id) not in user_data or not user_data[str(ctx.author.id)]:
        await ctx.send("你还没有添加过课程喵~")
        return

    # Iterate over the user's courses and calculate the remaining time to the first due date
    remaining_times = []
    for course_name in user_data[str(ctx.author.id)]:
        due_dates = courses[course_name]
        if due_dates[0] == "N/A":
            remaining_times.append(f"{course_name}: 没有截止日期喵~")
        else:
            first_due_date = datetime.datetime.strptime(due_dates[0], "%Y-%m-%d")
            remaining_time = first_due_date - datetime.datetime.now()
            remaining_time_str = f"{remaining_time.days}天{remaining_time.seconds//3600}小时{(remaining_time.seconds//60)%60}分钟"
            remaining_times.append(f"{course_name}: 距离第一个截止日期还有{remaining_time_str}")

    # Send the remaining time for each course as a message
    await ctx.send("\n".join(remaining_times))
    
bot.run(TOKEN)
