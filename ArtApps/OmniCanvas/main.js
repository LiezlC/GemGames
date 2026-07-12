// ============================
// OMNI-CANVAS: MAIN CONTROLLER
// ============================

// --- DOM References ---
const interactionPane = document.getElementById('interaction-pane');
const artboard = document.getElementById('artboard');
const btnClear = document.getElementById('btn-clear');
const btnSave = document.getElementById('btn-save');
const btnFullscreen = document.getElementById('btn-fullscreen');
const modalBackdrop = document.getElementById('modal-backdrop');
const btnCloseModal = document.getElementById('btn-close-modal');
const analysisLoader = document.getElementById('analysis-loader');
const analysisResult = document.getElementById('analysis-result');
const analysisText = document.getElementById('analysis-text');

// --- Metrics ---
let metrics = { strokes: 0, mouseDistance: 0, lastX: 0, lastY: 0, startTime: Date.now(), clicks: 0, dominantColors: [] };

// --- Kaleidoscope State ---
let kaleidoscopeLevel = 0; // 0=off, 1=2-fold, 2=4-fold, 3=8-fold

// ============================
// 1. LAYER MANAGEMENT
// ============================

// Layer visibility toggles
document.querySelectorAll('.layer-row input[type="checkbox"]').forEach(cb => {
    cb.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-target');
        const iframe = document.getElementById(id);
        if (e.target.checked) {
            iframe.classList.add('active');
        } else {
            iframe.classList.remove('active');
        }
    });
});

// Layer opacity sliders
document.querySelectorAll('.layer-opacity').forEach(slider => {
    slider.addEventListener('input', (e) => {
        const id = e.target.getAttribute('data-target');
        const iframe = document.getElementById(id);
        iframe.style.opacity = e.target.value / 100;
    });
});

// Layer blend mode selects
document.querySelectorAll('.layer-blend').forEach(select => {
    // Apply initial blend modes from HTML defaults
    const id = select.getAttribute('data-target');
    const iframe = document.getElementById(id);
    if (iframe) iframe.style.mixBlendMode = select.value;

    select.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-target');
        const iframe = document.getElementById(id);
        iframe.style.mixBlendMode = e.target.value;
    });
});

// ============================
// 2. EVENT BROADCASTING
// ============================

function broadcastToLayers(message) {
    document.querySelectorAll('.art-layer.active').forEach(iframe => {
        try { iframe.contentWindow.postMessage(message, '*'); } catch(e) {}
    });
}

function broadcastToAllLayers(message) {
    document.querySelectorAll('.art-layer').forEach(iframe => {
        try { iframe.contentWindow.postMessage(message, '*'); } catch(e) {}
    });
}

function broadcastEvent(e, actionType) {
    const rect = interactionPane.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Track metrics
    if (actionType === 'mousemove' && e.buttons > 0) {
        if (metrics.lastX > 0) {
            metrics.mouseDistance += Math.hypot(x - metrics.lastX, y - metrics.lastY);
        }
    } else if (actionType === 'mousedown') {
        metrics.strokes++;
    } else if (actionType === 'click') {
        metrics.clicks++;
    }
    metrics.lastX = x;
    metrics.lastY = y;

    broadcastToLayers({ type: 'omni-mouse', action: actionType, clientX: x, clientY: y });
}

// Mouse Events
interactionPane.addEventListener('mousedown', e => broadcastEvent(e, 'mousedown'));
interactionPane.addEventListener('mousemove', e => broadcastEvent(e, 'mousemove'));
interactionPane.addEventListener('mouseup', e => broadcastEvent(e, 'mouseup'));
interactionPane.addEventListener('mouseleave', e => broadcastEvent(e, 'mouseup'));
interactionPane.addEventListener('click', e => broadcastEvent(e, 'click'));
interactionPane.addEventListener('dblclick', e => broadcastEvent(e, 'dblclick'));

