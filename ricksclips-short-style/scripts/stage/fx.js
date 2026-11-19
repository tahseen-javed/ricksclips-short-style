// fx.js - PRO SAMPLE effects layer: F1 depth of field + foreground blur, F2 atmosphere, F3 comic fx, F5 cutaway diagram,
// F6 snap-in pulse, and the render-side checks (FX_OUT_OF_FRAME, FX_OVER_TEXT, FX_TOO_MANY, BLUR_HERO).
// Every effect is a pure function of (t, S.seed, shot): no Math.random, no clock. A short.json without the new keys
// returns before touching a pixel, so old videos render identically.
const SAFE = { x0: 0.06, x1: 0.94, y0: 0.08, y1: 0.80 }, TEXT_X1 = 0.88;
const fr = (x) => x - Math.floor(x), clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const hash = (a, b, c = 0) => fr(Math.sin(a * 12.9898 + b * 78.233 + c * 37.719) * 43758.5453);
const overlap = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
const cvs = {};
const canvas = (key, w, h) => { let c = cvs[key]; if (!c || c.width !== w || c.height !== h) { c = cvs[key] = document.createElement('canvas'); c.width = w; c.height = h; } return c; };
const rgba = (hex, a) => { const n = parseInt((hex || '#ffffff').slice(1), 16); return `rgba(${n >> 16 & 255},${n >> 8 & 255},${n & 255},${a})`; };
const FONT = (px, wgt = 800) => `${wgt} ${px}px ShortCaption, "Montserrat ExtraBold", Montserrat, "Arial Black", sans-serif`;

// ---- F6 snap-in: one punch (ease-out, ~0.12 s) and one settle back onto the shot's base move. No oscillation.
export function snap(s, tl) {
  const d = Math.min(s.dur ?? 0.28, 0.3), r = Math.min(0.12, d * 0.45), u = tl - s.t;
  if (!(u > 0 && u < d)) return 1;
  const e = u < r ? 1 - Math.pow(1 - u / r, 3) : 0.5 * (1 + Math.cos(Math.PI * (u - r) / (d - r)));
  return 1 + Math.min(s.zoom ?? 20, 35) / 100 * e;
}

// ---- scene helpers (normalised screen boxes [x0, y0, x1, y1])
function shotAt(env, t) { const sh = env.shots; let k = -1; for (let i = 0; i < sh.length; i++) if (sh[i].start <= t + 1e-6) k = i; return k < 0 ? null : { k, sh: sh[k], raw: sh[k].raw || {} }; }
function boxOf(env, o) {
  const v = new env.THREE.Vector3(); let x0 = 9, y0 = 9, x1 = -9, y1 = -9; o.updateMatrixWorld(true);
  o.traverse(m => {
    if (!m.isMesh || !m.visible || !m.geometry) return; const g = m.geometry; if (!g.boundingBox) g.computeBoundingBox(); const b = g.boundingBox;
    for (let k = 0; k < 8; k++) { v.set(k & 1 ? b.max.x : b.min.x, k & 2 ? b.max.y : b.min.y, k & 4 ? b.max.z : b.min.z).applyMatrix4(m.matrixWorld).project(env.camera); x0 = Math.min(x0, v.x * 0.5 + 0.5); x1 = Math.max(x1, v.x * 0.5 + 0.5); y0 = Math.min(y0, 0.5 - v.y * 0.5); y1 = Math.max(y1, 0.5 - v.y * 0.5); }
  });
  return x1 < x0 ? null : [x0, y0, x1, y1];
}
const textBoxes = (env) => { const r = []; env.setRoot.children.forEach(o => { const p = o.userData.prop; if (p && o.visible && (p.type === 'plane' || p.text)) { const b = boxOf(env, o); if (b) r.push(b); } }); return r; };
const propObj = (env, name) => env.setRoot.children.find(o => o.userData.prop && o.userData.prop.name === name);
function head(env, id, t) {
  const c = env.chars[id]; if (!c || !c.headAt) return null;
  const h = c.headAt(t), a = h.clone().project(env.camera), b = h.clone().add(new env.THREE.Vector3(0, c.headD / 2, 0)).project(env.camera);
  return { x: a.x * 0.5 + 0.5, y: 0.5 - a.y * 0.5, r: Math.abs(a.y - b.y) * 0.5 };
}
const pad = (b, p) => [b[0] - p, b[1] - p, b[2] + p, b[3] + p];
function focusBox(env, raw, t, cw, chh, whole) {
  const f = raw.dof.focus || raw.target || 'host';
  if (env.chars[f]) { if (whole) return boxOf(env, env.chars[f].mesh); const h = head(env, f, t); return h && [h.x - h.r * chh / cw, h.y - h.r, h.x + h.r * chh / cw, h.y + h.r]; }
  const o = propObj(env, f); return o ? boxOf(env, o) : null;
}

