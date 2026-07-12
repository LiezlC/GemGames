# OmniCanvas Mega-Build Prompt

> **Hand this entire prompt to Gemini / Claude / GPT to execute. It contains all file paths, variable names, and architectural decisions needed to build without exploration.**

---

## CONTEXT

You are working on **OmniCanvas**, a multi-layer art compositing app at:
```
C:\Users\Liezl\Documents\Content\ArtApps\OmniCanvas\
```

It composites multiple standalone HTML art applets as transparent iframe layers on a shared artboard. A unified "interaction pane" div sits on top, capturing all mouse/touch events and broadcasting them via `postMessage` to all active iframe layers simultaneously. The result: one gesture paints across multiple art engines at once.

### Current file structure:
```
OmniCanvas/
  index.html          ← main shell (artboard + UI panel)
  main.js             ← event broadcasting, layer management, save, psychoanalysis
  style.css           ← dark glassmorphism UI
  patch*.js           ← Node scripts used to inject postMessage handlers (reference only, don't run)
  applets/
    abstractify-kinetic-canvas/index.html
    digital-entropy-cube/index.html
    impasto-abstract-art-generator/index.html
    neon-neural-flow/index.html
```

### Source applets to integrate FROM (originals, better quality):
```
C:\Users\Liezl\Documents\Content\ArtApps\To_Omni\
  chromatic-dialogue-interactive-art/index.html    ← NEW, not yet in OmniCanvas
  ai-s-trippy-vision-interactive-neural-art/index.html  ← NEW, not yet in OmniCanvas
  noir-abstract-studio/index.html                  ← NEW, not yet in OmniCanvas
  abstractify-kinetic-canvas/index.html            ← ORIGINAL (cleaner than current OmniCanvas version)
  impasto-abstract-art-generator/index.html        ← ORIGINAL
  digital-entropy-cube/index.html                  ← ORIGINAL
```

### PostMessage Protocol (all applets must handle these):
```javascript
// Received by applets from parent:
{ type: 'omni-mouse', action: 'mousedown'|'mousemove'|'mouseup'|'click', clientX, clientY }
{ type: 'omni-color', color: '#hex' }
{ type: 'omni-settings', size: 1-100, viscosity: 1-100 }
{ type: 'omni-capture', zIndex: number }
{ type: 'omni-speed', speed: 0.1-3.0 }        // NEW - time warp
{ type: 'omni-scatter' }                        // NEW - random burst
{ type: 'omni-effect', effect: 'randomize'|'mirror'|'invert' }  // NEW

// Sent by applets to parent:
{ type: 'omni-capture-result', zIndex: number, dataUrl: 'data:image/png;base64,...' }
```

---

## BUILD TASKS — Execute in order

---

### TASK 1: Copy and integrate the 3 new applets

