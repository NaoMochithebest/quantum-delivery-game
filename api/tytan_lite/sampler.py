<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>量子あめ配達員 ⚛️🍬</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@400;700;900&family=Orbitron:wght@600;900&display=swap" rel="stylesheet">
<style>
:root {
  --quantum-cyan: #00f0ff;
  --quantum-pink: #ff2d95;
  --quantum-purple: #a855f7;
  --quantum-green: #39ff14;
  --bg-deep: #0a0a1a;
  --bg-panel: rgba(10, 15, 40, 0.85);
  --player-color: #ffdd00;
  --ai-color: #00f0ff;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Zen Maru Gothic', sans-serif;
  background: var(--bg-deep);
  color: #e8e8f0;
  overflow-x: hidden;
  min-height: 100vh;
}

/* Animated quantum background */
.bg-particles {
  position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background:
    radial-gradient(ellipse at 20% 50%, rgba(0,240,255,0.06) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 30%, rgba(255,45,149,0.05) 0%, transparent 60%),
    radial-gradient(ellipse at 50% 80%, rgba(168,85,247,0.04) 0%, transparent 50%);
}
.bg-particles::before {
  content: ''; position: absolute; inset: 0;
  background-image:
    radial-gradient(1px 1px at 10% 20%, rgba(0,240,255,0.4), transparent),
    radial-gradient(1px 1px at 30% 70%, rgba(255,45,149,0.3), transparent),
    radial-gradient(1.5px 1.5px at 60% 15%, rgba(168,85,247,0.5), transparent),
    radial-gradient(1px 1px at 80% 60%, rgba(57,255,20,0.3), transparent),
    radial-gradient(1px 1px at 45% 45%, rgba(0,240,255,0.3), transparent),
    radial-gradient(1.5px 1.5px at 90% 85%, rgba(255,221,0,0.4), transparent);
  animation: twinkle 4s ease-in-out infinite alternate;
}
@keyframes twinkle { 0%{opacity:.5} 100%{opacity:1} }

.app { position: relative; z-index: 1; max-width: 680px; margin: 0 auto; padding: 12px; text-align: center; }

/* Title */
.title {
  font-family: 'Orbitron', monospace;
  font-size: 1.8em; font-weight: 900;
  background: linear-gradient(135deg, var(--quantum-cyan), var(--quantum-pink), var(--quantum-purple));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  filter: drop-shadow(0 0 20px rgba(0,240,255,0.4));
  margin-bottom: 2px;
}
.title-emoji { font-size: 1.3em; -webkit-text-fill-color: initial; }
.subtitle { font-size: 0.82em; color: #7888aa; margin-bottom: 12px; line-height: 1.5; }

/* Level selector */
.level-bar {
  display: flex; gap: 6px; justify-content: center; margin-bottom: 12px; flex-wrap: wrap;
}
.level-btn {
  font-family: 'Zen Maru Gothic'; font-weight: 700; font-size: 13px;
  padding: 7px 14px; border: 2px solid #334; border-radius: 20px;
  background: transparent; color: #99a; cursor: pointer;
  transition: all 0.25s;
}
.level-btn:hover { border-color: var(--quantum-cyan); color: var(--quantum-cyan); }
.level-btn.active {
  background: linear-gradient(135deg, var(--quantum-cyan), var(--quantum-purple));
  color: #fff; border-color: transparent;
  box-shadow: 0 0 16px rgba(0,240,255,0.3);
}

/* Info panel */
.info-panel {
  background: var(--bg-panel);
  border: 1px solid rgba(0,240,255,0.15);
  border-radius: 12px; padding: 10px 16px; margin-bottom: 10px;
  backdrop-filter: blur(8px);
}
#status {
  font-size: 0.95em; min-height: 1.3em; margin-bottom: 6px;
  font-weight: 700;
}
.scores {
  display: flex; justify-content: space-around; font-size: 1.1em; font-weight: 900;
}
.score-you { color: var(--player-color); }
.score-ai { color: var(--ai-color); }
.score-label { font-weight: 400; font-size: 0.8em; opacity: 0.7; }

