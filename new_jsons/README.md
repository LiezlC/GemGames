# 📥 Add New Games Here

Drop your new Gemini-generated JSON files in this folder, then I'll help you extract them!

---

## 🎯 How It Works

### 1. Add Your JSON Files
Put any new JSON artifact files from Gemini in this `new_jsons/` folder.

### 2. Run the Extraction
Copy `extract_here.py` into this folder, then run:
```bash
cd new_jsons
python extract_here.py
```

### 3. Get Your Games!
Your extracted games will appear in `new_jsons/extracted/`

---

## 📋 Quick Instructions for Desktop

### On Windows:
```cmd
C:\Users\Liezl\Desktop\GemGames\new_jsons> copy ..\extract_here.py .
C:\Users\Liezl\Desktop\GemGames\new_jsons> python extract_here.py
```

### What You'll Get:
```
new_jsons/
├── your_game_1.json
├── your_game_2.json
├── extract_here.py (copy from parent folder)
└── extracted/
    ├── Game_Name_1/
    │   ├── index.html
    │   └── Game_Name_1.png
    └── Game_Name_2/
        ├── index.html
        └── Game_Name_2.png
```

---

## 🔧 Alternative: Use the Original Script

If you want to keep the old structure:

1. Create a `jsons/` subfolder inside `new_jsons/`:
   ```
   new_jsons/
   └── jsons/
       ├── your_game_1.json
       └── your_game_2.json
   ```

2. Copy `extract_artifacts.py` to `new_jsons/`

3. Run:
   ```bash
   cd new_jsons
   python extract_artifacts.py
   ```

---

## 💡 Tips

- **File Names**: Gemini JSON files usually end with `_artifact.json`
- **Multiple Files**: You can drop dozens of JSON files at once!
- **Git**: Add the extracted games to git when you're happy with them
- **Organization**: Once extracted, you can move games to the main `content/` or `extracted/` folders

---

## ❓ Getting Errors?

Common issues:

1. **"No JSON files found"**
   - Make sure JSON files are directly in `new_jsons/` (not in a subfolder)
   - OR use `extract_artifacts.py` with a `jsons/` subfolder

2. **"Invalid JSON"**
   - Check the JSON file isn't corrupted
   - Make sure it has the right structure: `{id, name, html, originalImage}`

3. **"Missing images"**
   - Some JSON files don't include images - that's okay!
   - The HTML game will still be extracted

---

## 🚀 Next Steps After Extraction

Once you've extracted your new games:

1. **Test them**: Open the `index.html` files to make sure they work
2. **Organize**: Decide which category they belong to
3. **Share**: Let me know and I can help categorize them!

---

**Ready to add your new games? Just drop the JSON files here!** 🎮
