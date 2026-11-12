# the webmenu channel

A lightweight, self-hosted web utility launcher for unmodded **Nintendo Switch** consoles. Using a local Python HTTP/HTTPS proxy server, it intercepts the Switch's captive portal check and loads a custom, Joy-Con-friendly dashboard packed with built-in tools and web apps.

---

## Features

* **Google & SwitchBrowse:** Browse and search the web directly through custom Google Programmable Search engines.
* **XploreSW:** Browse folders and download files directly from your host PC over local Wi-Fi.
* **App Store (`publish-app.bat`):** Easily publish and launch your own standalone `.html` web apps and mini-games.
* **Quick Notepad:** Local scratchpad that automatically saves notes in your Switch's browser storage.
* **Snake:** Classic playable Snake mini-game with on-screen directional controls.
* **Calculator:** Controller-friendly button calculator for quick arithmetic.
* **Joy-Con & Touch Tester:** Live diagnostic tool for Joy-Con sticks, buttons, and touchscreen input.
* **Browser Info:** Displays screen resolution, user agent details, and proxy status.

---

## Requirements

* **Windows PC** connected to the same Wi-Fi network as your Nintendo Switch.
* **Python 3** installed and added to your system PATH.
* *(Optional)* `PFSquareSansPro-Medium.ttf` and `PFSquareSansPro-Bold.ttf` placed inside a `/fonts` folder for the custom header typography.

---

## Setup & Usage

### 1. Start the Local Proxy Server
1. Open the `run/` folder and double-click **`start-launcher.bat`**.
2. Click **Yes** when prompted for Administrator permissions (used to open port `8080` in Windows Defender Firewall).
3. Note your host PC's **IPv4 address** printed in the launcher window (or check anytime by running `ipconfig` in Command Prompt).

### 2. Configure Your Nintendo Switch
1. On your Switch, open **System Settings** > **Internet** > **Internet Settings**.
2. Select your Wi-Fi network and choose **Change Settings**.
3. Ensure **DNS Settings** is set to **Automatic**.
4. Scroll down to **Proxy Settings** and set it to **On**:
   * **Server:** Your PC's local IPv4 address (e.g., `192.168.1.X`)
   * **Port:** `8080`
5. Save your settings and select **Connect to This Network**.
6. When the *"Registration is required to use this network"* prompt appears, select **Next** to launch **the webmenu channel**.

---

## Publishing Custom Apps to the App Store

1. Build any standalone `.html` web app (keep CSS inside `<style>` and JavaScript inside `<script>` tags, and link back to `../store.html`).
2. Run **`run/publish-app.bat`** on your PC.
3. Enter an **App Title**, **Short Description**, and drag-and-drop your `.html` file into the window.
4. Open **App Store** on your Switch to launch your new app immediately.

---

## Folder Structure

```text
webmenu/
├── run/
│   ├── start-launcher.bat   # Starts the proxy server and configures firewall rules
│   └── publish-app.bat      # Adds custom .html apps to the local App Store
├── fonts/                   # Optional custom font files
├── proxy_server.py          # Local Python proxy, file API, and HTTPS tunnel
├── index.html               # Main launcher dashboard
├── google.html              # Google Custom Search wrapper
├── switchbrowse.html        # SwitchBrowse search wrapper
├── xploresw.html            # PC file explorer frontend
├── store.html               # Local App Store frontend
├── notepad.html             # Local storage notepad
├── snake.html               # Playable Snake game
├── calc.html                # Button calculator
├── joycon.html              # Joy-Con and touchscreen tester
└── info.html                # Browser & resolution info
```

---

## Notes & Limitations

* **No Console Modification Required:** Everything runs safely inside the Switch's built-in captive portal WebKit applet.
* **20-Minute Session Limit:** Nintendo hardcodes a ~20-minute timeout into the login browser applet. If the window closes, simply reconnect to your Wi-Fi network in **Internet Settings** to start a fresh session.
