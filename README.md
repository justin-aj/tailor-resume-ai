# Tailor Resume AI

A professional LaTeX resume to PDF converter with clean, simple Python code. Convert your LaTeX resume to high-quality PDF using native pdflatex compilation.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![LaTeX](https://img.shields.io/badge/LaTeX-pdflatex-green.svg)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This project provides a simple, reliable way to convert LaTeX resume files to professional PDF documents. Built with clean Python code and native LaTeX compilation for the best possible output quality.

## ✨ Features

- 🚀 **Native LaTeX Compilation**: Uses pdflatex for authentic LaTeX rendering
- 🎨 **Professional Output**: High-quality PDFs with proper formatting
- 🔗 **Clickable Links**: Preserves hyperlinks in the final PDF
- 📱 **ATS-Friendly**: Machine-readable text for applicant tracking systems
- 🛠 **Simple API**: Clean, straightforward Python interface
- ⚡ **Fast Processing**: Efficient compilation with proper reference resolution
- 🔧 **Error Handling**: Clear error messages and validation
- 🌍 **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Requirements

- **Python**: 3.6 or higher
- **LaTeX Distribution**: One of the following:
  - Windows: [MiKTeX](https://miktex.org/)
  - macOS: [MacTeX](https://www.tug.org/mactex/)
  - Linux: [TeX Live](https://www.tug.org/texlive/)

## 🚀 Quick Start

### 1. Generate Resume (Simplest Way)
```bash
python generate_resume.py
```

### 2. Use as Python Module
```python
from latex_to_pdf import LaTeXToPDF

# Create renderer
renderer = LaTeXToPDF()

# Compile LaTeX file to PDF
pdf_path = renderer.compile_latex_file("tex_files/main.tex")
print(f"PDF generated: {pdf_path}")
```

### 3. Compile from String
```python
from latex_to_pdf import LaTeXToPDF

renderer = LaTeXToPDF()

latex_content = r"""
\documentclass{article}
\usepackage[margin=1in]{geometry}
\begin{document}
\title{My Resume}
\author{Your Name}
\maketitle
\section{Experience}
Your experience here...
\end{document}
"""

pdf_path = renderer.compile_from_string(latex_content, "my_resume.pdf")
```

## 📁 Project Structure

```
tailor-resume-ai/
├── 📁 .git/                     # Git repository
├── 📁 .venv/                    # Python virtual environment
├── 📁 tex_files/
│   └── 📄 main.tex              # Your LaTeX resume source
├── 📁 __pycache__/              # Python cache (ignored)
├── 📄 .gitignore                # Git ignore rules
├── 📄 latex_to_pdf.py           # 🔧 Main converter module
├── 📄 generate_resume.py        # 🎯 Simple resume generator script
├── 📄 README.md                 # 📖 This documentation
└── 📄 ajin_frank_justin_resume.pdf  # ✅ Generated PDF output
```

## 🔧 API Reference

### `LaTeXToPDF` Class

The main class for LaTeX to PDF conversion.

#### Constructor
```python
LaTeXToPDF()
```
- Initializes the converter
- Checks pdflatex availability
- Raises `RuntimeError` if pdflatex is not found

#### Methods

**`compile_latex_file(tex_file_path, output_dir=None)`**
- **Parameters**:
  - `tex_file_path` (str): Path to the .tex file
  - `output_dir` (str, optional): Directory to save PDF (defaults to same as .tex file)
- **Returns**: str - Path to generated PDF
- **Raises**: `FileNotFoundError`, `RuntimeError`

**`compile_from_string(latex_content, output_path)`**
- **Parameters**:
  - `latex_content` (str): LaTeX document content
  - `output_path` (str): Path where PDF should be saved
- **Returns**: str - Path to generated PDF
- **Raises**: `RuntimeError`

### Convenience Functions

**`render_resume(tex_file_path, output_path=None)`**
- Simple function to render a resume
- **Parameters**: Same as `compile_latex_file`
- **Returns**: str - Path to generated PDF

## 🛠 Installation & Setup

### 1. Install LaTeX Distribution

#### Windows (MiKTeX)
1. Download from [miktex.org](https://miktex.org/)
2. Run installer with default settings
3. MiKTeX will auto-install packages as needed

#### macOS (MacTeX)
```bash
# Using Homebrew
brew install --cask mactex

# Or download from: https://www.tug.org/mactex/
```

#### Linux (TeX Live)
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install texlive-latex-extra texlive-fonts-recommended

# Fedora/RHEL
sudo dnf install texlive-latex texlive-collection-latexextra

# Arch Linux
sudo pacman -S texlive-core texlive-latexextra
```

### 2. Verify Installation
```bash
pdflatex --version
```

### 3. Clone and Run
```bash
git clone https://github.com/justin-aj/tailor-resume-ai.git
cd tailor-resume-ai
python generate_resume.py
```

## 📝 Resume Template

The project includes a professional LaTeX resume template (`tex_files/main.tex`) with:

- 📋 **Clean Layout**: Professional, ATS-friendly design
- 🔗 **Hyperlinks**: Clickable email, LinkedIn, GitHub links
- 📑 **Sections**: Education, Experience, Skills, Projects
- 🎨 **Formatting**: Custom commands for consistent styling
- 📱 **Mobile-Friendly**: Proper contact information layout

## 🔍 Error Handling

The module provides clear error messages for common issues:

| Error | Cause | Solution |
|-------|-------|----------|
| `pdflatex not found` | LaTeX not installed | Install MiKTeX, MacTeX, or TeX Live |
| `File not found` | Invalid .tex path | Check file path and permissions |
| `Compilation failed` | LaTeX syntax error | Review LaTeX syntax and packages |
| `PDF not generated` | Compilation incomplete | Check LaTeX log for missing packages |

## 📊 Output Quality

Generated PDFs include:

- ✅ **Professional Typography**: Native LaTeX font rendering
- ✅ **Vector Graphics**: Crisp text at any zoom level
- ✅ **Hyperlinks**: Clickable email and web links
- ✅ **ATS Compatibility**: Machine-readable text structure
- ✅ **Print Quality**: High-resolution output suitable for printing
- ✅ **Small File Size**: Optimized PDF compression

**Example Output**: `ajin_frank_justin_resume.pdf` (~110KB)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- LaTeX resume template based on [Jake Gutierrez's template](https://github.com/sb2nov/resume)
- Built with Python and native pdflatex compilation
- Inspired by the need for simple, reliable resume generation

## 📞 Support

If you encounter any issues:

1. Check that pdflatex is properly installed
2. Verify your LaTeX syntax is correct
3. Review the error messages for specific guidance
4. Open an issue on GitHub with error details

---

**Built with ❤️ by [Ajin Frank Justin](https://github.com/justin-aj)**  
**September 2025** | **Version 1.0**
