const fs = require('fs');
const path = require('path');

const appletsDir = 'C:\\Users\\Liezl\\Documents\\Content\\OmniCanvas\\applets';
const applets = ['impasto-abstract-art-generator', 'neon-neural-flow', 'digital-entropy-cube', 'abstractify-kinetic-canvas'];

const html2canvasScript = `<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>`;

const captureLogic = `
        if (event.data && event.data.type === 'omni-capture') {
            const zIndex = event.data.zIndex;
            
            // Check if we have a raw canvas
            let rawCanvas = document.getElementById('flowCanvas') || document.getElementById('artCanvas');
            
            if (rawCanvas) {
                // Easy route: canvas.toDataURL
                window.parent.postMessage({
                    type: 'omni-capture-result',
                    zIndex: zIndex,
                    dataUrl: rawCanvas.toDataURL('image/png')
                }, '*');
            } else {
                // Hard route: html2canvas
                if (typeof html2canvas !== 'undefined') {
                    html2canvas(document.body, { backgroundColor: null, logging: false }).then(canvas => {
                        window.parent.postMessage({
                            type: 'omni-capture-result',
                            zIndex: zIndex,
                            dataUrl: canvas.toDataURL('image/png')
                        }, '*');
                    });
                } else {
                    console.error("html2canvas not loaded in iframe");
                }
            }
        }
`;

applets.forEach(app => {
    const indexPath = path.join(appletsDir, app, 'index.html');
    if (fs.existsSync(indexPath)) {
        let content = fs.readFileSync(indexPath, 'utf8');
        
        // Inject html2canvas CDN if not present and if the applet is a DOM-based one
        if (app === 'impasto-abstract-art-generator' || app === 'digital-entropy-cube') {
            if (!content.includes('html2canvas.min.js')) {
                content = content.replace('</head>', `    ${html2canvasScript}\n</head>`);
            }
        }
        
        // Add listener for omni-capture
        if (!content.includes('omni-capture')) {
            content = content.replace("if (event.data && event.data.type === 'omni-mouse'", captureLogic + "        if (event.data && event.data.type === 'omni-mouse'");
        }

        fs.writeFileSync(indexPath, content);
        console.log('Capture logic added to ' + app);
    }
});