// ---- F1 depth of field: half-resolution blur of the frame, the focus subject and every sign/text board kept sharp
function dof(ctx, raw, env, t, look, texts, cw, chh) {
  const r = Math.max(0.5, clamp(raw.dof.blur ?? 0.5, 0, 1) * (look.dofPx || 8) * cw / 1080), hw = cw >> 1, hh = chh >> 1;
  const sharp = canvas('sharp', cw, chh), sg = sharp.getContext('2d'); sg.globalCompositeOperation = 'copy'; sg.drawImage(ctx.canvas, 0, 0);
  const half = canvas('half', hw, hh), hg = half.getContext('2d'); hg.globalCompositeOperation = 'copy'; hg.filter = `blur(${r}px)`; hg.drawImage(ctx.canvas, 0, 0, hw, hh); hg.filter = 'none';
  const mask = canvas('mask', hw, hh), mg = mask.getContext('2d'); mg.clearRect(0, 0, hw, hh); mg.filter = `blur(${Math.max(2, hw * 0.015)}px)`; mg.fillStyle = '#fff';
  const fb = focusBox(env, raw, t, cw, chh, true);
  for (const b of [...(fb ? [fb] : []), ...texts].map(b => pad(b, 0.03))) mg.fillRect(b[0] * hw, b[1] * hh, (b[2] - b[0]) * hw, (b[3] - b[1]) * hh);
  mg.filter = 'none'; sg.globalCompositeOperation = 'destination-in'; sg.drawImage(mask, 0, 0, cw, chh); sg.globalCompositeOperation = 'source-over';
  ctx.drawImage(half, 0, 0, cw, chh); ctx.drawImage(sharp, 0, 0);
}
function fgBlur(ctx, f, look, cw, chh) {                     // soft out-of-focus object in a margin (outside the safe box)
  const hw = cw >> 1, hh = chh >> 1, c = canvas('fg', hw, hh), g = c.getContext('2d'), side = f.side || 'left'; g.clearRect(0, 0, hw, hh);
  g.filter = `blur(${(f.blur ?? 0.8) * 14 * hw / 540}px)`; g.fillStyle = look.fg || look.ink || '#222'; g.globalAlpha = 0.88; g.beginPath();
  if (side === 'low') g.ellipse(0.5 * hw, 1.04 * hh, 0.48 * hw, 0.11 * hh, 0, 0, 7); else g.ellipse((side === 'left' ? -0.03 : 1.03) * hw, 0.88 * hh, 0.13 * hw, 0.2 * hh, 0, 0, 7);
  g.fill(); g.globalAlpha = 0.35; g.fillStyle = look.accent || '#fff'; g.beginPath();
  if (side === 'low') g.ellipse(0.42 * hw, 0.97 * hh, 0.2 * hw, 0.025 * hh, 0, 0, 7); else g.ellipse((side === 'left' ? 0.02 : 0.98) * hw, 0.8 * hh, 0.04 * hw, 0.06 * hh, 0, 0, 7);
  g.fill(); g.filter = 'none'; g.globalAlpha = 1; ctx.drawImage(c, 0, 0, cw, chh);
}

