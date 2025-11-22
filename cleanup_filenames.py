#!/usr/bin/env python3
"""
Clean up and standardize all image filenames to match folder names.
This fixes git sync issues caused by excessively long filenames.
"""

from pathlib import Path
import re

def clean_game_folder(game_folder: Path) -> dict:
    """Rename images in a game folder to match the folder name."""

    result = {
        'folder': game_folder.name,
        'renamed': [],
        'errors': []
    }

    # Get folder name (this is the clean game name)
    folder_name = game_folder.name

    # Find the index.html
    html_file = game_folder / 'index.html'
    if not html_file.exists():
        result['errors'].append(f"No index.html found")
        return result

    # Find image/PDF files
    image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif', '.pdf']

    for file in game_folder.iterdir():
        if file.is_file() and file.suffix.lower() in image_extensions:
            old_name = file.name

            # Skip if already properly named
            if file.stem == folder_name:
                continue

            # New name: folder_name + original extension
            new_name = f"{folder_name}{file.suffix.lower()}"
            new_path = game_folder / new_name

            # Check if target already exists
            if new_path.exists() and new_path != file:
                # If it's different, need to handle collision
                counter = 1
                while new_path.exists():
                    new_name = f"{folder_name}_{counter}{file.suffix.lower()}"
                    new_path = game_folder / new_name
                    counter += 1

            try:
                # Rename the file
                file.rename(new_path)

                # Update HTML references
                if html_file.exists():
                    html_content = html_file.read_text(encoding='utf-8', errors='ignore')

                    # Replace old filename with new filename
                    html_content = html_content.replace(old_name, new_name)

                    # Write back
                    html_file.write_text(html_content, encoding='utf-8')

                result['renamed'].append(f"{old_name} → {new_name}")

            except Exception as e:
                result['errors'].append(f"Failed to rename {old_name}: {e}")

    return result

def main():
    """Clean up all game folders."""

    print("🧹 CLEANING UP IMAGE FILENAMES")
    print("=" * 80)
    print()
    print("This will:")
    print("  • Rename all images to match their folder names")
    print("  • Fix git sync issues from long filenames")
    print("  • Update HTML references automatically")
    print()
    print("=" * 80)
    print()

    base_dir = Path('extracted')

    total_renamed = 0
    total_errors = 0

    # Process each category
    for category_dir in sorted(base_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name in ['itch_io_packages', 'sonic']:
            continue

        print(f"\n📁 {category_dir.name.upper()}")
        print("-" * 80)

        # Process each game in category
        for game_dir in sorted(category_dir.iterdir()):
            if not game_dir.is_dir():
                continue

            result = clean_game_folder(game_dir)

            if result['renamed']:
                print(f"\n  🎮 {result['folder']}")
                for rename in result['renamed']:
                    print(f"     ✅ {rename}")
                total_renamed += len(result['renamed'])

            if result['errors']:
                print(f"\n  ⚠️  {result['folder']}")
                for error in result['errors']:
                    print(f"     ❌ {error}")
                total_errors += len(result['errors'])

    # Also process sonic category
    sonic_dir = base_dir / 'sonic'
    if sonic_dir.exists():
        print(f"\n📁 SONIC")
        print("-" * 80)

        for game_dir in sorted(sonic_dir.iterdir()):
            if not game_dir.is_dir():
                continue

            result = clean_game_folder(game_dir)

            if result['renamed']:
                print(f"\n  🎮 {result['folder']}")
                for rename in result['renamed']:
                    print(f"     ✅ {rename}")
                total_renamed += len(result['renamed'])

            if result['errors']:
                print(f"\n  ⚠️  {result['folder']}")
                for error in result['errors']:
                    print(f"     ❌ {error}")
                total_errors += len(result['errors'])

    print()
    print("=" * 80)
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"   Files renamed: {total_renamed}")
    print(f"   Errors: {total_errors}")
    print()
    print("All images now match their folder names - git-friendly! 🚀")

if __name__ == '__main__':
    main()
