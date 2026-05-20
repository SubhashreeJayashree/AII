
async function api(path, opts) {
  const res = await fetch(path, Object.assign({headers: {'Content-Type':'application/json'}}, opts));
  return res.json();
}

function el(tag, txt, className) {
  const e = document.createElement(tag);
  if (txt) e.textContent = txt;
  if (className) e.className = className;
  return e;
}

function dayName(d){ return ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][d]; }

async function loadAssignments() {
  const items = await api('/api/assignments');
  const container = document.getElementById('assignments');
  container.innerHTML = '';
  const pom = parseInt(document.getElementById('pom').value || 25);
  const blocksPerHour = 60 / pom;
  items.forEach(a => {
    const d = document.createElement('div'); d.className='assignment';
    const totalBlocks = Math.max(1, Math.ceil((a.est_hours||0) * blocksPerHour));
    const completed = parseInt(a.completed_blocks || 0);
    const remaining = Math.max(0, totalBlocks - completed);
    d.appendChild(el('div', `${a.title} — ${a.course || ''}`));
    d.appendChild(el('div', `Due: ${a.due_date} — Est hours: ${a.est_hours} — Blocks: ${totalBlocks}`));
    d.appendChild(el('div', `Completed: ${completed} — Remaining: ${remaining}`));
    // progress bar
    const progress = document.createElement('div'); progress.className='progress';
    const pct = Math.round((completed/totalBlocks)*100);
    const fill = document.createElement('div'); fill.className='fill'; fill.style.width = pct + '%';
    progress.appendChild(fill);
    d.appendChild(progress);
    const row = document.createElement('div'); row.className='row';
    const del = el('button','Delete'); del.onclick = async ()=>{ if (confirm('Delete this assignment?')){ await api('/api/assignments?id='+a.id, {method:'DELETE'}); loadAssignments(); } };
    row.appendChild(del);
    d.appendChild(row);
    container.appendChild(d);
  });
}

// Availability windows UI
let windowsState = [];
function makeWindowRow(w){
  const wrap = document.createElement('div'); wrap.className='av-day';
  const sel = document.createElement('select');
  for(let i=0;i<7;i++){ const o = document.createElement('option'); o.value=i; o.textContent = dayName(i); if (w && +w.day===i) o.selected=true; sel.appendChild(o); }
  const start = document.createElement('input'); start.type='time'; start.value = (w && w.start) || '19:00';
  const end = document.createElement('input'); end.type='time'; end.value = (w && w.end) || '20:00';
  const rem = el('button','Remove','ghost'); rem.onclick = ()=>{ wrap.remove(); };
  wrap.appendChild(sel); wrap.appendChild(start); wrap.appendChild(end); wrap.appendChild(rem);
  return wrap;
}

async function loadWindows(){
  const rows = await api('/api/availability');
  const c = document.getElementById('windows');
  c.innerHTML = '';
  // rows may be older hours format or windows format
  if (rows.length>0 && rows[0].start){
    rows.forEach(r=>{
      windowsState.push(r);
      c.appendChild(makeWindowRow(r));
    });
  } else {
    // fallback: build windows from hours (one evening window per day starting 19:00)
    rows.sort((a,b)=>a.day-b.day).forEach(r=>{
      const hours = parseFloat(r.hours)||0;
      if (hours<=0) return;
      const start = '19:00';
      // simple end calc
      const [hh,mm] = start.split(':').map(Number);
      const endDate = new Date(2000,0,1,hh,mm);
      endDate.setHours(endDate.getHours()+hours);
      const end = endDate.toTimeString().slice(0,5);
      const obj = {day: r.day, start: start, end: end};
      windowsState.push(obj);
      c.appendChild(makeWindowRow(obj));
    });
  }
}

document.getElementById('addWindow').onclick = ()=>{ const c = document.getElementById('windows'); c.appendChild(makeWindowRow({day:0,start:'19:00',end:'20:00'})); };
document.getElementById('saveWindows').onclick = async ()=>{
  const rows = Array.from(document.querySelectorAll('#windows .av-day'));
  const payload = rows.map(r=>{
    return { day: parseInt(r.querySelector('select').value), start: r.querySelector('input[type=time]').value, end: r.querySelectorAll('input[type=time]')[1].value };
  });
  await api('/api/availability', {method:'POST', body: JSON.stringify(payload)});
  alert('Saved windows');
};

// generate
document.getElementById('gen').onclick = async ()=>{
  const pom = parseInt(document.getElementById('pom').value || 25);
  const res = await api('/api/generate', {method:'POST', body: JSON.stringify({pomodoro: pom})});
  renderSchedule(res.schedule);
};

function renderSchedule(list) {
  const c = document.getElementById('schedule');
  c.innerHTML = '';
  if (!list || list.length===0) { c.textContent='No scheduled sessions'; return; }
  list.forEach(s=>{
    const d = document.createElement('div'); d.className='assignment';
    const when = new Date(s.start).toLocaleString();
    d.appendChild(el('div', `${when} — ${s.title} (${s.course})`));
    if (s.overbooked) d.appendChild(el('div','Overbooked', 'overbooked'));
    const btn = el('button', 'Mark Done');
    btn.onclick = async ()=>{
      const answer = prompt(`Mark how many pomodoro blocks done for "${s.title}"?`, '1');
      if (!answer) return;
      const count = parseInt(answer);
      if (isNaN(count) || count <= 0) { alert('Invalid number'); return; }
      if (!confirm(`Confirm marking ${count} block(s) as done for "${s.title}"?`)) return;
      await api('/api/complete', {method:'POST', body: JSON.stringify({task_id: s.task_id, count:count})});
      const pom = parseInt(document.getElementById('pom').value||25);
      const res = await api('/api/generate', {method:'POST', body: JSON.stringify({pomodoro: pom})});
      renderSchedule(res.schedule);
      await loadAssignments();
    };
    const progress = document.createElement('div'); progress.className='progress';
    const fill = document.createElement('div'); fill.className='fill'; fill.style.width = '0%';
    progress.appendChild(fill);
    d.appendChild(progress);
    d.appendChild(btn);
    c.appendChild(d);
  });

  window._lastSchedule = list;
}

// export
document.getElementById('export').onclick = async ()=>{
  if (!window._lastSchedule) { alert('Generate a schedule first'); return; }
  const res = await api('/api/export_ics', {method:'POST', body: JSON.stringify({schedule: window._lastSchedule})});
  const blob = new Blob([res.ics], {type:'text/calendar;charset=utf-8'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = 'study-schedule.ics';
  a.click();
  URL.revokeObjectURL(url);
};

window.addEventListener('load', ()=>{
  loadAssignments();
  loadWindows();
});
