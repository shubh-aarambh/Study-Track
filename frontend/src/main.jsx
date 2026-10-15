import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = '/api';
const NEXT = { PENDING: 'IN_PROGRESS', IN_PROGRESS: 'SUBMITTED', SUBMITTED: 'PENDING' };
const LABEL = { PENDING: 'Pending', IN_PROGRESS: 'In progress', SUBMITTED: 'Submitted' };
const EMPTY_STATS = { total: 0, pending: 0, inProgress: 0, submitted: 0, overdue: 0, avgProgress: 0 };

const isOverdue = (a) => a.due_date && a.status !== 'SUBMITTED' && new Date(a.due_date) < new Date(new Date().toDateString());
const fmtDate = (d) => (d ? new Date(d).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }) : 'No deadline');

function App() {
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState(EMPTY_STATS);
  const [filter, setFilter] = useState('ALL');
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const load = async () => {
    try {
      setError('');
      const [a, b] = await Promise.all([fetch(`${API}/assignments`), fetch(`${API}/assignments/stats`)]);
      if (!a.ok || !b.ok) throw Error('Backend unavailable');
      setItems(await a.json());
      setStats(await b.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => { load(); }, []);

  const visible = useMemo(() => (filter === 'ALL' ? items : items.filter((a) => a.status === filter)), [items, filter]);
  const upcoming = useMemo(() => items.filter((a) => a.status !== 'SUBMITTED' && a.due_date).slice(0, 4), [items]);

  const advance = async (a) => {
    await fetch(`${API}/assignments/${a.id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: NEXT[a.status], progress: NEXT[a.status] === 'IN_PROGRESS' ? Math.max(a.progress, 25) : undefined }),
    });
    load();
  };
  const remove = async (a) => { await fetch(`${API}/assignments/${a.id}`, { method: 'DELETE' }); load(); };
  const create = async (e) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    await fetch(`${API}/assignments`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: f.get('title'), subject: f.get('subject') || 'General', notes: f.get('notes'),
        priority: f.get('priority'), due_date: f.get('due_date') || null, progress: Number(f.get('progress') || 0),
      }),
    });
    e.currentTarget.reset();
    setShowForm(false);
    load();
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand"><span className="brand-mark">S</span><div><b>StudyTrack</b><small>Assignment planner</small></div></div>
        <nav>
          <a className="active">▦ <span>Dashboard</span></a>
          <a>✎ <span>Assignments</span></a>
          <a>◷ <span>Deadlines</span></a>
          <a>★ <span>Progress</span></a>
        </nav>
        <div className="side-bottom">
          <div className="upgrade"><strong>Average progress</strong>
            <div className="meter"><i style={{ width: `${stats.avgProgress}%` }} /></div>
            <p>{stats.avgProgress}% across all assignments</p></div>
          <div className="profile"><div className="avatar">ST</div><div><b>Student</b><small>Semester 4</small></div></div>
        </div>
      </aside>

      <main className="main">
        <header>
          <div>
            <p className="eyebrow">STUDY WORKSPACE / OVERVIEW</p>
            <h1>Stay ahead of every deadline</h1>
            <p className="muted">Track assignments, subjects and progress in one place.</p>
          </div>
          <button id="new-assignment" className="primary" onClick={() => setShowForm(true)}>＋ New assignment</button>
        </header>

        {error && <div className="alert">⚠ {error}. Start the backend and PostgreSQL, then refresh.</div>}

        <section className="stats">
          <Stat label="Total assignments" value={stats.total} icon="▦" tone="indigo" />
          <Stat label="In progress" value={stats.inProgress} icon="◔" tone="amber" />
          <Stat label="Submitted" value={stats.submitted} icon="✓" tone="green" />
          <Stat label="Overdue" value={stats.overdue} icon="!" tone="red" />
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-head">
              <div><h2>Assignments</h2><p className="muted">Everything on your plate this semester.</p></div>
              <div className="filters">
                {['ALL', 'PENDING', 'IN_PROGRESS', 'SUBMITTED'].map((x) => (
                  <button key={x} className={filter === x ? 'selected' : ''} onClick={() => setFilter(x)}>
                    {x === 'ALL' ? 'All' : LABEL[x]}
                  </button>
                ))}
              </div>
            </div>
            {loading ? <div className="empty">Loading assignments…</div> : (
              <div className="table-wrap">
                <table>
                  <thead><tr><th>Assignment</th><th>Subject</th><th>Due</th><th>Priority</th><th>Progress</th><th>Status</th><th></th></tr></thead>
                  <tbody>
                    {visible.map((a) => (
                      <tr key={a.id}>
                        <td><div className="task-title"><span className={`dot ${a.status.toLowerCase()}`} /><div><b>{a.title}</b><small>{a.notes}</small></div></div></td>
                        <td><span className="chip">{a.subject}</span></td>
                        <td className={isOverdue(a) ? 'late' : ''}>{fmtDate(a.due_date)}{isOverdue(a) && ' · overdue'}</td>
                        <td><span className={`priority ${a.priority.toLowerCase()}`}>{a.priority}</span></td>
                        <td><div className="bar"><i style={{ width: `${a.progress}%` }} /></div><small className="pct">{a.progress}%</small></td>
                        <td><span className={`status ${a.status.toLowerCase()}`}>{LABEL[a.status]}</span></td>
                        <td className="actions">
                          <button className="icon-btn" onClick={() => advance(a)} title="Advance status">↻</button>
                          <button className="icon-btn danger" onClick={() => remove(a)} title="Delete">🗑</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {!visible.length && <div className="empty">No assignments in this view.</div>}
              </div>
            )}
          </div>

          <aside className="panel activity">
            <div className="panel-head"><div><h2>Upcoming deadlines</h2><p className="muted">Nearest first.</p></div></div>
            {upcoming.length ? upcoming.map((a) => (
              <div className="activity-row" key={a.id}>
                <span className="activity-icon">{fmtDate(a.due_date).split(' ')[0]}</span>
                <div><b>{a.title}</b><small>{a.subject} · {fmtDate(a.due_date)}</small></div>
              </div>
            )) : <div className="empty">Nothing due. Enjoy the calm.</div>}
          </aside>
        </section>

        {showForm && (
          <div className="modal-backdrop">
            <form className="modal" onSubmit={create}>
              <div className="modal-head">
                <div><p className="eyebrow">CREATE ASSIGNMENT</p><h2>Add a new assignment</h2></div>
                <button type="button" className="close" onClick={() => setShowForm(false)}>×</button>
              </div>
              <label>Title<input name="title" required placeholder="e.g. DevOps capstone report" /></label>
              <label>Notes<textarea name="notes" placeholder="What needs to be done?" /></label>
              <div className="form-row">
                <label>Subject<input name="subject" placeholder="DevOps" /></label>
                <label>Due date<input name="due_date" type="date" /></label>
              </div>
              <div className="form-row">
                <label>Priority<select name="priority" defaultValue="MEDIUM"><option>LOW</option><option>MEDIUM</option><option>HIGH</option></select></label>
                <label>Progress %<input name="progress" type="number" min="0" max="100" defaultValue="0" /></label>
              </div>
              <button className="primary full">Create assignment</button>
            </form>
          </div>
        )}
      </main>
    </div>
  );
}

function Stat({ label, value, icon, tone }) {
  return (
    <div className="stat">
      <div className={`stat-icon ${tone}`}>{icon}</div>
      <div><small>{label}</small><strong>{value}</strong><span>Updated just now</span></div>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
