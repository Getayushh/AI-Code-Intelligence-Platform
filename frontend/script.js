// ═══════════════════════════════════════
//   script.js — Shared Utilities
// ═══════════════════════════════════════

// ── API ─────────────────────────────────
export const API_BASE =
  (location.hostname === 'localhost' ||
   location.hostname === '127.0.0.1' ||
   location.hostname === '')
    ? 'http://127.0.0.1:8000'
    : 'https://ayushh4-codeclone.hf.space';

// ── Toast ────────────────────────────────
let _toastTimer = null;

export function showToast(message, type = 'success') {
  let t = document.getElementById('toast');
  if (!t) {
    t = document.createElement('div');
    t.id = 'toast';
    t.className = 'toast';
    document.body.appendChild(t);
  }
  t.textContent = message;
  t.className = `toast ${type} show`;
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => t.classList.remove('show'), 3500);
}

// ── Loading overlay ───────────────────────
export function showLoading(text = 'Analyzing codebase...', sub = '') {
  let ov = document.getElementById('loadingOverlay');
  if (!ov) {
    ov = document.createElement('div');
    ov.id = 'loadingOverlay';
    ov.className = 'loading-overlay';
    ov.innerHTML = `
      <div class="spinner"></div>
      <div class="loading-text" id="loadingText">${text}</div>
      <div class="loading-sub" id="loadingSub">${sub}</div>
    `;
    document.body.appendChild(ov);
  }
  document.getElementById('loadingText').textContent = text;
  document.getElementById('loadingSub').textContent = sub;
  ov.classList.add('show');
}

export function hideLoading() {
  const ov = document.getElementById('loadingOverlay');
  if (ov) ov.classList.remove('show');
}

// ── Error box ────────────────────────────
export function showError(id, message) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.style.display = 'block';
}

export function hideError(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

// ── Animated counter ──────────────────────
export function animateCount(el, target, duration = 900, isFloat = false) {
  if (!el) return;
  let start = 0;
  const startTime = performance.now();
  function step(now) {
    const p = Math.min((now - startTime) / duration, 1);
    const ease = 1 - Math.pow(1 - p, 3);
    const v = ease * target;
    el.textContent = isFloat ? v.toFixed(2) : Math.floor(v);
    if (p < 1) requestAnimationFrame(step);
    else el.textContent = isFloat ? Number(target).toFixed(2) : target;
  }
  requestAnimationFrame(step);
}

// ── Risk color ───────────────────────────
export function riskColor(riskLevel = '') {
  const r = riskLevel.toLowerCase();
  if (r.includes('high') || r.includes('🔴'))   return 'var(--red)';
  if (r.includes('med')  || r.includes('🟡'))   return 'var(--amber)';
  return 'var(--green)';
}

export function riskBadgeClass(riskLevel = '') {
  const r = riskLevel.toLowerCase();
  if (r.includes('high') || r.includes('🔴'))  return 'badge-red';
  if (r.includes('med')  || r.includes('🟡'))  return 'badge-amber';
  return 'badge-green';
}

// ── Score color ──────────────────────────
export function scoreColor(sim) {
  if (sim >= 95) return 'var(--red)';
  if (sim >= 80) return 'var(--amber)';
  return 'var(--accent)';
}

// ── History ──────────────────────────────
export function saveToHistory(data, filename) {
  const hist = JSON.parse(localStorage.getItem('ci_history') || '[]');
  hist.unshift({
    filename,
    time: new Date().toISOString(),
    totalFiles: data.total_files,
    riskLevel: data.insights?.risk_level || 'Unknown',
    data
  });
  if (hist.length > 20) hist.splice(20);
  localStorage.setItem('ci_history', JSON.stringify(hist));
}

// ── Accordion helper ─────────────────────
export function initAccordion(containerSelector) {
  document.querySelectorAll(`${containerSelector} .accordion-header`).forEach(header => {
    header.addEventListener('click', () => {
      const item = header.closest('.accordion-item');
      const body = item.querySelector('.accordion-body');
      const isOpen = item.classList.contains('open');
      // Close all
      document.querySelectorAll(`${containerSelector} .accordion-item`).forEach(i => {
        i.classList.remove('open');
        i.querySelector('.accordion-body').style.maxHeight = null;
      });
      // Open clicked if it was closed
      if (!isOpen) {
        item.classList.add('open');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });
}

// ── Format date ──────────────────────────
export function formatDate(isoString) {
  if (!isoString) return '—';
  return new Date(isoString).toLocaleString(undefined, {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}
