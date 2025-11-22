#!/usr/bin/env python3
"""
Organize games by thematic content categories.
Creates symbolic links in content/ folder while preserving gameplay categories.
"""

from pathlib import Path
import os
import json

# Thematic categories based on user request
THEMES = {
    'Blurring_Boundaries': {
        'keywords': ['ai', 'neural', 'synth_mind', 'ainther', 'agi', 'singularity',
                    'algorithm', 'synthetic', 'consciousness', 'convergence', 'interface',
                    'cyber-organic', 'symbiosis', 'human-ai', 'resonance', 'authentic human',
                    'bio-acoustic', 'cyber-shepherd', 'eco-link', 'hybrid', 'fusion',
                    'voice ai impact', 'neural sync', 'neural void', 'neural nexus'],
        'description': 'AI-human convergence, AI consciousness, blurring lines between human and machine'
    },
    'Cosmo_Spacer': {
        'keywords': ['cosmic', 'void', 'event horizon', 'galactic', 'nebula', 'astral',
                    'celestial', 'orbital', 'hyperspace', 'infinity engine', 'quantum',
                    'space', 'stellar', 'universe'],
        'description': 'Space exploration, cosmic mysteries, and astronomical themes'
    },
    'Dragons': {
        'keywords': ['dragon', 'serpent', 'wyvern', 'drake', 'wyrm'],
        'description': 'Games featuring dragons, serpents, and mythical creatures'
    },
    'Farmy_Fun': {
        'keywords': ['farm', 'pastoral', 'homestead', 'agriculture', 'ranch', 'bitsoil',
                    'harvest', 'crop', 'eco-retreat', 'synth-farm', 'agri-tech'],
        'description': 'Farming simulators, pastoral themes, and agricultural games'
    },
    'Mystic_Rituals': {
        'keywords': ['oracle', 'mystic', 'ritual', 'vigil', 'altar', 'shrine', 'temple',
                    'doorway', 'sanctuary', 'ethereal', 'spiritual', 'sacred'],
        'description': 'Mystical experiences, rituals, and spiritual journeys'
    },
    'Neon_Cyber': {
        'keywords': ['neon', 'cyber', 'synth', 'chromatic', 'grid', 'circuit',
                    'digital', 'data', 'protocol', 'sector', 'tactical'],
        'description': 'Cyberpunk aesthetics, neon-soaked environments, digital worlds'
    },
    'Nature_Harmony': {
        'keywords': ['eco-', 'nature', 'plant', 'lumina', 'grove', 'bio', 'organic',
                    'wildlife', 'wilderness', 'garden', 'forest', 'valley', 'river',
                    'wisdom in the wild', 'dreamscape forager'],
        'description': 'Natural environments, ecology, and environmental themes'
    },
    'HouseSim': {
        'keywords': ['house', 'home', 'interior', 'architect', 'builder', 'estate',
                    'veranda', 'village', 'habitat', 'bistro', 'apartment', 'dwelling'],
        'description': 'Home design, architecture, and interior simulation games'
    },
    'Light_Patterns': {
        'keywords': ['memory', 'sync', 'pattern', 'sequence', 'repeat', 'match',
                    'lumina light memory', 'neural sync', 'flicker', 'sequence'],
        'description': 'Memory games with flickering light patterns that must be repeated'
    },
    'Paint_Splash': {
        'keywords': ['splash', 'kinetic', 'abstractify', 'canvas', 'chromatic dialogue'],
        'description': 'Interactive paint splashing - click to splash paint on canvas, colors flow and merge'
    },
    'Us_vs_Them': {
        'keywords': ['battle', 'war', 'combat', 'versus', 'conflict', 'defense',
                    'guardian', 'protector', 'invasion', 'attack', 'roast battle'],
        'description': 'Competitive games, conflicts, and adversarial challenges'
    },
    'UX_Landings': {
        'keywords': ['interface', 'dashboard', 'control', 'ui', 'ux', 'menu',
                    'landing', 'portal', 'console', 'simulator', 'chronicles'],
        'description': 'UI/UX focused games with interactive interfaces and dashboards'
    },
    'Zazen': {
        'keywords': ['zen', 'candle', 'vigil', 'keeper of the flame', 'altar', 'ritual',
                    'enlightenment', 'ascension', 'meditation', 'contemplat'],
        'description': 'Ritual activities - lighting candles, moving objects to attain enlightenment'
    },
    'Hyper_Drive': {
        'keywords': ['void drifter', 'hyperspace', 'journey', 'drift', 'neon rain zen walk',
                    'infrared journey', 'neural void voyager', 'rift walker', 'tunnel',
                    'perspective', 'moving', 'voyage'],
        'description': 'First-person motion through space or tunnels - feeling of being inside a moving vehicle'
    }
}