**1a. Copy source files into OmniCanvas/applets/**

Create these three new folders under `OmniCanvas/applets/`:
- `chromatic-dialogue/`
- `trippy-neural-art/`
- `noir-abstract-studio/`

Copy the `index.html` from each To_Omni source folder into the corresponding new folder.

**1b. Inject OmniCanvas integration into each new applet**

For ALL THREE new applets, add this integration block just before `</body>`. Adapt the canvas/container ID per applet (see table below).

```javascript
<script>
// === OmniCanvas Integration Layer ===
(function() {
    // Hide UI when running as iframe layer
    if (window.self !== window.top) {
        document.addEventListener('DOMContentLoaded', () => {
            document.body.style.backgroundColor = 'transparent';
            document.documentElement.style.backgroundColor = 'transparent';
            // Hide applet-specific UI (see HIDE_SELECTORS below)
            const hide = document.querySelectorAll(HIDE_SELECTORS);
            hide.forEach(el => el.style.display = 'none');
            // Make canvas background transparent
            const canvas = document.getElementById(CANVAS_ID);
            if (canvas) {
                const ctx = canvas.getContext('2d');
                // Don't clear - just ensure future draws are on transparent
            }
        });
    }

    window.addEventListener('message', (event) => {
        const d = event.data;
        if (!d || !d.type) return;

        // --- Mouse event forwarding ---
        if (d.type === 'omni-mouse') {
            const target = document.getElementById(CANVAS_ID) || document.getElementById(CONTAINER_ID) || document.body;
            const ev = new MouseEvent(d.action, {
                view: window, bubbles: true, cancelable: true,
                clientX: d.clientX, clientY: d.clientY
            });
            target.dispatchEvent(ev);
            // Also dispatch touch events for apps that use them
            try {
                const touchMap = { mousedown: 'touchstart', mousemove: 'touchmove', mouseup: 'touchend' };
                const touchType = touchMap[d.action];
                if (touchType) {
                    const touch = new Touch({
                        identifier: Date.now(), target,
                        clientX: d.clientX, clientY: d.clientY,
                        radiusX: 2.5, radiusY: 2.5, rotationAngle: 10, force: 0.5
                    });
                    target.dispatchEvent(new TouchEvent(touchType, {
                        cancelable: true, bubbles: true,
                        touches: touchType === 'touchend' ? [] : [touch],
                        targetTouches: touchType === 'touchend' ? [] : [touch],
                        changedTouches: [touch]
                    }));
                }
            } catch(e) {}
        }

        // --- Color override ---
        if (d.type === 'omni-color') {
            COLOR_OVERRIDE_LOGIC
        }

        // --- Size/Viscosity ---
        if (d.type === 'omni-settings') {
            window.omniSize = d.size;
            window.omniVisc = d.viscosity;
        }

        // --- Capture for save ---
        if (d.type === 'omni-capture') {
            CAPTURE_LOGIC
        }

        // --- Speed control ---
        if (d.type === 'omni-speed') {
            window.omniSpeed = d.speed; // applet animation loops should multiply their time delta by this
        }

        // --- Scatter burst ---
        if (d.type === 'omni-scatter') {
            SCATTER_LOGIC
        }

        // --- Effects ---
        if (d.type === 'omni-effect') {
            if (d.effect === 'mirror') {
                const c = document.getElementById(CANVAS_ID);
                if (c) c.style.transform = c.style.transform === 'scaleX(-1)' ? '' : 'scaleX(-1)';
            }
            if (d.effect === 'invert') {
                document.body.style.filter = document.body.style.filter === 'invert(1)' ? '' : 'invert(1)';
            }
            if (d.effect === 'randomize') {
                // Trigger applet-specific randomization
                RANDOMIZE_LOGIC
            }
        }
    });
})();
</script>
```

**Per-applet substitution table:**

| Placeholder | chromatic-dialogue | trippy-neural-art | noir-abstract-studio |
|-------------|-------------------|-------------------|---------------------|
| `CANVAS_ID` | `'artCanvas'` | `'canvas-layer'` | `'artCanvas'` |
| `CONTAINER_ID` | `'app-container'` | `'ui-layer'` | `'canvas-container'` |
| `HIDE_SELECTORS` | `'.controls, .overlay, .tooltip'` | `'.controls, #ui-layer, .brain-container'` | `'#tutorial, #ui-layer, .toolbar, .header'` |
| `COLOR_OVERRIDE_LOGIC` | `if(typeof currentPalette!=='undefined') currentPalette[0]=d.color; // also set mouse-spawned drip color` | `if(typeof state!=='undefined') state.colorOffset = parseInt(d.color.substring(1),16) % 360;` | `// Noir uses currentTool colors - override the draw color: window.omniColorOverride = d.color;` |
| `CAPTURE_LOGIC` | `const c=document.getElementById('artCanvas'); window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');` | `const c=document.getElementById('canvas-layer'); window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');` | `const c=document.getElementById('artCanvas'); window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');` |
| `SCATTER_LOGIC` | `for(let i=0;i<20;i++){const x=Math.random()*window.innerWidth;const y=Math.random()*window.innerHeight;particles.push(new Drip(x,y,currentPalette[Math.floor(Math.random()*currentPalette.length)]));particles.push(new Splatter(x,y,currentPalette[Math.floor(Math.random()*currentPalette.length)]));}` | `for(let i=0;i<5;i++){const idx=Math.floor(Math.random()*neuronPositions.length);state.activeNeurons.push({...neuronPositions[idx],time:0});}` | `const tools=['city','red','light','white','fog'];for(let i=0;i<15;i++){const x=Math.random()*width;const y=Math.random()*height;currentTool=tools[Math.floor(Math.random()*tools.length)];drawWithTool(x,y);}` |
| `RANDOMIZE_LOGIC` | `const keys=Object.keys(palettes);currentPalette=palettes[keys[Math.floor(Math.random()*keys.length)]];` | `state.warp=Math.random()*100;state.colorOffset=Math.random()*360;state.speed=Math.random()*50;` | `generateRandom();` |

**1c. Also make the canvas backgrounds transparent in each applet**

In each new applet's `index.html`, find the CSS rule that sets `body` or the main container background color, and add `!important` transparent override when in iframe. The integration script above handles `document.body.style.backgroundColor = 'transparent'` but you may also need to:

- **Chromatic Dialogue**: Find `background: radial-gradient(...)` or `background-color: #0a0a0f` in its `<style>` and wrap in a CSS class `.omni-transparent { background: transparent !important; }` — then add that class via the integration script.
- **Trippy Vision**: Same approach for its dark background.
- **Noir Abstract**: Its gradient background IS the art base, so for this one set `mix-blend-mode: multiply` on the iframe instead so it composites nicely rather than going fully transparent.

**1d. For the 3 EXISTING applets that were already patched** (abstractify, impasto, entropy cube):

The current OmniCanvas versions were patched via regex text replacement and have messy injected code. **Replace each `OmniCanvas/applets/X/index.html` with a fresh copy from `To_Omni/X/index.html`**, then apply the same clean integration block from above.

Per-applet specifics for existing applets:

| Placeholder | abstractify-kinetic-canvas | impasto-abstract-art-generator | digital-entropy-cube |
|-------------|---------------------------|-------------------------------|---------------------|
| `CANVAS_ID` | `'artCanvas'` | `null` (DOM-based, no canvas) | `null` (CSS 3D, no canvas) |
| `CONTAINER_ID` | `'canvas-container'` | `'canvas-container'` | `'scene'` |
| `HIDE_SELECTORS` | `'.ui-panel, .header-overlay, .hint, .texture-overlay'` | `'#intro, #controls'` | `'#ui-layer, #reset-btn'` |
| `CAPTURE_LOGIC` | `const c=document.getElementById('artCanvas'); window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');` | `html2canvas(document.body,{backgroundColor:null,logging:false}).then(c=>{window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');});` | `html2canvas(document.body,{backgroundColor:null,logging:false}).then(c=>{window.parent.postMessage({type:'omni-capture-result',zIndex:d.zIndex,dataUrl:c.toDataURL('image/png')},'*');});` |
| `COLOR_OVERRIDE_LOGIC` | `if(typeof activeColor!=='undefined') activeColor=d.color;` | `if(typeof currentColor!=='undefined') currentColor=d.color;` | `if(typeof COLORS!=='undefined'){COLORS[0]=d.color;COLORS[2]=d.color;COLORS[4]=d.color;}` |
| `SCATTER_LOGIC` | `for(let i=0;i<15;i++){const x=Math.random()*canvas.width;const y=Math.random()*canvas.height;particles.push(new SplatterParticle(x,y,activeColor));}` | `for(let i=0;i<30;i++){createStroke(Math.random()*window.innerWidth,Math.random()*window.innerHeight);}` | `document.querySelectorAll('.face').forEach(f=>{createImpact({offsetX:Math.random()*300,offsetY:Math.random()*300},f);});` |
| `RANDOMIZE_LOGIC` | `const keys=Object.keys(PALETTES);currentPalette=PALETTES[keys[Math.floor(Math.random()*keys.length)]];activeColor=currentPalette[Math.floor(Math.random()*currentPalette.length)];` | `const colors=['#e63946','#f1faee','#a8dadc','#457b9d','#1d3557','#ffbe0b','#fb5607','#8ac926'];currentColor=colors[Math.floor(Math.random()*colors.length)];createExplosion();` | `COLORS.forEach((_,i)=>{COLORS[i]='#'+Math.floor(Math.random()*16777215).toString(16).padStart(6,'0');});` |

For **impasto** and **entropy cube** (DOM-based, no raw canvas), add html2canvas CDN before `</head>`:
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
```

---

### TASK 2: Update the main OmniCanvas shell (index.html + main.js + style.css)

**2a. Update `index.html`** — Add the 3 new iframe layers and all new UI controls.

Replace the current `<!-- Layers -->` section inside `#artboard` with:

```html
<!-- Layers — ordered back to front -->
<iframe id="layer-noir" src="applets/noir-abstract-studio/index.html" class="art-layer active"></iframe>
<iframe id="layer-abstractify" src="applets/abstractify-kinetic-canvas/index.html" class="art-layer active"></iframe>
<iframe id="layer-chromatic" src="applets/chromatic-dialogue/index.html" class="art-layer"></iframe>
<iframe id="layer-impasto" src="applets/impasto-abstract-art-generator/index.html" class="art-layer active"></iframe>
<iframe id="layer-trippy" src="applets/trippy-neural-art/index.html" class="art-layer"></iframe>
<iframe id="layer-neon" src="applets/neon-neural-flow/index.html" class="art-layer active"></iframe>
<iframe id="layer-entropy" src="applets/digital-entropy-cube/index.html" class="art-layer active"></iframe>
```

Note: chromatic and trippy start unchecked (not `.active`) so the default isn't too overwhelming — user toggles them on.

Replace the **layer-manager** section with:

```html
<div class="layer-manager">
    <h3>Active Media Layers</h3>

    <div class="layer-row" data-layer="layer-noir">
        <input type="checkbox" data-target="layer-noir" checked>
        <span class="name">🌆 Noir Studio</span>
        <input type="range" class="layer-opacity" data-target="layer-noir" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-noir" title="Blend Mode">
            <option value="normal">Normal</option>
            <option value="multiply">Multiply</option>
            <option value="screen">Screen</option>
            <option value="overlay">Overlay</option>
            <option value="difference">Difference</option>
            <option value="color-dodge">Color Dodge</option>
            <option value="exclusion">Exclusion</option>
            <option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-abstractify">
        <input type="checkbox" data-target="layer-abstractify" checked>
        <span class="name">🎨 Kinetic Canvas</span>
        <input type="range" class="layer-opacity" data-target="layer-abstractify" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-abstractify" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen">Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-chromatic">
        <input type="checkbox" data-target="layer-chromatic">
        <span class="name">💧 Chromatic Dialogue</span>
        <input type="range" class="layer-opacity" data-target="layer-chromatic" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-chromatic" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen" selected>Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-impasto">
        <input type="checkbox" data-target="layer-impasto" checked>
        <span class="name">🔪 Impasto Strokes</span>
        <input type="range" class="layer-opacity" data-target="layer-impasto" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-impasto" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen">Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-trippy">
        <input type="checkbox" data-target="layer-trippy">
        <span class="name">🌀 Trippy Neural Art</span>
        <input type="range" class="layer-opacity" data-target="layer-trippy" min="0" max="100" value="70" title="Opacity">
        <select class="layer-blend" data-target="layer-trippy" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen" selected>Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-neon">
        <input type="checkbox" data-target="layer-neon" checked>
        <span class="name">💫 Neon Neural Flow</span>
        <input type="range" class="layer-opacity" data-target="layer-neon" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-neon" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen" selected>Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>

    <div class="layer-row" data-layer="layer-entropy">
        <input type="checkbox" data-target="layer-entropy" checked>
        <span class="name">🧊 Entropy Cube</span>
        <input type="range" class="layer-opacity" data-target="layer-entropy" min="0" max="100" value="100" title="Opacity">
        <select class="layer-blend" data-target="layer-entropy" title="Blend Mode">
            <option value="normal">Normal</option><option value="multiply">Multiply</option><option value="screen" selected>Screen</option><option value="overlay">Overlay</option><option value="difference">Difference</option><option value="color-dodge">Color Dodge</option><option value="exclusion">Exclusion</option><option value="luminosity">Luminosity</option>
        </select>
    </div>
</div>
```

**Remove the "Target Mode" radio group** (all/background/cube) — it's too limited now. The per-layer toggles handle this better.

**Replace the Brush Dynamics section** with an expanded controls section:

```html
<!-- Brush Dynamics -->
<div class="settings-section">
    <h3>Brush Dynamics</h3>
    <div class="slider-row">
        <label>Thickness <span id="val-size">50%</span></label>
        <input type="range" id="global-size" min="1" max="100" value="50">
    </div>
    <div class="slider-row">
        <label>Viscosity / Chaos <span id="val-visc">50%</span></label>
        <input type="range" id="global-visc" min="1" max="100" value="50">
    </div>
</div>

<!-- Global Effects Engine -->
<div class="settings-section">
    <h3>Effects Engine</h3>
    <div class="slider-row">
        <label>Time Warp <span id="val-speed">1.0x</span></label>
        <input type="range" id="global-speed" min="10" max="300" value="100">
    </div>
    <div class="slider-row">
        <label>Bloom / Glow <span id="val-bloom">0%</span></label>
        <input type="range" id="global-bloom" min="0" max="100" value="0">
    </div>
    <div class="effects-grid">
        <button id="btn-scatter" class="btn-fx" title="Random paint burst on all layers">💥 Scatter</button>
        <button id="btn-mirror" class="btn-fx" title="Flip canvas horizontally">🪞 Mirror</button>
        <button id="btn-kaleidoscope" class="btn-fx" title="Cycle kaleidoscope symmetry">🔮 Kaleidoscope</button>
        <button id="btn-glitch" class="btn-fx" title="Random glitch distortion">⚡ Glitch</button>
        <button id="btn-invert" class="btn-fx" title="Invert all colors">🔄 Invert</button>
        <button id="btn-randomize" class="btn-fx" title="Randomize all layer palettes">🎲 Randomize</button>
    </div>
</div>

<!-- Color -->
<div class="settings-section">
    <div class="color-picker-wrapper">
        <label for="global-color">Brush Color:</label>
        <input type="color" id="global-color" value="#ff3366">
    </div>
</div>

<!-- Actions -->
<div class="actions">
    <button id="btn-clear" class="btn secondary">Reset Canvas</button>
    <button id="btn-fullscreen" class="btn secondary">⛶ Fullscreen</button>
    <button id="btn-save" class="btn primary">💾 Save Artwork</button>
</div>

<!-- Oracle Readings -->
<div class="settings-section oracle-section">
    <h3>Oracle Readings</h3>
    <div class="oracle-grid">
        <button id="btn-psycho" class="btn-oracle" data-oracle="psycho">🧠 The Psychoanalyst</button>
        <button id="btn-fortune" class="btn-oracle" data-oracle="fortune">🔮 Fortune Teller</button>
        <button id="btn-critic" class="btn-oracle" data-oracle="critic">🎩 Art Critic</button>
        <button id="btn-astro" class="btn-oracle" data-oracle="astro">⭐ Astrologer</button>
    </div>
    <details class="api-settings">
        <summary>🔑 Premium Readings (API Key)</summary>
        <p class="api-hint">Add your API key to unlock AI-powered vision readings</p>
        <select id="api-provider">
            <option value="anthropic">Anthropic (Claude)</option>
            <option value="openai">OpenAI (GPT-4V)</option>
        </select>
        <input type="password" id="api-key" placeholder="sk-... or your API key">
        <button id="btn-save-key" class="btn secondary">Save Key</button>
        <div class="premium-oracles hidden" id="premium-oracles">
            <button id="btn-deep-vision" class="btn-oracle premium" data-oracle="vision">👁️ Deep Vision Oracle</button>
            <button id="btn-story" class="btn-oracle premium" data-oracle="story">📜 Story Weaver</button>
            <button id="btn-appraisal" class="btn-oracle premium" data-oracle="appraisal">💰 Collector's Appraisal</button>
        </div>
    </details>
</div>
```

**2b. Update `style.css`** — Add styles for new controls:

Append these rules to the existing `style.css`:

```css
/* === Layer Row Controls === */
.layer-row {
    display: grid;
    grid-template-columns: 24px 1fr 60px 80px;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    padding: 4px 0;
}

