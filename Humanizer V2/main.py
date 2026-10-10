import os
import sys
import time
import re
import socket
import asyncio
import base64
from tls_client import Session
import httpx
import json
from datetime import datetime
from colorama import init, Fore, Style
from pystyle import Center, Colorate, Colors
from dateutil.parser import isoparse
from datetime import datetime, timezone
import random
import base64
import aiohttp
import websocket
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Set up event loop policy to handle cleanup properly
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Store a single event loop instance
_event_loop = None

def get_event_loop():
    """Get or create a single event loop instance"""
    global _event_loop
    if _event_loop is None or _event_loop.is_closed():
        _event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_event_loop)
    return _event_loop

init(autoreset=True)
sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

ORANGE = "\033[38;2;238;108;0m"

config = {}
customization = {}
loaded_counts = {
    "Tokens": 0,
    "Pronouns": 0,
    "Bios": 0,
    "Global Names": 0,
    "Profile Pictures": 0,
    "Banners": 0,
    "Statuses": 0
}

ratelimited_proxies = defaultdict(int)
ratelimited_accounts = defaultdict(int)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_console_title(title="Discord Humanizer By Setting Guide"):
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end='', flush=True)

def vg(lines, start_rgb=(0, 255, 200), end_rgb=(0, 100, 180)):
    total = len(lines)
    result = []
    for i, line in enumerate(lines):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i // max(1, total - 1)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i // max(1, total - 1)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i // max(1, total - 1)
        result.append(f'\033[38;2;{r};{g};{b}m{line}\033[0m')
    return result

def ascii_nig():
    clear_console()
    
    if os.name == 'nt':
        os.system('chcp 65001 >nul')
    
    ascii_art = [
        "██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗██╗███████╗███████╗██████╗ ",
        "██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║██║╚══███╔╝██╔════╝██╔══██╗",
        "███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║██║  ███╔╝ █████╗  ██████╔╝",
        "██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║ ███╔╝  ██╔══╝  ██╔══██╗",
        "██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║██║███████╗███████╗██║  ██║",
        "╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝",
        "Support Server: .gg/836mYHnxpk                       Developer: @alyahex1"
    ]

    try:
        width = os.get_terminal_size().columns
    except:
        width = 80

    print('\n' * 2)
    colored_lines = vg(ascii_art, start_rgb=(255, 20, 147), end_rgb=(255, 182, 193))

    for line in colored_lines:
        centered_line = line.center(width) if width else line
        print(centered_line)
        time.sleep(0.1)

    print('\n' * 2)


def current_time():
    return f"{Fore.LIGHTBLACK_EX}{datetime.now().strftime('')}{Style.RESET_ALL}"

def log(message_type, message, color=Fore.WHITE):
    type_styles = {
        "SUCCESS": f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}SUCCESS{Fore.WHITE}]{Style.RESET_ALL}",
        "UPDATED": f"{Fore.WHITE}[{Fore.MAGENTA}UPDATED{Fore.WHITE}]{Style.RESET_ALL}",
        "ERROR": f"{Fore.WHITE}[{Fore.LIGHTRED_EX}ERROR{Fore.WHITE}]{Style.RESET_ALL}",
        "WARNING": f"{Fore.WHITE}[{Fore.LIGHTMAGENTA_EX}WARNING{Fore.WHITE}]{Style.RESET_ALL}",
        "INFO": f"{Fore.WHITE}[{ORANGE}INFO{Fore.WHITE}]{Style.RESET_ALL}",
        "RETRY": f"{Fore.WHITE}[{Fore.LIGHTYELLOW_EX}RETRY{Fore.WHITE}]{Style.RESET_ALL}",
        "RATELIMIT": f"{Fore.WHITE}[{Fore.RED}RATELIMIT{Fore.WHITE}]{Style.RESET_ALL}",
        "START": f"{Fore.WHITE}[{Fore.CYAN}STARTING{Fore.WHITE}]{Style.RESET_ALL}"
    }

    styled_type = type_styles.get(message_type, f"[{message_type}]")

    if message_type == "UPDATED" and ":" in message:
        parts = message.split(":")
        if len(parts) >= 2:
            label = parts[0].strip()
            value = parts[1].strip()
            rest = ":".join(parts[2:]).strip() if len(parts) > 2 else ""
            
            if label in ["Display Name", "Pronouns", "Bio", "Custom Status"]:
                masked_value = value[:6] + "..." if len(value) > 6 else value
                processed_message = (
                    f"{label} {Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} "
                    f"{Fore.LIGHTMAGENTA_EX}{masked_value}{Style.RESET_ALL}"
                )
            else:
                processed_message = (
                    f"{label} {Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} "
                    f"{Fore.LIGHTMAGENTA_EX}{value}{Style.RESET_ALL}"
                )
            
            if rest:
                processed_message += f" {Fore.LIGHTBLACK_EX}:{Style.RESET_ALL} {rest}"
        else:
            processed_message = message
    else:
        processed_message = message.replace(":", f"{Fore.LIGHTBLACK_EX}:{Style.RESET_ALL}")

    processed_message = re.sub(r"\[\s*([A-Za-z0-9]{8,12}\*{2})\s*\]", 
                               lambda m: f"{Fore.LIGHTBLACK_EX}[ {m.group(1)} ]{Style.RESET_ALL}",
                               processed_message)

    if message_type == "UPDATED":
        processed_message = re.sub(r"\[\s*(\d{3}/\d{3})\s*\]",
                                   lambda m: f"{Fore.CYAN}[ {m.group(1)} ]{Style.RESET_ALL}",
                                   processed_message)

    print(f"{current_time()} {styled_type} {Fore.LIGHTBLACK_EX}•{Fore.RESET} {Fore.WHITE}{processed_message}{Style.RESET_ALL}")