// Touch Events
interactionPane.addEventListener('touchstart', e => { e.preventDefault(); broadcastEvent(e.touches[0], 'mousedown'); }, {passive: false});
interactionPane.addEventListener('touchmove', e => { e.preventDefault(); broadcastEvent(e.touches[0], 'mousemove'); }, {passive: false});
interactionPane.addEventListener('touchend', e => { broadcastEvent(e.changedTouches[0] || {clientX:0,clientY:0}, 'mouseup'); });

// ============================
// 3. GLOBAL CONTROLS
// ============================

// Color
document.getElementById('global-color').addEventListener('input', (e) => {
    metrics.dominantColors.push(e.target.value);
    broadcastToAllLayers({ type: 'omni-color', color: e.target.value });
});

// Size & Viscosity
function broadcastSettings() {
    const size = parseInt(document.getElementById('global-size').value);
    const visc = parseInt(document.getElementById('global-visc').value);
    document.getElementById('val-size').textContent = size + '%';
    document.getElementById('val-visc').textContent = visc + '%';
    broadcastToAllLayers({ type: 'omni-settings', size, viscosity: visc });
}
document.getElementById('global-size').addEventListener('input', broadcastSettings);
document.getElementById('global-visc').addEventListener('input', broadcastSettings);

// Time Warp
document.getElementById('global-speed').addEventListener('input', (e) => {
    const speed = e.target.value / 100;
    document.getElementById('val-speed').textContent = speed.toFixed(1) + 'x';
    broadcastToAllLayers({ type: 'omni-speed', speed });
});

// Bloom / Glow
document.getElementById('global-bloom').addEventListener('input', (e) => {
    const v = e.target.value;
    document.getElementById('val-bloom').textContent = v + '%';
    const blur = v * 0.08;
    const brightness = 1 + v * 0.008;
    artboard.style.filter = v > 0 ? `blur(${blur}px) brightness(${brightness})` : '';
});

// ============================
// 4. EFFECTS ENGINE
// ============================

// Scatter
document.getElementById('btn-scatter').addEventListener('click', () => {
    broadcastToLayers({ type: 'omni-scatter' });
    // Visual feedback
    artboard.classList.add('glitching');
    setTimeout(() => artboard.classList.remove('glitching'), 500);
});

// Mirror
let mirrored = false;
document.getElementById('btn-mirror').addEventListener('click', (e) => {
    mirrored = !mirrored;
    artboard.style.transform = mirrored
        ? 'translate(-50%, -50%) scaleX(-1)'
        : 'translate(-50%, -50%)';
    e.target.classList.toggle('active', mirrored);
});

// Kaleidoscope
document.getElementById('btn-kaleidoscope').addEventListener('click', (e) => {
    kaleidoscopeLevel = (kaleidoscopeLevel + 1) % 4;
    // Remove existing reflections
    artboard.querySelectorAll('.kaleidoscope-reflect').forEach(el => el.remove());
    artboard.className = 'kaleidoscope-' + kaleidoscopeLevel;

    if (kaleidoscopeLevel >= 1) {
        // Create CSS-based reflection overlays
        const reflect = document.createElement('div');
        reflect.className = 'kaleidoscope-reflect';
        reflect.style.transform = 'scaleX(-1)';
        reflect.style.opacity = '0.6';
        reflect.style.mixBlendMode = 'screen';
        artboard.appendChild(reflect);
    }
    if (kaleidoscopeLevel >= 2) {
        const reflect2 = document.createElement('div');
        reflect2.className = 'kaleidoscope-reflect';
        reflect2.style.transform = 'scaleY(-1)';
        reflect2.style.opacity = '0.4';
        reflect2.style.mixBlendMode = 'screen';
        artboard.appendChild(reflect2);
    }
    if (kaleidoscopeLevel >= 3) {
        const reflect3 = document.createElement('div');
        reflect3.className = 'kaleidoscope-reflect';
        reflect3.style.transform = 'scale(-1, -1)';
        reflect3.style.opacity = '0.3';
        reflect3.style.mixBlendMode = 'screen';
        artboard.appendChild(reflect3);
    }

    e.target.classList.toggle('active', kaleidoscopeLevel > 0);
    e.target.textContent = kaleidoscopeLevel === 0 ? '🔮 Kaleidoscope'
        : `🔮 K×${[0,2,4,8][kaleidoscopeLevel]}`;
});