.layer-row input[type="checkbox"] {
    appearance: none;
    width: 16px; height: 16px;
    border: 2px solid var(--border);
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.2s;
}
.layer-row input[type="checkbox"]:checked {
    background: var(--accent);
    border-color: var(--accent);
}
.layer-row input[type="checkbox"]:checked::after {
    content: "✓"; position: absolute; top: -2px; left: 2px;
    color: #000; font-size: 12px; font-weight: bold;
}

.layer-opacity {
    width: 100%;
    height: 4px;
    -webkit-appearance: none;
    background: rgba(255,255,255,0.15);
    border-radius: 2px;
    outline: none;
}
.layer-opacity::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 12px; height: 12px;
    background: var(--accent);
    border-radius: 50%;
    cursor: pointer;
}

.layer-blend {
    background: rgba(0,0,0,0.4);
    color: #aaa;
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 0.7rem;
    padding: 2px;
    cursor: pointer;
}

/* === Settings Sections === */
.settings-section {
    border-top: 1px solid var(--border);
    padding-top: 12px;
    margin-top: 12px;
}
.settings-section h3 {
    font-size: 0.85rem;
    text-transform: uppercase;
    color: #aaa;
    margin: 0 0 10px 0;
    letter-spacing: 1px;
}

.slider-row {
    margin-bottom: 8px;
}
.slider-row label {
    font-size: 0.8rem;
    color: #ccc;
    display: flex;
    justify-content: space-between;
    margin-bottom: 3px;
}
.slider-row input[type="range"] {
    width: 100%;
}

