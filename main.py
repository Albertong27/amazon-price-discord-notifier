import requests, configparser
import asyncio
from bs4 import BeautifulSoup
import discord, json, time

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config.get('Discord', 'bot_token')
channel_id = int(config.get('Discord', 'channel_id'))

item_file_path = 'items.json'

with open(item_file_path, 'r') as f:
    items = json.load(f)

for i in range(len(items)):
    items[i]['id'] = i + 1

def save_items():
    with open(item_file_path, 'w') as f:
        json.dump(items, f)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    while(True):
        for item in items:
            try:
                response = requests.get(item['url'])
                soup = BeautifulSoup(response.content, 'html.parser')
                
                title = soup.find('span', {'id': 'productTitle'}).text.strip()
                out_of_stock_tag = soup.find('div', {'id': 'outOfStock'})
                if out_of_stock_tag is not None :
                    if 'Temporarily out of stock' in out_of_stock_tag.text:
                        channel = client.get_channel(channel_id)
                        if channel is not None:
                            await channel.send(f"Item {title} is currently out of stock !")
                        continue
                price = float(soup.find('span', {'class': 'a-offscreen'}).text.replace('S$', ''))
                
                if 'history' not in item: item['history'] = []
                item['history'].append({'timestamp': time.time(), 'price': price})
                save_items()
            except:
                print("Something Wrong at main checker loop")
                continue
            if price < item['threshold']:
                channel = client.get_channel(channel_id)
                message = f"The price for {title} has dropped to ${price}."
                if channel is not None:
                    await channel.send(message)
        await asyncio.sleep(60*60*6)

@client.event
async def on_message(message):
    if message.channel.id == channel_id and message.author != client.user:
        if message.content.startswith('!add'):
            try:
                url = message.content.split(' ')[1]
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                title_tag = soup.find('span', {'id': 'productTitle'})
                price_tag = soup.find('span', {'class': 'a-offscreen'})
                if title_tag is not None and price_tag is not None:
                    title = title_tag.text.strip()
                    price = float(soup.find('span', {'class': 'a-offscreen'}).text.replace('S$', ''))
                    item = {'id': len(items) + 1, 'name': title, 'url': url, 'threshold': price, 'history': []}
                    items.append(item)
                    save_items()
                    await message.channel.send(f"Item '{title}' has been added with a threshold of S${price:.2f}")
                else:
                    await message.channel.send("Failed to extract product title and/or price - is none")
            except IndexError:
                await message.channel.send("Please provide a valid Amazon URL")
            except ValueError:
                await message.channel.send("Failed to extract price from Amazon page - is value error")
        elif message.content.startswith('!remove'):
            try:
                item_id = int(message.content[8:])
                item = next((x for x in items if x['id'] == item_id), None)
                if item:
                    items.remove(item)
                    await message.channel.send(f"Removed Amazon item <{item['url']}>")
                    save_items()
                else:
                    await message.channel.send("Invalid item ID")
            except ValueError:
                await message.channel.send("Invalid item ID")
        elif message.content.startswith('!list'):
            message_text = "Amazon items:\n"
            for item in items:
                message_text += f"{item['id']}. <{item['url']}> (threshold: ${item['threshold']})\n"
            await message.channel.send(message_text)
        elif message.content.startswith('!threshold'):
            try:
                parts = message.content.split()
                item_id = int(parts[1])
                new_threshold = float(parts[2])
                item = next((x for x in items if x['id'] == item_id), None)
                if item:
                    item['threshold'] = new_threshold
                    await message.channel.send(f"Price threshold updated to ${new_threshold} for item {item_id} (<{item['url']}>)")
                    save_items()
                else:
                    await message.channel.send("Invalid item ID")
            except (ValueError, IndexError):
                await message.channel.send("Invalid item ID or threshold")
        elif message.content.startswith('!ping'):
            await message.channel.send("Pong!")
        elif message.content.startswith('!help'):
            await message.channel.send("!ping, !add, !remove, !threshold")
        elif message.content.startswith('!history'):
            try:
                item_id = int(message.content[9:])
                item = next((x for x in items if x['id'] == item_id), None)
                if item and 'history' in item:
                    # Send a message with the item's price history
                    message_text = f"Price history for {item['url']}:\n"
                    for price in item['history']:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(price['timestamp'] + 28800))
                        message_text += f"{timestamp}: S${price['price']:.2f}\n"
                    await message.channel.send(message_text)
                else:
                    await message.channel.send("Invalid item ID or no price history available")
            except ValueError:
                await message.channel.send("Invalid item ID")

async def main():
    await client.start(bot_token)
asyncio.run(main())