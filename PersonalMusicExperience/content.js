// Main content script that manages the injected UI and track monitoring

// Handle Trusted Types for sites that enforce it (like Spotify)
let pmePolicy;
try {
  if (window.trustedTypes && trustedTypes.createPolicy) {
    pmePolicy = trustedTypes.createPolicy('pme-policy', {
      createHTML: (string) => string
    });
  }
} catch (e) {
  console.warn('PME: TrustedTypes policy creation failed', e);
}

function getSafeHTML(html) {
  return pmePolicy ? pmePolicy.createHTML(html) : html;
}

// List of available adapters loaded before this script
const adapters = [SpotifyAdapter, YouTubeMusicAdapter, AppleMusicAdapter];

// Current active adapter
let activeAdapter = null;

// UI Elements
let floatingBtn = null;
let sidePanel = null;
let trackDisplay = null;

let currentTrackCache = null;
let currentVibeCache = null;

// Initialize the content script
async function init() {
  // Check if extension is enabled via storage
  const isEnabled = await StorageUtils.get('extension_enabled', true);
  if (!isEnabled) {
    console.log('Personal Music Experience is disabled.');
    return;
  }

  // Find which platform we are on
  activeAdapter = adapters.find(adapter => adapter.detect());
  
  if (!activeAdapter) {
    console.log('Personal Music Experience: Platform not supported.');
    return;
  }
  
  console.log(`Personal Music Experience: Initialized on ${activeAdapter.name}`);
  
  createUI();
  startTrackMonitoring();
  
  // Initial render of recommendations
  renderRecommendations('balanced', null);
}

// Create the floating button and side panel overlay
function createUI() {
  // 1. Create Floating Button
  floatingBtn = document.createElement('div');
  floatingBtn.id = 'pme-floating-btn';
  floatingBtn.innerHTML = getSafeHTML(`
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9 18V5l12-2v13"></path>
      <circle cx="6" cy="18" r="3"></circle>
      <circle cx="18" cy="16" r="3"></circle>
    </svg>
  `);
  document.body.appendChild(floatingBtn);

  // 2. Create Side Panel
  sidePanel = document.createElement('div');
  sidePanel.id = 'pme-side-panel';
  
  sidePanel.innerHTML = getSafeHTML(`
    <div class="pme-header">
      <h2>Personal Music Exp</h2>
      <button class="pme-close-btn">&times;</button>
    </div>
    
    <div class="pme-platform-info">
      Detected Platform: <strong>${activeAdapter.name}</strong>
    </div>
    
    <div class="pme-now-playing">
      <h3>Now Playing</h3>
      <div id="pme-track-display">Current track not detected</div>
    </div>
    
    <div class="pme-sections">
      <div class="pme-section pme-discover-section">
        <h3>Discover Something New</h3>
        <div id="pme-discover-context">Based on your recent listening</div>
        <div class="pme-discovery-controls">
          <label for="pme-discovery-level">Level:</label>
          <select id="pme-discovery-level">
            <option value="familiar">Familiar</option>
            <option value="balanced" selected>Balanced</option>
            <option value="exploratory">Exploratory</option>
          </select>
        </div>
        <div id="pme-recommendations-list" class="pme-cards">
          <!-- Cards will be rendered here -->
        </div>
      </div>
      
      <div class="pme-section pme-vibe-section">
        <h3>Find by Vibe</h3>
        <div id="pme-vibe-context">Select a vibe to explore</div>
        <div class="pme-tags" id="pme-vibe-tags">
          <span class="pme-tag" data-vibe="chill">Chill</span>
          <span class="pme-tag" data-vibe="focus">Focus</span>
          <span class="pme-tag" data-vibe="energetic">Energetic</span>
          <span class="pme-tag" data-vibe="sad">Sad</span>
          <span class="pme-tag" data-vibe="late night">Late Night</span>
          <span class="pme-tag" data-vibe="workout">Workout</span>
          <span class="pme-tag" data-vibe="romantic">Romantic</span>
          <span class="pme-tag" data-vibe="relaxing">Relaxing</span>
        </div>
        <div id="pme-vibe-recommendations-list" class="pme-cards" style="margin-top: 12px;">
          <!-- Cards will be rendered here -->
        </div>
      </div>
      
      <div class="pme-section">
        <h3>Understand</h3>
        <p>Lyrics, artist backstory, and song meaning insights.</p>
      </div>
      
      <div class="pme-section">
        <h3>My Music</h3>
        <p>Your saved collections and personal tags.</p>
      </div>
      
      <div class="pme-section">
        <h3>My Preferences</h3>
        <p>Tweak discovery algorithm settings.</p>
      </div>
    </div>
  `);
  
  document.body.appendChild(sidePanel);
  
  trackDisplay = document.getElementById('pme-track-display');
  
  // 3. Event Listeners
  floatingBtn.addEventListener('click', () => {
    sidePanel.classList.add('pme-open');
    floatingBtn.style.display = 'none';
  });
  
  const closeBtn = sidePanel.querySelector('.pme-close-btn');
  closeBtn.addEventListener('click', () => {
    sidePanel.classList.remove('pme-open');
    floatingBtn.style.display = 'flex';
  });
  
  // Listen for Discovery Level changes
  const levelSelect = document.getElementById('pme-discovery-level');
  levelSelect.addEventListener('change', (e) => {
    renderRecommendations(e.target.value, currentTrackCache);
  });
  
  // Listen for Vibe tag clicks
  const vibeTags = document.querySelectorAll('#pme-vibe-tags .pme-tag');
  vibeTags.forEach(tag => {
    tag.addEventListener('click', (e) => {
      vibeTags.forEach(t => t.classList.remove('active'));
      e.target.classList.add('active');
      const selectedVibe = e.target.getAttribute('data-vibe');
      currentVibeCache = selectedVibe;
      
      const listEl = document.getElementById('pme-vibe-recommendations-list');
      if (listEl) listEl.style.display = 'flex';
      
      renderVibeRecommendations(selectedVibe, currentTrackCache);
    });
  });
}

