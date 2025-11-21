#!/usr/bin/env python3
"""
Automated Game Organizer for Gemini Games Collection
Categorizes and renames game folders based on actual game titles.
"""

import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Category definitions with keywords
CATEGORIES = {
    'memory': {
        'keywords': ['memory', 'match', 'remember', 'recall', 'neural sync', 'pattern'],
        'description': 'Memory and pattern matching games'
    },
    'puzzle': {
        'keywords': ['puzzle', 'logic', 'builder', 'simulator', 'protocol', 'synthesis'],
        'description': 'Puzzle and logic games'
    },
    'action': {
        'keywords': ['dodge', 'jump', 'shoot', 'avoid', 'runner', 'battle', 'combat'],
        'description': 'Action and reflex games'
    },
    'rhythm': {
        'keywords': ['sync', 'beat', 'rhythm', 'tempo', 'music', 'harmony'],
        'description': 'Rhythm and timing games'
    },
    'adventure': {
        'keywords': ['explore', 'quest', 'journey', 'adventure', 'keeper', 'guardian', 'voyager'],
        'description': 'Adventure and exploration games'
    },
    'simulation': {
        'keywords': ['simulation', 'farm', 'tycoon', 'builder', 'os', 'system', 'garden'],
        'description': 'Simulation and management games'
    },
    'visual': {
        'keywords': ['visual', 'art', 'interactive art', 'experience', 'soundscape'],
        'description': 'Visual experiences and interactive art'
    },
    'arcade': {
        'keywords': ['score', 'highscore', 'arcade', 'classic', 'retro', 'neon'],
        'description': 'Arcade-style games'
    }
}

def clean_filename(name: str, max_length: int = 60) -> str:
    """Clean a string to be a valid, readable filename."""
    # Remove special characters
    name = re.sub(r'[<>:"|?*\\/]', '', name)
    # Replace problematic characters with underscores
    name = re.sub(r'[^\w\s\-\.]', '_', name)
    # Remove multiple spaces/underscores
    name = re.sub(r'[\s_]+', '_', name)
    # Remove leading/trailing underscores and dots
    name = name.strip('_. ')
    # Limit length
    if len(name) > max_length:
        name = name[:max_length].rstrip('_. ')
    return name

def extract_game_info(html_path: Path) -> Dict:
    """Extract game title and characteristics from HTML."""
    try:
        content = html_path.read_text(encoding='utf-8')

        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1).strip() if title_match else None

        # Extract h1 as fallback
        if not title:
            h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
            title = h1_match.group(1).strip() if h1_match else "Untitled Game"

        # Detect audio
        has_audio = bool(re.search(r'AudioContext|createOscillator', content))

        # Categorize based on content
        categories = categorize_game(title, content)

        return {
            'title': title,
            'has_audio': has_audio,
            'categories': categories,
            'content_length': len(content)
        }
    except Exception as e:
        return {
            'title': 'Untitled Game',
            'has_audio': False,
            'categories': ['visual'],
            'error': str(e)
        }

def categorize_game(title: str, content: str) -> List[str]:
    """Determine game categories based on title and content."""
    text = (title + ' ' + content[:5000]).lower()

    matches = []
    for category, info in CATEGORIES.items():
        score = sum(1 for keyword in info['keywords'] if keyword in text)
        if score > 0:
            matches.append((category, score))

    # Sort by score and return top categories
    matches.sort(key=lambda x: -x[1])

    if matches:
        # Return primary category and secondary if score is close
        categories = [matches[0][0]]
        if len(matches) > 1 and matches[1][1] >= matches[0][1] * 0.6:
            categories.append(matches[1][0])
        return categories

    return ['visual']

def scan_games(base_dir: Path) -> List[Dict]:
    """Scan all games and extract information."""
    games = []

    # Scan all directories (including sonic subdirectory)
    for item in base_dir.rglob('*'):
        if item.is_dir() and item.name != 'index.html':
            html_file = item / 'index.html'
            if html_file.exists():
                info = extract_game_info(html_file)
                info['current_path'] = item
                info['relative_path'] = item.relative_to(base_dir)
                games.append(info)

    return games

