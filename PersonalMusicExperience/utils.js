// Storage utility layer
// Uses chrome.storage.local to persist data without leaving the browser.
// The 'storage' permission in manifest.json is required to use this API.

const StorageUtils = {
  /**
   * Get a value from local storage
   */
  async get(key, defaultValue = null) {
    try {
      const result = await chrome.storage.local.get(key);
      return result[key] !== undefined ? result[key] : defaultValue;
    } catch (e) {
      console.error('Storage get error:', e);
      return defaultValue;
    }
  },
  
  /**
   * Set a value in local storage
   */
  async set(key, value) {
    try {
      await chrome.storage.local.set({ [key]: value });
      return true;
    } catch (e) {
      console.error('Storage set error:', e);
      return false;
    }
  },
  
  /**
   * Clear all local storage data
   */
  async clear() {
    try {
      await chrome.storage.local.clear();
      return true;
    } catch (e) {
      console.error('Storage clear error:', e);
      return false;
    }
  }
};
