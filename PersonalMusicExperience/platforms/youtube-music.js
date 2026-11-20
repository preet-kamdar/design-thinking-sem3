// Platform adapter for YouTube Music
const YouTubeMusicAdapter = {
  name: 'YouTube Music',
  
  detect() {
    return window.location.hostname === 'music.youtube.com';
  },
  
  getCurrentTrack() {
    try {
      // Look for the track details in the bottom player bar
      const titleEl = document.querySelector('yt-formatted-string.title.ytmusic-player-bar');
      const artistEl = document.querySelector('yt-formatted-string.byline.ytmusic-player-bar');
      
      if (titleEl && artistEl) {
        let artist = artistEl.getAttribute('title') || artistEl.textContent.trim();
        // YouTube Music byline includes album and year separated by bullet points
        artist = artist.split('•')[0].trim();
        
        return {
          title: titleEl.getAttribute('title') || titleEl.textContent.trim(),
          artist: artist
        };
      }
      return null;
    } catch (e) {
      console.warn('YouTube Music track detection error', e);
      return null;
    }
  }
};