// Render the discovery cards
async function renderRecommendations(level, currentTrack) {
  const contextEl = document.getElementById('pme-discover-context');
  const listEl = document.getElementById('pme-recommendations-list');
  
  if (!contextEl || !listEl) return;
  
  // Update context label
  if (currentTrack) {
    contextEl.textContent = `Based on: ${currentTrack.title} – ${currentTrack.artist}`;
  } else {
    contextEl.textContent = 'Based on your recent listening';
  }
  
  // Get saved songs to check button states
  const savedSongs = await StorageUtils.get('saved_songs', []);
  
  // Fetch dynamic recommendations using the Recommendation Engine
  const items = RecommendationEngine.getRecommendations({
    platform: activeAdapter ? activeAdapter.name : 'default',
    currentTrack: currentTrack,
    discoveryLevel: level
  });
  
  let html = '';
  for (const item of items) {
    const isSaved = savedSongs.some(song => song.id === item.id);
    const btnClass = isSaved ? 'pme-save-btn saved' : 'pme-save-btn';
    const btnText = isSaved ? 'Saved' : 'Save';
    
    html += `
      <div class="pme-card">
        <div class="pme-card-title">${escapeHTML(item.title)}</div>
        <div class="pme-card-artist">${escapeHTML(item.artist)}</div>
        <div class="pme-card-genre">${escapeHTML(item.genre)}</div>
        <div class="pme-card-reason">${escapeHTML(item.reason)}</div>
        <button class="${btnClass}" data-id="${item.id}">${btnText}</button>
      </div>
    `;
  }
  
  listEl.innerHTML = getSafeHTML(html);
  
  // Add save listeners
  const saveButtons = listEl.querySelectorAll('.pme-save-btn');
  saveButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const btnEl = e.target;
      const songId = btnEl.getAttribute('data-id');
      
      // Find the song details from our fetched items
      const songDetails = items.find(i => i.id === songId);
      if (!songDetails) return;
      
      let currentSaved = await StorageUtils.get('saved_songs', []);
      
      // Check if already saved
      if (!currentSaved.some(s => s.id === songId)) {
        currentSaved.push(songDetails);
        await StorageUtils.set('saved_songs', currentSaved);
        
        btnEl.classList.add('saved');
        btnEl.textContent = 'Saved';
      }
    });
  });
}