def propose_reorganization(games: List[Dict], base_dir: Path) -> Dict:
    """Propose how to reorganize games into categories."""
    plan = {
        'categories': {},
        'renames': [],
        'summary': {}
    }

    for game in games:
        # Determine primary category
        primary_category = game['categories'][0] if game['categories'] else 'visual'

        # Special case: audio games go in sonic
        if game['has_audio']:
            primary_category = 'sonic'

        # Create clean folder name from title
        clean_name = clean_filename(game['title'])

        # Proposed new path
        new_path = base_dir / primary_category / clean_name

        # Track if this is a rename/move
        if new_path != game['current_path']:
            plan['renames'].append({
                'old_path': game['current_path'],
                'new_path': new_path,
                'title': game['title'],
                'category': primary_category
            })

        # Add to category list
        if primary_category not in plan['categories']:
            plan['categories'][primary_category] = []

        plan['categories'][primary_category].append({
            'title': game['title'],
            'folder': clean_name,
            'has_audio': game['has_audio']
        })

    # Generate summary
    for category, games_list in plan['categories'].items():
        plan['summary'][category] = {
            'count': len(games_list),
            'description': CATEGORIES.get(category, {}).get('description', 'Special category')
        }

    return plan

def preview_plan(plan: Dict):
    """Show a preview of the reorganization plan."""
    print("\n" + "=" * 80)
    print("📋 REORGANIZATION PLAN")
    print("=" * 80)

    print("\n📊 CATEGORY SUMMARY:")
    print("-" * 80)
    for category, info in sorted(plan['summary'].items()):
        count = info['count']
        desc = info['description']
        print(f"  {category.upper():<15} : {count:3d} games - {desc}")

    print(f"\n📝 RENAMES/MOVES: {len(plan['renames'])} changes")
    print("-" * 80)

    # Show first 20 renames
    for i, change in enumerate(plan['renames'][:20], 1):
        old_name = change['old_path'].name[:40]
        new_name = change['new_path'].name[:40]
        category = change['category']
        print(f"\n{i:3d}. {change['title'][:60]}")
        print(f"     FROM: {old_name}")
        print(f"     TO:   {category}/{new_name}")

    if len(plan['renames']) > 20:
        print(f"\n     ... and {len(plan['renames']) - 20} more changes")

def execute_plan(plan: Dict, dry_run: bool = True):
    """Execute the reorganization plan."""
    if dry_run:
        print("\n⚠️  DRY RUN MODE - No actual changes will be made")
        return

    print("\n" + "=" * 80)
    print("🚀 EXECUTING REORGANIZATION")
    print("=" * 80)

    # Create category directories
    created_dirs = set()
    for change in plan['renames']:
        category_dir = change['new_path'].parent
        if category_dir not in created_dirs:
            category_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.add(category_dir)
            print(f"📁 Created: {category_dir.name}/")

    # Execute moves/renames
    successful = 0
    failed = []

    for i, change in enumerate(plan['renames'], 1):
        try:
            old_path = change['old_path']
            new_path = change['new_path']

            # Check if destination already exists
            if new_path.exists():
                # Add a number suffix
                counter = 2
                while new_path.exists():
                    new_name = f"{new_path.stem}_{counter}"
                    new_path = new_path.parent / new_name
                    counter += 1

            # Move/rename
            shutil.move(str(old_path), str(new_path))
            successful += 1

            if i % 10 == 0:
                print(f"  Processed {i}/{len(plan['renames'])}...")

        except Exception as e:
            failed.append((change['title'], str(e)))

    print(f"\n✅ Successfully reorganized: {successful} games")
    if failed:
        print(f"❌ Failed: {len(failed)} games")
        for title, error in failed[:5]:
            print(f"   - {title}: {error}")

def save_catalog(games: List[Dict], output_file: Path):
    """Save a catalog of all games."""
    catalog = []
    for game in games:
        catalog.append({
            'title': game['title'],
            'categories': game['categories'],
            'has_audio': game['has_audio'],
            'path': str(game['relative_path'])
        })

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Catalog saved to: {output_file}")

def main():
    """Main execution."""
    import sys

    base_dir = Path(__file__).parent / 'extracted'

    print("🎮 GEMINI GAMES ORGANIZER")
    print("=" * 80)

    # Scan all games
    print("\n🔍 Scanning games...")
    games = scan_games(base_dir)
    print(f"   Found {len(games)} games")

    # Propose reorganization
    print("\n🤔 Analyzing and categorizing...")
    plan = propose_reorganization(games, base_dir)

    # Preview the plan
    preview_plan(plan)

    # Save catalog
    catalog_file = base_dir.parent / 'games_catalog.json'
    save_catalog(games, catalog_file)

    # Ask for confirmation
    print("\n" + "=" * 80)
    if '--execute' in sys.argv or '-e' in sys.argv:
        execute_plan(plan, dry_run=False)
        print("\n✨ Reorganization complete!")
    else:
        print("ℹ️  This was a PREVIEW only. No changes were made.")
        print("   To execute the reorganization, run:")
        print("   python3 organize_games.py --execute")

if __name__ == '__main__':
    main()