// Glitch
document.getElementById('btn-glitch').addEventListener('click', () => {
    const hue = Math.random() * 360;
    const layers = document.querySelectorAll('.art-layer.active');
    layers.forEach((l, i) => {
        l.style.filter = `hue-rotate(${hue + i * 45}deg) saturate(${1 + Math.random() * 2})`;
        l.style.transform = `translate(${Math.random()*6-3}px, ${Math.random()*6-3}px)`;
    });
    artboard.classList.add('glitching');
    setTimeout(() => {
        layers.forEach(l => { l.style.filter = ''; l.style.transform = ''; });
        artboard.classList.remove('glitching');
    }, 600);
});

// Invert
let inverted = false;
document.getElementById('btn-invert').addEventListener('click', (e) => {
    inverted = !inverted;
    artboard.style.filter = inverted ? 'invert(1)' : '';
    e.target.classList.toggle('active', inverted);
});

// Randomize
document.getElementById('btn-randomize').addEventListener('click', () => {
    const randomColor = '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6,'0');
    document.getElementById('global-color').value = randomColor;
    broadcastToAllLayers({ type: 'omni-color', color: randomColor });
    broadcastToAllLayers({ type: 'omni-effect', effect: 'randomize' });
});

// Fullscreen
document.getElementById('btn-fullscreen').addEventListener('click', () => {
    document.body.classList.toggle('fullscreen');
});

// ============================
// 5. CLEAR & SAVE
// ============================

btnClear.addEventListener('click', () => {
    document.querySelectorAll('.art-layer').forEach(iframe => { iframe.src = iframe.src; });
    metrics = { strokes: 0, mouseDistance: 0, lastX: 0, lastY: 0, startTime: Date.now(), clicks: 0, dominantColors: [] };
});

// Save via capture protocol
let captureExpected = 0;
let captures = [];

btnSave.addEventListener('click', () => {
    btnSave.textContent = 'Rendering...';
    btnSave.disabled = true;
    const activeIframes = document.querySelectorAll('.art-layer.active');
    captureExpected = activeIframes.length;
    captures = [];
    if (captureExpected === 0) {
        alert("Enable at least one layer to save.");
        btnSave.innerHTML = '💾 Save Artwork';
        btnSave.disabled = false;
        return;
    }
    activeIframes.forEach((iframe, i) => {
        iframe.contentWindow.postMessage({ type: 'omni-capture', zIndex: i, layerId: iframe.id }, '*');
    });
});

window.addEventListener('message', (e) => {
    if (e.data && e.data.type === 'omni-capture-result') {
        const activeIframes = document.querySelectorAll('.art-layer.active');
        const layerId = activeIframes[e.data.zIndex] ? activeIframes[e.data.zIndex].id : '';
        captures.push({ zIndex: e.data.zIndex, dataUrl: e.data.dataUrl, layerId });
        if (captures.length === captureExpected) finalizeCapture();
    }
});