/* === Effects Grid === */
.effects-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 6px;
    margin-top: 8px;
}

.btn-fx {
    padding: 8px 4px;
    background: rgba(255,255,255,0.06);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: #ccc;
    font-size: 0.72rem;
    cursor: pointer;
    transition: all 0.2s;
    text-align: center;
}
.btn-fx:hover {
    background: rgba(255,255,255,0.15);
    color: white;
    border-color: var(--accent);
    box-shadow: 0 0 10px rgba(0,243,255,0.2);
}
.btn-fx.active {
    background: rgba(0,243,255,0.15);
    border-color: var(--accent);
    color: var(--accent);
}

/* === Oracle Section === */
.oracle-section {
    border-top: 2px solid rgba(188,19,254,0.3);
}

.oracle-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px;
}

.btn-oracle {
    padding: 10px 6px;
    background: linear-gradient(135deg, rgba(255,51,102,0.1), rgba(188,19,254,0.1));
    border: 1px solid rgba(188,19,254,0.3);
    border-radius: 8px;
    color: #ccc;
    font-size: 0.78rem;
    cursor: pointer;
    transition: all 0.3s;
    text-align: center;
}
.btn-oracle:hover {
    background: linear-gradient(135deg, rgba(255,51,102,0.25), rgba(188,19,254,0.25));
    color: white;
    box-shadow: 0 0 15px rgba(188,19,254,0.3);
    transform: translateY(-1px);
}
.btn-oracle.premium {
    border-color: gold;
    background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,165,0,0.08));
}
.btn-oracle.premium:hover {
    box-shadow: 0 0 15px rgba(255,215,0,0.3);
}