// ---- F2 atmosphere: seeded additive sprites (dust, bokeh) and soft light-ray quads; ambient, may bleed off the edge
function star(g, x, y, s, fill, stroke) { g.beginPath(); for (let i = 0; i < 8; i++) { const a = i * Math.PI / 4, r = i % 2 ? s * 0.22 : s; g.lineTo(x + Math.sin(a) * r, y - Math.cos(a) * r); } g.closePath(); g.fillStyle = fill; g.fill(); if (stroke) { g.strokeStyle = stroke; g.stroke(); } }
function sprite(shape, col) {
  const key = 'spr' + shape + col; if (cvs[key]) return cvs[key];
  const c = cvs[key] = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
  if (shape === 'glint') { g.shadowColor = col; g.shadowBlur = 10; star(g, 32, 32, 26, col); star(g, 32, 32, 11, '#ffffff'); }
  else if (shape === 'hex') { g.beginPath(); for (let i = 0; i < 6; i++) { const a = i * Math.PI / 3; g.lineTo(32 + Math.cos(a) * 26, 32 + Math.sin(a) * 26); } g.closePath(); g.fillStyle = rgba(col, 0.45); g.fill(); g.lineWidth = 2; g.strokeStyle = rgba(col, 0.9); g.stroke(); }
  else { const r = g.createRadialGradient(32, 32, 0, 32, 32, 32), glow = shape === 'glow'; r.addColorStop(0, rgba(col, 1)); r.addColorStop(glow ? 0.18 : 0.45, rgba(col, glow ? 0.65 : 0.8)); r.addColorStop(1, rgba(col, 0)); g.fillStyle = r; g.fillRect(0, 0, 64, 64); }
  return c;
}
function atmos(ctx, a, t, seed, look, cw, chh) {
  ctx.globalCompositeOperation = 'lighter';
  if (a.rays) {
    const left = (look.raySide ?? -1) < 0, ox = left ? -0.1 * cw : 1.1 * cw, ang = (a.rays.angle ?? 25) * Math.PI / 180, I = clamp(a.rays.intensity ?? 0.6, 0, 1) * 0.16, col = look.ray || '#fff1c8';
    for (let i = 0; i < 4; i++) {
      const th = ang + (i - 1.5) * 0.12 + Math.sin(t * 0.35 + i * 1.7) * 0.03, wd = cw * (0.06 + 0.05 * hash(seed, i, 3)), dx = Math.sin(th) * chh * 1.3 * (left ? 1 : -1), dy = Math.cos(th) * chh * 1.3;
      const g = ctx.createLinearGradient(ox, 0, ox + dx, dy); g.addColorStop(0, rgba(col, I)); g.addColorStop(1, rgba(col, 0));
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(ox - wd * 0.3, -0.05 * chh); ctx.lineTo(ox + wd * 0.3, -0.05 * chh); ctx.lineTo(ox + dx + wd, dy); ctx.lineTo(ox + dx - wd, dy); ctx.fill();
    }
  }
  for (const kind of ['dust', 'bokeh']) {
    const p = a[kind]; if (!p) continue;
    const dust = kind === 'dust', n = Math.min(80, p.count ?? (dust ? 26 : 14)), spr = sprite(dust ? (look.dust || 'round') : (look.bokeh || 'round'), dust ? (look.particle || '#ffe6b0') : (look.bokehColor || look.particle || '#ffd9a0')), drift = p.drift ?? 1;
    for (let i = 0; i < n; i++) {
      const h1 = hash(seed, i, dust ? 1 : 11), h2 = hash(seed, i, dust ? 2 : 12), h3 = hash(seed, i, dust ? 3 : 13);
      const x = fr(h1 + Math.sin(t * 0.25 + h3 * 6.28) * 0.02 * drift) * cw, y = fr(h2 - t * (dust ? 0.012 : 0.004) * drift * (0.5 + h3)) * chh;
      const sz = (dust ? 0.012 : 0.05) * cw * (p.size ?? 1) * (0.5 + h3);
      ctx.globalAlpha = (dust ? 0.55 : (p.alpha ?? 0.35)) * (0.55 + 0.45 * Math.sin(t * (1 + h1 * 2) + h2 * 6.28)); ctx.drawImage(spr, x - sz / 2, y - sz / 2, sz, sz);
    }
  }
  ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
}
function clipOut(ctx, boxes, cw, chh) { ctx.beginPath(); ctx.rect(0, 0, cw, chh); for (const b of boxes) ctx.rect(b[0] * cw, b[1] * chh, (b[2] - b[0]) * cw, (b[3] - b[1]) * chh); ctx.clip('evenodd'); }

