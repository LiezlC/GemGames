#!/usr/bin/env python3
"""
Add touch/mobile controls to games that only have keyboard/mouse controls.
"""

import re
from pathlib import Path

def add_touch_support(html_content: str) -> str:
    """Add touch event support to HTML game."""

    # Check if already has touch support
    if 'ontouchstart' in html_content.lower() or 'touchstart' in html_content.lower():
        return html_content

    # Find the closing </script> tag before </body>
    script_insert = """
    // ===== MOBILE TOUCH SUPPORT =====
    // Added for mobile-friendly gameplay

    (function() {
        // Touch to click conversion
        document.addEventListener('touchstart', function(e) {
            if (e.target.tagName === 'BUTTON' || e.target.onclick) {
                e.preventDefault();
                e.target.click();
            }
        }, { passive: false });

        // Swipe detection for mobile
        let touchStartX = 0;
        let touchStartY = 0;
        let touchEndX = 0;
        let touchEndY = 0;

        document.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, false);

        document.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            handleSwipe();
        }, false);

        function handleSwipe() {
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            const minSwipeDistance = 50;

            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    // Swipe right - simulate right arrow
                    simulateKey('ArrowRight', 39);
                } else {
                    // Swipe left - simulate left arrow
                    simulateKey('ArrowLeft', 37);
                }
            } else if (Math.abs(deltaY) > minSwipeDistance) {
                if (deltaY > 0) {
                    // Swipe down - simulate down arrow
                    simulateKey('ArrowDown', 40);
                } else {
                    // Swipe up - simulate up arrow
                    simulateKey('ArrowUp', 38);
                }
            }
        }

        function simulateKey(key, keyCode) {
            const event = new KeyboardEvent('keydown', {
                key: key,
                keyCode: keyCode,
                code: key,
                which: keyCode,
                bubbles: true
            });
            document.dispatchEvent(event);
        }

        // Tap anywhere to start (for games requiring click to begin)
        let hasStarted = false;
        document.addEventListener('touchstart', function(e) {
            if (!hasStarted) {
                hasStarted = true;
                // Simulate spacebar/enter for start
                simulateKey(' ', 32);
            }
        }, { once: true });

        // Prevent double-tap zoom
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function(e) {
            const now = Date.now();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);

        // Add mobile controls hint
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                body::after {
                    content: '👆 Tap to play • Swipe to move';
                    position: fixed;
                    bottom: 10px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: rgba(0,0,0,0.7);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-size: 12px;
                    z-index: 10000;
                    pointer-events: none;
                    animation: fadeOut 4s forwards;
                }
                @keyframes fadeOut {
                    0%, 70% { opacity: 1; }
                    100% { opacity: 0; }
                }
            }
        `;
        document.head.appendChild(style);
    })();
    """

    # Insert before closing body tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'<script>{script_insert}</script>\n</body>')
    elif '</html>' in html_content:
        html_content = html_content.replace('</html>', f'<script>{script_insert}</script>\n</html>')

    return html_content

def process_game(game_path: Path) -> bool:
    """Add touch support to a game."""

    html_file = game_path / 'index.html'

    if not html_file.exists():
        return False

    try:
        # Read original
        content = html_file.read_text(encoding='utf-8')

        # Check if already has touch
        if 'MOBILE TOUCH SUPPORT' in content:
            print(f"  ⏭️  Already has touch support")
            return False

        # Add touch support
        enhanced = add_touch_support(content)

        # Write back
        html_file.write_text(enhanced, encoding='utf-8')

        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Add touch controls to top games."""

    top_games = [
        'sonic/Cosmic_Query_Event_Horizon',
        'sonic/Neon_Sync_Overdrive',
        'sonic/SYNTH_MIND_Neural_Interface',
        'simulation/Protocol_DRAGON_Server_Guardian',
        'sonic/Serpent_s_Cove_Guardian_of_the_Deep',
        'simulation/Cyber-Shepherd_OS',
        'action/Void_Drifter_Event_Horizon',
        'puzzle/The_Vigil_Keeper_of_the_Flame',
        'sonic/Dreamscape_Forager',
        'puzzle/Neon_Wyvern_Protocol',
        'sonic/Bio-Acoustic_Plant_Interface',
    ]

    print("📱 ADDING MOBILE TOUCH CONTROLS")
    print("=" * 80)
    print()

    base_dir = Path('extracted')
    enhanced_count = 0

    for game_rel_path in top_games:
        game_path = base_dir / game_rel_path
        game_name = game_rel_path.split('/')[-1].replace('_', ' ')

        print(f"🎮 {game_name}")

        if process_game(game_path):
            enhanced_count += 1
            print(f"  ✅ Touch controls added")

        print()

    print("=" * 80)
    print(f"✅ Enhanced {enhanced_count} games with mobile touch support!")
    print()
    print("Features added:")
    print("  • Tap to click (buttons work)")
    print("  • Swipe gestures (left/right/up/down)")
    print("  • Tap to start games")
    print("  • Prevent double-tap zoom")
    print("  • Mobile controls hint (fades after 4 seconds)")

if __name__ == '__main__':
    main()