def load_config():
    global config, customization
    try:
        with open("config.json", "r", encoding="utf-8") as file:
            config = json.load(file)
            customization = config.get("CustomizationSettings", {})
            config["RetryLimit"] = max(1, min(config.get("RetryLimit", 1), 3))
        log("SUCCESS", "Successfully Loaded CONFIG", Fore.LIGHTWHITE_EX)
    except Exception as error:
        log("ERROR", f"Failed to load config.json: {error}", Fore.RED)

def load_lines(filepath, label, color, enabled=True, store_key=None):
    if not enabled:
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
        log("SUCCESS", f"{Fore.LIGHTWHITE_EX}Successfully Loaded {len(lines)} {label}", color)
        if store_key:
            loaded_counts[store_key] = len(lines)
        return lines
    except Exception as error:
        log("ERROR", f"Failed to load {label} from {filepath}: {error}", Fore.RED)
        return []

def load_tokens(filepath, label, color, enabled=True, store_key=None):
    if not enabled:
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
        
        processed_tokens = []
        for line in lines:
            if ':' in line and line.count(':') >= 2:
                parts = line.split(':')
                if len(parts) >= 3:
                    token = ':'.join(parts[2:])
                    processed_tokens.append(token)
                else:
                    processed_tokens.append(line)
            else:
                processed_tokens.append(line)
        
        log("SUCCESS", f"{Fore.LIGHTWHITE_EX}Successfully Loaded {len(processed_tokens)} {label}", color)
        if store_key:
            loaded_counts[store_key] = len(processed_tokens)
        return processed_tokens
    except Exception as error:
        log("ERROR", f"Failed to load {label} from {filepath}: {error}", Fore.RED)
        return []

def load_images(folder, extensions, label, color, enabled=True, store_key=None):
    if not enabled:
        return []
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
        files = [f for f in os.listdir(folder) if f.lower().endswith(extensions)]
        log("SUCCESS", f"{Fore.LIGHTWHITE_EX}Successfully Loaded {len(files)} {label}", color)
        if store_key:
            loaded_counts[store_key] = len(files)
        return files
    except Exception as error:
        log("ERROR", f"Failed to load {label} from {folder}: {error}", Fore.RED)
        return []

def load_status(filepath, label, color, enabled=True, store_key=None):
    if not enabled:
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
        statuses = []
        for line in lines:
            if ':' in line:
                emoji, text = line.split(':', 1)
                statuses.append({'emoji': emoji.strip(), 'text': text.strip()})
            else:
                statuses.append({'emoji': None, 'text': line.strip()})
        log("SUCCESS", f"{Fore.LIGHTWHITE_EX}Successfully Loaded {len(statuses)} {label}", color)
        if store_key:
            loaded_counts[store_key] = len(statuses)
        return statuses
    except Exception as error:
        log("ERROR", f"Failed to load {label} from {filepath}: {error}", Fore.RED)
        return []

def load_proxies(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            proxies = [line.strip() for line in file if line.strip()]
        log("SUCCESS", f"{Fore.LIGHTWHITE_EX}Successfully Loaded {len(proxies)} Proxies", Fore.YELLOW)
        return proxies
    except Exception as error:
        log("ERROR", f"Failed to load proxies from {filepath}: {error}", Fore.RED)
        return []

def go_online(token):
    try:
        ws = websocket.WebSocket()
        ws.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        hello = json.loads(ws.recv())
        heartbeat_interval = hello['d']['heartbeat_interval'] / 1000

        status = random.choice(['online', 'dnd', 'idle'])
        activity_type = None
        gamejson = None

        auth = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "windows",
                    "$browser": "Chrome",
                    "$device": "Windows"
                },
                "presence": {
                    "activities": [],
                    "status": status,
                    "since": 0,
                    "afk": False
                }
            }
        }
        ws.send(json.dumps(auth))
        return ws, heartbeat_interval
    except Exception as e:
        log("ERROR", f"WebSocket Error: {e}", Fore.RED)
        return None, None

def set_offline(ws):
    try:
        if ws:
            offline_payload = {
                "op": 3,
                "d": {
                    "status": "invisible",
                    "since": 0,
                    "activities": [],
                    "afk": False
                }
            }
            ws.send(json.dumps(offline_payload))
            time.sleep(1)
    except Exception as e:
        log("ERROR", f"Error setting offline: {e}", Fore.RED)

