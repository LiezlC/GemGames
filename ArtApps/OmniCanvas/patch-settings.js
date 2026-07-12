const fs = require('fs');
const path = require('path');

// 1. Update OmniCanvas/index.html with new sliders
const indexHtmlPath = 'C:\\Users\\Liezl\\Documents\\Content\\OmniCanvas\\index.html';
let indexHtml = fs.readFileSync(indexHtmlPath, 'utf8');

const slidersHtml = `
            <div class="settings-group" style="margin-bottom: 15px; border-top: 1px solid var(--border); padding-top: 15px;">
                <h3 style="font-size: 0.85rem; text-transform: uppercase; color: #aaa; margin-bottom: 10px; margin-top: 0;">Brush Dynamics</h3>
                
                <div style="margin-bottom: 10px;">
                    <label style="font-size: 0.8rem; color: #ccc; display: flex; justify-content: space-between;">
                        Thickness <span id="val-size">50%</span>
                    </label>
                    <input type="range" id="global-size" min="1" max="100" value="50" style="width: 100%;">
                </div>
                
                <div style="margin-bottom: 10px;">
                    <label style="font-size: 0.8rem; color: #ccc; display: flex; justify-content: space-between;">
                        Viscosity / Chaos <span id="val-visc">50%</span>
                    </label>
                    <input type="range" id="global-visc" min="1" max="100" value="50" style="width: 100%;">
                </div>
            </div>
`;

if (!indexHtml.includes('global-size')) {
    indexHtml = indexHtml.replace('<div class="actions">', slidersHtml + '\n        <div class="actions">');
    fs.writeFileSync(indexHtmlPath, indexHtml);
}

// 2. Update OmniCanvas/main.js to broadcast settings
const mainJsPath = 'C:\\Users\\Liezl\\Documents\\Content\\OmniCanvas\\main.js';
let mainJs = fs.readFileSync(mainJsPath, 'utf8');
const settingsJs = `
// Global Settings Broadcaster
function broadcastSettings() {
    const size = parseInt(document.getElementById('global-size').value);
    const visc = parseInt(document.getElementById('global-visc').value);
    document.querySelectorAll('.art-layer').forEach(iframe => {
        try {
            iframe.contentWindow.postMessage({
                type: 'omni-settings',
                size: size,
                viscosity: visc
            }, '*');
        } catch (err) {}
    });
}

document.getElementById('global-size').addEventListener('input', (e) => {
    document.getElementById('val-size').innerText = e.target.value + '%';
    broadcastSettings();
});
document.getElementById('global-visc').addEventListener('input', (e) => {
    document.getElementById('val-visc').innerText = e.target.value + '%';
    broadcastSettings();
});
`;

if (!mainJs.includes('omni-settings')) {
    mainJs = mainJs.replace('// Mouse Events', settingsJs + '\n// Mouse Events');
    fs.writeFileSync(mainJsPath, mainJs);
}

// 3. Patch the specific applets to use omniSettings
const appletsDir = 'C:\\Users\\Liezl\\Documents\\Content\\OmniCanvas\\applets';
const applets = ['impasto-abstract-art-generator', 'neon-neural-flow', 'digital-entropy-cube', 'abstractify-kinetic-canvas'];

const settingsLogic = `
        if (event.data && event.data.type === 'omni-settings') {
            window.omniSize = event.data.size; // 1 to 100
            window.omniVisc = event.data.viscosity; // 1 to 100
        }
`;

applets.forEach(app => {
    const indexPath = path.join(appletsDir, app, 'index.html');
    if (fs.existsSync(indexPath)) {
        let content = fs.readFileSync(indexPath, 'utf8');
        
        // Add listener for omni-settings
        if (!content.includes('omni-settings')) {
            content = content.replace("if (event.data && event.data.type === 'omni-mouse'", settingsLogic + "        if (event.data && event.data.type === 'omni-mouse'");
        }

        // App-specific patches to use window.omniSize and window.omniVisc
        if (app === 'digital-entropy-cube') {
            // Fix synthetic offset issues by using bounding box directly if offset is 0
            if(!content.includes('rect.left')) {
                content = content.replace('const x = e.offsetX;', 'const x = (e.offsetX === 0 || e.offsetX === undefined) ? e.clientX - rect.left : e.offsetX;');
                content = content.replace('const y = e.offsetY;', 'const y = (e.offsetY === 0 || e.offsetY === undefined) ? e.clientY - rect.top : e.offsetY;');
            }
            
            // Map Size to Splatter Size
            content = content.replace('const size = Math.random() * 40 + 10;', 'let bSize = window.omniSize || 50; const size = Math.random() * bSize + (bSize/2);');
            // Map Viscosity to Number of Shapes
            content = content.replace('const numShapes = Math.floor(Math.random() * 5) + 3;', 'let bVisc = window.omniVisc || 50; const numShapes = Math.floor(Math.random() * (bVisc/10)) + 3;');
        }
        
        if (app === 'abstractify-kinetic-canvas') {
            content = content.replace('ctx.lineWidth = Math.random() * 30 + 10;', 'let bSize = window.omniSize || 50; ctx.lineWidth = Math.random() * (bSize*0.6) + (bSize*0.2);');
            content = content.replace('Math.random() * 300 + 100;', 'let bVisc = window.omniVisc || 50; Math.random() * (bVisc*6) + (bVisc*2);');
        }

        if (app === 'neon-neural-flow') {
            content = content.replace('this.size = Math.random() * 1.5 + 0.5;', 'let bSize = window.omniSize || 50; this.size = Math.random() * (bSize/20) + 0.5;');
            content = content.replace('config.chaos = 0.2;', 'let bVisc = window.omniVisc || 50; config.chaos = bVisc / 100;');
            content = content.replace('config.chaos = 0.2', 'config.chaos = (window.omniVisc !== undefined ? window.omniVisc/100 : 0.2)');
        }

        if (app === 'impasto-abstract-art-generator') {
            content = content.replace('const width = Math.random() * 80 + 20;', 'let bSize = window.omniSize || 50; const width = Math.random() * (bSize*1.6) + (bSize*0.4);');
            content = content.replace('const height = Math.random() * 80 + 20;', 'let bSize = window.omniSize || 50; const height = Math.random() * (bSize*1.6) + (bSize*0.4);');
            content = content.replace('box-shadow: 2px 2px 5px rgba(0,0,0,0.5)', 'box-shadow: ${ (window.omniVisc || 50) > 60 ? Math.random()*10 + "px " + Math.random()*10 + "px 15px rgba(0,0,0,0.3)" : "2px 2px 5px rgba(0,0,0,0.5)" }');
        }

        fs.writeFileSync(indexPath, content);
        console.log('Settings logic added to ' + app);
    }
});
