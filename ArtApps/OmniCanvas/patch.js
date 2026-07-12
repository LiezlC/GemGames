const fs = require('fs');
const path = require('path');

const appletsDir = 'C:\\Users\\Liezl\\Documents\\Content\\OmniCanvas\\applets';
const applets = ['impasto-abstract-art-generator', 'neon-neural-flow', 'digital-entropy-cube', 'abstractify-kinetic-canvas'];

const injection = `
<script>
    window.addEventListener('message', (event) => {
        if (event.data && event.data.type === 'omni-mouse' && event.source === window.parent) {
            const { action, clientX, clientY } = event.data;
            let target = document.elementFromPoint(clientX, clientY) || document.body;
            
            // Neon Neural Flow specific: dispatch to canvas
            if (document.getElementById('flowCanvas')) target = document.getElementById('flowCanvas');
            else if (document.getElementById('artCanvas')) target = document.getElementById('artCanvas');
            else if (document.getElementById('canvas-container')) target = document.getElementById('canvas-container');
            
            // Fake mouse/touch events
            const ev = new MouseEvent(action, {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: clientX,
                clientY: clientY
            });
            target.dispatchEvent(ev);

            // Also dispatch parallel Touch events for apps that use them
            if (action.startsWith('mouse')) {
                const touchType = action.replace('mouse', 'touch');
                if (touchType === 'touchdown') var type = 'touchstart';
                else if (touchType === 'touchup') var type = 'touchend';
                else var type = touchType;
                
                try {
                    const touch = new Touch({
                        identifier: Date.now(),
                        target: target,
                        clientX: clientX,
                        clientY: clientY,
                        radiusX: 2.5,
                        radiusY: 2.5,
                        rotationAngle: 10,
                        force: 0.5,
                    });
                    const touchEvent = new TouchEvent(type, {
                        cancelable: true,
                        bubbles: true,
                        touches: type === 'touchend' ? [] : [touch],
                        targetTouches: type === 'touchend' ? [] : [touch],
                        changedTouches: [touch]
                    });
                    target.dispatchEvent(touchEvent);
                } catch(e) {}
            }
        }
    });

    // Make backgrounds transparent
    document.addEventListener('DOMContentLoaded', () => {
        document.body.style.backgroundColor = 'transparent';
        document.documentElement.style.backgroundColor = 'transparent';
        
        // Hide UI elements if running in OmniCanvas iframe to avoid stacking 4 UIs
        if (window.self !== window.top) {
            const uis = document.querySelectorAll('#ui-layer, .ui-panel, #controls, #intro, .hint, .header-overlay');
            uis.forEach(ui => ui.style.display = 'none');
            
            // For digital entropy cube: click body to start
            if(document.body.innerHTML.includes('Digital Entropy Cube')) {
                // hide some things
            }
        }
    });
</script>
`;

applets.forEach(app => {
    const indexPath = path.join(appletsDir, app, 'index.html');
    if (fs.existsSync(indexPath)) {
        let content = fs.readFileSync(indexPath, 'utf8');
        // Replace background colors in CSS
        content = content.replace(/background-color:\s*var\(--bg-color\);/g, 'background-color: transparent !important;');
        content = content.replace(/background:\s*(radial-gradient|linear-gradient).*?;/g, 'background: transparent !important;');
        content = content.replace(/background-color:\s*#.*?;/g, 'background-color: transparent !important;');
        
        if (!content.includes('omni-mouse')) {
            content = content.replace('</body>', injection + '\n</body>');
            fs.writeFileSync(indexPath, content);
            console.log('Patched ' + app);
        }
    }
});