function finalizeCapture() {
    captures.sort((a, b) => a.zIndex - b.zIndex);
    const canvas = document.createElement('canvas');
    canvas.width = artboard.offsetWidth;
    canvas.height = artboard.offsetHeight;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const drawNext = (index) => {
        if (index >= captures.length) {
            const link = document.createElement('a');
            link.download = `omni-canvas-${Date.now()}.png`;
            link.href = canvas.toDataURL('image/png');
            link.click();
            btnSave.innerHTML = '💾 Save Artwork';
            btnSave.disabled = false;
            return;
        }
        const img = new Image();
        img.onload = () => {
            // Apply blend modes based on iframe settings
            const iframe = document.getElementById(captures[index].layerId);
            const blendSelect = document.querySelector(`.layer-blend[data-target="${captures[index].layerId}"]`);
            const blendMode = blendSelect ? blendSelect.value : 'source-over';
            const blendMap = {
                'normal': 'source-over', 'multiply': 'multiply', 'screen': 'screen',
                'overlay': 'overlay', 'difference': 'difference',
                'color-dodge': 'color-dodge', 'exclusion': 'exclusion', 'luminosity': 'luminosity'
            };
            ctx.globalCompositeOperation = blendMap[blendMode] || 'source-over';
            // Apply opacity
            const opacitySlider = document.querySelector(`.layer-opacity[data-target="${captures[index].layerId}"]`);
            ctx.globalAlpha = opacitySlider ? opacitySlider.value / 100 : 1;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            ctx.globalAlpha = 1;
            drawNext(index + 1);
        };
        img.src = captures[index].dataUrl;
    };
    drawNext(0);
}

// ============================
// 6. ORACLE READINGS SYSTEM
// ============================

// --- Free Readings (Algorithmic) ---

