// Platform adapter for Spotify
const SpotifyAdapter = {
  name: 'Spotify',
  
  detect() {
    return window.location.hostname === 'open.spotify.com';
  },
  
  getCurrentTrack() {
    try {
      // Look for the track title and artist in the bottom player
      const titleEl = document.querySelector('[data-testid="context-item-info-title"]');
      const artistEl = document.querySelector('[data-testid="context-item-info-subtitles"]');
      
      if (titleEl && artistEl) {
        return {
          title: titleEl.textContent.trim(),
          artist: artistEl.textContent.trim()
        };
      }
      return null;
    } catch (e) {
      console.warn('Spotify track detection error', e);
      return null;
    }
  }
};