async def check_token(session, token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    try:
        async with session.get("https://discord.com/api/v9/users/@me", headers=headers) as resp:
            if resp.status == 200:
                return True
            else:
                error = await resp.text()
                log("ERROR", f"Invalid Token : [ {token[:12]}*** ] : [ {resp.status} ] - {error}", Fore.RED)
                return False
    except Exception as e:
        log("ERROR", f"Token Check Exception : [ {token[:12]}*** ] : [ {str(e)} ]", Fore.RED)
        return False

async def update_hypesquad(session, token, retry_count=0):
    house_ids = {"bravery": 1, "brilliance": 2, "balance": 3}
    house = random.choice(list(house_ids.keys()))
    payload = {"house_id": house_ids[house]}
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    url = "https://discord.com/api/v9/hypesquad/online"
    try:
        async with session.post(url, headers=headers, json=payload) as resp:
            if resp.status == 204:
                log("UPDATED", f"HypeSquad Badge : {house.capitalize()} : [ {token[:12]}** ]", Fore.GREEN)
                return True
            else:
                error = await resp.text()
                if retry_count < config.get("RetryLimit", 1):
                    log("RETRY", f"Retrying HypeSquad ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    return await update_hypesquad(session, token, retry_count + 1)
                log("ERROR", f"Failed HypeSquad : [ {token[:12]}** ] : [ {resp.status} ] - {error}", Fore.RED)
                return False
    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying HypeSquad ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_hypesquad(session, token, retry_count + 1)
        log("ERROR", f"Exception updating HypeSquad: {str(e)}", Fore.RED)
        return False

async def update_name(session, token, name, retry_count=0):
    headers = {
        "authority": "discord.com",
        "method": "PATCH",
        "scheme": "https",
        "accept": "/",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com/",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "Content-Type": "application/json",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
    }

    payload = {
        "global_name": name
    }

    try:
        response = sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        
        if response.status_code == 200:
            log("UPDATED", f"Display Name : {name} : [ {token[:12]}** ] : [ 200/200 ]", Fore.GREEN)
            return True
        else:
            error = response.text
            try:
                error_json = json.loads(error)
                if "errors" in error_json and "global_name" in error_json["errors"]:
                    global_name_errors = error_json["errors"]["global_name"]
                    if "_errors" in global_name_errors:
                        for err in global_name_errors["_errors"]:
                            if err.get("code") == "GLOBAL_NAME_RATE_LIMIT":
                                log("RATELIMIT", f"Account is in ratelimit (Global Name), Waiting: {response.status_code}", Fore.RED)
                                if retry_count < config.get("RetryLimit", 1):
                                    log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                                    await asyncio.sleep(random.uniform(1.0, 2.0))
                                    return await update_name(session, token, name, retry_count + 1)
                                else:
                                    log("ERROR", f"Failed Name : [ {token[:12]}** ] : [ {response.status_code} ] - {error}", Fore.RED)
                                    return False
            except json.JSONDecodeError:
                pass
            
            if "GLOBAL_NAME_RATE_LIMIT" in error or "You are changing your global name too often" in error:
                log("RATELIMIT", f"Account is in ratelimit (Global Name), Waiting: {response.status_code}", Fore.RED)
                if retry_count < config.get("RetryLimit", 1):
                    log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    return await update_name(session, token, name, retry_count + 1)
            else:
                if retry_count < config.get("RetryLimit", 1):
                    log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    return await update_name(session, token, name, retry_count + 1)
            
            log("ERROR", f"Failed Name : [ {token[:12]}** ] : [ {response.status_code} ] - {error}", Fore.RED)
            return False
    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_name(session, token, name, retry_count + 1)
        log("ERROR", f"Exception updating name: {str(e)}", Fore.RED)
        return False

async def update_pronoun(session, token, pronoun, retry_count=0):
    headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    payload = {"pronouns": pronoun}
    url = "https://discord.com/api/v9/users/@me/profile"
    try:
        async with session.patch(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                log("UPDATED", f"Pronouns : {pronoun} : [ {token[:12]}** ]", Fore.GREEN)
                return True
            else:
                if retry_count < config.get("RetryLimit", 1):
                    log("RETRY", f"Retrying Pronoun ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    return await update_pronoun(session, token, pronoun, retry_count + 1)
                error = await resp.text()
                log("ERROR", f"Failed Pronoun : [ {token[:12]}** ] : [ {resp.status} ] - {error}", Fore.RED)
                return False
    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Pronoun ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_pronoun(session, token, pronoun, retry_count + 1)
        log("ERROR", f"Exception updating pronoun: {str(e)}", Fore.RED)
        return False

async def update_bio(session, token, bio, retry_count=0):
    headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    payload = {"bio": bio}
    url = "https://discord.com/api/v9/users/@me/profile"
    try:
        async with session.patch(url, headers=headers, json=payload) as resp:
            if resp.status == 200:
                log("UPDATED", f"Bio : {bio} : [ {token[:12]}** ]", Fore.GREEN)
                return True
            else:
                if retry_count < config.get("RetryLimit", 1):
                    log("RETRY", f"Retrying Bio ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                    await asyncio.sleep(random.uniform(1.0, 2.0))
                    return await update_bio(session, token, bio, retry_count + 1)
                error = await resp.text()
                log("ERROR", f"Failed Bio : [ {token[:12]}** ] : [ {resp.status} ] - {error}", Fore.RED)
                return False
    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Bio ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_bio(session, token, bio, retry_count + 1)
        log("ERROR", f"Exception updating bio: {str(e)}", Fore.RED)
        return False

async def update_profile_fields(session, token, name, pronoun=None, bio=None, hypesquad=True, retry_count=0):

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    
    results = {
        'name': False,
        'pronouns': None if pronoun is None else False,
        'bio': None if bio is None else False,
        'hypesquad': False
    }
    
    try:
        name_payload = {"global_name": name}
        try:
            response = sesh.patch(
                "https://discord.com/api/v9/users/@me",
                headers=headers,
                json=name_payload
            )
            if response.status_code == 200:
                results['name'] = True
                log("UPDATED", f"Display Name : {name} : [ {token[:12]}** ]", Fore.GREEN)
            else:
                error = response.text
                try:
                    error_json = json.loads(error)
                    if "errors" in error_json and "global_name" in error_json["errors"]:
                        global_name_errors = error_json["errors"]["global_name"]
                        if "_errors" in global_name_errors:
                            for err in global_name_errors["_errors"]:
                                if err.get("code") == "GLOBAL_NAME_RATE_LIMIT":
                                    log("RATELIMIT", f"Account is in ratelimit (Global Name), Waiting: {response.status_code}", Fore.RED)
                                    if retry_count < config.get("RetryLimit", 1):
                                        log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                                        await asyncio.sleep(random.uniform(1.0, 2.0))
                                        return await update_profile_fields(
                                            session, token,
                                            name=name,
                                            pronoun=pronoun,
                                            bio=bio,
                                            hypesquad=hypesquad,
                                            retry_count=retry_count + 1
                                        )
                                    else:
                                        log("ERROR", f"Name update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                                        return False
                except json.JSONDecodeError:
                    pass
                
                if "GLOBAL_NAME_RATE_LIMIT" in error or "You are changing your global name too often" in error:
                    log("RATELIMIT", f"Account is in ratelimit (Global Name), Waiting: {response.status_code}", Fore.RED)
                    if retry_count < config.get("RetryLimit", 1):
                        log("RETRY", f"Retrying Name ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                        await asyncio.sleep(random.uniform(1.0, 2.0))
                        return await update_profile_fields(
                            session, token,
                            name=name,
                            pronoun=pronoun,
                            bio=bio,
                            hypesquad=hypesquad,
                            retry_count=retry_count + 1
                        )
                else:
                    log("ERROR", f"Name update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                    return False
        except Exception as e:
            log("ERROR", f"Name update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)

        if pronoun or bio:
            profile_payload = {}
            if pronoun:
                profile_payload["pronouns"] = pronoun
            if bio:
                profile_payload["bio"] = bio
            
            try:
                async with session.patch(
                    "https://discord.com/api/v9/users/@me/profile",
                    headers=headers,
                    json=profile_payload
                ) as resp:
                    if resp.status == 200:
                        if pronoun:
                            results['pronouns'] = True
                            log("UPDATED", f"Pronouns : {pronoun} : [ {token[:12]}** ]", Fore.GREEN)
                        if bio:
                            results['bio'] = True
                            log("UPDATED", f"Bio : {bio} : [ {token[:12]}** ]", Fore.GREEN)
                    else:
                        error = await resp.text()
                        log("ERROR", f"Profile update failed : [ {token[:12]}** ]: {error}", Fore.RED)
            except Exception as e:
                log("ERROR", f"Profile update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)

        house = random.choice(["bravery", "brilliance", "balance"])
        hypesquad_payload = {"house_id": {"bravery": 1, "brilliance": 2, "balance": 3}[house]}
        
        try:
            async with session.post(
                "https://discord.com/api/v9/hypesquad/online",
                headers=headers,
                json=hypesquad_payload
            ) as resp:
                if resp.status == 204:
                    results['hypesquad'] = True
                    log("UPDATED", f"HypeSquad : {house.capitalize()} : [ {token[:12]}** ]", Fore.GREEN)
                else:
                    error = await resp.text()
                    log("ERROR", f"HypeSquad update failed : [ {token[:12]}** ]: {error}", Fore.RED)
        except Exception as e:
            log("ERROR", f"HypeSquad update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        
        mandatory_failures = [
            k for k in ['name', 'hypesquad']
            if results[k] is False and results[k] is not None
        ]
        
        optional_failures = [
            k for k in ['pronouns', 'bio'] 
            if results[k] is False
        ]
        
        if (mandatory_failures or optional_failures) and retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying failed updates : Mandatory: {mandatory_failures} | Optional: {optional_failures} : [ {token[:12]}** ] (Attempt {retry_count + 1}/{config.get('RetryLimit', 1)})", Fore.YELLOW)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_profile_fields(
                session, token,
                name=name,
                pronoun=pronoun if 'pronouns' in optional_failures else None,
                bio=bio if 'bio' in optional_failures else None,
                hypesquad=True,
                retry_count=retry_count + 1
            )
        
        if mandatory_failures:
            log("ERROR", f"Mandatory updates failed after retries : [ {token[:12]}** ]: {', '.join(mandatory_failures)}", Fore.RED)
            return False
        
        if optional_failures:
            log("WARNING", f"Optional updates failed : [ {token[:12]}** ]: {', '.join(optional_failures)}", Fore.YELLOW)

        if status and status['text'] != "Don't clear":
            try:
                clear_payload = {"custom_status": None}
                clear_resp = await session.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=clear_payload)
                if clear_resp.status == 200:
                    log("UPDATED", f"Cleared Custom Status : [ {token[:12]}** ]", Fore.GREEN)
                else:
                    log("WARNING", f"Failed to clear status : [ {token[:12]}** ]", Fore.YELLOW)
            except Exception as e:
                log("ERROR", f"Exception clearing status : [ {token[:12]}** ]: {str(e)}", Fore.RED)

        return True
        
    except Exception as e:
        log("ERROR", f"Profile update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying due to exception : [ {token[:12]}** ] (Attempt {retry_count + 1}/{config.get('RetryLimit', 1)})", Fore.YELLOW)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await update_profile_fields(
                session, token,
                name=name,
                pronoun=pronoun,
                bio=bio,
                hypesquad=True,
                retry_count=retry_count + 1
            )
        return False

async def upd_pr(session, token, name, pronoun=None, bio=None, avatar_path=None, banner_path=None, status=None, retry_count=0):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTE2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
    }
    
    results = {
        'name': None if name is None else False,
        'pronouns': None if pronoun is None else False,
        'bio': None if bio is None else False,
        'hypesquad': False if config.get("CustomizationSettings", {}).get("Hypesquad", True) else None,
        'avatar': None if avatar_path is None else False,
        'banner': None if banner_path is None else False,
        'status': None if status is None else False
    }
    
    try:
        tasks = []
        
        if name:
            name_payload = {"global_name": name}
            tasks.append(("name", sesh.patch("https://discord.com/api/v9/users/@me", headers=headers, json=name_payload)))

        if pronoun or bio:
            profile_payload = {}
            if pronoun:
                profile_payload["pronouns"] = pronoun
            if bio:
                profile_payload["bio"] = bio
            tasks.append(("profile", session.patch("https://discord.com/api/v9/users/@me/profile", headers=headers, json=profile_payload)))

        if config.get("CustomizationSettings", {}).get("Hypesquad", True):
            house = random.choice(["bravery", "brilliance", "balance"])
            hypesquad_payload = {"house_id": {"bravery": 1, "brilliance": 2, "balance": 3}[house]}
            tasks.append(("hypesquad", session.post("https://discord.com/api/v9/hypesquad/online", headers=headers, json=hypesquad_payload)))

        if status:
            custom_status_payload = {"custom_status": {"text": status['text'], "emoji_name": status['emoji']}}
            tasks.append(("status", session.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=custom_status_payload)))
        
        if avatar_path and os.path.exists(avatar_path):
            try:
                file_size = os.path.getsize(avatar_path) / (1024 * 1024)
                if file_size <= 10:
                    with open(avatar_path, "rb") as f:
                        img_data = f.read()
                        ext = os.path.splitext(avatar_path)[1].lower().replace('.', '')
                        mime_type = "image/gif" if ext == "gif" else f"image/{'jpeg' if ext == 'jpg' else ext}"
                        b64 = base64.b64encode(img_data).decode()
                        avatar_data = f"data:{mime_type};base64,{b64}"
                    
                    avatar_payload = {"avatar": avatar_data}
                    tasks.append(("avatar", sesh.patch("https://discord.com/api/v9/users/@me", headers=headers, json=avatar_payload)))
            except Exception as e:
                log("ERROR", f"Avatar preparation failed : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        
        if banner_path and os.path.exists(banner_path):
            try:
                profile_response = sesh.get("https://discord.com/api/v9/users/@me", headers=headers)
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    if profile_data.get("premium_type", 0):
                        with open(banner_path, "rb") as f:
                            img_data = f.read()
                            ext = os.path.splitext(banner_path)[1].lower().replace('.', '')
                            if ext == "jpg":
                                ext = "jpeg"
                            b64 = base64.b64encode(img_data).decode()
                            banner_data = f"data:image/{ext};base64,{b64}"
                        
                        banner_payload = {"banner": banner_data}
                        tasks.append(("banner", sesh.patch("https://discord.com/api/v9/users/@me", headers=headers, json=banner_payload)))
                    else:
                        log("SKIP", f"Account has no nitro : [ {token[:12]}** ] - Skipping banner update", Fore.YELLOW)
            except Exception as e:
                log("ERROR", f"Banner failed : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        
        for task_name, task in tasks:
            try:
                if task_name in ["profile", "hypesquad", "status"]:
                    async with task as resp:
                        if task_name == "profile":
                            if resp.status == 200:
                                if pronoun:
                                    results['pronouns'] = True
                                    log("UPDATED", f"Pronouns : {pronoun} : [ {token[:12]}** ]", Fore.GREEN)
                                if bio:
                                    results['bio'] = True
                                    log("UPDATED", f"Bio : {bio} : [ {token[:12]}** ]", Fore.GREEN)
                            else:
                                error = await resp.text()
                                log("ERROR", f"Profile update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                        elif task_name == "hypesquad":
                            if resp.status == 204:
                                results['hypesquad'] = True
                                log("UPDATED", f"HypeSquad : {house.capitalize()} : [ {token[:12]}** ]", Fore.GREEN)
                            else:
                                error = await resp.text()
                                log("ERROR", f"HypeSquad update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                        elif task_name == "status":
                            if resp.status == 200:
                                results['status'] = True
                                log("UPDATED", f"Custom Status : {status['emoji']} {status['text']} : [ {token[:12]}** ]", Fore.GREEN)
                            else:
                                error = await resp.text()
                                log("ERROR", f"Status update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                else:
                    response = task
                    if task_name == "name":
                        if response.status_code == 200:
                            results['name'] = True
                            log("UPDATED", f"Display Name : {name} : [ {token[:12]}** ]", Fore.GREEN)
                        else:
                            error = response.text
                            log("ERROR", f"Name update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                    elif task_name == "avatar":
                        if response.status_code == 200:
                            results['avatar'] = True
                            log("UPDATED", f"PFP : {os.path.basename(avatar_path)} : [ {token[:12]}** ]", Fore.GREEN)
                        else:
                            error = response.text
                            log("ERROR", f"Avatar update failed : [ {token[:12]}** ]: {error}", Fore.RED)
                    elif task_name == "banner":
                        if response.status_code == 200:
                            results['banner'] = True
                            log("UPDATED", f"Banner : {os.path.basename(banner_path)} : [ {token[:12]}** ]", Fore.GREEN)
                        else:
                            error = response.text
                            log("ERROR", f"Banner update failed : [ {token[:12]}** ]: {error}", Fore.RED)
            except Exception as e:
                log("ERROR", f"{task_name} update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        
        mandatory_failures = [
            k for k in ['name', 'hypesquad'] 
            if results[k] is False
        ]
        
        optional_failures = [
            k for k in ['pronouns', 'bio', 'avatar', 'banner', 'status']
            if results[k] is False
        ]
        
        if (mandatory_failures or optional_failures) and retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying failed updates : Mandatory: {mandatory_failures} | Optional: {optional_failures} : [ {token[:12]}** ] (Attempt {retry_count + 1}/{config.get('RetryLimit', 1)})", Fore.YELLOW)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await upd_pr(
                session, token,
                name=name,
                pronoun=pronoun if 'pronouns' in optional_failures else None,
                bio=bio if 'bio' in optional_failures else None,
                avatar_path=avatar_path if 'avatar' in optional_failures else None,
                banner_path=banner_path if 'banner' in optional_failures else None,
                status=status if 'status' in optional_failures else None,
                retry_count=retry_count + 1
            )
        
        if mandatory_failures:
            log("ERROR", f"Mandatory updates failed after retries : [ {token[:12]}** ]: {', '.join(mandatory_failures)}", Fore.RED)
            return False
        
        if optional_failures:
            log("WARNING", f"Optional updates failed : [ {token[:12]}** ]: {', '.join(optional_failures)}", Fore.YELLOW)
        
        return True
        
    except Exception as e:
        log("ERROR", f"Fast profile update exception : [ {token[:12]}** ]: {str(e)}", Fore.RED)
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying due to exception : [ {token[:12]}** ] (Attempt {retry_count + 1}/{config.get('RetryLimit', 1)})", Fore.YELLOW)
            await asyncio.sleep(random.uniform(1.0, 2.0))
            return await upd_pr(
                session, token,
                name=name,
                pronoun=pronoun,
                bio=bio,
                avatar_path=avatar_path,
                banner_path=banner_path,
                status=status,
                retry_count=retry_count + 1
            )
        return False

def update_avatar(token, image_path, retry_count=0):
    if not os.path.exists(image_path):
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Avatar ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            time.sleep(random.uniform(2.0, 3.0))
            return update_avatar(token, image_path, retry_count + 1)
        log("ERROR", f"Avatar image not found: {image_path}", Fore.RED)
        return False

    try:
        headers = {
            "authorization": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        check_response = sesh.get(
            "https://discord.com/api/v9/users/@me",
            headers=headers
        )
        
        if check_response.status_code != 200:
            if retry_count < config.get("RetryLimit", 1):
                log("RETRY", f"Retrying Token Check ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                time.sleep(random.uniform(3.0, 5.0))
                return update_avatar(token, image_path, retry_count + 1)
            log("ERROR", f"Invalid Token Session : [ {token[:12]}** ] : [ {check_response.status_code} ]", Fore.RED)
            return False

        file_size = os.path.getsize(image_path) / (1024 * 1024)
        if file_size > 10:
            log("ERROR", f"Avatar too large ({file_size:.2f}MB > 10MB limit)", Fore.RED)
            return False

        with open(image_path, "rb") as f:
            img_data = f.read()
            ext = os.path.splitext(image_path)[1].lower().replace('.', '')
            mime_type = "image/gif" if ext == "gif" else f"image/{'jpeg' if ext == 'jpg' else ext}"
            b64 = base64.b64encode(img_data).decode()
            avatar_data = f"data:{mime_type};base64,{b64}"

        headers.update({
            "content-type": "application/json",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgM10uMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        })

        payload = {"avatar": avatar_data}

        response = sesh.patch(
            "https://discord.com/api/v9/users/@me",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            log("UPDATED", f"PFP : {os.path.basename(image_path)} : [ {token[:12]}** ]", Fore.GREEN)
            return True
        else:
            error = response.text
            if retry_count < config.get("RetryLimit", 1):
                log("RETRY", f"Retrying Avatar ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                time.sleep(random.uniform(3.0, 5.0))
                return update_avatar(token, image_path, retry_count + 1)
            log("ERROR", f"PFP Fail : [ {token[:12]}** ] : [ {response.status_code} ] - {error}", Fore.RED)
            return False

    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Avatar ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            time.sleep(random.uniform(3.0, 5.0))
            return update_avatar(token, image_path, retry_count + 1)
        log("ERROR", f"Exception setting PFP: {str(e)}", Fore.RED)
        return False

def update_banner(token, image_path, retry_count=0):
    try:
        headers = {
            "authorization": token,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        profile_response = sesh.get(
            "https://discord.com/api/v9/users/@me",
            headers=headers
        )
        
        if profile_response.status_code == 200:
            profile_data = profile_response.json()
            if not profile_data.get("premium_type", 0):
                log("SKIP", f"Account has no nitro : [ {token[:12]}** ] - Skipping banner update", Fore.YELLOW)
                return False
        else:
            if retry_count < config.get("RetryLimit", 1):
                log("RETRY", f"Retrying Nitro Check ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                time.sleep(random.uniform(1.0, 2.0))
                return update_banner(token, image_path, retry_count + 1)
            log("ERROR", f"Failed to check nitro status : [ {token[:12]}** ] : [ {profile_response.status_code} ]", Fore.RED)
            return False
            
    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Nitro Check ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            time.sleep(random.uniform(1.0, 2.0))
            return update_banner(token, image_path, retry_count + 1)
        log("ERROR", f"Exception checking nitro status: {str(e)}", Fore.RED)
        return False

    if not os.path.exists(image_path):
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Banner ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            time.sleep(random.uniform(1.0, 2.0))
            return update_banner(token, image_path, retry_count + 1)
        log("ERROR", f"Banner image not found: {image_path}", Fore.RED)
        return False

    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
            ext = os.path.splitext(image_path)[1].lower().replace('.', '')
            if ext == "jpg":
                ext = "jpeg"
            b64 = base64.b64encode(img_data).decode()
            banner_data = f"data:image/{ext};base64,{b64}"

        headers = {
            "authorization": token,
            "content-type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEyMC4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTIwLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwLjAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MjUxNDQxLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=="
        }

        payload = {"banner": banner_data}

        response = sesh.patch(
            "https://discord.com/api/v9/users/@me",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            log("UPDATED", f"Banner : {os.path.basename(image_path)} : [ {token[:12]}** ]", Fore.GREEN)
            return True
        else:
            error = response.text
            if retry_count < config.get("RetryLimit", 1):
                log("RETRY", f"Retrying Banner ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
                time.sleep(random.uniform(1.0, 2.0))
                return update_banner(token, image_path, retry_count + 1)
            log("ERROR", f"Banner Fail : [ {token[:12]}** ] : [ {response.status_code} ] - {error}", Fore.RED)
            return False

    except Exception as e:
        if retry_count < config.get("RetryLimit", 1):
            log("RETRY", f"Retrying Banner ({retry_count + 1}/{config.get('RetryLimit', 1)}) : [ {token[:12]}** ]", Fore.MAGENTA)
            time.sleep(random.uniform(1.0, 2.0))
            return update_banner(token, image_path, retry_count + 1)
        log("ERROR", f"Exception setting Banner: {str(e)}", Fore.RED)
        return False


def process_token_with_proxy(token, proxy, idx, names, pronouns, bios, avatars, banners, statuses):
    """Process a single token with a specific proxy"""
    global ratelimited_proxies, ratelimited_accounts
    
    try:
        if ratelimited_proxies[proxy] > 0:
            ratelimit_proxy_time = ratelimited_proxies[proxy]
            log("RATELIMIT", f"Proxy is in ratelimit ({ratelimit_proxy_time}), Switching to new proxy", Fore.RED)
            return False
        
        if ratelimited_accounts[token] > 0:
            ratelimit_account_time = ratelimited_accounts[token]
            log("RATELIMIT", f"Account is in ratelimit ({ratelimit_account_time}), Switching to next account", Fore.RED)
            return False
        
        proxy_session = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        proxy_session.proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
         
        if idx > 0:
            time.sleep(random.uniform(1.0, 2.0))
 
        ws, heartbeat_interval = go_online(token)
        if not ws:
            log("ERROR", f"Failed to connect WebSocket for token : [ {token[:12]}....] {Fore.LIGHTBLACK_EX}•{Fore.RESET} ({proxy})", Fore.RED)
            return False
 
        log("START", f"{Fore.LIGHTBLACK_EX}" + f"{Fore.WHITE}Started Humanization {Fore.LIGHTBLACK_EX}: [ {token[:12]}....] {Fore.LIGHTBLACK_EX}•{Fore.RESET} ({proxy})", Fore.GREEN)
        time.sleep(random.uniform(0.3, 0.8))
 
        async def check_with_proxy():
            async with aiohttp.ClientSession() as session:
                return await check_token(session, token)
                 
        # Create a new event loop for this thread to avoid conflicts
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)
        valid = thread_loop.run_until_complete(check_with_proxy())
        thread_loop.close()
        if not valid:
            ws.close()
            return False
 
        avatar_path = None
        banner_path = None
        status = None
 
        if avatars:
            avatar_path = os.path.join("avatar", random.choice(avatars))
 
        if banners:
            banner_path = os.path.join("banners", random.choice(banners))
 
        if statuses:
            status = random.choice(statuses)
 
        async def update_with_proxy():
            async with aiohttp.ClientSession() as session:
                name_val = random.choice(names) if names else None
                pronoun_val = random.choice(pronouns) if pronouns else None
                bio_val = random.choice(bios) if bios else None

                return await upd_pr(
                    session,
                    token,
                    name=name_val,
                    pronoun=pronoun_val,
                    bio=bio_val,
                    avatar_path=avatar_path,
                    banner_path=banner_path,
                    status=status
                )
 
        # Create a new event loop for this thread to avoid conflicts
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)
        success = thread_loop.run_until_complete(update_with_proxy())
        thread_loop.close()
         
        if success:
            log("SUCCESS", f"{Fore.GREEN}Finished humanizing token : [ {token[:12]}** ] {Fore.LIGHTBLACK_EX}•{Fore.RESET} ({proxy})", Fore.GREEN)
         
        return success
                 
    except Exception as e:
        error_message = str(e).lower()
        is_rate_limited = False
        
        if "rate limit" in error_message or "429" in error_message:
            is_rate_limited = True
        elif "global_name_rate_limit" in error_message or "you are changing your global name too often" in error_message:
            is_rate_limited = True
        
        if is_rate_limited:
            if proxy in ratelimited_proxies:
                ratelimited_proxies[proxy] += 1
            else:
                ratelimited_proxies[proxy] = 1
            
            if token in ratelimited_accounts:
                ratelimited_accounts[token] += 1
            else:
                ratelimited_accounts[token] = 1
            
            log("RATELIMIT", f"Proxy is in ratelimit ({ratelimited_proxies[proxy]}), Switching to new proxy", Fore.RED)
            log("RATELIMIT", f"Account is in ratelimit ({ratelimited_accounts[token]}), Switching to next account", Fore.RED)
        else:
            log("ERROR", f"Exception for token {token[:12]}** {Fore.LIGHTBLACK_EX}•{Fore.RESET} ({proxy}): {e}", Fore.RED)
        
        try:
            if 'ws' in locals():
                ws.close()
        except:
            pass
        time.sleep(1)
        return False

async def main():
    start_time = datetime.now()
    clear_console()
    set_console_title()
    ascii_nig()

    if not os.path.exists("config.json"):
        log("ERROR", "config.json not found")
        exit()

    load_config()

    tokens = load_tokens("input/tokens.txt", "Tokens", Fore.YELLOW, True, "Tokens")
    pronouns = load_lines("data/pronouns.txt", "Pronouns", Fore.YELLOW, customization.get("Pronouns", False), "Pronouns")
    bios = load_lines("data/bios.txt", "Bios", Fore.YELLOW, customization.get("Bio", False), "Bios")
    names = load_lines("data/names.txt", "Global Names", Fore.YELLOW, customization.get("DisplayName", False), "Global Names")
    avatars = load_images("avatar", (".png", ".jpg", ".jpeg", ".webp"), "Profile Pictures", Fore.YELLOW, customization.get("Avatar", False), "Profile Pictures")
    banners = load_images("banners", (".png", ".jpg", ".jpeg", ".webp"), "Banners", Fore.YELLOW, customization.get("Banner", False), "Banners")
    statuses = load_status("data/status.txt", "Statuses", Fore.YELLOW, customization.get("Status", False), "Statuses")

    use_proxy = config.get("use_proxy", False)
    proxies = []
    
    if use_proxy:
        proxies = load_proxies("input/proxies.txt")
        if not proxies:
            log("WARNING", "use_proxy is True but no proxies loaded. Running without proxies.", Fore.YELLOW)
            use_proxy = False

    log("INFO", f"Proxy Mode: {'Enabled' if use_proxy else 'Disabled'}", Fore.CYAN)
    if use_proxy:
        log("INFO", f"Loaded {len(proxies)} proxies for rotation", Fore.CYAN)

    summary = []
    if customization.get("Pronouns"):
        summary.append(f"{loaded_counts['Pronouns']} Pronouns")
    if customization.get("DisplayName"):
        summary.append(f"{loaded_counts['Global Names']} Names")
    if customization.get("Bio"):
        summary.append(f"{loaded_counts['Bios']} Bio's")
    if customization.get("Avatar"):
        summary.append(f"{loaded_counts['Profile Pictures']} PFP's")
    if customization.get("Banner"):
        summary.append(f"{loaded_counts['Banners']} Banners")
    if customization.get("Status"):
        summary.append(f"{loaded_counts['Statuses']} Statuses")
    if summary:
        log("INFO", f"Available Data: {' | '.join(summary)}", Fore.MAGENTA)

    if not tokens:
        log("ERROR", "No tokens loaded!", Fore.RED)
        return

    if use_proxy and proxies:
        log("INFO", "Starting multi-threaded processing (Proxy mode, 10 threads)", Fore.BLUE)
        
        def worker(token, proxy, idx):
            return process_token_with_proxy(token, proxy, idx, names, pronouns, bios, avatars, banners, statuses)
        
        successful_tokens = 0
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for idx, token in enumerate(tokens):
                proxy = proxies[idx % len(proxies)]
                futures.append(executor.submit(worker, token, proxy, idx))
            
            for future in futures:
                result = future.result()
                if result:
                    successful_tokens += 1
        
        if all(ratelimited_proxies[proxy] > 0 for proxy in proxies):
            log("RATELIMIT", f"Every Proxy is in ratelimit, Waiting: {max(ratelimited_proxies.values())}", Fore.RED)
            time.sleep(max(ratelimited_proxies.values()))
            ratelimited_proxies.clear()
        
        if all(ratelimited_accounts[token] > 0 for token in tokens):
            log("RATELIMIT", f"Every account is in ratelimit, Waiting: {max(ratelimited_accounts.values())}", Fore.RED)
            time.sleep(max(ratelimited_accounts.values()))
            ratelimited_accounts.clear()
        
        if ratelimited_accounts:
            log("INFO", "Retrying accounts that were skipped due to ratelimit", Fore.BLUE)
            for token, ratelimit_time in list(ratelimited_accounts.items()):
                if ratelimit_time > 0:
                    log("RATELIMIT", f"Account is in ratelimit, Waiting: {ratelimit_time}", Fore.RED)
                    time.sleep(ratelimit_time)
                    proxy = proxies[len(ratelimited_accounts) % len(proxies)]
                    result = process_token_with_proxy(token, proxy, 0, names, pronouns, bios, avatars, banners, statuses)
                    if result:
                        successful_tokens += 1
                    ratelimited_accounts[token] = 0
    else:
        async with aiohttp.ClientSession() as session:
            for idx, token in enumerate(tokens):
                try:
                    if idx > 0:
                        await asyncio.sleep(random.uniform(1.0, 2.0))

                    ws, heartbeat_interval = go_online(token)
                    if not ws:
                        log("ERROR", f"Failed to connect WebSocket for token : [ {token[:12]}....]", Fore.RED)
                        continue

                    log("START", f"{Fore.LIGHTBLACK_EX}" + f"{Fore.WHITE}Started Humanization {Fore.LIGHTBLACK_EX}: [ {token[:12]}....]", Fore.GREEN)
                    await asyncio.sleep(random.uniform(0.3, 0.8))

                    valid = await check_token(session, token)
                    if not valid:
                        ws.close()
                        continue

                    avatar_path = None
                    banner_path = None
                    status = None

                    if avatars:
                        avatar_path = os.path.join("avatar", random.choice(avatars))

                    if banners:
                        banner_path = os.path.join("banners", random.choice(banners))

                    if statuses:
                        status = random.choice(statuses)

                    name_val = random.choice(names) if names else None
                    pronoun_val = random.choice(pronouns) if pronouns else None
                    bio_val = random.choice(bios) if bios else None

                    await upd_pr(
                        session,
                        token,
                        name=name_val,
                        pronoun=pronoun_val,
                        bio=bio_val,
                        avatar_path=avatar_path,
                        banner_path=banner_path,
                        status=status
                    )
                    
                    log("SUCCESS", f"Finished humanizing token : [ {token[:12]}** ]", Fore.GREEN)

                except Exception as e:
                    log("ERROR", f"Exception for token {token[:12]}**: {e}", Fore.RED)
                    try:
                        if 'ws' in locals():
                            ws.close()
                    except:
                        pass
                    await asyncio.sleep(1)

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    processed_count = successful_tokens if use_proxy and proxies else len(tokens)
    log("INFO", f"Execution completed in {execution_time:.2f} seconds | Processed {processed_count} tokens", Fore.BLUE)

if __name__ == "__main__":
    loop = get_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError:
        pass
    finally:
        # Properly close the event loop
        if not loop.is_closed():
            loop.close()
    # Suppress asyncio event loop closed warning
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="asyncio")
