import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

conn = sqlite3.connect('database.db')
c = conn.cursor()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    c.execute("SELECT id FROM users")
    existing_user_ids = set([row[0] for row in c.fetchall()])

    # loop through all the members in all the guilds the bot is a part of
    for guild in bot.guilds:
        for member in guild.members:
            # check if the member's ID is already in the database
            if member!= bot.user and member.id not in existing_user_ids:
                # insert the new member's ID into the database
                c.execute("INSERT INTO users (id) VALUES (?)", (member.id,))
                conn.commit()
                existing_user_ids.add(member.id)
                
@bot.command(name='courses')
async def show_courses(ctx):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # get all the courses from the database
    c.execute("SELECT id, name FROM courses")
    courses = c.fetchall()

    # create a list of strings representing the courses
    course_list = [f"{course[0]}: {course[1]}" for course in courses]

    # send the course list to the user as a message
    message = await ctx.send("Please select a course to enroll in by clicking on it:\n" + "\n".join(course_list))

    # add reactions to the message for each course
    for i in range(len(courses)):
        await message.add_reaction(f"{i+1}\u20e3")

    # wait for the user to react to the message
    def check(reaction, user):
        return user == ctx.author and reaction.message == message

    reaction, user = await bot.wait_for('reaction_add', check=check)

    # get the index of the selected course
    index = int(str(reaction.emoji)[0]) - 1

    # get the course id from the database
    course_id = courses[index][0]

    # add the enrollment to the database
    c.execute("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", (ctx.author.id, course_id))
    conn.commit()

    # send a confirmation message to the user
    await ctx.send(f"You have enrolled in {courses[index][1]}!")


bot.run(TOKEN)
