import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = '/api';
const NEXT = { PENDING: 'IN_PROGRESS', IN_PROGRESS: 'SUBMITTED', SUBMITTED: 'PENDING' };
const LABEL = { PENDING: 'Pending', IN_PROGRESS: 'In Progress', SUBMITTED: 'Submitted' };
const EMPTY_STATS = { total: 0, pending: 0, inProgress: 0, submitted: 0, overdue: 0, avgProgress: 0 };

const isOverdue = (a) => a.due_date && a.status !== 'SUBMITTED' && new Date(a.due_date) < new Date(new Date().toDateString());
const fmtDate = (d) => (d ? new Date(d).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' }) : 'No deadline');

function App() {
  const [activeTab, setActiveTab] = useState('DASHBOARD');
  const [items, setItems] = useState([]);
  const [stats, setStats] = useState(EMPTY_STATS);
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [filterSubject, setFilterSubject] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [editingItem, setEditingItem] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [backendHealth, setBackendHealth] = useState({ status: 'CHECKING', db: 'CHECKING' });
  const [toasts, setToasts] = useState([]);

  const addToast = (msg) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, msg }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3500);
  };

  const load = async () => {
    try {
      const [resAssignments, resStats] = await Promise.all([
        fetch(`${API}/assignments`),
        fetch(`${API}/assignments/stats`),
      ]);
      if (resAssignments.ok) setItems(await resAssignments.json());
      if (resStats.ok) setStats(await resStats.json());

      // Check health & readiness
      const [resHealth, resReady] = await Promise.all([
        fetch('/health').catch(() => null),
        fetch('/ready').catch(() => null),
      ]);
      setBackendHealth({
        status: resHealth && resHealth.ok ? 'UP' : 'DOWN',
        db: resReady && resReady.ok ? 'READY' : 'ERROR',
      });
    } catch (e) {
      console.error('Fetch error:', e);
      setBackendHealth({ status: 'DOWN', db: 'DISCONNECTED' });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  const subjects = useMemo(() => {
    const set = new Set(['DevOps', 'Cloud Computing', 'Database Systems', 'Algorithms']);
    items.forEach((i) => i.subject && set.add(i.subject));
    return Array.from(set);
  }, [items]);

  const filteredItems = useMemo(() => {
    return items.filter((a) => {
      const matchesStatus = filterStatus === 'ALL' || a.status === filterStatus;
      const matchesSubject = filterSubject === 'ALL' || a.subject === filterSubject;
      const matchesSearch =
        !searchQuery ||
        a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (a.notes && a.notes.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (a.subject && a.subject.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesStatus && matchesSubject && matchesSearch;
    });
  }, [items, filterStatus, filterSubject, searchQuery]);

  const upcoming = useMemo(() => {
    return items
      .filter((a) => a.status !== 'SUBMITTED' && a.due_date)
      .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
      .slice(0, 5);
  }, [items]);

  const advance = async (a) => {
    const nextStatus = NEXT[a.status];
    const newProgress = nextStatus === 'IN_PROGRESS' ? Math.max(a.progress, 25) : nextStatus === 'SUBMITTED' ? 100 : 0;
    try {
      const res = await fetch(`${API}/assignments/${a.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: nextStatus, progress: newProgress }),
      });
      if (res.ok) {
        addToast(`Advanced "${a.title}" to ${LABEL[nextStatus]}`);
        load();
      }
    } catch {
      addToast('Failed to advance assignment');
    }
  };

  const remove = async (a) => {
    if (!window.confirm(`Delete assignment "${a.title}"?`)) return;
    try {
      const res = await fetch(`${API}/assignments/${a.id}`, { method: 'DELETE' });
      if (res.ok) {
        addToast(`Deleted "${a.title}"`);
        load();
      }
    } catch {
      addToast('Failed to delete assignment');
    }
  };

  const saveAssignment = async (e) => {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const payload = {
      title: f.get('title'),
      subject: f.get('subject') || 'General',
      notes: f.get('notes') || '',
      priority: f.get('priority'),
      due_date: f.get('due_date') || null,
      progress: Number(f.get('progress') || 0),
    };

    try {
      if (editingItem) {
        const res = await fetch(`${API}/assignments/${editingItem.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (res.ok) addToast(`Updated "${payload.title}"`);
      } else {
        const res = await fetch(`${API}/assignments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (res.ok) addToast(`Created "${payload.title}"`);
      }
      setShowModal(false);
      setEditingItem(null);
      load();
    } catch {
      addToast('Error saving assignment');
    }
  };

  const openCreate = () => {
    setEditingItem(null);
    setShowModal(true);
  };

  const openEdit = (item) => {
    setEditingItem(item);
    setShowModal(true);
  };

  return (
    <div className="app">
      {/* Toast Notifications */}
      <div className="toast-container">
        {toasts.map((t) => (
          <div key={t.id} className="toast">
            <span>✨</span>
            <span>{t.msg}</span>
          </div>
        ))}
      </div>

      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark">S</span>
          <div>
            <b>StudyTrack</b>
            <small>Cloud-Native DevOps Edition</small>
          </div>
        </div>

        <nav>
          <a className={activeTab === 'DASHBOARD' ? 'active' : ''} onClick={() => setActiveTab('DASHBOARD')}>
            <span>▦</span> <span>Dashboard</span>
          </a>
          <a className={activeTab === 'ASSIGNMENTS' ? 'active' : ''} onClick={() => setActiveTab('ASSIGNMENTS')}>
            <span>✎</span> <span>Assignments</span>
          </a>
          <a className={activeTab === 'DEADLINES' ? 'active' : ''} onClick={() => setActiveTab('DEADLINES')}>
            <span>◷</span> <span>Deadlines</span>
          </a>
          <a className={activeTab === 'DEVOPS' ? 'active' : ''} onClick={() => setActiveTab('DEVOPS')}>
            <span>⚡</span> <span>DevOps & Metrics</span>
          </a>
        </nav>

        <div className="side-bottom">
          <div className="health-badge">
            <span className="health-dot" style={{ background: backendHealth.status === 'UP' ? '#10b981' : '#ef4444' }} />
            <div>
              <strong>API: {backendHealth.status}</strong>
              <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.6)' }}>DB: {backendHealth.db}</div>
            </div>
          </div>

          <div className="side-progress">
            <strong>
              <span>Overall Progress</span>
              <span>{stats.avgProgress}%</span>
            </strong>
            <div className="meter" style={{ marginTop: '8px' }}>
              <i style={{ width: `${stats.avgProgress}%` }} />
            </div>
            <p>{stats.submitted} of {stats.total} submitted</p>
          </div>
        </div>
      </aside>

      {/* Main Area */}
      <main className="main">
        <header>
          <div>
            <p className="eyebrow">
              {activeTab === 'DASHBOARD' && 'WORKSPACE / OVERVIEW'}
              {activeTab === 'ASSIGNMENTS' && 'STUDY PLANNER / ASSIGNMENTS'}
              {activeTab === 'DEADLINES' && 'CALENDAR / SCHEDULE'}
              {activeTab === 'DEVOPS' && 'OBSERVABILITY / INFRASTRUCTURE'}
            </p>
            <h1>
              {activeTab === 'DASHBOARD' && 'Stay Ahead of Every Deadline'}
              {activeTab === 'ASSIGNMENTS' && 'Assignment Management'}
              {activeTab === 'DEADLINES' && 'Upcoming Due Dates & Milestones'}
              {activeTab === 'DEVOPS' && 'DevOps Pipeline & Observability'}
            </h1>
            <p className="muted">
              {activeTab === 'DASHBOARD' && 'Full visibility into assignments, progress KPIs, and upcoming priorities.'}
              {activeTab === 'ASSIGNMENTS' && 'Filter, search, organize, and update course tasks in real time.'}
              {activeTab === 'DEADLINES' && 'Track near-term deadlines and avoid overdue submissions.'}
              {activeTab === 'DEVOPS' && 'Monitor container health, Prometheus telemetry, and API documentation.'}
            </p>
          </div>

          <div className="header-actions">
            <button id="new-assignment" className="btn btn-primary" onClick={openCreate}>
              ＋ New Assignment
            </button>
            <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="btn btn-secondary" title="Open FastAPI Swagger Documentation">
              API Docs ↗
            </a>
          </div>
        </header>

        {/* Global KPI Cards */}
        <section className="stats">
          <Stat label="Total Assignments" value={stats.total} icon="▦" tone="indigo" />
          <Stat label="In Progress" value={stats.inProgress} icon="◔" tone="amber" />
          <Stat label="Submitted" value={stats.submitted} icon="✓" tone="green" />
          <Stat label="Overdue" value={stats.overdue} icon="!" tone="red" />
        </section>

        {/* TAB 1: DASHBOARD */}
        {activeTab === 'DASHBOARD' && (
          <section className="content-grid">
            <div className="panel">
              <div className="panel-head">
                <div>
                  <h2>All Assignments</h2>
                  <p className="muted">Tracked across this semester</p>
                </div>
                <div className="filters">
                  {['ALL', 'PENDING', 'IN_PROGRESS', 'SUBMITTED'].map((x) => (
                    <button key={x} className={filterStatus === x ? 'selected' : ''} onClick={() => setFilterStatus(x)}>
                      {x === 'ALL' ? 'All' : LABEL[x]}
                    </button>
                  ))}
                </div>
              </div>

              {loading ? (
                <div className="empty">Loading assignments from backend…</div>
              ) : (
                <AssignmentTable
                  items={filteredItems}
                  onAdvance={advance}
                  onEdit={openEdit}
                  onDelete={remove}
                />
              )}
            </div>

            <aside className="panel activity">
              <div className="panel-head">
                <div>
                  <h2>Upcoming Deadlines</h2>
                  <p className="muted">Nearest due date first</p>
                </div>
              </div>
              {upcoming.length ? (
                upcoming.map((a) => (
                  <div className="activity-row" key={a.id}>
                    <span className="activity-icon">
                      {fmtDate(a.due_date).split(' ')[0]}
                    </span>
                    <div>
                      <b>{a.title}</b>
                      <small>{a.subject} · {fmtDate(a.due_date)}</small>
                    </div>
                  </div>
                ))
              ) : (
                <div className="empty">No pending deadlines right now. Enjoy the calm!</div>
              )}
            </aside>
          </section>
        )}

        {/* TAB 2: DETAILED ASSIGNMENTS */}
        {activeTab === 'ASSIGNMENTS' && (
          <div className="panel">
            <div className="panel-head">
              <div className="toolbar">
                <input
                  type="text"
                  className="search-input"
                  placeholder="🔍 Search title or notes…"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
                <select
                  className="subject-select"
                  value={filterSubject}
                  onChange={(e) => setFilterSubject(e.target.value)}
                >
                  <option value="ALL">All Subjects</option>
                  {subjects.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              <div className="filters">
                {['ALL', 'PENDING', 'IN_PROGRESS', 'SUBMITTED'].map((x) => (
                  <button key={x} className={filterStatus === x ? 'selected' : ''} onClick={() => setFilterStatus(x)}>
                    {x === 'ALL' ? 'All' : LABEL[x]}
                  </button>
                ))}
              </div>
            </div>

            <AssignmentTable
              items={filteredItems}
              onAdvance={advance}
              onEdit={openEdit}
              onDelete={remove}
            />
          </div>
        )}

        {/* TAB 3: DEADLINES TIMELINE */}
        {activeTab === 'DEADLINES' && (
          <div className="panel" style={{ padding: '24px' }}>
            <h2 style={{ marginBottom: '16px' }}>Chronological Milestones</h2>
            {items.filter((a) => a.due_date).length === 0 ? (
              <div className="empty">No assignments have due dates set yet.</div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
                {items
                  .filter((a) => a.due_date)
                  .sort((a, b) => new Date(a.due_date) - new Date(b.due_date))
                  .map((a) => (
                    <div
                      key={a.id}
                      style={{
                        background: 'var(--bg-card)',
                        border: isOverdue(a) ? '1px solid rgba(239,68,68,0.5)' : '1px solid var(--border)',
                        borderRadius: '12px',
                        padding: '16px',
                      }}
                    >
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span className="chip">{a.subject}</span>
                        <span className={`priority ${a.priority.toLowerCase()}`}>{a.priority}</span>
                      </div>
                      <h3 style={{ margin: '0 0 6px', fontSize: '15px', color: '#fff' }}>{a.title}</h3>
                      <p style={{ margin: '0 0 12px', fontSize: '11px', color: 'var(--text-subtle)' }}>
                        {a.notes || 'No description provided.'}
                      </p>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '11px' }}>
                        <span className={isOverdue(a) ? 'late' : 'muted'}>
                          📅 {fmtDate(a.due_date)} {isOverdue(a) && '(OVERDUE)'}
                        </span>
                        <span className={`status ${a.status.toLowerCase()}`}>{LABEL[a.status]}</span>
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 4: DEVOPS & OBSERVABILITY */}
        {activeTab === 'DEVOPS' && (
          <div className="panel">
            <div className="panel-head">
              <div>
                <h2>Infrastructure & Observability Hub</h2>
                <p className="muted">Live operational metrics and service endpoints</p>
              </div>
            </div>

            <div className="devops-grid">
              <div className="devops-card">
                <h3>Backend Health & Probes</h3>
                <p>Kubernetes liveness and readiness probe status for FastAPI.</p>
                <div className="code-snippet">
                  {`GET /health -> {"status": "${backendHealth.status}"}`}
                  <br />
                  {`GET /ready  -> {"status": "${backendHealth.db}"}`}
                </div>
                <div style={{ marginTop: '12px', display: 'flex', gap: '8px' }}>
                  <a href="http://localhost:8000/health" target="_blank" rel="noreferrer" className="btn btn-secondary">
                    Check /health
                  </a>
                  <a href="http://localhost:8000/ready" target="_blank" rel="noreferrer" className="btn btn-secondary">
                    Check /ready
                  </a>
                </div>
              </div>

              <div className="devops-card">
                <h3>Prometheus Metrics</h3>
                <p>Real-time application metrics scraped by kube-prometheus-stack.</p>
                <div className="code-snippet">
                  Endpoint: http://localhost:8000/metrics<br />
                  Scrape Interval: 15s (ServiceMonitor)
                </div>
                <div style={{ marginTop: '12px' }}>
                  <a href="http://localhost:8000/metrics" target="_blank" rel="noreferrer" className="btn btn-secondary">
                    Open /metrics Stream ↗
                  </a>
                </div>
              </div>

              <div className="devops-card">
                <h3>Interactive API Documentation</h3>
                <p>Swagger OpenAPI specification for student assignment CRUD.</p>
                <div className="code-snippet">
                  Base URL: http://localhost:8000/docs<br />
                  OpenAPI JSON: http://localhost:8000/openapi.json
                </div>
                <div style={{ marginTop: '12px' }}>
                  <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="btn btn-primary">
                    Launch Swagger UI ↗
                  </a>
                </div>
              </div>

              <div className="devops-card">
                <h3>CI/CD Pipeline Details</h3>
                <p>Automated tests, container security scanning, and deployment.</p>
                <div className="code-snippet">
                  CI/CD: GitHub Actions (Ubuntu 24.04)<br />
                  Security: Aquasecurity Trivy v0.36.0 (High/Crit)<br />
                  Registry: GitHub Container Registry (ghcr.io)
                </div>
                <div style={{ marginTop: '12px' }}>
                  <a
                    href="https://github.com/shubh-aarambh/studytrack-devops-capstone/actions"
                    target="_blank"
                    rel="noreferrer"
                    className="btn btn-secondary"
                  >
                    View GitHub Actions ↗
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal: Create or Edit Assignment */}
        {showModal && (
          <div className="modal-backdrop">
            <form className="modal" onSubmit={saveAssignment}>
              <div className="modal-head">
                <div>
                  <p className="eyebrow">{editingItem ? 'EDIT ASSIGNMENT' : 'NEW ASSIGNMENT'}</p>
                  <h2>{editingItem ? 'Update Assignment' : 'Add a New Assignment'}</h2>
                </div>
                <button type="button" className="close" onClick={() => setShowModal(false)}>×</button>
              </div>

              <label>
                Title *
                <input
                  name="title"
                  required
                  defaultValue={editingItem?.title || ''}
                  placeholder="e.g. Kubernetes Helm Deployment Report"
                />
              </label>

              <label>
                Notes / Requirements
                <textarea
                  name="notes"
                  defaultValue={editingItem?.notes || ''}
                  placeholder="What needs to be accomplished for this task?"
                />
              </label>

              <div className="form-row">
                <label>
                  Subject
                  <input
                    name="subject"
                    defaultValue={editingItem?.subject || 'DevOps'}
                    placeholder="e.g. Cloud Computing"
                  />
                </label>

                <label>
                  Due Date
                  <input
                    name="due_date"
                    type="date"
                    defaultValue={editingItem?.due_date || ''}
                  />
                </label>
              </div>

              <div className="form-row">
                <label>
                  Priority
                  <select name="priority" defaultValue={editingItem?.priority || 'MEDIUM'}>
                    <option value="LOW">LOW</option>
                    <option value="MEDIUM">MEDIUM</option>
                    <option value="HIGH">HIGH</option>
                  </select>
                </label>

                <label>
                  Progress ({editingItem?.progress || 0}%)
                  <input
                    name="progress"
                    type="range"
                    min="0"
                    max="100"
                    step="5"
                    defaultValue={editingItem?.progress || 0}
                    onChange={(e) => {
                      const label = e.currentTarget.parentElement;
                      if (label) label.firstChild.textContent = `Progress (${e.currentTarget.value}%)`;
                    }}
                  />
                </label>
              </div>

              <button className="btn btn-primary full">
                {editingItem ? 'Save Changes' : 'Create Assignment'}
              </button>
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
      <div>
        <small>{label}</small>
        <strong>{value}</strong>
        <span>Live synchronized</span>
      </div>
    </div>
  );
}

function AssignmentTable({ items, onAdvance, onEdit, onDelete }) {
  if (!items.length) {
    return <div className="empty">No assignments found matching criteria.</div>;
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Assignment</th>
            <th>Subject</th>
            <th>Due Date</th>
            <th>Priority</th>
            <th>Progress</th>
            <th>Status</th>
            <th style={{ textAlign: 'right' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((a) => (
            <tr key={a.id}>
              <td>
                <div className="task-title">
                  <span className={`dot ${a.status.toLowerCase()}`} />
                  <div>
                    <b>{a.title}</b>
                    <small>{a.notes || 'No description'}</small>
                  </div>
                </div>
              </td>
              <td>
                <span className="chip">{a.subject}</span>
              </td>
              <td className={isOverdue(a) ? 'late' : ''}>
                {fmtDate(a.due_date)}
                {isOverdue(a) && ' · Overdue'}
              </td>
              <td>
                <span className={`priority ${a.priority.toLowerCase()}`}>{a.priority}</span>
              </td>
              <td>
                <div className="bar">
                  <i style={{ width: `${a.progress}%` }} />
                </div>
                <small className="pct">{a.progress}%</small>
              </td>
              <td>
                <span className={`status ${a.status.toLowerCase()}`}>{LABEL[a.status]}</span>
              </td>
              <td className="actions" style={{ textAlign: 'right' }}>
                <button className="icon-btn" onClick={() => onAdvance(a)} title="Advance status">
                  ↻ Cycle
                </button>
                <button className="icon-btn" onClick={() => onEdit(a)} title="Edit assignment">
                  ✎ Edit
                </button>
                <button className="icon-btn danger" onClick={() => onDelete(a)} title="Delete assignment">
                  🗑
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const container = document.getElementById('root');
if (!container._reactRoot) {
  container._reactRoot = createRoot(container);
}
container._reactRoot.render(<App />);
