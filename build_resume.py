"""
Resume Builder - Simple file combiner for LaTeX sections

This script combines individual LaTeX files into main.tex
"""

import os
from pathlib import Path
import datetime


def combine_tex_files(tex_dir="tex_files"):
    """
    Simply combine all .tex files (except main.tex) into main.tex
    
    Args:
        tex_dir (str): Directory containing the .tex files
    """
    tex_path = Path(tex_dir)
    main_file = tex_path / "main.tex"
    
    # List of files to combine in order
    files_to_combine = [
        "head.tex",
        "heading.tex", 
        "education.tex",
        "programming.tex",
        "experience.tex",
        "projects.tex"
    ]
    
    print(f"🔧 Combining LaTeX files in {tex_dir}/")
    
    # Create backups directory if it doesn't exist
    backup_dir = tex_path / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    # Backup existing main.tex if it exists
    if main_file.exists():
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"main_backup_{timestamp}.tex"
        
        # Copy instead of rename to keep original for now
        import shutil
        shutil.copy2(main_file, backup_file)
        print(f"📋 Backed up existing main.tex to backups/{backup_file.name}")
    
    # Combine files
    combined_content = []
    
    for filename in files_to_combine:
        file_path = tex_path / filename
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                combined_content.append(content)
                print(f"✅ Added {filename}")
        else:
            print(f"⚠️  Skipped {filename} (not found)")
    
    # Add document end
    combined_content.append("\n%\n\\end{document}")
    
    # Write to main.tex
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(combined_content))
    
    file_size = main_file.stat().st_size
    print(f"✅ Created main.tex ({file_size} bytes)")
    
    return str(main_file)


if __name__ == "__main__":
    try:
        result = combine_tex_files()
        print(f"🎉 Success! Combined files into: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
