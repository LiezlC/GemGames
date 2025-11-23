#!/usr/bin/env python3
"""
Generate gallery index pages for both gameplay and thematic organization.
"""

from pathlib import Path
import json

def scan_category(category_path):
    """Scan a category folder and return list of games."""
    games = []
    if not category_path.is_dir():
        return games

    for game_dir in sorted(category_path.iterdir()):
        if game_dir.is_dir():
            html_file = game_dir / 'index.html'
            if html_file.exists():
                # Get game title from folder name
                title = game_dir.name.replace('_', ' ')
                games.append({
                    'name': title,
                    'folder': game_dir.name,
                    'path': game_dir.relative_to(Path('extracted'))
                })

    return games

def generate_gameplay_gallery():
    """Generate extracted/index.html for gameplay categories."""

    # Category definitions
    categories = {
        'action': {'emoji': '⚡', 'name': 'Action', 'desc': 'Fast-paced reflex games'},
        'adventure': {'emoji': '🗺️', 'name': 'Adventure', 'desc': 'Exploration and discovery'},
        'arcade': {'emoji': '👾', 'name': 'Arcade', 'desc': 'Classic arcade-style games'},
        'memory': {'emoji': '🧠', 'name': 'Memory', 'desc': 'Pattern matching and recall'},
        'puzzle': {'emoji': '🧩', 'name': 'Puzzle', 'desc': 'Logic and problem solving'},
        'rhythm': {'emoji': '🎵', 'name': 'Rhythm', 'desc': 'Timing and music games'},
        'simulation': {'emoji': '🌐', 'name': 'Simulation', 'desc': 'Interactive simulations'},
        'sonic': {'emoji': '🔊', 'name': 'Sonic', 'desc': 'Games with audio synthesis'},
        'visual': {'emoji': '🎨', 'name': 'Visual', 'desc': 'Interactive art experiences'}
    }

    extracted_dir = Path('extracted')

    # Scan all categories
    total_games = 0
    category_data = {}

    for cat_id, cat_info in categories.items():
        cat_path = extracted_dir / cat_id
        games = scan_category(cat_path)
        if games:
            category_data[cat_id] = {
                'info': cat_info,
                'games': games
            }
            total_games += len(games)

    # Count audio games
    sonic_count = len(category_data.get('sonic', {}).get('games', []))

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Games Collection - {total_games} Games Organized</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 3px solid #667eea;
        }}

        h1 {{
            font-size: 2.5em;
            color: #667eea;
            margin-bottom: 10px;
        }}

        .subtitle {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 20px;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #764ba2;
        }}

        .stat-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .view-toggle {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}

        .view-toggle a {{
            display: inline-block;
            padding: 12px 30px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            margin: 5px;
            border: 2px solid #667eea;
            font-weight: 600;
            transition: all 0.3s;
        }}

        .view-toggle a:hover {{
            background: #667eea;
            color: white;
            transform: translateY(-2px);
        }}

        .category-section {{
            margin-bottom: 50px;
        }}

        .category-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .category-emoji {{
            font-size: 2em;
        }}

        .category-info {{
            flex: 1;
        }}

        .category-name {{
            font-size: 1.5em;
            font-weight: 600;
            margin-bottom: 5px;
        }}

        .category-desc {{
            opacity: 0.9;
            font-size: 0.95em;
        }}

        .category-count {{
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }}

        .games-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            padding: 0 10px;
        }}

        .game-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            cursor: pointer;
        }}

        .game-card:hover {{
            border-color: #667eea;
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
        }}

        .game-card a {{
            text-decoration: none;
            color: #333;
            display: block;
        }}

        .game-title {{
            font-weight: 600;
            font-size: 1.05em;
            margin-bottom: 10px;
            color: #667eea;
        }}

        .game-play {{
            display: inline-block;
            padding: 8px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 6px;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
            color: #666;
        }}

        footer p {{
            margin: 10px 0;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 25px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            transition: all 0.3s;
        }}

        .back-link:hover {{
            background: #764ba2;
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Gemini Games Collection</h1>
            <p class="subtitle">{total_games} AI-Generated Browser Games</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">{total_games}</div>
                    <div class="stat-label">Total Games</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{len(category_data)}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat">
                    <div class="stat-number">{sonic_count}</div>
                    <div class="stat-label">With Audio</div>
                </div>
            </div>
        </header>

        <div class="view-toggle">
            <strong>Browse by:</strong>
            <a href="index.html" class="active">Gameplay Type</a>
            <a href="../content/index.html">Theme</a>
            <a href="top_games.html">Top Rated</a>
        </div>

        <main>
'''

    # Add each category
    for cat_id in ['action', 'adventure', 'arcade', 'memory', 'puzzle', 'rhythm', 'simulation', 'sonic', 'visual']:
        if cat_id not in category_data:
            continue

        cat = category_data[cat_id]
        info = cat['info']
        games = cat['games']

        html += f'''
        <section class="category-section">
            <div class="category-header">
                <div class="category-emoji">{info['emoji']}</div>
                <div class="category-info">
                    <div class="category-name">{info['name']}</div>
                    <div class="category-desc">{info['desc']}</div>
                </div>
                <div class="category-count">{len(games)} games</div>
            </div>

            <div class="games-grid">
'''

        for game in games:
            html += f'''
                <div class="game-card">
                    <a href="{game['path']}/index.html">
                        <div class="game-title">{game['name']}</div>
                        <div class="game-play">Play Game</div>
                    </a>
                </div>
'''

        html += '''
            </div>
        </section>
'''

    html += f'''
        </main>

        <footer>
            <p><strong>All games created by Google Gemini 3.0</strong></p>
            <p>November 2024 | HTML5 Canvas & Web Audio API</p>
            <a href="../README.md" class="back-link">Back to README</a>
        </footer>
    </div>
</body>
</html>
'''

    # Write file
    output_file = Path('extracted/index.html')
    output_file.write_text(html, encoding='utf-8')
    print(f"✅ Generated {output_file}")
    print(f"   Total games: {total_games}")
    print(f"   Categories: {len(category_data)}")

def generate_theme_gallery():
    """Generate content/index.html for thematic categories."""

    # Load theme categorization metadata
    metadata_file = Path('theme_categorization.json')
    if not metadata_file.exists():
        print("⚠️  No theme_categorization.json found, skipping theme gallery")
        return

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    theme_stats = metadata['themes']

    # Theme definitions with emojis
    theme_info = {
        'Blurring_Boundaries': {'emoji': '🤖', 'name': 'Blurring Boundaries'},
        'Cosmo_Spacer': {'emoji': '🌌', 'name': 'Cosmo Spacer'},
        'Dragons': {'emoji': '🐉', 'name': 'Dragons'},
        'Farmy_Fun': {'emoji': '🌾', 'name': 'Farmy Fun'},
        'Mystic_Rituals': {'emoji': '🕯️', 'name': 'Mystic Rituals'},
        'Neon_Cyber': {'emoji': '💠', 'name': 'Neon Cyber'},
        'Nature_Harmony': {'emoji': '🌿', 'name': 'Nature Harmony'},
        'HouseSim': {'emoji': '🏠', 'name': 'HouseSim'},
        'Light_Patterns': {'emoji': '💡', 'name': 'Light Patterns'},
        'Paint_Splash': {'emoji': '🎨', 'name': 'Paint Splash'},
        'Us_vs_Them': {'emoji': '⚔️', 'name': 'Us vs Them'},
        'UX_Landings': {'emoji': '🖥️', 'name': 'UX Landings'},
        'Zazen': {'emoji': '🧘', 'name': 'Zazen'},
        'Hyper_Drive': {'emoji': '🚀', 'name': 'Hyper Drive'}
    }

    # Count unique games (not entries)
    unique_games = set()
    for theme_games in theme_stats.values():
        unique_games.update(theme_games)
    total_unique = len(unique_games)

    total_entries = sum(len(games) for games in theme_stats.values())

    # Generate HTML
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GemGames - Thematic Collection</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            padding: 20px;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 40px 20px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 10px;
            background: linear-gradient(to right, #fff, #a8edea);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .subtitle {{
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 20px;
        }}

        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}

        .stat {{
            background: rgba(255, 255, 255, 0.1);
            padding: 10px 20px;
            border-radius: 10px;
            backdrop-filter: blur(5px);
        }}

        .stat strong {{
            color: #a8edea;
        }}

        .view-toggle {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .view-toggle a {{
            display: inline-block;
            padding: 12px 30px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            margin: 0 10px;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }}

        .view-toggle a:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}

        .view-toggle a.active {{
            background: rgba(168, 237, 234, 0.3);
            border: 2px solid #a8edea;
        }}

        .themes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }}

        .theme-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }}

        .theme-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(168, 237, 234, 0.5);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}

        .theme-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }}

        .theme-emoji {{
            font-size: 3em;
        }}

        .theme-title {{
            font-size: 1.5em;
            font-weight: 600;
        }}

        .theme-count {{
            background: rgba(168, 237, 234, 0.3);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            margin-left: auto;
        }}

        .theme-games {{
            max-height: 300px;
            overflow-y: auto;
            padding-right: 10px;
        }}

        .theme-games::-webkit-scrollbar {{
            width: 8px;
        }}

        .theme-games::-webkit-scrollbar-track {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }}

        .theme-games::-webkit-scrollbar-thumb {{
            background: rgba(168, 237, 234, 0.5);
            border-radius: 10px;
        }}

        .game-link {{
            display: block;
            padding: 10px;
            margin: 5px 0;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            color: white;
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .game-link:hover {{
            background: rgba(168, 237, 234, 0.3);
            transform: translateX(5px);
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding: 30px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}

        footer p {{
            margin: 10px 0;
        }}

        .back-link {{
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }}

        .back-link:hover {{
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>GemGames Thematic Collection</h1>
            <p class="subtitle">Browse by Theme & Content</p>
            <div class="stats">
                <div class="stat"><strong>{total_unique}</strong> Unique Games</div>
                <div class="stat"><strong>{len([t for t in theme_stats.values() if t])}</strong> Themes</div>
                <div class="stat"><strong>{total_entries}</strong> Total Entries</div>
            </div>
        </header>

        <div class="view-toggle">
            <strong>Browse by:</strong>
            <a href="../extracted/index.html">Gameplay Type</a>
            <a href="index.html" class="active">Theme</a>
            <a href="../extracted/top_games.html">Top Rated</a>
        </div>

        <div class="themes-grid">
'''

    # Add each theme
    for theme_id, info in theme_info.items():
        games = theme_stats.get(theme_id, [])
        if not games:
            continue

        html += f'''
            <div class="theme-card">
                <div class="theme-header">
                    <div class="theme-emoji">{info['emoji']}</div>
                    <div class="theme-title">{info['name']}</div>
                    <div class="theme-count">{len(games)}</div>
                </div>
                <div class="theme-games">
'''

        for game_name in sorted(games):
            # Convert game name back to path-safe format
            game_path = game_name.replace(' ', '_')
            html += f'''
                    <a href="{theme_id}/{game_path}/index.html" class="game-link">{game_name}</a>
'''

        html += '''
                </div>
            </div>
'''

    html += f'''
        </div>

        <footer>
            <p><strong>All games created by Google Gemini 3.0</strong></p>
            <p>November 2024 | Organized by thematic content</p>
            <a href="../README.md" class="back-link">Back to README</a>
        </footer>
    </div>
</body>
</html>
'''

    # Write file
    output_file = Path('content/index.html')
    output_file.write_text(html, encoding='utf-8')
    print(f"✅ Generated {output_file}")
    print(f"   Unique games: {total_unique}")
    print(f"   Total entries: {total_entries}")
    print(f"   Themes: {len([t for t in theme_stats.values() if t])}")

def main():
    """Generate all gallery pages."""
    print("🎨 GALLERY GENERATION")
    print("=" * 80)
    print()

    generate_gameplay_gallery()
    print()
    generate_theme_gallery()
    print()
    print("=" * 80)
    print("✨ Gallery generation complete!")
    print()

if __name__ == '__main__':
    main()
