"""
Simple LaTeX to PDF Renderer using pdflatex

This module provides a clean and straightforward way to compile LaTeX files to PDF
using the pdflatex command-line tool.
"""

import os
import subprocess
import shutil
import tempfile
from pathlib import Path
from typing import Optional


class LaTeXToPDF:
    """Simple LaTeX to PDF converter using pdflatex."""
    
    def __init__(self):
        """Initialize the converter and check if pdflatex is available."""
        self.check_pdflatex()
    
    def check_pdflatex(self) -> None:
        """Check if pdflatex is installed and accessible."""
        try:
            result = subprocess.run(
                ["pdflatex", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError("pdflatex is not working properly")
            print("✅ pdflatex is available and ready to use")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            raise RuntimeError(
                "❌ pdflatex not found. Please install a LaTeX distribution like:\n"
                "- MiKTeX (Windows): https://miktex.org/\n"
                "- TeX Live (Cross-platform): https://www.tug.org/texlive/\n"
                "- MacTeX (macOS): https://www.tug.org/mactex/"
            )
    
    def compile_latex_file(self, tex_file_path: str, output_dir: Optional[str] = None) -> str:
        """
        Compile a LaTeX file to PDF.
        
        Args:
            tex_file_path (str): Path to the .tex file
            output_dir (str, optional): Directory to save the PDF. If None, saves in same dir as tex file
            
        Returns:
            str: Path to the generated PDF file
        """
        tex_path = Path(tex_file_path)
        
        if not tex_path.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_file_path}")
        
        # Determine output directory
        if output_dir is None:
            output_dir = tex_path.parent
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Copy the .tex file to temp directory
            temp_tex_file = temp_dir_path / tex_path.name
            shutil.copy2(tex_path, temp_tex_file)
            
            print(f"📄 Compiling {tex_path.name}...")
            
            # Run pdflatex compilation (run twice for references)
            for run_number in [1, 2]:
                print(f"🔄 pdflatex run {run_number}/2...")
                
                result = subprocess.run([
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory", str(temp_dir_path),
                    str(temp_tex_file)
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode != 0:
                    print(f"❌ pdflatex failed on run {run_number}")
                    print("STDOUT:", result.stdout)
                    print("STDERR:", result.stderr)
                    if run_number == 2:  # Only fail on the final run
                        raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")
                else:
                    print(f"✅ pdflatex run {run_number} completed successfully")
            
            # Check if PDF was generated
            pdf_filename = tex_path.stem + ".pdf"
            temp_pdf_path = temp_dir_path / pdf_filename
            
            if not temp_pdf_path.exists():
                raise RuntimeError(f"PDF was not generated: {temp_pdf_path}")
            
            # Move PDF to output directory
            final_pdf_path = output_dir / pdf_filename
            shutil.copy2(temp_pdf_path, final_pdf_path)
            
            print(f"🎉 PDF generated successfully: {final_pdf_path}")
            return str(final_pdf_path)
    
    def compile_from_string(self, latex_content: str, output_path: str) -> str:
        """
        Compile LaTeX content from a string to PDF.
        
        Args:
            latex_content (str): LaTeX document content
            output_path (str): Path where the PDF should be saved
            
        Returns:
            str: Path to the generated PDF file
        """
        output_path = Path(output_path)
        output_dir = output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create temporary .tex file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False) as temp_file:
            temp_file.write(latex_content)
            temp_tex_path = temp_file.name
        
        try:
            # Compile the temporary file
            temp_pdf_path = self.compile_latex_file(temp_tex_path, output_dir)
            
            # Rename to desired output path
            final_path = str(output_path)
            shutil.move(temp_pdf_path, final_path)
            
            return final_path
        finally:
            # Clean up temporary file
            os.unlink(temp_tex_path)


def render_resume(tex_file_path: str, output_path: Optional[str] = None) -> str:
    """
    Convenience function to render a resume from LaTeX file.
    
    Args:
        tex_file_path (str): Path to the LaTeX resume file
        output_path (str, optional): Path for the output PDF
        
    Returns:
        str: Path to the generated PDF
    """
    renderer = LaTeXToPDF()
    
    if output_path:
        # If specific output path is given, use compile_from_string method
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return renderer.compile_from_string(content, output_path)
    else:
        # Use direct file compilation
        return renderer.compile_latex_file(tex_file_path)


if __name__ == "__main__":
    # Example usage
    try:
        # Path to your resume
        resume_tex = r".venv\tex_files\main.tex"
        output_pdf = "ajin_resume.pdf"
        
        print("🚀 Starting LaTeX to PDF conversion...")
        print("=" * 50)
        
        # Create renderer
        renderer = LaTeXToPDF()
        
        # Compile the resume
        pdf_path = renderer.compile_latex_file(resume_tex, ".")
        
        print("=" * 50)
        print(f"✅ Success! Your resume is ready: {pdf_path}")
        
        # Show file size
        file_size = os.path.getsize(pdf_path)
        print(f"📊 File size: {file_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error: {e}")
