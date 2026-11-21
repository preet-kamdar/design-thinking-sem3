/* ---------------------------------------------------------------------------
   Frontend JavaScript for the dashboard.

   BEGINNER NOTES — read this before the rest:
   - This file runs in the BROWSER. app.py runs on the SERVER. They talk over HTTP.
   - "document" means the current web page.
   - querySelector(...) finds ONE element; querySelectorAll(...) finds ALL matches.
   - addEventListener('click', function) means "when clicked, run this function".
   - classList.add/toggle changes CSS classes, which changes how things look.
   - fetch(...) sends a request to Flask and brings back JSON (data).
   - In HTML, data-title="..." becomes JavaScript button.dataset.title here.
   - async + await means "wait for the server, then carry on with the result".
   --------------------------------------------------------------------------- */


// Small helper: POST some data as JSON and return the JSON answer.
// Every button below uses this instead of repeating the same five lines.
async function postJSON(url, body) {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  return response.json();
}


// 1. MOBILE MENU
//    On small screens the navigation links are hidden. This button shows them.
const menuButton = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav');
if (menuButton && navLinks) {
  menuButton.addEventListener('click', function () {
    const isOpen = navLinks.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen)); // for screen readers
  });
}


// 2. SAVE BUTTONS (on Discover and Find by Vibe)
//    Each button carries the song details in data-* attributes. We read those
//    attributes, send them to /api/save, and Flask inserts a row into SQLite.
document.querySelectorAll('.save').forEach(function (button) {
  button.addEventListener('click', async function () {
    if (button.classList.contains('saved')) return; // do not save twice

    const song = {
      title: button.dataset.title,
      artist: button.dataset.artist,
      genre: button.dataset.genre,
      reason: button.dataset.reason,
      source: button.dataset.source
    };

    try {
      const result = await postJSON('/api/save', song);
      if (result.ok) {
        button.classList.add('saved');     // CSS turns it green
        button.textContent = 'Saved ✓';    // change the label
      }
    } catch (error) {
      console.error('Save failed:', error); // visible in DevTools Console
    }
  });
});


// 3. REMOVE BUTTONS (on My Music)
//    The button's data-id is the row's id in the saved_songs table.
document.querySelectorAll('.unsave').forEach(function (button) {
  button.addEventListener('click', async function () {
    try {
      const result = await postJSON('/api/unsave/' + button.dataset.id, {});
      if (result.ok) {
        button.closest('.song-row').remove(); // remove the whole row from the page
      }
    } catch (error) {
      console.error('Remove failed:', error);
    }
  });
});


// 4. STUDY PAGE — TASK TIMER
//    Start: remember the time. Stop: work out the duration, count clicks, send
//    everything to /api/task so Flask can store it in the test_tasks table.
const taskPanel = document.getElementById('task-panel');
const taskStatus = document.getElementById('task-status');
if (taskPanel) {
  let activeTask = null;
  let startedAt = null;
  let startTime = 0;
  let clicks = 0;
  let errors = 0;

  // The "true" counts clicks anywhere on the page, including inside buttons.
  document.addEventListener('click', function () {
    if (activeTask) clicks++;
  }, true);

  taskPanel.querySelectorAll('.task-start').forEach(function (button) {
    button.addEventListener('click', async function () {
      if (!activeTask) {
        // --- START THE TIMER ---
        activeTask = button.dataset.task;
        startedAt = new Date().toISOString();
        startTime = performance.now();
        clicks = 0;
        errors = 0;
        button.classList.add('running');
        button.querySelector('span').textContent = 'Running… click again to stop';
        taskStatus.textContent = 'Task started: ' + activeTask;
        await postJSON('/api/event', { type: 'task_start', detail: activeTask });

      } else if (button.classList.contains('running')) {
        // --- STOP THE TIMER ---
        const duration = Math.round(performance.now() - startTime);
        button.classList.remove('running');
        button.querySelector('span').textContent = 'Start timer';
        const completed = confirm('Did you complete the task successfully?');
        if (!completed) errors++;

        await postJSON('/api/task', {
          task: activeTask,
          started_at: startedAt,
          ended_at: new Date().toISOString(),
          duration_ms: duration,
          clicks: clicks,
          errors: errors,
          completed: completed
        });
        taskStatus.textContent = 'Recorded: ' + activeTask + ' — ' +
          (duration / 1000).toFixed(1) + 's, ' + clicks + ' clicks.';
        activeTask = null;
        setTimeout(function () { location.reload(); }, 1200); // show the new table row
      }
    });
  });
}


// 5. SUS FORM (System Usability Scale)
//    Ten questions answered 1-5. Odd questions are positive: score = answer - 1.
//    Even questions are negative: score = 5 - answer. Add them (0-40), x 2.5 = 0-100.
const susForm = document.getElementById('sus-form');
if (susForm) {
  susForm.addEventListener('submit', async function (event) {
    event.preventDefault(); // stop the browser from reloading the page

    let total = 0;
    for (let i = 1; i <= 10; i++) {
      const picked = susForm.querySelector('input[name="q' + i + '"]:checked');
      if (!picked) return;                   // require every question to be answered
      const answer = Number(picked.value);   // radio values arrive as text
      if (i % 2 === 1) {
        total = total + (answer - 1);        // questions 1,3,5,7,9
      } else {
        total = total + (5 - answer);        // questions 2,4,6,8,10
      }
    }

    const score = total * 2.5;
    const result = document.getElementById('sus-result');
    result.textContent = 'SUS score: ' + score.toFixed(1) + ' / 100 — ' +
      (score >= 68 ? 'above average usability.' : 'below average; needs iteration.');

    await postJSON('/api/event', { type: 'sus_score', detail: score.toFixed(1) });
  });
}