const ORACLE_TEMPLATES = {
    psycho: {
        title: 'Psychoanalytical Interpretation',
        icon: '🧠',
        generate: (m) => {
            const activeLayers = document.querySelectorAll('.art-layer.active');
            const layerNames = Array.from(activeLayers).map(l => l.id.replace('layer-',''));
            const chaosVal = (m.mouseDistance / 1000) + m.strokes;
            let chaosStr = chaosVal > 50 ? "Extreme" : chaosVal > 20 ? "High" : chaosVal > 10 ? "Moderate" : "Low";

            const templates = [
                () => layerNames.includes('entropy') && layerNames.includes('neon')
                    ? `A classic "Schism" pattern. You weave the connective tissue of Neon Neural Flow through the decaying blocks of the Entropy Cube. This mirrors a conscious attempt to find meaning within a deteriorating system in your waking life. The ${chaosStr.toLowerCase()} entropy suggests ${chaosVal > 20 ? 'urgency in this search' : 'a tentative, exploratory approach'}.`
                    : null,
                () => layerNames.includes('noir')
                    ? `The Noir layer reveals an architectural subconscious — you build structures even in abstraction. ${m.strokes > 20 ? 'The frantic layering suggests you are constructing walls faster than doors.' : 'The sparse placement suggests you prefer to inhabit negative space, a hallmark of the contemplative introvert.'}`
                    : null,
                () => layerNames.includes('chromatic')
                    ? `The Chromatic Dialogue layer is telling. Two silhouettes, facing each other across the void you paint between them. ${m.clicks > 10 ? 'Your aggressive splattering between them suggests unresolved communication — words replaced by color.' : 'Your gentle dripping suggests patience, a willingness to let dialogue emerge organically.'}`
                    : null,
                () => layerNames.includes('trippy')
                    ? `Activating the Neural Art layer reveals a desire to see the unseen — to find patterns in chaos. The psychedelic waveforms act as a Rorschach for your relationship with ${chaosVal > 30 ? 'overstimulation' : 'controlled exploration'}.`
                    : null,
                () => activeLayers.length >= 5
                    ? `Full-spectrum integration: ${activeLayers.length} simultaneous complexes. The simultaneous activation suggests a mind comfortable holding contradictions — order and chaos, structure and flow, noise and silence coexisting without resolution. This is either profound integration or magnificent avoidance.`
                    : null,
                () => m.strokes > 30
                    ? `High gestural frequency (${m.strokes} gestures). The staccato rhythm of your interaction betrays anxious energy. You are not painting — you are discharging psychological static. The canvas acts as a grounding rod for overstimulated neural pathways.`
                    : null,
                () => `A restrained approach. You leave much void untouched. This negative space speaks louder than the strokes themselves, indicating contemplation, or perhaps a hesitance to leave a permanent mark on your environment.`
            ];

            const result = templates.find(t => t() !== null)?.() || templates[templates.length-1]();
            return { text: result, metrics: { gestures: m.strokes, complexes: activeLayers.length, entropy: chaosStr } };
        }
    },

    fortune: {
        title: 'The Oracle Speaks',
        icon: '🔮',
        generate: (m) => {
            const hour = new Date().getHours();
            const activeLayers = document.querySelectorAll('.art-layer.active').length;
            const seed = (m.strokes * 7 + m.clicks * 13 + activeLayers * 31 + hour) % 100;

            const cards = ['The Tower', 'The Star', 'The Moon', 'The Fool', 'The Empress',
                'Wheel of Fortune', 'The Hermit', 'Strength', 'Temperance', 'The World'];
            const card = cards[seed % cards.length];

            const elements = ['Fire', 'Water', 'Earth', 'Air', 'Aether'];
            const element = elements[activeLayers % elements.length];

            const auraColors = ['Indigo (Third Eye Activation)', 'Gold (Creative Manifestation)',
                'Violet (Transformation)', 'Emerald (Heart Resonance)', 'Crimson (Primal Force)',
                'Silver (Lunar Intuition)', 'Copper (Earthly Grounding)'];
            const aura = auraColors[(m.strokes + m.clicks) % auraColors.length];

            const fortunes = [
                `The card drawn is <strong>${card}</strong>, aligned with the element of <strong>${element}</strong>. Your aura burns <strong>${aura}</strong>. The strokes you have laid carry the signature of someone at a crossroads — but the crossroads has more than four paths, and the map you need is the one you're painting right now.`,
                `<strong>${card}</strong> rises from your canvas, wreathed in <strong>${element}</strong>. Your ${m.strokes} gestures form a sigil the ancients would recognize. The universe whispers: what you seek is not ahead of you — it is beneath the layers you've already painted. Dig gently.`,
                `The spirits read <strong>${card}</strong> in the ${activeLayers} layers of your creation. Element: <strong>${element}</strong>. Aura: <strong>${aura}</strong>. A threshold approaches in the next lunar cycle. The colors you chose unconsciously mirror the palette of this threshold. Walk through it.`,
                `Your canvas channels <strong>${card}</strong>. With ${m.strokes} sacred gestures upon ${activeLayers} planes of existence, you weave ${element}al energy. The Oracle sees a pattern: you create to communicate what speech cannot carry. The right person will understand this painting without explanation.`
            ];

            return { text: fortunes[seed % fortunes.length], metrics: { card, element, aura: aura.split(' (')[0] } };
        }
    },

    critic: {
        title: 'Gallery Review',
        icon: '🎩',
        generate: (m) => {
            const activeLayers = document.querySelectorAll('.art-layer.active');
            const layerCount = activeLayers.length;
            const chaosVal = (m.mouseDistance / 1000) + m.strokes;
            const duration = Math.round((Date.now() - m.startTime) / 1000);

            const artists = ['Rothko', 'Pollock', 'Kandinsky', 'Basquiat', 'Klein', 'Hirst', 'Koons', 'Kusama', 'Richter', 'Twombly'];
            const artist = artists[(m.strokes + layerCount) % artists.length];

            const movements = ['Neo-Expressionist', 'Post-Digital Primitivist', 'Quantum Maximalist',
                'Cyber-Baroque', 'Deconstructed Sublime', 'Algorithmic Impressionist'];
            const movement = movements[(m.clicks + layerCount) % movements.length];

            const prices = ['$12,400', '$47,000', '$125,000', '$2.3M', '$890,000', 'Priceless (museum acquisition pending)'];
            const price = prices[Math.min(Math.floor(chaosVal / 10), prices.length - 1)];

            const reviews = [
                `*adjusts monocle* One detects unmistakable ${movement} influences, reminiscent of late-period ${artist}, yet filtered through a distinctly digital sensibility. The ${layerCount}-layer composition demonstrates ${chaosVal > 30 ? 'a bold, almost reckless disregard for negative space — refreshing' : 'admirable restraint — the confidence to let the void participate'}. Created in ${duration} seconds, which is ${duration < 30 ? 'suspiciously fast — genius or charlatan?' : 'a measured, considered timeframe'}. Estimated auction value: <strong>${price}</strong>.`,
                `Hmm, yes. *sips champagne* What we have here is clearly ${movement}, though I suspect the artist would bristle at categorization. The interplay between ${layerCount} simultaneous media channels creates a tension that ${artist} could only dream of — they never had access to this many layers of pretension simultaneously. The ${m.strokes} gestural interventions suggest ${m.strokes > 20 ? 'horror vacui — an almost pathological need to fill space' : 'wabi-sabi — a mature acceptance of imperfection'}. I'll take it for my private collection. <strong>${price}</strong>.`,
            ];

            return { text: reviews[(m.strokes + m.clicks) % reviews.length], metrics: { movement: movement.split(' ')[0], reference: artist, value: price } };
        }
    },

    astro: {
        title: 'Cosmic Art Chart',
        icon: '⭐',
        generate: (m) => {
            const now = new Date();
            const signs = ['Aries ♈', 'Taurus ♉', 'Gemini ♊', 'Cancer ♋', 'Leo ♌', 'Virgo ♍',
                'Libra ♎', 'Scorpio ♏', 'Sagittarius ♐', 'Capricorn ♑', 'Aquarius ♒', 'Pisces ♓'];
            const sunSign = signs[now.getMonth()];
            const risingSign = signs[(m.strokes + now.getHours()) % 12];
            const moonSign = signs[(m.clicks + now.getMinutes()) % 12];

            const activeLayers = document.querySelectorAll('.art-layer.active').length;
            const planets = ['Mercury (Communication)', 'Venus (Aesthetics)', 'Mars (Drive)',
                'Jupiter (Expansion)', 'Saturn (Structure)', 'Neptune (Imagination)', 'Pluto (Transformation)'];
            const dominant = planets[activeLayers % planets.length];

            const readings = [
                `<strong>Sun:</strong> ${sunSign} | <strong>Rising:</strong> ${risingSign} | <strong>Moon:</strong> ${moonSign}<br><br>Your art chart reveals <strong>${dominant}</strong> as your dominant planetary influence today. The ${risingSign.split(' ')[0]} rising manifests in your ${m.strokes > 15 ? 'aggressive, confident strokes — fire and forward motion' : 'contemplative approach — earth energy, grounding'}. With the Moon in ${moonSign.split(' ')[0]}, your emotional canvas craves ${activeLayers > 4 ? 'complexity — you process feelings through layered abstraction' : 'simplicity — each layer must earn its place'}. The stars recommend: add more ${activeLayers < 5 ? 'layers' : 'negative space'} to achieve cosmic balance.`,
                `The celestial canvas mirrors yours: <strong>${sunSign}</strong> sun illuminates your creative core, while <strong>${risingSign}</strong> rising determines how the world receives this work. <strong>${moonSign}</strong> moon whispers to your inner artist. <br><br>Dominant planet: <strong>${dominant}</strong>. This means your art today is ${dominant.includes('Venus') ? 'driven by pure aesthetic pleasure' : dominant.includes('Mars') ? 'fueled by primal creative force' : dominant.includes('Neptune') ? 'channeling the collective unconscious' : 'building structures in the astral plane'}. The ${m.strokes} gestures you've made align with the ${m.strokes % 2 === 0 ? 'feminine' : 'masculine'} principle. Balance approaches.`
            ];

            return { text: readings[(m.strokes + now.getSeconds()) % readings.length], metrics: { sun: sunSign.split(' ')[0], rising: risingSign.split(' ')[0], planet: dominant.split(' ')[0] } };
        }
    }
};

