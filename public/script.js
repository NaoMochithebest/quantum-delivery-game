const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const statusDiv = document.getElementById('status');
const playerScoreSpan = document.getElementById('player-score');
const aiScoreSpan = document.getElementById('ai-score');
const competeBtn = document.getElementById('competeBtn');
const undoBtn = document.getElementById('undoBtn');

const HOUSE_COUNT = 5;
const MIN_HOUSE_DISTANCE = 80;
let houses = [], playerPath = [], aiPathData = null, gameEnded = false;

function initGame() {
    houses = []; playerPath = []; aiPathData = null; gameEnded = false;
    competeBtn.disabled = true; undoBtn.disabled = true;
    statusDiv.textContent = "あなたの番です：家を順番にクリックしてください";
    statusDiv.classList.remove('loading');
    playerScoreSpan.textContent = "---"; aiScoreSpan.textContent = "---";
    for (let i = 0; i < HOUSE_COUNT; i++) {
        let a = 0, h;
        do { h = { x: Math.floor(Math.random()*(canvas.width-140)+70), y: Math.floor(Math.random()*(canvas.height-140)+70), id: i }; a++; } while (houses.some(o=>Math.hypot(o.x-h.x,o.y-h.y)<MIN_HOUSE_DISTANCE) && a<200);
        houses.push(h);
    }
    draw();
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.strokeStyle='rgba(15,52,96,0.4)'; ctx.lineWidth=0.5;
    for(let x=0;x<canvas.width;x+=50){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke();}
    for(let y=0;y<canvas.height;y+=50){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke();}
    if(playerPath.length>1){
        // 往路（実線・黄色）
        ctx.strokeStyle='#ffeb3b';ctx.lineWidth=3;ctx.setLineDash([]);ctx.beginPath();
        ctx.moveTo(houses[playerPath[0]].x,houses[playerPath[0]].y);
        for(let i=1;i<playerPath.length;i++) ctx.lineTo(houses[playerPath[i]].x,houses[playerPath[i]].y);
        ctx.stroke();
        // 帰り（点線・オレンジ）
        if(playerPath.length===HOUSE_COUNT){
            const last=houses[playerPath[playerPath.length-1]], first=houses[playerPath[0]];
            ctx.strokeStyle='#ff9800';ctx.lineWidth=2.5;ctx.setLineDash([8,6]);ctx.beginPath();
            ctx.moveTo(last.x,last.y);ctx.lineTo(first.x,first.y);ctx.stroke();ctx.setLineDash([]);
            // 帰り矢印
            const angle=Math.atan2(first.y-last.y,first.x-last.x);
            const mx=(last.x+first.x)/2, my=(last.y+first.y)/2;
            ctx.fillStyle='#ff9800';ctx.beginPath();
            ctx.moveTo(mx+10*Math.cos(angle),my+10*Math.sin(angle));
            ctx.lineTo(mx-6*Math.cos(angle-0.5),my-6*Math.sin(angle-0.5));
            ctx.lineTo(mx-6*Math.cos(angle+0.5),my-6*Math.sin(angle+0.5));
            ctx.closePath();ctx.fill();
            // 🏠ラベル
            ctx.fillStyle='#ff9800';ctx.font='12px sans-serif';ctx.textAlign='center';
            ctx.fillText('🏠帰り',mx,my-12);
        }
    }
    if(aiPathData){
        // AI往路（点線・水色）
        ctx.strokeStyle='#00d4ff';ctx.lineWidth=2.5;ctx.setLineDash([10,5]);ctx.beginPath();
        ctx.moveTo(houses[aiPathData[0]].x,houses[aiPathData[0]].y);
        for(let i=1;i<aiPathData.length;i++) ctx.lineTo(houses[aiPathData[i]].x,houses[aiPathData[i]].y);
        ctx.stroke();
        // AI帰り（細い点線・水色薄め）
        const aiLast=houses[aiPathData[aiPathData.length-1]], aiFirst=houses[aiPathData[0]];
        ctx.strokeStyle='rgba(0,212,255,0.5)';ctx.lineWidth=2;ctx.setLineDash([4,4]);ctx.beginPath();
        ctx.moveTo(aiLast.x,aiLast.y);ctx.lineTo(aiFirst.x,aiFirst.y);ctx.stroke();
        ctx.setLineDash([]);
    }
    houses.forEach((house,idx)=>{
        const vi=playerPath.indexOf(idx);
        if(vi<0&&!gameEnded&&playerPath.length>0){ctx.strokeStyle='rgba(255,235,59,0.3)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(house.x,house.y,22,0,Math.PI*2);ctx.stroke();}
        ctx.fillStyle=vi>=0?'#ff9800':'#ffeb3b';ctx.beginPath();ctx.arc(house.x,house.y,14,0,Math.PI*2);ctx.fill();
        ctx.fillStyle='#1a1a2e';ctx.font='bold 13px sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(idx+1,house.x,house.y);
        if(vi>=0){ctx.fillStyle='rgba(255,235,59,0.8)';ctx.font='10px sans-serif';ctx.fillText(`${vi+1}番目`,house.x,house.y+24);}
    });
}

function calcTourDist(path){
    let d=0;
    for(let i=0;i<path.length-1;i++) d+=Math.hypot(houses[path[i]].x-houses[path[i+1]].x,houses[path[i]].y-houses[path[i+1]].y);
    d+=Math.hypot(houses[path[path.length-1]].x-houses[path[0]].x,houses[path[path.length-1]].y-houses[path[0]].y);
    return Math.floor(d);
}

canvas.addEventListener('click',e=>{if(!gameEnded)selectHouseAt(getPos(e));});
canvas.addEventListener('touchend',e=>{if(gameEnded)return;e.preventDefault();const t=e.changedTouches[0],r=canvas.getBoundingClientRect();selectHouseAt({x:(t.clientX-r.left)*(canvas.width/r.width),y:(t.clientY-r.top)*(canvas.height/r.height)});},{passive:false});
canvas.addEventListener('touchstart',e=>e.preventDefault(),{passive:false});
canvas.addEventListener('touchmove',e=>e.preventDefault(),{passive:false});

function getPos(e){const r=canvas.getBoundingClientRect();return{x:(e.clientX-r.left)*(canvas.width/r.width),y:(e.clientY-r.top)*(canvas.height/r.height)};}

function selectHouseAt(pos){
    let bi=-1,bd=35;
    houses.forEach((h,i)=>{if(playerPath.includes(i))return;const d=Math.hypot(h.x-pos.x,h.y-pos.y);if(d<bd){bd=d;bi=i;}});
    if(bi>=0){
        playerPath.push(bi);undoBtn.disabled=false;draw();
        const rem=HOUSE_COUNT-playerPath.length;
        if(rem>1) statusDiv.textContent=`あと${rem}軒！`;
        else if(rem===1) statusDiv.textContent=`あと1軒！ 選んだら最初の家に帰るよ 🏠`;
        else finishPlayerTurn();
    }
}

function undoLast(){
    if(!playerPath.length||gameEnded)return;
    playerPath.pop();undoBtn.disabled=!playerPath.length;competeBtn.disabled=true;playerScoreSpan.textContent="---";
    statusDiv.textContent=playerPath.length?`あと${HOUSE_COUNT-playerPath.length}軒！`:"あなたの番です：家を順番にクリックしてください";draw();
}

function finishPlayerTurn(){
    const d=calcTourDist(playerPath);playerScoreSpan.textContent=d;
    statusDiv.textContent=`🏠 帰還完了！ 総距離: ${d} — 量子AIと対決ボタンを押そう`;competeBtn.disabled=false;undoBtn.disabled=true;
}

async function callQuantumAI(){
    if(gameEnded)return;gameEnded=true;competeBtn.disabled=true;undoBtn.disabled=true;
    statusDiv.textContent="量子アニーリング中 (Tytan起動中)...";statusDiv.classList.add('loading');
    try{
        const res=await fetch('/api/solve_tsp',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({houses})});
        if(!res.ok){const e=await res.json().catch(()=>({}));throw new Error(e.error||`サーバーエラー(${res.status})`);}
        const data=await res.json();
        if(data.path&&Array.isArray(data.path)){
            aiPathData=data.path;const aiDist=calcTourDist(data.path);aiScoreSpan.textContent=aiDist;draw();
            statusDiv.classList.remove('loading');const pDist=parseInt(playerScoreSpan.textContent);
            if(pDist<aiDist)statusDiv.textContent=`🎉 あなたの勝利！ (${pDist} < ${aiDist})`;
            else if(pDist===aiDist)statusDiv.textContent=`🤝 引き分け！ (${pDist} = ${aiDist})`;
            else statusDiv.textContent=`🤖 量子AIの勝利！ (${aiDist} < ${pDist})`;
        }else throw new Error('AIからの応答が不正です');
    }catch(e){console.error(e);statusDiv.classList.remove('loading');statusDiv.textContent=`エラー: ${e.message}`;}
}

initGame();
