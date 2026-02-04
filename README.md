# Discord-C2-POC: Malware Mechanics Study

A Proof-of-Concept (POC) Command and Control (C2) written in Python, demonstrating how legitimate communication channels (Discord API) can be used for remote administration and firewall evasion.

**⚠️ DISCLAIMER: FOR EDUCATIONAL PURPOSES ONLY**
This repository is a research project designed to understand the internal mechanics of Command & Control (C2) infrastructure. It is strictly for educational purposes to demonstrate how malware interacts with operating systems and external APIs "under the hood."
**Do not use this code on systems you do not own.** The author takes no responsibility for misuse.

## 📖 Project Overview

The goal of this project is to deconstruct how modern malware operates by building a functional Proof-of-Concept (POC) from scratch. Rather than using pre-made tools (like Metasploit).

This tool demonstrates that by using the Discord API, command traffic appears as legitimate HTTPS traffic to `discord.com`, effectively bypassing standard firewall rules and network monitoring.

## 🚀 Usage & Build Instructions

### Prerequisites

- Python 3.8+
- A Discord Bot Token (Developer Portal)

### Configuration

1.  Clone the repository:
    ```bash
    git clone https://github.com/paulustimothy/Beginner-Discord-C2-POC.git
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Bot Setup:**
    - Create a new Application in the [Discord Developer Portal](https://discord.com/developers/applications).
    - **Bot Tab:** Enable "Message Content Intent" ✅.
    - **OAuth2 > URL Generator:** Select `bot`.
    - **Bot Permissions:** Select `Send Messages` and `Manage Channels`.
    - Copy the generated URL to invite the bot to your private server.
    - **Bot Tab:** Click "Reset Token" and copy the new token.

### Building the Binary

To compile the agent into a standalone executable for testing in a VM:

```bash
pyinstaller --onefile --noconsole bot.py
```
