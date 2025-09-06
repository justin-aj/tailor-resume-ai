"""
Generate Ajin's Resume PDF

Simple script to convert the LaTeX resume to PDF using pdflatex.
"""

from latex_to_pdf import LaTeXToPDF
import os


def main():
    """Generate the resume PDF."""
    print("🎯 Generating Ajin Frank Justin's Resume")
    print("=" * 45)
    
    # Paths
    tex_file = r"tex_files\main.tex"
    output_pdf = "ajin_frank_justin_resume.pdf"
    
    try:
        # Create the PDF renderer
        renderer = LaTeXToPDF()
        
        # Compile the resume
        pdf_path = renderer.compile_latex_file(tex_file, ".")
        
        # Rename to a better filename
        if os.path.exists(pdf_path) and pdf_path != output_pdf:
            if os.path.exists(output_pdf):
                os.remove(output_pdf)  # Remove existing file first
            os.rename(pdf_path, output_pdf)
            pdf_path = output_pdf
        
        # Show results
        file_size = os.path.getsize(pdf_path)
        print("=" * 45)
        print(f"✅ Resume Generated Successfully!")
        print(f"📄 File: {pdf_path}")
        print(f"📊 Size: {file_size:,} bytes")
        print(f"🎯 Ready for job applications!")
        
        return pdf_path
        
    except Exception as e:
        print(f"❌ Error generating resume: {e}")
        return None


if __name__ == "__main__":
    main()
