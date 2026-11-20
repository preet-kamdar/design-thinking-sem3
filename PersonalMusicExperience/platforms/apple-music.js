// Platform adapter for Apple Music
const AppleMusicAdapter = {
  name: 'Apple Music',
  
  detect() {
    return window.location.hostname === 'music.apple.com' || window.location.hostname === 'beta.music.apple.com';
  },
  
  getCurrentTrack() {
    try {
      // Strategy 1: Check standard DOM for data-testid
      const titleEl = document.querySelector('span[data-testid="track-title"]');
      const artistEl = document.querySelector('span[data-testid="track-artist"]');
      
      if (titleEl && artistEl) {
        return {
          title: titleEl.textContent.trim(),
          artist: artistEl.textContent.trim()
        };
      }
      
      // Strategy 2: Check standard DOM for legacy classes
      const altTitleEl = document.querySelector('.web-chrome-playback-lcd__song-name-scroll-inner-text-wrapper');
      const altArtistEl = document.querySelector('.web-chrome-playback-lcd__sub-copy-scroll-inner-text-wrapper');
      
      if (altTitleEl && altArtistEl) {
          return {
              title: altTitleEl.textContent.trim(),
              artist: altArtistEl.textContent.trim()
          };
      }
      
      // Strategy 3: Check Web Components (Shadow DOM) which Apple Music uses heavily
      const playbackControls = document.querySelector('apple-music-playback-controls');
      if (playbackControls && playbackControls.shadowRoot) {
        const lcd = playbackControls.shadowRoot.querySelector('apple-music-lcd');
        if (lcd && lcd.shadowRoot) {
          const shadowTitle = lcd.shadowRoot.querySelector('.lcd-meta__title, .lcd-meta__line1');
          const shadowArtist = lcd.shadowRoot.querySelector('.lcd-meta__subtitle, .lcd-meta__line2');
          
          if (shadowTitle && shadowArtist) {
            return {
              title: shadowTitle.textContent.trim(),
              artist: shadowArtist.textContent.trim()
            };
          }
        }
      }

      return null;
    } catch (e) {
      console.warn('Apple Music track detection error', e);
      return null;
    }
  }
};
