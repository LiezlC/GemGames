#!/usr/bin/env python3
"""
Extract HTML and images from Gemini artifact JSON files.
Looks for JSON files in the CURRENT directory.
"""

import json
import os
import base64
import re
from pathlib import Path
from typing import Dict, List, Tuple

def clean_filename(name: str) -> str:
    """Clean filename to be filesystem-safe."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"|?*]', '_', name)
    # Remove leading/trailing spaces and dots
    name = name.strip('. ')
    # Limit length
    if len(name) > 200:
        name = name[:200]
    return name

def extract_image_data(data_uri: str) -> Tuple[bytes, str]:
    """
    Extract image/PDF bytes and extension from data URI.

    Returns:
        Tuple of (file_bytes, file_extension)
    """
    if not data_uri or not data_uri.startswith('data:'):
        raise ValueError("Invalid data URI format")

    # Parse the data URI: data:image/jpeg;base64,<base64_data> or data:application/pdf;base64,<base64_data>
    # Try image format first
    match = re.match(r'data:image/(\w+(?:\+\w+)?);base64,(.+)', data_uri)
    if match:
        file_format = match.group(1).lower()
        base64_data = match.group(2)

        # Map format to file extension
        ext_map = {
            'jpeg': 'jpg',
            'jpg': 'jpg',
            'png': 'png',
            'webp': 'webp',
            'gif': 'gif',
            'svg+xml': 'svg'
        }
        extension = ext_map.get(file_format, file_format)
    else:
        # Try PDF or other application formats
        match = re.match(r'data:application/(\w+);base64,(.+)', data_uri)
        if match:
            file_format = match.group(1).lower()
            base64_data = match.group(2)
            extension = file_format  # pdf, etc.
        else:
            raise ValueError(f"Could not parse data URI format")

    # Decode base64 data
    try:
        file_bytes = base64.b64decode(base64_data)
    except Exception as e:
        raise ValueError(f"Failed to decode base64 data: {e}")

    return file_bytes, extension

def process_json_file(json_path: Path, output_dir: Path) -> Dict:
    """
    Process a single JSON artifact file.

    Returns:
        Dict with processing results
    """
    result = {
        'json_file': json_path.name,
        'success': False,
        'error': None,
        'image_saved': False,
        'html_saved': False,
        'project_name': None
    }

    try:
        # Read JSON file
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Extract fields
        artifact_id = data.get('id', '')
        original_name = data.get('name', '')
        html_content = data.get('html', '')
        image_data_uri = data.get('originalImage', '')

        # Use the original name (without extension) as the project name
        if original_name:
            project_name = Path(original_name).stem
        else:
            # Fallback to JSON filename
            project_name = json_path.stem.replace('_artifact', '')

        project_name = clean_filename(project_name)
        result['project_name'] = project_name

        # Create project directory
        project_dir = output_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # Save HTML file
        if html_content:
            html_path = project_dir / 'index.html'
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            result['html_saved'] = True

        # Save original file (image or PDF)
        if image_data_uri:
            try:
                file_bytes, extension = extract_image_data(image_data_uri)
                file_path = project_dir / f'{project_name}.{extension}'

                with open(file_path, 'wb') as f:
                    f.write(file_bytes)

                result['image_saved'] = True
            except Exception as e:
                result['error'] = f"File extraction failed: {e}"
                print(f"  ⚠️  Failed to extract file: {e}")
        else:
            result['error'] = "No file data found in JSON"

        result['success'] = result['html_saved'] or result['image_saved']

    except json.JSONDecodeError as e:
        result['error'] = f"Invalid JSON: {e}"
    except Exception as e:
        result['error'] = f"Processing error: {e}"

    return result

def main():
    """Main extraction process."""
    # Look for JSON files in CURRENT directory (where the script is run from)
    current_dir = Path.cwd()
    output_dir = current_dir / 'extracted'

    print(f"🔍 Scanning for JSON files in: {current_dir}")
    print(f"📁 Output directory: {output_dir}\n")

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Get all JSON files in current directory
    json_files = sorted(current_dir.glob('*.json'))

    if not json_files:
        print("❌ No JSON files found in current directory!")
        print("\nMake sure you're running this script from the folder")
        print("that contains your JSON files, OR put the JSON files")
        print("in a 'jsons/' subfolder.\n")
        return

    print(f"Found {len(json_files)} JSON files\n")
    print("=" * 60)

    # Process each file
    results = []
    successful = 0
    failed = 0
    missing_images = 0

    for i, json_file in enumerate(json_files, 1):
        print(f"\n[{i}/{len(json_files)}] Processing: {json_file.name[:50]}...")

        result = process_json_file(json_file, output_dir)
        results.append(result)

        if result['success']:
            successful += 1
            status_parts = []
            if result['html_saved']:
                status_parts.append("✅ HTML")
            if result['image_saved']:
                status_parts.append("✅ Image")
            else:
                missing_images += 1
                status_parts.append("⚠️  No image")

            print(f"  {' | '.join(status_parts)}")
            print(f"  📂 Saved to: extracted/{result['project_name']}/")
        else:
            failed += 1
            print(f"  ❌ Failed: {result['error']}")

    # Summary
    print("\n" + "=" * 60)
    print("\n📊 EXTRACTION SUMMARY")
    print(f"  Total files processed: {len(json_files)}")
    print(f"  ✅ Successful: {successful}")
    print(f"  ❌ Failed: {failed}")
    print(f"  ⚠️  Missing images: {missing_images}")

    # List projects with missing images
    if missing_images > 0:
        print(f"\n⚠️  Projects with missing images:")
        for result in results:
            if result['success'] and not result['image_saved']:
                print(f"    - {result['project_name']}")

    # List failed extractions
    if failed > 0:
        print(f"\n❌ Failed extractions:")
        for result in results:
            if not result['success']:
                print(f"    - {result['json_file']}: {result['error']}")

    print("\n✨ Extraction complete!")
    print(f"\n👉 Open: {output_dir}\\index.html to view your games!")

if __name__ == '__main__':
    main()
