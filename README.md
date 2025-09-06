# LaTeX Resume to PDF Converter

A simple and clean Python module to convert LaTeX resume files to PDF using pdflatex.

## Features

✅ **Simple**: Clean, straightforward code  
✅ **Fast**: Uses pdflatex for native LaTeX compilation  
✅ **Reliable**: Runs pdflatex twice to resolve references  
✅ **Error Handling**: Clear error messages and validation  
✅ **Cross-platform**: Works on Windows, macOS, and Linux  

## Requirements

- Python 3.6+
- pdflatex (from a LaTeX distribution like MiKTeX, TeX Live, or MacTeX)

## Quick Start

### Generate Your Resume
```bash
python generate_resume.py
```

### Use the Module Directly
```python
from latex_to_pdf import LaTeXToPDF

# Create renderer
renderer = LaTeXToPDF()

# Compile LaTeX file to PDF
pdf_path = renderer.compile_latex_file("path/to/resume.tex", "output_directory")
print(f"PDF generated: {pdf_path}")
```

### Compile from String
```python
from latex_to_pdf import render_resume

# Compile LaTeX content from string
latex_content = r"""
\documentclass{article}
\begin{document}
Hello World!
\end{document}
"""

pdf_path = renderer.compile_from_string(latex_content, "output.pdf")
```

## File Structure

```
tailor-resume-ai/
├── .venv/
│   └── tex_files/
│       └── main.tex              # Your LaTeX resume
├── latex_to_pdf.py               # Main converter module
├── generate_resume.py            # Simple script to generate resume
└── ajin_frank_justin_resume.pdf  # Generated PDF
```

## Module API

### `LaTeXToPDF` Class

#### Methods:

- `__init__()`: Initialize and check pdflatex availability
- `compile_latex_file(tex_file_path, output_dir=None)`: Compile .tex file to PDF
- `compile_from_string(latex_content, output_path)`: Compile LaTeX string to PDF

### Convenience Functions:

- `render_resume(tex_file_path, output_path=None)`: Simple function to render resume

## Error Handling

The module provides clear error messages for common issues:

- ❌ **pdflatex not found**: Install LaTeX distribution
- ❌ **File not found**: Check LaTeX file path
- ❌ **Compilation failed**: Check LaTeX syntax

## Installation Notes

### Windows (MiKTeX)
1. Download from https://miktex.org/
2. Install with default settings
3. MiKTeX will auto-install packages as needed

### macOS (MacTeX)
```bash
brew install --cask mactex
```

### Linux (TeX Live)
```bash
# Ubuntu/Debian
sudo apt-get install texlive-latex-extra texlive-fonts-recommended

# Fedora
sudo dnf install texlive-latex texlive-collection-latexextra
```

## Generated PDF

Your resume will be compiled with:
- Professional formatting
- Clickable hyperlinks
- ATS-friendly text
- Vector graphics for crisp printing

**Output**: `ajin_frank_justin_resume.pdf` (109,495 bytes)

---

**Created**: September 2025  
**Author**: Ajin Frank Justin  
**Purpose**: Simple LaTeX to PDF conversion for resumes
