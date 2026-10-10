# 🎭 Humanizer V2 - Discord Account & Token Customizer

A high-performance automated Discord account & token humanizer designed to bulk update user profiles, avatars, banners, and status activity using TLS spoofing and asynchronous websockets.

## ✨ Key Features
- **TLS Fingerprint Spoofing**: Uses `tls_client` to mimic legitimate browser handshakes, bypassing anti-bot automated flags.
- **Bulk Profile Updates**:
  - Automatically applies avatars from `avatar/` directory.
  - Uploads matching banner assets from `banners/`.
  - Configures randomized "About Me" bios and display names.
- **Active WebSocket Heartbeat**: Simulates realistic online user presence and client activity.
- **Multi-Threaded Architecture**: Fast parallel token processing with error recovery.

## 🛠️ Requirements & Dependencies
- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  *(Includes: `tls_client`, `httpx`, `aiohttp`, `colorama`, `pystyle`, `websocket-client`)*

## 🚀 Setup & Usage
1. Configure preferences in `config.json` (delays, feature toggles, presence settings).
2. Place profile picture assets into the `avatar/` folder.
3. Place header banners into the `banners/` folder.
4. Add tokens into input list.
5. Run the tool:
   ```bash
   python main.py
   ```

## ⚠️ Disclaimer
This tool is intended strictly for educational, security testing, and research purposes.
