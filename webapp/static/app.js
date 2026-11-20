/* Frontend logic for the companion dashboard. */
(function () {
  'use strict';

  // Mobile nav
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
  }

  // Save buttons (Discover / Vibe)
  document.querySelectorAll('.save').forEach((btn) => {
    btn.addEventListener('click', async () => {
      if (btn.classList.contains('saved')) return;
      const payload = {
        title: btn.dataset.title,
        artist: btn.dataset.artist,
        genre: btn.dataset.genre,
        reason: btn.dataset.reason,
        source: btn.dataset.source,
      };
      try {
        const res = await fetch('/api/save', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (data.ok) {
          btn.classList.add('saved');
          btn.textContent = 'Saved ✓';
        }
      } catch (err) {
        console.error('Save failed', err);
      }
    });
  });

  // Remove buttons (My Music)
  document.querySelectorAll('.unsave').forEach((btn) => {
    btn.addEventListener('click', async () => {
      try {
        const res = await fetch('/api/unsave/' + btn.dataset.id, { method: 'POST' });
        const data = await res.json();
        if (data.ok) btn.closest('.song-row').remove();
      } catch (err) {
        console.error('Remove failed', err);
      }
    });
  });

  // Stage 5 task timer: start / stop, clicks counted globally.
  const panel = document.getElementById('task-panel');
  const status = document.getElementById('task-status');
  if (panel) {
    let activeTask = null;
    let startedAt = null;
    let startMs = 0;
    let clicks = 0;
    let errors = 0;

    document.addEventListener('click', () => { if (activeTask) clicks++; }, true);

    panel.querySelectorAll('.task-start').forEach((btn) => {
      btn.addEventListener('click', async () => {
        if (!activeTask) {
          activeTask = btn.dataset.task;
          startedAt = new Date().toISOString();
          startMs = performance.now();
          clicks = 0; errors = 0;
          btn.classList.add('running');
          btn.querySelector('span').textContent = 'Running… click again to stop';
          status.textContent = 'Task started: ' + activeTask;
          await fetch('/api/event', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'task_start', detail: activeTask }),
          });
        } else if (btn.classList.contains('running')) {
          const duration = Math.round(performance.now() - startMs);
          btn.classList.remove('running');
          btn.querySelector('span').textContent = 'Start timer';
          const completed = confirm('Did you complete the task successfully?');
          if (!completed) errors++;
          await fetch('/api/task', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              task: activeTask, started_at: startedAt, ended_at: new Date().toISOString(),
              duration_ms: duration, clicks, errors, completed,
            }),
          });
          status.textContent = `Recorded: ${activeTask} — ${(duration / 1000).toFixed(1)}s, ${clicks} clicks.`;
          activeTask = null;
          setTimeout(() => location.reload(), 1200);
        }
      });
    });
  }

  // SUS score: odd items x-1, even items 5-x, sum * 2.5
  const susForm = document.getElementById('sus-form');
  if (susForm) {
    susForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const values = [];
      for (let i = 1; i <= 10; i++) {
        const el = susForm.querySelector(`input[name="q${i}"]:checked`);
        if (!el) return;
        values.push(Number(el.value));
      }
      const raw = values.reduce((sum, v, i) => sum + (i % 2 === 0 ? 5 - v : v - 1), 0);
      const score = raw * 2.5;
      const result = document.getElementById('sus-result');
      result.textContent = `SUS score: ${score.toFixed(1)} / 100 — ` +
        (score >= 68 ? 'above average usability.' : 'below average; needs iteration.');
      await fetch('/api/event', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'sus_score', detail: score.toFixed(1) }),
      });
    });
  }
})();