/* API Settings */
.api-settings {
    margin-top: 10px;
    font-size: 0.8rem;
}
.api-settings summary {
    cursor: pointer;
    color: #888;
    padding: 6px 0;
}
.api-settings summary:hover { color: #ccc; }
.api-hint {
    font-size: 0.75rem;
    color: #666;
    margin: 6px 0;
}
.api-settings input[type="password"],
.api-settings select {
    width: 100%;
    padding: 6px 8px;
    background: rgba(0,0,0,0.4);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: #ccc;
    font-size: 0.8rem;
    margin-bottom: 6px;
}

/* === Scrollable Panel === */
#ui-panel {
    max-height: calc(100vh - 40px);
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(255,255,255,0.2) transparent;
}
#ui-panel::-webkit-scrollbar { width: 4px; }
#ui-panel::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }

/* === Kaleidoscope Effect === */
#artboard.kaleidoscope-2 { }
#artboard.kaleidoscope-4 .art-layer {
    clip-path: polygon(0 0, 50% 0, 50% 100%, 0 100%);
}
.kaleidoscope-reflect {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    transform: scaleX(-1);
    z-index: 45;
}

/* === Glitch Effect === */
@keyframes glitchShake {
    0% { transform: translate(-50%,-50%); }
    25% { transform: translate(-50%,-50%) translate(3px,-2px); }
    50% { transform: translate(-50%,-50%) translate(-3px,2px); }
    75% { transform: translate(-50%,-50%) translate(2px,3px); }
    100% { transform: translate(-50%,-50%); }
}
#artboard.glitching {
    animation: glitchShake 0.1s linear 5;
}

