# Personal Music Experience (Prototype)

A Manifest V3 Chrome extension prototype created for a Design Thinking college project. It injects a persistent, modular side panel UI into supported music streaming websites.

## Project Structure

\`\`\`
├── manifest.json            # Extension configuration (Manifest V3)
├── background.js            # Minimal background service worker
├── content.js               # Main script injected into pages (UI and tracking logic)
├── content.css              # Styles for the injected side panel and button
├── utils.js                 # Shared utilities (local storage wrapper)
├── popup.html/css/js        # Browser toolbar popup UI
├── platforms/               # Modular adapters for each music site
│   ├── spotify.js
│   ├── youtube-music.js
│   └── apple-music.js
└── README.md                # Documentation
\`\`\`

## How to Load in Chrome (Locally Unpacked)

1. Open Google Chrome.
2. Go to \`chrome://extensions/\` in the URL bar.
3. Enable **"Developer mode"** in the top right corner.
4. Click **"Load unpacked"** in the top left corner.
5. Select the \`PersonalMusicExperience\` folder that contains the \`manifest.json\` file.
6. The extension is now installed. Pin it to your toolbar by clicking the puzzle piece icon.

## Testing the Extension

### Spotify Web
1. Navigate to https://open.spotify.com
2. Wait for the page to load. You will see a green floating button in the bottom right corner.
3. Play a song. Click the button to open the side panel. It should display the current track and artist.

### YouTube Music
1. Navigate to https://music.youtube.com
2. Look for the floating button in the bottom right corner.
3. Play a song and open the panel to see the track details.

### Apple Music Web
1. Navigate to https://music.apple.com
2. Play a song and check the panel.

## Architecture

**Platform Adapters**
To prevent a messy single file, the logic for finding the current song is split into individual adapters inside \`platforms/\`. The \`content.js\` script loops through these adapters, finds the one matching the current URL, and uses it to poll for track changes. If a music service updates their website layout, you only need to fix the specific adapter.

**Local Storage**
User data (like preferences or saved items in a real app) is stored strictly locally using \`chrome.storage.local\`. A utility layer in \`utils.js\` simplifies reading and writing this data. The data never leaves your browser. No OAuth, tracking, or API keys are required.

**Permissions Explained**
- \`storage\`: Required to use the \`chrome.storage\` API for saving user preferences (like the enable/disable toggle and prototype data) locally.
- \`host_permissions\`: Defines the specific music website URLs where the extension is allowed to inject the \`content.js\` script and \`content.css\` UI. 

## Known Limitations
- The extension uses a lightweight polling mechanism (checking every 2 seconds) to detect track changes. Single Page Applications (SPAs) like these music sites frequently tear down and rebuild their DOM elements, making \`MutationObserver\` overly complex and fragile for a simple prototype.
- If a streaming service significantly changes its webpage structure, the CSS selectors in the platform adapters will need to be updated.
- Currently, "Discover", "My Music", and other tabs contain placeholder/demo data for the Design Thinking prototype.
