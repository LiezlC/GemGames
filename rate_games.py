#!/usr/bin/env python3
"""
Automated Game Quality Analyzer & Rater
Scores and ranks games based on code quality, mechanics, and polish.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

def analyze_game_quality(html_path: Path) -> Dict:
    """Analyze a game's HTML to determine quality metrics."""

    try:
        content = html_path.read_text(encoding='utf-8')
    except:
        return {'error': 'Cannot read file', 'total_score': 0}

    # Extract title
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1) if title_match else "Untitled"

    scores = {
        'code_sophistication': 0,
        'gameplay_depth': 0,
        'visual_polish': 0,
        'interactivity': 0,
        'audio': 0,
        'completeness': 0
    }

    content_lower = content.lower()

    # 1. CODE SOPHISTICATION (0-25 points)
    sophistication_indicators = {
        'class ': 3,  # OOP usage
        'requestanimationframe': 5,  # Proper animation
        'canvas': 4,  # Canvas graphics
        'svg': 3,  # SVG graphics
        'setinterval': 2,  # Timing mechanics
        'settimeout': 2,
        'math.random': 2,  # Randomization
        'math.sin': 3,  # Mathematical animations
        'math.cos': 3,
        'localstorage': 4,  # Save state
        'array.from': 2,
        'map(': 2,
        'filter(': 2,
        'reduce(': 3,
    }

    for indicator, points in sophistication_indicators.items():
        if indicator in content_lower:
            scores['code_sophistication'] += points

    scores['code_sophistication'] = min(scores['code_sophistication'], 25)

    # 2. GAMEPLAY DEPTH (0-25 points)
    gameplay_features = {
        'score': 5,
        'highscore': 3,
        'level': 4,
        'lives': 3,
        'health': 3,
        'timer': 3,
        'countdown': 3,
        'difficulty': 4,
        'gameover': 4,
        'win': 3,
        'victory': 3,
        'defeat': 2,
        'power': 2,
        'upgrade': 3,
        'achievement': 4,
        'combo': 3,
        'multiplier': 3,
    }

    for feature, points in gameplay_features.items():
        if feature in content_lower:
            scores['gameplay_depth'] += points

    scores['gameplay_depth'] = min(scores['gameplay_depth'], 25)

    # 3. VISUAL POLISH (0-20 points)
    visual_features = {
        'gradient': 2,
        'box-shadow': 2,
        'text-shadow': 1,
        'transform': 3,
        'transition': 3,
        'animation': 4,
        '@keyframes': 4,
        'opacity': 2,
        'rgba': 2,
        'linear-gradient': 2,
        'radial-gradient': 3,
        'filter:': 3,
        'backdrop-filter': 4,
    }

    for feature, points in visual_features.items():
        if feature in content_lower:
            scores['visual_polish'] += points

    scores['visual_polish'] = min(scores['visual_polish'], 20)

    # 4. INTERACTIVITY (0-15 points)
    interaction_features = {
        'onclick': 2,
        'onmousemove': 3,
        'onmousedown': 2,
        'onmouseup': 2,
        'onkeydown': 3,
        'onkeyup': 2,
        'ontouchstart': 3,
        'ontouchmove': 3,
        'addeventlistener': 4,
        'drag': 3,
    }

    for feature, points in interaction_features.items():
        if feature in content_lower:
            scores['interactivity'] += points

    scores['interactivity'] = min(scores['interactivity'], 15)

    # 5. AUDIO (0-10 points)
    audio_features = {
        'audiocontext': 10,
        'createoscillator': 5,
        'new audio': 5,
        '<audio': 5,
        'playsound': 5,
    }

    for feature, points in audio_features.items():
        if feature in content_lower:
            scores['audio'] = max(scores['audio'], points)

    scores['audio'] = min(scores['audio'], 10)

    # 6. COMPLETENESS (0-5 points)
    completeness_features = {
        'instructions': 2,
        'how to play': 2,
        'controls': 2,
        'start': 1,
        'restart': 1,
        'reset': 1,
    }

    for feature, points in completeness_features.items():
        if feature in content_lower:
            scores['completeness'] += points

    scores['completeness'] = min(scores['completeness'], 5)

    # Calculate total (max 100)
    total = sum(scores.values())

    # Bonus points for exceptional length/complexity
    lines = len(content.split('\n'))
    if lines > 500:
        total += 5
    if lines > 1000:
        total += 5

    scores['total_score'] = min(total, 100)
    scores['title'] = title
    scores['lines_of_code'] = lines

    # Determine quality tier
    if total >= 70:
        scores['tier'] = 'Excellent'
    elif total >= 50:
        scores['tier'] = 'Good'
    elif total >= 30:
        scores['tier'] = 'Fair'
    else:
        scores['tier'] = 'Basic'

    # Identify standout features
    standout = []
    if scores['audio'] >= 8:
        standout.append('🔊 Audio')
    if scores['gameplay_depth'] >= 15:
        standout.append('🎮 Deep Gameplay')
    if scores['visual_polish'] >= 15:
        standout.append('✨ Polished Visuals')
    if scores['code_sophistication'] >= 18:
        standout.append('🧠 Sophisticated Code')
    if scores['interactivity'] >= 10:
        standout.append('🎯 Highly Interactive')

    scores['standout_features'] = standout

    return scores