// ---- F3 comic fx, drawn in the channel ink around the head anchor (boxes in head radii, x mirrored when m = -1)
const FXBOX = { sweat: [0.55, -0.9, 1.15, 0.15], blush: [-0.7, 0.1, 0.7, 0.42], z: [0.5, -2.1, 1.65, -0.65], glint: [0.5, -1.4, 1.3, -0.5], bang: [-0.05, -2.1, 0.55, -1.0], question: [-0.05, -2.1, 0.6, -1.0] };
function fxList(S) {
  if (S._fxR) return S._fxR; const caps = S._captions || [];
  return S._fxR = (S.fx || []).map(f => { let t0 = f.t; if (typeof t0 === 'string') { const w = t0.replace(/^say:/, '').trim().toLowerCase().split(/\s+/)[0]; const c = caps.find(c => c.text.toLowerCase().includes(w)); t0 = c ? c.t0 : NaN; } return { ...f, t0, dur: f.dur ?? 0.9 }; }).filter(f => isFinite(f.t0)).sort((a, b) => a.t0 - b.t0);
}
const comicActive = (S, t) => fxList(S).filter(f => t >= f.t0 && t < f.t0 + f.dur);
function place(f, h, cw, chh, avoid) {
  const B = FXBOX[f.type]; if (!B) return null; const R = h.r * chh, hx = h.x * cw, hy = h.y * chh; let best = null;
  for (const m of [1, -1]) {
    const x0 = hx + Math.min(B[0] * m, B[2] * m) * R, x1 = hx + Math.max(B[0] * m, B[2] * m) * R, y0 = hy + B[1] * R, y1 = hy + B[3] * R;
    const ox = clamp(0, SAFE.x0 * cw - x0, TEXT_X1 * cw - x1), oy = clamp(0, SAFE.y0 * chh - y0, SAFE.y1 * chh - y1);
    const box = [(x0 + ox) / cw, (y0 + oy) / chh, (x1 + ox) / cw, (y1 + oy) / chh], hit = avoid.some(b => overlap(b, box));
    if (!best || (best.hit && !hit)) best = { m, ox, oy, box, hit, R, hx, hy }; if (!hit) break;
  }
  return best;
}
function drawComic(g, type, R, ink, acc, m) {
  g.lineWidth = Math.max(2, R * 0.06); g.strokeStyle = ink; g.lineJoin = 'round';
  if (type === 'sweat') { const x = 0.85 * R * m, y = -0.45 * R, s = 0.26 * R; g.beginPath(); g.moveTo(x, y - s * 1.4); g.bezierCurveTo(x + s, y - 0.2 * s, x + s, y + s, x, y + s); g.bezierCurveTo(x - s, y + s, x - s, y - 0.2 * s, x, y - s * 1.4); g.fillStyle = '#9fdcff'; g.fill(); g.stroke(); }
  else if (type === 'blush') { g.fillStyle = 'rgba(255,110,140,0.55)'; for (const sx of [-1, 1]) { g.beginPath(); g.ellipse(sx * 0.42 * R, 0.26 * R, 0.2 * R, 0.1 * R, 0, 0, 7); g.fill(); for (let j = 0; j < 3; j++) { const bx = sx * 0.42 * R + (j - 1) * 0.09 * R; g.beginPath(); g.moveTo(bx - 0.02 * R, 0.2 * R); g.lineTo(bx - 0.06 * R, 0.32 * R); g.stroke(); } } }
  else if (type === 'glint') star(g, 0.9 * R * m, -0.95 * R, 0.36 * R, '#ffffff', acc);
  else { const z = type === 'z', glyph = z ? 'Z' : type === 'bang' ? '!' : '?'; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = z ? '#ffffff' : acc;
    for (let j = 0; j < (z ? 3 : 1); j++) { const px = (z ? R * (0.75 + j * 0.3) : 0.25 * R) * m, py = z ? -R * (0.95 + j * 0.38) : -1.55 * R, fs = (z ? 0.42 - j * 0.08 : 0.85) * R; g.font = FONT(fs, 900); g.lineWidth = Math.max(2, fs * 0.14); g.strokeText(glyph, px, py); g.fillText(glyph, px, py); } }
}
const backOut = (u) => 1 + 2.7 * Math.pow(u - 1, 3) + 1.7 * Math.pow(u - 1, 2);
function speed(g, hx, hy, e, ink, cw, chh, seed) {           // screen-space streaks from the frame edge towards the head
  g.strokeStyle = ink; g.globalAlpha *= 0.55; const R0 = Math.max(cw, chh);
  for (let i = 0; i < 22; i++) { const a = hash(seed, i, 7) * 6.2832, r0 = R0 * (0.75 + 0.1 * hash(seed, i, 8)), len = chh * (0.12 + 0.12 * fr(hash(seed, i, 9) + e * 2.5)); g.lineWidth = cw * (0.004 + 0.006 * hash(seed, i, 10)); g.beginPath(); g.moveTo(hx + Math.cos(a) * r0, hy + Math.sin(a) * r0); g.lineTo(hx + Math.cos(a) * (r0 - len), hy + Math.sin(a) * (r0 - len)); g.stroke(); }
}
function drawFx(ctx, f, t, env, look, cw, chh, avoid) {
  const e = t - f.t0, ink = look.ink || '#222', acc = look.accent || '#ffcc33', h = head(env, f.on || 'host', t); if (!h) return;
  ctx.save(); ctx.globalAlpha = clamp(Math.min(e / 0.08, (f.dur - e) / 0.2), 0, 1);
  if (f.type === 'speed') { clipOut(ctx, avoid, cw, chh); speed(ctx, h.x * cw, h.y * chh, e, ink, cw, chh, env.S.seed || 1); ctx.restore(); return; }
  const p = place(f, h, cw, chh, avoid); if (!p) { ctx.restore(); return; }
  const sc = e < 0.16 ? backOut(e / 0.16) : 1, wob = Math.sin(e * 10) * 0.07 * Math.exp(-e * 1.5), cx = (p.box[0] + p.box[2]) / 2 * cw, cy = (p.box[1] + p.box[3]) / 2 * chh;
  ctx.translate(cx, cy); ctx.rotate(wob); ctx.scale(sc, sc); ctx.translate(-cx + p.hx + p.ox, -cy + p.hy + p.oy + (f.type === 'sweat' ? Math.min(e, 0.9) * 0.2 * p.R : 0));
  drawComic(ctx, f.type, p.R, ink, acc, p.m); ctx.restore();
}

