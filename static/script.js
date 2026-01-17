// --- MATRIX BACKGROUND ---
const canvas = document.getElementById('matrix');
if (canvas) {
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const letters = "01NASHTTRIKE01CRYPT".split("");
    const fontSize = 14; const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);
    function draw() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "#0f0"; ctx.font = fontSize + "px monospace";
        drops.forEach((y, i) => {
            const text = letters[Math.floor(Math.random() * letters.length)];
            ctx.fillText(text, i * fontSize, y * fontSize);
            if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        });
    }
    setInterval(draw, 50);
}

const term = document.getElementById('terminal');

// STEP 1: LOGIN
const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const u = document.getElementById('username').value;
        const p = document.getElementById('password').value;

        // Fetch call to the Python backend
        const res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ u, p }) // Must match app.py keys
        });

        if (res.ok) {
            term.innerHTML = `<span style="color:#0f0">[SUCCESS] Node Breach.</span>`;
            document.getElementById('step-1').style.display = 'none';
            document.getElementById('step-2').style.display = 'block';
        } else {
            term.innerHTML = `<span style="color:red">[ERROR] Access Denied.</span>`;
        }
    });
}

// STEP 2: SECURITY VERIFY
const secBtn = document.getElementById('sec-btn');
if (secBtn) {
    secBtn.onclick = async () => {
        const a = document.getElementById('sec-answer').value;
        const res = await fetch('/auth/verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ a })
        });

        if (res.ok) {
            term.innerHTML = `<span style="color:#0f0">[SUCCESS] Identity Verified.</span>`;
            document.getElementById('step-2').style.display = 'none';
            document.getElementById('step-3').style.display = 'block';
        } else {
            term.innerHTML = `<span style="color:red">[FAIL] Key Incorrect.</span>`;
        }
    };
}

// STEP 3: FINALIZE
const finalBtn = document.getElementById('final-btn');
if (finalBtn) {
    finalBtn.onclick = async () => {
        const t = document.getElementById('team-name').value;
        if (!t) return;

        // Fetch random flag from .env via Python
        const response = await fetch('/auth/get-flag');
        const data = await response.json();
        const key = data.flag;
        const formUrl = data.url;

        sessionStorage.setItem("nash_token", key);

        const f = document.createElement('form');
        f.method = 'POST'; f.action = formUrl; f.target = 'hidden_iframe';
        
        // Form Entry IDs
        const tI = document.createElement('input'); tI.name = "entry.1988266406"; tI.value = t; f.appendChild(tI);
        const sI = document.createElement('input'); sI.name = "entry.569318071"; sI.value = key; f.appendChild(sI);
        
        document.body.appendChild(f);
        f.submit();
        
        term.innerHTML = `<span style="color:#0f0">[LOGGED] Finalizing session...</span>`;
        setTimeout(() => { window.location.href = "/feed_pro"; }, 1500);
    };
}

// ONLOAD FOR FEED_PRO
window.onload = () => {
    const list = document.getElementById('pro-log-list');
    const token = sessionStorage.getItem("nash_token");
    if (list && token) {
        setTimeout(() => {
            const li = document.createElement('li');
            li.style.color = "#ffcc00"; // Gold color
            li.style.marginTop = "10px";
            li.style.fontWeight = "bold";
            li.innerHTML = `> [FLAG_CODE]: ${token}`;
            list.appendChild(li);
        }, 1000);
    }
};