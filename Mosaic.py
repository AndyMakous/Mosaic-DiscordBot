from sqlite3.dbapi2 import connect
import discord
from discord.ext import commands
import json
import re
import sqlite3

# Get configuration.json
with open("configuration.json", "r") as config:
    data = json.load(config)
    token = data["token"]
    prefix = data["prefix"]

# Regex to detect URLs
url_regex = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
sites_regex = re.compile('bandcamp|soundcloud|youtube|spotify')

# sqlite3 database and cursor
connection = sqlite3.connect('tracks.db')
cursor = connection.cursor()
create_command = """CREATE TABLE IF NOT EXISTS 
tracks(track_id INTEGER PRIMARY KEY, url TEXT)"""
cursor.execute(create_command)
select_command = 'SELECT * FROM tracks'
# insert_command = f'INSERT INTO tracks VALUES ({message.id},{url.group()})'

class Mosaic(discord.Client):
    async def on_ready(self):
        print(f'{self.user} connected.')
    
    async def on_message(self, message):
        if (message.author == self.user):
            return
        url = url_regex.search(message.content)
        if (url):
            insert_command = f'INSERT INTO tracks VALUES ({message.id},\'{url.group()}\')'
            cursor.execute(insert_command)
            cursor.execute(select_command)
            results = cursor.fetchall()
            await message.channel.send(results)
            await message.add_reaction('🎧')
    

client = Mosaic()
client.run(token)