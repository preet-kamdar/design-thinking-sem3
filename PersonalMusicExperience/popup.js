document.addEventListener('DOMContentLoaded', async () => {
  const enableToggle = document.getElementById('enable-toggle');
  const resetBtn = document.getElementById('reset-btn');
  const resetMsg = document.getElementById('reset-msg');

  // Load current toggle state from storage
  const isEnabled = await StorageUtils.get('extension_enabled', true);
  enableToggle.checked = isEnabled;

  // Handle toggle changes
  enableToggle.addEventListener('change', async (e) => {
    await StorageUtils.set('extension_enabled', e.target.checked);
  });

  // Handle reset data button
  resetBtn.addEventListener('click', async () => {
    const success = await StorageUtils.clear();
    
    // Restore the toggle state since we just cleared all storage
    await StorageUtils.set('extension_enabled', enableToggle.checked);
    
    if (success) {
      resetMsg.textContent = 'Local data reset successfully.';
      setTimeout(() => {
        resetMsg.textContent = '';
      }, 3000);
    } else {
      resetMsg.textContent = 'Failed to reset data.';
      resetMsg.style.color = '#f15e6c';
    }
  });
});