def rate_all_games(extracted_dir: Path) -> List[Dict]:
    """Rate all games in the collection."""

    games = []

    # Scan all game directories
    for category_dir in extracted_dir.iterdir():
        if category_dir.is_dir():
            for game_dir in category_dir.iterdir():
                if game_dir.is_dir():
                    html_file = game_dir / 'index.html'
                    if html_file.exists():
                        scores = analyze_game_quality(html_file)
                        scores['category'] = category_dir.name
                        scores['folder'] = game_dir.name
                        scores['path'] = str(game_dir.relative_to(extracted_dir))
                        games.append(scores)

    # Sort by total score
    games.sort(key=lambda x: x.get('total_score', 0), reverse=True)

    return games

def generate_report(games: List[Dict], output_file: Path):
    """Generate a detailed quality report."""

    report = []

    report.append("=" * 80)
    report.append("🎮 GEMINI GAMES QUALITY REPORT")
    report.append("=" * 80)
    report.append("")

    # Overall stats
    total_games = len(games)
    excellent = sum(1 for g in games if g.get('tier') == 'Excellent')
    good = sum(1 for g in games if g.get('tier') == 'Good')
    fair = sum(1 for g in games if g.get('tier') == 'Fair')
    basic = sum(1 for g in games if g.get('tier') == 'Basic')

    avg_score = sum(g.get('total_score', 0) for g in games) / total_games if total_games > 0 else 0

    report.append("📊 OVERALL STATISTICS")
    report.append("-" * 80)
    report.append(f"Total Games Analyzed: {total_games}")
    report.append(f"Average Quality Score: {avg_score:.1f}/100")
    report.append("")
    report.append("Quality Distribution:")
    report.append(f"  ⭐⭐⭐ Excellent (70+): {excellent:3d} games")
    report.append(f"  ⭐⭐  Good (50-69):    {good:3d} games")
    report.append(f"  ⭐    Fair (30-49):    {fair:3d} games")
    report.append(f"  ○     Basic (<30):    {basic:3d} games")
    report.append("")

    # Top 20 Games
    report.append("")
    report.append("=" * 80)
    report.append("🏆 TOP 20 GAMES - RECOMMENDED FOR SHARING")
    report.append("=" * 80)
    report.append("")

    for i, game in enumerate(games[:20], 1):
        report.append(f"{i:2d}. {game['title'][:60]}")
        report.append(f"    Score: {game['total_score']}/100 | Tier: {game['tier']} | Category: {game['category']}")

        breakdown = f"    "
        breakdown += f"Code:{game['code_sophistication']:2d} "
        breakdown += f"Gameplay:{game['gameplay_depth']:2d} "
        breakdown += f"Visual:{game['visual_polish']:2d} "
        breakdown += f"Interactive:{game['interactivity']:2d} "
        if game['audio'] > 0:
            breakdown += f"Audio:{game['audio']:2d} "
        report.append(breakdown)

        if game['standout_features']:
            report.append(f"    Features: {' '.join(game['standout_features'])}")

        report.append(f"    Path: {game['path']}")
        report.append("")

    # Category breakdown
    report.append("")
    report.append("=" * 80)
    report.append("📁 QUALITY BY CATEGORY")
    report.append("=" * 80)
    report.append("")

    categories = {}
    for game in games:
        cat = game['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(game['total_score'])

    for cat in sorted(categories.keys()):
        scores = categories[cat]
        avg = sum(scores) / len(scores)
        best = max(scores)
        report.append(f"{cat.upper():<15} Avg: {avg:5.1f} | Best: {best:3d} | Games: {len(scores):3d}")

    # Bottom 10 (might need improvement or not worth sharing)
    report.append("")
    report.append("=" * 80)
    report.append("⚠️  BOTTOM 10 - LOWER PRIORITY FOR SHARING")
    report.append("=" * 80)
    report.append("")

    for i, game in enumerate(games[-10:][::-1], 1):
        report.append(f"{i:2d}. {game['title'][:60]}")
        report.append(f"    Score: {game['total_score']}/100 | {game['category']}/{game['folder'][:40]}")
        report.append("")

    # Export recommendations
    report.append("")
    report.append("=" * 80)
    report.append("💡 SHARING RECOMMENDATIONS")
    report.append("=" * 80)
    report.append("")
    report.append("Based on quality analysis, here's what to share:")
    report.append("")
    report.append(f"✅ DEFINITELY SHARE: Top {excellent} excellent games (70+ score)")
    report.append(f"   These have sophisticated mechanics, polish, and engagement")
    report.append("")
    report.append(f"🤔 CONSIDER: Next {good} good games (50-69 score)")
    report.append(f"   Solid games that work well, less complex but enjoyable")
    report.append("")
    report.append(f"📦 OPTIONAL: {fair} fair games (30-49 score)")
    report.append(f"   Simpler experiences, include if you want variety")
    report.append("")
    report.append(f"⏭️  SKIP: {basic} basic games (<30 score)")
    report.append(f"   Very simple or minimal interactivity")
    report.append("")

    # Write to file
    report_text = "\n".join(report)
    output_file.write_text(report_text, encoding='utf-8')

    return report_text

def create_top_games_gallery(games: List[Dict], extracted_dir: Path, threshold: int = 70):
    """Create a curated gallery of only the best games."""

    top_games = [g for g in games if g.get('total_score', 0) >= threshold]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Top Gemini Games - Curated Collection</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1400px;
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
            font-size: 1.1em;
            color: #666;
            margin-bottom: 10px;
        }}

        .quality-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 10px;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }}

        .card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
            position: relative;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
            border-color: #667eea;
        }}

        .rank {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #667eea;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9em;
        }}

        .score {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }}

        .card-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
            margin-bottom: 12px;
            line-height: 1.3;
            min-height: 2.6em;
        }}

        .features {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 12px;
            min-height: 1.5em;
        }}

        .btn-play {{
            display: block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .btn-play:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 10px rgba(102, 126, 234, 0.4);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏆 Top Gemini Games</h1>
            <p class="subtitle">Curated Collection of {len(top_games)} Highest Quality Games</p>
            <div class="quality-badge">Score {threshold}+ / 100 - Excellent Tier</div>
        </header>

        <div class="grid">
"""

    for i, game in enumerate(top_games, 1):
        title = game['title'][:50]
        score = game['total_score']
        features = ' '.join(game['standout_features'][:3])
        path = game['path'] + '/index.html'

        html += f"""
            <div class="card">
                <div class="rank">#{i}</div>
                <div class="score">{score}/100</div>
                <div class="card-title">{title}</div>
                <div class="features">{features}</div>
                <a href="{path}" class="btn-play" target="_blank">▶ Play Game</a>
            </div>
"""

    html += """
        </div>
    </div>
</body>
</html>
"""

    output_file = extracted_dir / 'top_games.html'
    output_file.write_text(html, encoding='utf-8')

    return output_file

def main():
    """Main execution."""

    base_dir = Path(__file__).parent
    extracted_dir = base_dir / 'extracted'

    print("🎮 AUTOMATED GAME QUALITY ANALYZER")
    print("=" * 80)
    print()

    # Rate all games
    print("🔍 Analyzing all games...")
    games = rate_all_games(extracted_dir)
    print(f"   Analyzed {len(games)} games")
    print()

    # Save detailed JSON
    json_file = base_dir / 'game_ratings.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(games, f, indent=2)
    print(f"💾 Saved detailed ratings: {json_file}")

    # Generate report
    print("📝 Generating quality report...")
    report_file = base_dir / 'QUALITY_REPORT.txt'
    report_text = generate_report(games, report_file)
    print(f"✅ Report saved: {report_file}")
    print()

    # Create curated gallery
    print("🏆 Creating curated 'Top Games' gallery...")
    gallery_file = create_top_games_gallery(games, extracted_dir, threshold=70)
    print(f"✨ Gallery created: {gallery_file}")
    print()

    # Preview top 10
    print("=" * 80)
    print("🌟 TOP 10 GAMES PREVIEW")
    print("=" * 80)
    print()

    for i, game in enumerate(games[:10], 1):
        score_bar = "█" * (game['total_score'] // 5) + "░" * (20 - game['total_score'] // 5)
        print(f"{i:2d}. [{score_bar}] {game['total_score']:3d}/100 - {game['title'][:55]}")
        if game['standout_features']:
            print(f"    {' '.join(game['standout_features'])}")

    print()
    print("=" * 80)
    print("✅ Analysis complete!")
    print()
    print(f"📖 Read full report: QUALITY_REPORT.txt")
    print(f"🎮 View top games: extracted/top_games.html")
    print(f"📊 See all ratings: game_ratings.json")

if __name__ == '__main__':
    main()