def get_game_themes(game_name: str, game_path: Path) -> list:
    """Determine which thematic categories a game belongs to."""
    themes = []
    game_name_lower = game_name.lower().replace('_', ' ').replace('-', ' ')

    # Check HTML content for additional context
    html_file = game_path / 'index.html'
    html_content = ""
    if html_file.exists():
        try:
            html_content = html_file.read_text(encoding='utf-8', errors='ignore').lower()
        except:
            pass

    for theme, data in THEMES.items():
        for keyword in data['keywords']:
            keyword_lower = keyword.lower()
            # Check game name
            if keyword_lower in game_name_lower:
                if theme not in themes:
                    themes.append(theme)
                break
            # Check HTML content for strong matches
            elif keyword_lower in html_content[:3000]:  # Check first part of HTML
                # Only add if it's a significant match
                if html_content[:3000].count(keyword_lower) >= 2:
                    if theme not in themes:
                        themes.append(theme)
                    break

    return themes

def create_theme_structure():
    """Create the content folder with thematic categories."""
    content_dir = Path('content')
    content_dir.mkdir(exist_ok=True)

    for theme, data in THEMES.items():
        theme_dir = content_dir / theme
        theme_dir.mkdir(exist_ok=True)

        # Create a README in each theme folder
        readme = theme_dir / 'README.md'
        readme.write_text(f"# {theme.replace('_', ' ')}\n\n{data['description']}\n")

    return content_dir

def main():
    """Categorize all games by theme."""

    print("🎨 THEMATIC CATEGORIZATION")
    print("=" * 80)
    print()
    print("Creating content structure with themes:")
    for theme, data in THEMES.items():
        print(f"  📁 {theme.replace('_', ' ')}: {data['description']}")
    print()
    print("=" * 80)
    print()

    # Create content structure
    content_dir = create_theme_structure()

    # Track categorization
    theme_stats = {theme: [] for theme in THEMES.keys()}
    uncategorized = []

    # Process all games
    extracted_dir = Path('extracted')

    for category_dir in sorted(extracted_dir.iterdir()):
        if not category_dir.is_dir():
            continue

        print(f"\n📁 Processing {category_dir.name.upper()} games...")

        for game_dir in sorted(category_dir.iterdir()):
            if not game_dir.is_dir():
                continue

            game_name = game_dir.name

            # Determine themes for this game
            themes = get_game_themes(game_name, game_dir)

            if themes:
                print(f"  🎮 {game_name}")
                for theme in themes:
                    print(f"     → {theme.replace('_', ' ')}")

                    # Create symbolic link
                    link_path = content_dir / theme / game_name
                    target_path = Path('..') / '..' / game_dir.relative_to(Path('.'))

                    # Remove existing link if present
                    if link_path.exists() or link_path.is_symlink():
                        link_path.unlink()

                    # Create symlink
                    try:
                        link_path.symlink_to(target_path)
                        theme_stats[theme].append(game_name)
                    except Exception as e:
                        print(f"     ⚠️  Could not create link: {e}")
            else:
                uncategorized.append(game_name)

    # Summary
    print()
    print("=" * 80)
    print("\n📊 THEMATIC CATEGORIZATION SUMMARY\n")

    total_categorized = 0
    for theme, games in sorted(theme_stats.items()):
        if games:
            print(f"  {theme.replace('_', ' ')}: {len(games)} games")
            total_categorized += len(games)

    print(f"\n  Total categorized: {total_categorized} game entries")
    print(f"  Uncategorized: {len(uncategorized)} games")

    if uncategorized and len(uncategorized) <= 20:
        print("\n  Uncategorized games:")
        for game in uncategorized[:20]:
            print(f"    • {game}")

    print()
    print("=" * 80)
    print("\n✅ Thematic categorization complete!")
    print(f"\n   Games organized in: content/")
    print(f"   Original categories preserved in: extracted/")
    print()
    print("   Both organizational systems now available:")
    print("   • By gameplay type: extracted/[action|puzzle|simulation|etc]/")
    print("   • By theme: content/[AI-Aware|Dragons|Cosmo_Spacer|etc]/")
    print()

    # Save categorization metadata
    metadata = {
        'themes': theme_stats,
        'uncategorized': uncategorized,
        'total_games': sum(len(games) for games in theme_stats.values()),
        'themes_used': len([t for t in theme_stats.values() if t])
    }

    with open('theme_categorization.json', 'w') as f:
        json.dump(metadata, f, indent=2)

    print("   Metadata saved to: theme_categorization.json")

if __name__ == '__main__':
    main()