// Render the vibe recommendations
async function renderVibeRecommendations(vibe, currentTrack) {
  const contextEl = document.getElementById('pme-vibe-context');
  const listEl = document.getElementById('pme-vibe-recommendations-list');
  
  if (!contextEl || !listEl) return;
  
  // Update context label
  if (currentTrack) {
    contextEl.textContent = `Current track: ${currentTrack.title} – ${currentTrack.artist}`;
  } else {
    contextEl.textContent = 'Select a vibe to explore';
  }
  
  if (!vibe) {
    listEl.innerHTML = '';
    return;
  }
  
  const savedSongs = await StorageUtils.get('saved_songs', []);
  const items = RecommendationEngine.getVibeRecommendations({
    platform: activeAdapter ? activeAdapter.name : 'default',
    vibe: vibe,
    currentTrack: currentTrack
  });
  
  let html = '';
  for (const item of items) {
    const isSaved = savedSongs.some(song => song.id === item.id);
    const btnClass = isSaved ? 'pme-save-btn saved' : 'pme-save-btn';
    const btnText = isSaved ? 'Saved' : 'Save';
    
    html += `
      <div class="pme-card">
        <div class="pme-card-title">${escapeHTML(item.title)}</div>
        <div class="pme-card-artist">${escapeHTML(item.artist)}</div>
        <div class="pme-card-genre">${escapeHTML(item.genre)}</div>
        <div class="pme-card-reason">${escapeHTML(item.reason)}</div>
        <button class="${btnClass}" data-id="${item.id}">${btnText}</button>
      </div>
    `;
  }
  
  listEl.innerHTML = getSafeHTML(html);
  
  const saveButtons = listEl.querySelectorAll('.pme-save-btn');
  saveButtons.forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const btnEl = e.target;
      const songId = btnEl.getAttribute('data-id');
      const songDetails = items.find(i => i.id === songId);
      if (!songDetails) return;
      
      let currentSaved = await StorageUtils.get('saved_songs', []);
      if (!currentSaved.some(s => s.id === songId)) {
        currentSaved.push(songDetails);
        await StorageUtils.set('saved_songs', currentSaved);
        btnEl.classList.add('saved');
        btnEl.textContent = 'Saved';
      }
    });
  });
}

// Track Monitoring
let lastTrackString = '';

function startTrackMonitoring() {
  setInterval(() => {
    if (!activeAdapter) return;
    
    const trackInfo = activeAdapter.getCurrentTrack();
    
    if (trackInfo) {
      const currentTrackString = `${trackInfo.title} by ${trackInfo.artist}`;
      if (currentTrackString !== lastTrackString) {
        lastTrackString = currentTrackString;
        currentTrackCache = trackInfo;
        updateTrackUI(trackInfo);
        
        // Update recommendations context based on the new track
        const levelSelect = document.getElementById('pme-discovery-level');
        if (levelSelect) {
          renderRecommendations(levelSelect.value, trackInfo);
        }
        
        if (currentVibeCache) {
          renderVibeRecommendations(currentVibeCache, trackInfo);
        }
      }
    } else {
      if (lastTrackString !== '') {
        lastTrackString = '';
        currentTrackCache = null;
        updateTrackUI(null);
        
        // Update recommendations context back to default
        const levelSelect = document.getElementById('pme-discovery-level');
        if (levelSelect) {
          renderRecommendations(levelSelect.value, null);
        }
        
        if (currentVibeCache) {
          renderVibeRecommendations(currentVibeCache, null);
        }
      }
    }
  }, 2000); // Check every 2 seconds
}

// Update the UI with the latest track info
function updateTrackUI(trackInfo) {
  if (!trackDisplay) return;
  
  if (trackInfo) {
    trackDisplay.innerHTML = getSafeHTML(`
      <div class="pme-track-title">${escapeHTML(trackInfo.title)}</div>
      <div class="pme-track-artist">${escapeHTML(trackInfo.artist)}</div>
    `);
  } else {
    trackDisplay.innerHTML = getSafeHTML('Current track not detected');
  }
}

// Helper to prevent XSS when injecting track info into the DOM
function escapeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str || '';
  return div.innerHTML;
}

// Run initialization
init();