/* === Fullscreen === */
body.fullscreen #ui-panel { display: none; }
body.fullscreen #artboard {
    width: 100vw !important;
    height: 100vh !important;
    left: 50% !important;
    border-radius: 0;
}
body.fullscreen #interaction-pane {
    width: 100vw !important;
    height: 100vh !important;
    left: 50% !important;
}

/* === Oracle Modal Enhancements === */
.oracle-type-label {
    display: inline-block;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #666;
    margin-bottom: 8px;
}
```

**2c. Rewrite `main.js`** — Complete replacement with all new functionality.

```javascript
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
        // This uses a visual trick: we clone the artboard content with CSS transforms
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
                    model: 'claude-sonnet-4-20250514',
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
```

---

### TASK 3: Verify & Test

After building, test by opening `OmniCanvas/index.html` in a browser (use a local server like `python -m http.server` from the OmniCanvas directory to avoid iframe CORS issues).

**Checklist:**
- [ ] All 7 layers appear and can be toggled on/off
- [ ] Drawing on the canvas affects all active layers
- [ ] Opacity sliders work per-layer
- [ ] Blend mode dropdowns change layer compositing
- [ ] Color picker updates all layers
- [ ] Size/Viscosity sliders affect stroke behavior
- [ ] Scatter button creates random bursts across layers
- [ ] Mirror flips the canvas
- [ ] Kaleidoscope cycles through symmetry levels
- [ ] Glitch creates momentary distortion
- [ ] Invert toggles color inversion
- [ ] Randomize changes colors across all layers
- [ ] Fullscreen hides UI and expands canvas
- [ ] Save exports a composited PNG
- [ ] All 4 free Oracle readings produce different themed text
- [ ] API key entry shows premium oracle buttons
- [ ] Keyboard shortcuts (S, M, K, G, I, R, F, 1-7) work
- [ ] Applet UIs are hidden (no stacked controls from individual applets)
- [ ] Canvas backgrounds are transparent (layers composite properly)

**Common issues to fix:**
- If an applet's background isn't transparent, check the applet's CSS for hardcoded `background` rules and override them in the integration script's DOMContentLoaded
- If mouse events don't reach an applet, check that the applet's event listeners use `clientX`/`clientY` (not `offsetX`/`offsetY` which won't work with synthetic events)
- If html2canvas capture fails, ensure the CDN script is loaded before the integration script
- The `Touch` constructor may not be available in all browsers — the try/catch handles this gracefully

---

## FUTURE ENHANCEMENT IDEAS (not for this build)

- **Sound reactivity**: Web Audio API oscillator that responds to brush strokes
- **Gallery mode**: Save/load multiple artworks to localStorage
- **Layer reordering**: Drag to reorder iframe z-index
- **Preset "recipes"**: Save/load combinations of layer states, blend modes, and effects
- **Recording mode**: Capture creation process as timelapse video (MediaRecorder API)
- **Collaborative mode**: WebRTC to share canvas with another person
- **Import image as layer**: Upload a photo as a background layer
