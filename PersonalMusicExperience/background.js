// Minimal Background Service Worker
// Manifest V3 requires a service worker for background tasks.
// We keep this file minimal since our main logic is in the content script and popup.

chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Personal Music Experience prototype installed.');
    // Initialize default preferences in local storage
    chrome.storage.local.set({ extension_enabled: true });
  }
});