// ---- F5 cutaway diagram: full-frame card in the channel palette; text exactly as given, fitted (never cropped) into x 0.09-0.85, y 0.10-0.62
function label(g, s, x, y, px, maxW, ink, align = 'center') {
  g.font = FONT(px); const w = g.measureText(s).width; if (w > maxW) { px *= maxW / w; g.font = FONT(px); }
  g.textAlign = align; g.textBaseline = 'middle'; g.lineJoin = 'round'; g.lineWidth = px * 0.18; g.strokeStyle = '#ffffff'; g.strokeText(s, x, y); g.fillStyle = ink; g.fillText(s, x, y);
}
const numOf = (s) => { const m = String(s).replace(/,/g, '').match(/-?\d+(\.\d+)?/); return m ? +m[0] : null; };
function cutaway(ctx, raw, sh, t, look, cw, chh, hasNext) {
  const e = t - sh.start, a = clamp(Math.min(e / 0.3, hasNext ? (sh.dur - e) / 0.3 : 1), 0, 1); if (a <= 0) return;
  const D = raw.diagram || {}, ink = look.ink || '#222', acc = look.accent || '#e0b43a', paper = look.paper || ['#f6ecd6', '#e8d5ae'];
  const items = (D.items || []).slice(0, 6), n = items.length, step = clamp((sh.dur - 0.8) / Math.max(1, n), 0.15, 0.45);
  const pop = (i) => { const u = clamp((e - 0.35 - i * step) / 0.22, 0, 1); return 1 - Math.pow(1 - u, 3); };
  const X = (v) => v * cw, Y = (v) => v * chh, vals = items.map(numOf), have = vals.filter(v => v !== null), mx = Math.max(1e-9, ...have.map(Math.abs));
  const norm = (i) => vals[i] !== null && have.length >= 2 ? Math.abs(vals[i]) / mx : (i + 1) / Math.max(1, n);
  ctx.save(); ctx.globalAlpha = a;
  const g = ctx.createLinearGradient(0, 0, 0, chh); g.addColorStop(0, paper[0]); g.addColorStop(1, paper[1]); ctx.fillStyle = g; ctx.fillRect(0, 0, cw, chh);
  ctx.strokeStyle = rgba(ink, 0.07); ctx.lineWidth = Math.max(1, cw * 0.002); for (let i = 1; i < 12; i++) { ctx.beginPath(); ctx.moveTo(i * cw / 12, 0); ctx.lineTo(i * cw / 12, chh); ctx.moveTo(0, i * chh / 12); ctx.lineTo(cw, i * chh / 12); ctx.stroke(); }
  ctx.lineWidth = Math.max(2, cw * 0.006); ctx.strokeStyle = ink; ctx.strokeRect(X(0.07), Y(0.09), X(0.8), Y(0.55));
  label(ctx, D.title || '', X(0.47), Y(0.155), Y(0.05), X(0.72), ink);
  const kind = D.kind || 'timeline', at = (x, y, i, mw) => { const p = pop(i); if (p <= 0) return; ctx.globalAlpha = a * p; label(ctx, items[i], X(x), Y(y) + (1 - p) * Y(0.02), Y(0.034), mw ?? X(2 * Math.min(x - 0.09, 0.85 - x)), ink); ctx.globalAlpha = a; };
  const dot = (x, y, r, i) => { const p = pop(i); if (p <= 0) return; ctx.beginPath(); ctx.arc(X(x), Y(y), r * p, 0, 7); ctx.fillStyle = acc; ctx.fill(); ctx.stroke(); };
  const yAt = (i) => n > 1 ? 0.27 + i * 0.32 / (n - 1) : 0.42;
  if (kind === 'timeline') { ctx.beginPath(); ctx.moveTo(X(0.17), Y(0.25)); ctx.lineTo(X(0.17), Y(0.25) + Y(0.35) * clamp(e / 0.6, 0, 1)); ctx.stroke(); items.forEach((s, i) => { dot(0.17, yAt(i), X(0.022), i); at(0.5, yAt(i), i, X(0.6)); }); }
  else if (kind === 'map') { ctx.setLineDash([X(0.015), X(0.012)]); ctx.beginPath(); items.forEach((s, i) => { if (pop(i) > 0) ctx.lineTo(X(i % 2 ? 0.64 : 0.3), Y(yAt(i))); }); ctx.stroke(); ctx.setLineDash([]); items.forEach((s, i) => { const x = i % 2 ? 0.64 : 0.3; dot(x, yAt(i), X(0.025), i); at(x, yAt(i) + 0.035, i); }); }
  else if (kind === 'org') { const box = (x, y, w, i) => { const p = pop(i); if (p <= 0) return; ctx.globalAlpha = a * p; ctx.fillStyle = '#ffffff'; ctx.fillRect(X(x - w / 2), Y(y - 0.03), X(w), Y(0.06)); ctx.strokeRect(X(x - w / 2), Y(y - 0.03), X(w), Y(0.06)); label(ctx, items[i], X(x), Y(y), Y(0.03), X(w - 0.03), ink); ctx.globalAlpha = a; };
    items.forEach((s, i) => { if (!i) return box(0.47, 0.28, 0.44, 0); const x = (i - 1) % 2 ? 0.66 : 0.28, y = 0.41 + Math.floor((i - 1) / 2) * 0.12; if (pop(i) > 0) { ctx.beginPath(); ctx.moveTo(X(0.47), Y(0.31)); ctx.lineTo(X(0.47), Y(y - 0.06)); ctx.lineTo(X(x), Y(y - 0.06)); ctx.lineTo(X(x), Y(y - 0.03)); ctx.stroke(); } box(x, y, 0.34, i); }); }
  else if (kind === 'bars' || kind === 'chart') { const slot = 0.7 / Math.max(1, n), pts = [];
    items.forEach((s, i) => { const p = pop(i), x = 0.12 + slot * (i + 0.5), hgt = 0.26 * norm(i) * p; pts.push([x, 0.58 - hgt]);
      if (kind === 'bars') { ctx.fillStyle = acc; ctx.fillRect(X(x - slot * 0.3), Y(0.58 - hgt), X(slot * 0.6), Y(hgt)); ctx.strokeRect(X(x - slot * 0.3), Y(0.58 - hgt), X(slot * 0.6), Y(hgt)); }
      at(x, 0.58 - hgt - 0.03, i, X(slot * 0.95)); });
    ctx.beginPath(); ctx.moveTo(X(0.1), Y(0.58)); ctx.lineTo(X(0.84), Y(0.58)); ctx.stroke();
    if (kind === 'chart') { ctx.strokeStyle = acc; ctx.lineWidth *= 1.6; ctx.beginPath(); pts.forEach((q, i) => { if (pop(i) > 0) ctx.lineTo(X(q[0]), Y(q[1])); }); ctx.stroke(); ctx.strokeStyle = ink; ctx.lineWidth /= 1.6; pts.forEach((q, i) => dot(q[0], q[1], X(0.014), i)); } }
  else if (kind === 'counter') { const i0 = Math.max(0, vals.findIndex(v => v !== null)), s0 = String(items[i0] ?? ''), v0 = vals[i0], u = clamp((e - 0.3) / Math.max(0.3, sh.dur * 0.55), 0, 1), k = 1 - Math.pow(1 - u, 3);
    const shown = v0 === null || u >= 1 ? s0 : s0.replace(/[\d,.]+/, (m) => { const dec = (m.split('.')[1] || '').length, num = (v0 * k).toFixed(dec); return m.includes(',') ? Number(num).toLocaleString('en-US', { minimumFractionDigits: dec }) : num; });
    ctx.save(); ctx.font = FONT(Y(0.1), 900); label(ctx, shown, X(0.47), Y(0.36), Y(0.1), X(0.72), ink); ctx.restore(); items.forEach((s, i) => { if (i !== i0) at(0.47, 0.47 + 0.05 * (i - (i > i0 ? 1 : 0)), i, X(0.7)); }); }
  else { const slots = [[0.25, 0.25], [0.69, 0.25], [0.2, 0.55], [0.74, 0.55], [0.47, 0.61], [0.47, 0.22]];   // brain
    ctx.fillStyle = rgba(acc, 0.35); for (const dx of [-0.08, 0.08]) { ctx.beginPath(); ctx.ellipse(X(0.47 + dx), Y(0.4), X(0.16), Y(0.1), 0, 0, 7); ctx.fill(); ctx.stroke(); }
    ctx.beginPath(); for (let i = 0; i <= 20; i++) ctx.lineTo(X(0.47 + 0.004 * Math.sin(i * 1.3)), Y(0.31 + i * 0.009)); ctx.stroke();
    items.forEach((s, i) => { const [x, y] = slots[i]; if (pop(i) > 0) { ctx.beginPath(); ctx.moveTo(X(0.47), Y(0.4)); ctx.lineTo(X(x), Y(y)); ctx.stroke(); } dot(x, y, X(0.018), i); at(x, y + 0.035, i); }); }
  ctx.restore();
}