// Oracle Button Handlers
document.querySelectorAll('.btn-oracle[data-oracle]').forEach(btn => {
    btn.addEventListener('click', () => {
        const oracleType = btn.getAttribute('data-oracle');
        const oracle = ORACLE_TEMPLATES[oracleType];

        // Premium oracles
        if (['vision', 'story', 'appraisal'].includes(oracleType)) {
            handlePremiumOracle(oracleType);
            return;
        }

        if (!oracle) return;

        // Show modal
        modalBackdrop.classList.remove('hidden');
        analysisLoader.classList.remove('hidden');
        analysisResult.classList.add('hidden');

        // Generate after dramatic pause
        setTimeout(() => {
            const result = oracle.generate(metrics);

            // Update modal content
            document.querySelector('#psycho-modal h2').innerHTML = `${oracle.icon} ${oracle.title}`;
            analysisText.innerHTML = result.text + '<br><br><em>(Unlock AI-powered vision analysis with an API key for deeper readings...)</em>';

            // Update metric displays
            const metricKeys = Object.keys(result.metrics);
            const metricEls = document.querySelectorAll('.metric');
            metricEls.forEach((el, i) => {
                if (metricKeys[i]) {
                    el.querySelector('span').textContent = result.metrics[metricKeys[i]];
                    el.querySelector('label').textContent = metricKeys[i].charAt(0).toUpperCase() + metricKeys[i].slice(1);
                }
            });

            analysisLoader.classList.add('hidden');
            analysisResult.classList.remove('hidden');
        }, 2000);
    });
});