/* Canvas */
.canvas-wrap {
  position: relative; margin: 0 auto; border-radius: 14px; overflow: hidden;
  border: 2px solid rgba(0,240,255,0.2);
  box-shadow: 0 0 30px rgba(0,240,255,0.08), inset 0 0 60px rgba(0,0,0,0.3);
  max-width: 100%;
}
canvas {
  display: block; width: 100%; height: auto;
  cursor: crosshair;
  background:
    radial-gradient(ellipse at center, #101828 0%, #080c18 100%);
}

/* Buttons */
.controls { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 12px; }
.btn {
  font-family: 'Zen Maru Gothic'; font-weight: 700; font-size: 14px;
  padding: 10px 18px; border: none; border-radius: 10px;
  cursor: pointer; transition: all 0.2s; position: relative; overflow: hidden;
}
.btn:active:not(:disabled) { transform: scale(0.96); }
.btn:disabled { opacity: 0.35; cursor: not-allowed; }
.btn-undo { background: #1a2444; color: #8899bb; }
.btn-undo:hover:not(:disabled) { background: #253060; color: #aabbdd; }
.btn-reset {
  background: linear-gradient(135deg, #2a1a4e, #1a2a4e);
  color: var(--quantum-purple); border: 1px solid rgba(168,85,247,0.3);
}
.btn-reset:hover { background: linear-gradient(135deg, #3a2a6e, #2a3a6e); }
.btn-fight {
  background: linear-gradient(135deg, var(--quantum-pink), var(--quantum-purple));
  color: #fff;
  box-shadow: 0 0 20px rgba(255,45,149,0.3);
  font-size: 15px;
}
.btn-fight:hover:not(:disabled) {
  box-shadow: 0 0 30px rgba(255,45,149,0.5);
  filter: brightness(1.1);
}

/* SA settings panel */
.settings-toggle {
  font-size: 12px; color: #556; cursor: pointer; margin-top: 10px;
  user-select: none;
}
.settings-toggle:hover { color: var(--quantum-cyan); }
.settings-panel {
  display: none; margin-top: 8px; padding: 10px;
  background: var(--bg-panel); border-radius: 10px;
  border: 1px solid rgba(0,240,255,0.1);
}
.settings-panel.open { display: block; }
.setting-row {
  display: flex; align-items: center; justify-content: space-between;
  margin: 6px 0; font-size: 13px;
}
.setting-row label { color: #8899aa; flex: 1; text-align: left; }
.setting-row input {
  width: 80px; padding: 4px 8px; background: #0d1525; color: var(--quantum-cyan);
  border: 1px solid #334; border-radius: 6px; font-family: 'Orbitron'; font-size: 12px;
  text-align: center;
}

/* Legend */
.legend {
  margin-top: 10px; font-size: 12px; display: flex; justify-content: center; gap: 18px;
}
.leg-you { color: var(--player-color); }
.leg-ai { color: var(--ai-color); }

/* Win/lose overlay */
.result-overlay {
  display: none; position: fixed; inset: 0; z-index: 100;
  background: rgba(0,0,0,0.75); backdrop-filter: blur(6px);
  justify-content: center; align-items: center;
}
.result-overlay.show { display: flex; }
.result-card {
  background: var(--bg-panel); border-radius: 20px; padding: 30px 40px;
  text-align: center; border: 2px solid rgba(0,240,255,0.2);
  animation: popIn 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes popIn { 0%{transform:scale(0.5);opacity:0} 100%{transform:scale(1);opacity:1} }
.result-emoji { font-size: 4em; margin-bottom: 10px; }
.result-text { font-size: 1.4em; font-weight: 900; margin-bottom: 6px; }
.result-detail { font-size: 0.9em; color: #8899aa; margin-bottom: 16px; }
.btn-next {
  font-family: 'Zen Maru Gothic'; font-weight: 700;
  padding: 12px 30px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, var(--quantum-cyan), var(--quantum-green));
  color: #0a0a1a; font-size: 16px; cursor: pointer;
}
.btn-next:hover { filter: brightness(1.15); }

/* Loading animation */
.loading #status { animation: quantumPulse 1s ease-in-out infinite; }
@keyframes quantumPulse {
  0%,100% { color: var(--quantum-cyan); }
  33% { color: var(--quantum-pink); }
  66% { color: var(--quantum-purple); }
}

/* touch */
.app { touch-action: none; -webkit-user-select: none; user-select: none; }
</style>
</head>
<body>
<div class="bg-particles"></div>
<div class="app">
  <div class="title"><span class="title-emoji">⚛️</span> QUANTUM CANDY <span class="title-emoji">🍬</span></div>
  <p class="subtitle">あめ配達員になって最短ルートを作ろう！（出発したら帰らない一筆書き）<br>量子AIに勝てるかな？</p>

  <div class="level-bar" id="levelBar"></div>

  <div class="info-panel">
    <div id="status">レベルを選んでスタート！</div>
    <div class="scores">
      <div><span class="score-label">あなた 🧒</span><br><span class="score-you" id="pScore">---</span></div>
      <div><span class="score-label">量子AI 🤖</span><br><span class="score-ai" id="aiScore">---</span></div>
    </div>
  </div>

  <div class="canvas-wrap">
    <canvas id="c" width="600" height="600"></canvas>
  </div>

  <div class="controls">
    <button class="btn btn-undo" id="undoBtn" onclick="undo()" disabled>↩ もどす</button>
    <button class="btn btn-reset" onclick="resetLevel()">🔄 やりなおし</button>
    <button class="btn btn-fight" id="fightBtn" onclick="fight()" disabled>⚡ 量子AIと対決！</button>
  </div>

  <div class="settings-toggle" onclick="toggleSettings()">⚙️ 量子パラメータ設定 ▾</div>
  <div class="settings-panel" id="settingsPanel">
    <div class="setting-row"><label>ショット数 (shots)</label><input id="cfgShots" type="number" value="100" min="10" max="1000" step="10"></div>
    <div class="setting-row"><label>温度ステップ数 (T_num)</label><input id="cfgTnum" type="number" value="5000" min="500" max="50000" step="500"></div>
    <div style="font-size:11px;color:#556;margin-top:6px;">ショット↑ T_num↑ = AIが賢くなるけど遅くなる</div>
  </div>

  <div class="legend">
    <span class="leg-you">━━ あなた</span>
    <span class="leg-ai">┅┅ 量子AI</span>
  </div>
</div>

<!-- Result overlay -->
<div class="result-overlay" id="resultOverlay">
  <div class="result-card">
    <div class="result-emoji" id="resEmoji"></div>
    <div class="result-text" id="resText"></div>
    <div class="result-detail" id="resDetail"></div>
    <button class="btn-next" id="resBtn" onclick="nextAction()">つぎへ</button>
  </div>
</div>

<script>
// =============================================
// LEVELS
// =============================================
const LEVELS = [
  { name: "🌱 かんたん",   houses: 4,  shots: 80,  T_num: 3000,  label: "4軒" },
  { name: "🌿 ふつう",     houses: 5,  shots: 100, T_num: 5000,  label: "5軒" },
  { name: "🔥 むずかしい", houses: 6,  shots: 150, T_num: 8000,  label: "6軒" },
  { name: "💀 ゲキムズ",   houses: 7,  shots: 200, T_num: 12000, label: "7軒" },
  { name: "⚛️ 量子マスター", houses: 8, shots: 300, T_num: 20000, label: "8軒" },
];

let currentLevel = 1;
let houses = [], playerPath = [], aiPath = null, gameEnded = false;
let wins = 0, losses = 0;

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
const statusEl = document.getElementById('status');
const pScoreEl = document.getElementById('pScore');
const aiScoreEl = document.getElementById('aiScore');
const fightBtn = document.getElementById('fightBtn');
const undoBtn = document.getElementById('undoBtn');

// Build level buttons
const levelBar = document.getElementById('levelBar');
LEVELS.forEach((lv, i) => {
  const btn = document.createElement('button');
  btn.className = 'level-btn' + (i === currentLevel ? ' active' : '');
  btn.textContent = lv.name;
  btn.onclick = () => selectLevel(i);
  levelBar.appendChild(btn);
});

function selectLevel(i) {
  currentLevel = i;
  document.querySelectorAll('.level-btn').forEach((b,j) => b.classList.toggle('active', j===i));
  const lv = LEVELS[i];
  document.getElementById('cfgShots').value = lv.shots;
  document.getElementById('cfgTnum').value = lv.T_num;
  initGame();
}

function resetLevel() { initGame(); }

// =============================================
// GAME INIT
// =============================================
function initGame() {
  const lv = LEVELS[currentLevel];
  houses = []; playerPath = []; aiPath = null; gameEnded = false;
  fightBtn.disabled = true; undoBtn.disabled = true;
  statusEl.textContent = `Lv.${currentLevel+1} ${lv.label}の街 — 家をタップしてね！`;
  document.querySelector('.info-panel').classList.remove('loading');
  pScoreEl.textContent = "---"; aiScoreEl.textContent = "---";

  const N = lv.houses;
  const minDist = Math.max(60, 360 / N);
  for (let i = 0; i < N; i++) {
    let a = 0, h;
    do {
      h = { x: 40 + Math.random()*(canvas.width-80), y: 40 + Math.random()*(canvas.height-80), id: i };
      a++;
    } while (houses.some(o => Math.hypot(o.x-h.x, o.y-h.y) < minDist) && a < 300);
    houses.push(h);
  }
  draw();
}

// =============================================
// DRAW
// =============================================
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Subtle grid
  ctx.strokeStyle = 'rgba(0, 240, 255, 0.04)';
  ctx.lineWidth = 0.5;
  for (let x = 0; x < canvas.width; x += 40) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,canvas.height); ctx.stroke(); }
  for (let y = 0; y < canvas.height; y += 40) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(canvas.width,y); ctx.stroke(); }

  const N = houses.length;

  // Player path
  if (playerPath.length > 1) {
    ctx.strokeStyle = 'rgba(255, 221, 0, 0.8)';
    ctx.lineWidth = 3; ctx.setLineDash([]); ctx.shadowColor = '#ffdd00'; ctx.shadowBlur = 8;
    ctx.beginPath();
    ctx.moveTo(houses[playerPath[0]].x, houses[playerPath[0]].y);
    for (let i = 1; i < playerPath.length; i++) ctx.lineTo(houses[playerPath[i]].x, houses[playerPath[i]].y);
    // パス問題: ループを閉じない
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  // AI path
  if (aiPath) {
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.7)';
    ctx.lineWidth = 2.5; ctx.setLineDash([8,5]); ctx.shadowColor = '#00f0ff'; ctx.shadowBlur = 10;
    ctx.beginPath();
    ctx.moveTo(houses[aiPath[0]].x, houses[aiPath[0]].y);
    for (let i = 1; i < aiPath.length; i++) ctx.lineTo(houses[aiPath[i]].x, houses[aiPath[i]].y);
    // パス問題: ループを閉じない
    ctx.stroke();
    ctx.setLineDash([]); ctx.shadowBlur = 0;
  }

  // Houses
  houses.forEach((h, idx) => {
    const vi = playerPath.indexOf(idx);
    const unvisited = vi < 0 && !gameEnded;

    // Glow for unvisited
    if (unvisited && playerPath.length > 0) {
      ctx.beginPath(); ctx.arc(h.x, h.y, 24, 0, Math.PI*2);
      ctx.strokeStyle = 'rgba(0,240,255,0.2)'; ctx.lineWidth = 1.5; ctx.stroke();
    }

    // House body — candy-colored circles
    const colors = ['#ff2d95','#00f0ff','#a855f7','#39ff14','#ffdd00','#ff6b35','#00d4aa','#f472b6'];
    const col = colors[idx % colors.length];

    // Outer glow
    ctx.shadowColor = col; ctx.shadowBlur = vi >= 0 ? 5 : 15;
    ctx.fillStyle = vi >= 0 ? col : col;
    ctx.globalAlpha = vi >= 0 ? 0.6 : 1;
    ctx.beginPath(); ctx.arc(h.x, h.y, 16, 0, Math.PI*2); ctx.fill();
    ctx.globalAlpha = 1; ctx.shadowBlur = 0;

    // Inner white circle
    ctx.fillStyle = vi >= 0 ? 'rgba(255,255,255,0.9)' : '#fff';
    ctx.beginPath(); ctx.arc(h.x, h.y, 10, 0, Math.PI*2); ctx.fill();

    // Number
    ctx.fillStyle = '#0a0a1a';
    ctx.font = 'bold 12px "Orbitron"';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(idx+1, h.x, h.y+1);

    // Visit order badge
    if (vi >= 0) {
      ctx.fillStyle = 'rgba(255,221,0,0.9)';
      ctx.font = '700 10px "Zen Maru Gothic"';
      ctx.fillText(`${vi+1}番`, h.x, h.y + 26);
    }
  });
}

// =============================================
// DISTANCE
// =============================================
function tourDist(path) {
  // パス問題: 最初の街に帰らない → N-1本の辺のみ
  let d = 0;
  for (let i = 0; i < path.length-1; i++) d += Math.hypot(houses[path[i]].x-houses[path[i+1]].x, houses[path[i]].y-houses[path[i+1]].y);
  return Math.floor(d);
}

// =============================================
// INPUT
// =============================================
canvas.addEventListener('click', e => { if (!gameEnded) selectAt(pos(e)); });
canvas.addEventListener('touchend', e => {
  if (gameEnded) return; e.preventDefault();
  const t = e.changedTouches[0], r = canvas.getBoundingClientRect();
  selectAt({ x:(t.clientX-r.left)*(canvas.width/r.width), y:(t.clientY-r.top)*(canvas.height/r.height) });
}, {passive:false});
canvas.addEventListener('touchstart', e => e.preventDefault(), {passive:false});
canvas.addEventListener('touchmove', e => e.preventDefault(), {passive:false});

function pos(e) { const r=canvas.getBoundingClientRect(); return {x:(e.clientX-r.left)*(canvas.width/r.width), y:(e.clientY-r.top)*(canvas.height/r.height)}; }

function selectAt(p) {
  let bi=-1, bd=35;
  houses.forEach((h,i) => { if (playerPath.includes(i)) return; const d=Math.hypot(h.x-p.x,h.y-p.y); if(d<bd){bd=d;bi=i;} });
  if (bi >= 0) {
    playerPath.push(bi); undoBtn.disabled = false; draw();
    const rem = houses.length - playerPath.length;
    if (rem > 0) statusEl.textContent = `あと${rem}軒！ つぎの家をタップ 👆`;
    else finishPlayer();
  }
}

function undo() {
  if (!playerPath.length || gameEnded) return;
  playerPath.pop(); undoBtn.disabled = !playerPath.length; fightBtn.disabled = true;
  pScoreEl.textContent = "---";
  statusEl.textContent = playerPath.length ? `あと${houses.length-playerPath.length}軒！` : `家をタップしてね！`;
  draw();
}

function finishPlayer() {
  const d = tourDist(playerPath);
  pScoreEl.textContent = d;
  statusEl.textContent = `ルート完成！距離 ${d} — 量子AIと勝負しよう！（全${N}軒を回る最短パス）`;
  fightBtn.disabled = false; undoBtn.disabled = true;
}

// =============================================
// QUANTUM AI FIGHT
// =============================================
async function fight() {
  if (gameEnded) return;
  gameEnded = true; fightBtn.disabled = true; undoBtn.disabled = true;
  statusEl.textContent = "⚛️ 量子アニーリング中...";
  document.querySelector('.info-panel').classList.add('loading');

  const shots = parseInt(document.getElementById('cfgShots').value) || 100;
  const T_num = parseInt(document.getElementById('cfgTnum').value) || 5000;

  try {
    const res = await fetch('/api/solve_tsp', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ houses, shots, T_num })
    });
    if (!res.ok) { const e = await res.json().catch(()=>({})); throw new Error(e.error || `Error ${res.status}`); }
    const data = await res.json();
    if (!data.path || !Array.isArray(data.path)) throw new Error('不正な応答');

    aiPath = data.path;
    const aiDist = tourDist(data.path);
    aiScoreEl.textContent = aiDist;
    draw();

    document.querySelector('.info-panel').classList.remove('loading');
    const pDist = parseInt(pScoreEl.textContent);

    showResult(pDist, aiDist);
  } catch(e) {
    console.error(e);
    document.querySelector('.info-panel').classList.remove('loading');
    statusEl.textContent = `⚠️ ${e.message}`;
  }
}

function showResult(pDist, aiDist) {
  const overlay = document.getElementById('resultOverlay');
  const emoji = document.getElementById('resEmoji');
  const text = document.getElementById('resText');
  const detail = document.getElementById('resDetail');

  if (pDist < aiDist) {
    wins++;
    emoji.textContent = '🎉🏆🍬';
    text.textContent = 'きみの勝ち！';
    text.style.color = '#39ff14';
    detail.textContent = `きみ ${pDist} vs 量子AI ${aiDist}`;
    statusEl.textContent = '🎉 勝利！';
  } else if (pDist === aiDist) {
    emoji.textContent = '🤝⚡';
    text.textContent = '引き分け！';
    text.style.color = '#ffdd00';
    detail.textContent = `どちらも ${pDist}`;
    statusEl.textContent = '🤝 引き分け！';
  } else {
    losses++;
    emoji.textContent = '🤖⚛️💪';
    text.textContent = '量子AIの勝ち！';
    text.style.color = '#00f0ff';
    detail.textContent = `量子AI ${aiDist} vs きみ ${pDist}`;
    statusEl.textContent = '🤖 量子AIの勝利！';
  }

  const nextLvl = currentLevel < LEVELS.length - 1;
  document.getElementById('resBtn').textContent = pDist <= aiDist && nextLvl ? '🚀 次のレベルへ！' : '🔄 もう一回！';
  overlay.classList.add('show');
}

// Fix: use string directly since CSS var() doesn't work in JS
document.getElementById('resText') && (function(){
  const style = document.getElementById('resText').style;
  // Will be set dynamically in showResult
})();

function nextAction() {
  document.getElementById('resultOverlay').classList.remove('show');
  const pDist = parseInt(pScoreEl.textContent);
  const aiDist = parseInt(aiScoreEl.textContent);
  if (pDist <= aiDist && currentLevel < LEVELS.length - 1) {
    selectLevel(currentLevel + 1);
  } else {
    initGame();
  }
}

function toggleSettings() {
  document.getElementById('settingsPanel').classList.toggle('open');
}

// Start
selectLevel(1);
</script>
</body>
</html>