// ---- frame hook: called after the 3D render, before the caption
export function post(ctx, t, env) {
  const cur = shotAt(env, t); if (!cur) return;
  const S = env.S, raw = cur.raw, a = raw.type === 'cutaway' ? null : (raw.atmos || S.atmos), act = comicActive(S, t);
  if (!raw.dof && !raw.fgBlur && !a && !act.length && raw.type !== 'cutaway') return;     // nothing new: pixel-identical
  const look = S.fxLook || {}, cw = ctx.canvas.width, chh = ctx.canvas.height, seed = S.seed || 1;
  env.camera.updateMatrixWorld(); const texts = textBoxes(env), h = head(env, raw.target || 'host', t);
  const face = h ? [[h.x - h.r * chh / cw, h.y - h.r, h.x + h.r * chh / cw, h.y + h.r]] : [], capOn = (S._captions || []).some(c => t >= c.t0 && t < c.t1), cap = capOn ? [[0.18, 0.63, 0.82, 0.77]] : [];
  ctx.save();
  if (raw.dof && raw.type !== 'cutaway') dof(ctx, raw, env, t, look, texts, cw, chh);
  if (a) { ctx.save(); clipOut(ctx, [...texts, ...face], cw, chh); atmos(ctx, a, t, seed, look, cw, chh); ctx.restore(); }
  if (raw.fgBlur && raw.type !== 'cutaway') fgBlur(ctx, raw.fgBlur, look, cw, chh);
  if (raw.type !== 'cutaway') for (const f of act.slice(0, 2)) drawFx(ctx, f, t, env, look, cw, chh, [...texts, ...cap]);
  if (raw.type === 'cutaway') cutaway(ctx, raw, cur.sh, t, look, cw, chh, cur.k < env.shots.length - 1);
  ctx.restore();
}

