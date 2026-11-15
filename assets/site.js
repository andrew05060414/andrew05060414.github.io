/* Native dialogs enhance ordinary anchors. All content remains readable without JS. */
const root = document.querySelector('.aw');
const themeButton = document.querySelector('[data-theme-toggle]');
const zh = document.documentElement.lang === 'zh-CN';
let theme = 'crt';
try { theme = localStorage.getItem('aw-theme') === 'paper' ? 'paper' : 'crt'; } catch { /* Storage can be disabled. */ }
function applyTheme() {
  root.classList.toggle('pal-paper', theme === 'paper');
  root.classList.toggle('pal-crt', theme !== 'paper');
  document.querySelector('meta[name="theme-color"]').content = theme === 'paper' ? '#eae7df' : '#0a0b09';
  themeButton.setAttribute('aria-pressed', String(theme === 'paper'));
}
applyTheme();
themeButton.addEventListener('click', () => {
  theme = theme === 'crt' ? 'paper' : 'crt';
  applyTheme();
  try { localStorage.setItem('aw-theme', theme); } catch { /* Keep the theme for this page. */ }
});

const clock = document.querySelector('[data-clock]');
const timeZone = document.querySelector('[data-timezone]');
function updateClock() {
  const now = new Date();
  clock.dateTime = now.toISOString();
  clock.textContent = new Intl.DateTimeFormat('en-GB', { timeZone:'America/New_York', hour:'2-digit', minute:'2-digit', hour12:false }).format(now);
  timeZone.textContent = new Intl.DateTimeFormat('en-US', {timeZone:'America/New_York',timeZoneName:'short'}).formatToParts(now).find(p => p.type === 'timeZoneName').value;
}
updateClock();
setInterval(updateClock, 30000);

if ('HTMLDialogElement' in window && typeof HTMLDialogElement.prototype.showModal === 'function') {
  const dialog = document.createElement('dialog');
  dialog.className = 'file-dialog';
  dialog.setAttribute('closedby', 'any');
  const slot = document.createElement('div');
  dialog.append(slot);
  root.append(dialog);
  const archives = document.querySelector('.archives');
  let current = null;
  let launchedFromHash = false;
  function restore() {
    if (current) archives.append(current);
    current = null;
    dialog.returnValue = '';
    if (document.querySelector('.file-section:target') || launchedFromHash) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    launchedFromHash = false;
  }
  dialog.addEventListener('close', restore);
  for (const link of document.querySelectorAll('[data-panel]')) {
    link.setAttribute('aria-haspopup', 'dialog');
    link.addEventListener('click', event => {
      const section = document.getElementById(link.dataset.panel);
      if (!section) return;
      event.preventDefault();
      current = section;
      slot.append(section);
      dialog.setAttribute('aria-labelledby', section.id + '-title');
      dialog.showModal();
    });
  }
  dialog.addEventListener('click', event => {
    if (event.target.closest('[data-close]')) {
      event.preventDefault();
      dialog.close();
    }
  });
  // Progressive light-dismiss fallback for Safari. A drag ending outside is not a click.
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    const outside = e => { const r = dialog.getBoundingClientRect(); return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom; };
    let pressedOutside = false;
    dialog.addEventListener('pointerdown', e => { pressedOutside = outside(e); });
    dialog.addEventListener('pointerup', e => { if (pressedOutside && outside(e)) dialog.close(); });
  }
  const id = decodeURIComponent(location.hash.slice(1));
  const launch = [...document.querySelectorAll('.dock [data-panel]')].find(a => a.dataset.panel === id);
  if (launch) { launchedFromHash = true; launch.click(); }
  root.classList.add('enhanced');
}

// Keep the selected file when following the alternate-language link.
for (const link of document.querySelectorAll('.lgs a')) {
  link.addEventListener('click', () => {
    const open = document.querySelector('dialog[open] .file-section');
    if (open) link.hash = open.id;
  });
}
document.documentElement.dataset.ready = 'true';