btnCloseModal.addEventListener('click', () => modalBackdrop.classList.add('hidden'));

// --- Premium Readings (API-Powered) ---

// Save API key to localStorage
document.getElementById('btn-save-key')?.addEventListener('click', () => {
    const key = document.getElementById('api-key').value;
    const provider = document.getElementById('api-provider').value;
    if (key) {
        localStorage.setItem('omni-api-key', key);
        localStorage.setItem('omni-api-provider', provider);
        document.getElementById('premium-oracles').classList.remove('hidden');
        document.getElementById('btn-save-key').textContent = '✓ Saved';
    }
});

// Load saved key on startup
window.addEventListener('DOMContentLoaded', () => {
    const savedKey = localStorage.getItem('omni-api-key');
    if (savedKey) {
        document.getElementById('api-key').value = savedKey;
        document.getElementById('api-provider').value = localStorage.getItem('omni-api-provider') || 'anthropic';
        document.getElementById('premium-oracles').classList.remove('hidden');
    }
});

async function handlePremiumOracle(type) {
    const apiKey = localStorage.getItem('omni-api-key');
    const provider = localStorage.getItem('omni-api-provider') || 'anthropic';

    if (!apiKey) {
        alert('Please add your API key in the Oracle Readings section first.');
        return;
    }

    // Capture current canvas state
    modalBackdrop.classList.remove('hidden');
    analysisLoader.classList.remove('hidden');
    analysisResult.classList.add('hidden');
    document.querySelector('#psycho-modal h2').textContent = '👁️ Consulting the AI Oracle...';

    // Trigger a save-style capture, then use the composited image
    const activeIframes = document.querySelectorAll('.art-layer.active');
    const tempCaptures = [];
    let tempExpected = activeIframes.length;

    const capturePromise = new Promise((resolve) => {
        const handler = (e) => {
            if (e.data?.type === 'omni-capture-result') {
                tempCaptures.push(e.data);
                if (tempCaptures.length >= tempExpected) {
                    window.removeEventListener('message', handler);
                    resolve(tempCaptures);
                }
            }
        };
        window.addEventListener('message', handler);
        activeIframes.forEach((iframe, i) => {
            iframe.contentWindow.postMessage({ type: 'omni-capture', zIndex: i }, '*');
        });
    });

    const capturedLayers = await capturePromise;

    // Composite into single image
    const canvas = document.createElement('canvas');
    canvas.width = artboard.offsetWidth;
    canvas.height = artboard.offsetHeight;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#111';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    for (const cap of capturedLayers.sort((a,b) => a.zIndex - b.zIndex)) {
        const img = await new Promise(r => { const i = new Image(); i.onload = () => r(i); i.src = cap.dataUrl; });
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }

    const imageDataUrl = canvas.toDataURL('image/jpeg', 0.8);
    const base64 = imageDataUrl.split(',')[1];

    // Build prompts per type
    const prompts = {
        vision: "You are a mystical art oracle. Analyze this digital artwork in vivid, evocative language. Describe what you see, what it might mean psychologically, and what hidden symbols or patterns you detect. Be dramatic and insightful. 2-3 paragraphs.",
        story: "You are a literary artist. Look at this digital artwork and write a short, evocative piece of creative writing (poem, flash fiction, or prose poem) inspired by it. 150-250 words. Make it beautiful.",
        appraisal: "You are a tongue-in-cheek art auction house appraiser. Examine this digital artwork and provide a comedic but detailed appraisal including: the art movement it belongs to (make one up if needed), comparable artists, provenance (invent an amusing backstory), and an estimated auction value with justification. Be witty and specific about what you see."
    };

    try {
        let responseText;

        if (provider === 'anthropic') {
            const resp = await fetch('https://api.anthropic.com/v1/messages', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'x-api-key': apiKey,
                    'anthropic-version': '2023-06-01',
                    'anthropic-dangerous-direct-browser-access': 'true'
                },
                body: JSON.stringify({
                    model: 'claude-3-sonnet-20240229',
                    max_tokens: 1024,
                    messages: [{
                        role: 'user',
                        content: [
                            { type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: base64 } },
                            { type: 'text', text: prompts[type] }
                        ]
                    }]
                })
            });
            const data = await resp.json();
            responseText = data.content?.[0]?.text || data.error?.message || 'The oracle is silent...';
        } else {
            // OpenAI
            const resp = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: 'gpt-4o',
                    max_tokens: 1024,
                    messages: [{
                        role: 'user',
                        content: [
                            { type: 'image_url', image_url: { url: imageDataUrl } },
                            { type: 'text', text: prompts[type] }
                        ]
                    }]
                })
            });
            const data = await resp.json();
            responseText = data.choices?.[0]?.message?.content || data.error?.message || 'The oracle is silent...';
        }

        const titles = { vision: '👁️ Deep Vision Oracle', story: '📜 Story Weaver', appraisal: '💰 Collector\'s Appraisal' };
        document.querySelector('#psycho-modal h2').textContent = titles[type];
        analysisText.innerHTML = responseText.replace(/\n/g, '<br>');

        // Hide metrics for premium readings, they're not relevant
        document.querySelector('.metrics').style.display = 'none';
        analysisLoader.classList.add('hidden');
        analysisResult.classList.remove('hidden');

    } catch (err) {
        analysisText.innerHTML = `Oracle error: ${err.message}. Check your API key and try again.`;
        analysisLoader.classList.add('hidden');
        analysisResult.classList.remove('hidden');
    }
}

// ============================
// 7. KEYBOARD SHORTCUTS
// ============================

document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;

    switch(e.key.toLowerCase()) {
        case 's': if (!e.ctrlKey) document.getElementById('btn-scatter').click(); break;
        case 'm': document.getElementById('btn-mirror').click(); break;
        case 'k': document.getElementById('btn-kaleidoscope').click(); break;
        case 'g': document.getElementById('btn-glitch').click(); break;
        case 'i': document.getElementById('btn-invert').click(); break;
        case 'r': document.getElementById('btn-randomize').click(); break;
        case 'f': document.getElementById('btn-fullscreen').click(); break;
        case 'escape': document.body.classList.remove('fullscreen'); break;
        case '1': case '2': case '3': case '4': case '5': case '6': case '7':
            const idx = parseInt(e.key) - 1;
            const cbs = document.querySelectorAll('.layer-row input[type="checkbox"]');
            if (cbs[idx]) { cbs[idx].checked = !cbs[idx].checked; cbs[idx].dispatchEvent(new Event('change')); }
            break;
    }
});