// ---- render-side checks, called by window.visCheck (elements in `out`, flags in the Set)
function energy(g, b, cw, chh) {
  const x = Math.max(0, b[0] * cw | 0), y = Math.max(0, b[1] * chh | 0), w = Math.min(cw - x, (b[2] - b[0]) * cw | 0), h = Math.min(chh - y, (b[3] - b[1]) * chh | 0); if (w < 6 || h < 6) return 0;
  const d = g.getImageData(x, y, w, h).data; let s = 0; for (let j = 0; j < h; j += 2) for (let i = 0; i + 2 < w; i += 2) { const k = (j * w + i) * 4; s += Math.abs(d[k] - d[k + 8]) + Math.abs(d[k + 1] - d[k + 9]); } return s;
}
export function check(t, out, flags, env) {
  const cur = shotAt(env, t); if (!cur) return; const S = env.S, act = comicActive(S, t), raw = cur.raw;
  if (act.length > 2) flags.add('FX_TOO_MANY');
  if ((!act.length || raw.type === 'cutaway') && !(raw.dof && raw.type !== 'cutaway')) return;
  const cw = env.octx.canvas.width, chh = env.octx.canvas.height; env.camera.updateMatrixWorld();
  const texts = textBoxes(env), caps = out.filter(o => o.name.startsWith('caption:')).map(o => o.box), signs = out.filter(o => !o.name.startsWith('char:') && !o.name.startsWith('caption:') && !o.name.startsWith('fx:')).map(o => o.box);
  if (raw.type !== 'cutaway') for (const f of act.slice(0, 2)) {
    if (f.type === 'speed') continue; const h = head(env, f.on || 'host', t); if (!h) continue; const p = place(f, h, cw, chh, [...texts, ...caps]); if (!p) continue; const b = p.box;
    const fl = b[0] < SAFE.x0 || b[2] > SAFE.x1 || b[1] < SAFE.y0 || b[3] > SAFE.y1 ? 'FX_OUT_OF_FRAME' : [...caps, ...signs].some(x => overlap(x, b)) ? 'FX_OVER_TEXT' : null;
    if (fl) flags.add(fl); out.push({ name: 'fx:' + f.type, box: b.map(n => +n.toFixed(3)), flag: fl });
  }
  const dur = (q, nx) => q && q.out !== 'cut' ? Math.min(q.outDur ?? (q.out === 'dissolve' ? 8 / 30 : 0.8), 0.9 * q.dur, 0.9 * nx.dur) : 0;   // mid-glide / mid-dissolve frames blend two shots: not a sharpness sample
  const gIn = cur.k ? dur(env.shots[cur.k - 1], cur.sh) : 0, nxt = env.shots[cur.k + 1], gOut = nxt ? dur(cur.sh, nxt) : 0;
  if (Math.abs(t - cur.sh.start) <= gIn / 2 + 0.04 || (nxt && t >= nxt.start - gOut / 2 - 0.04)) return;
  if (raw.dof && raw.type !== 'cutaway') {
    const fb = focusBox(env, raw, t, cw, chh, false); if (!fb) { flags.add('BLUR_HERO'); return; }
    const rc = canvas('raw', cw, chh), rg = rc.getContext('2d'); rg.globalCompositeOperation = 'copy'; rg.drawImage(env.base, 0, 0, cw, chh);
    const e0 = energy(rg, fb, cw, chh), r = e0 ? energy(env.octx, fb, cw, chh) / e0 : 1;
    out.push({ name: 'dof:' + (raw.dof.focus || 'host'), box: fb.map(n => +n.toFixed(3)), sharp: +r.toFixed(3) }); if (r < 0.85) flags.add('BLUR_HERO');
  }
}
