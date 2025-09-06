"""
Complete Resume Generator - Build and Compile

This script combines the build and compile process:
1. Builds main.tex from individual section files
2. Compiles main.tex to PDF using pdflatex

Usage: python complete_build.py
"""

from build_resume import combine_tex_files
from latex_to_pdf import LaTeXToPDF
import sys


def complete_resume_build():
    """Complete process: build main.tex from sections and compile to PDF."""
    
    print("🚀 Complete Resume Build Process")
    print("=" * 50)
    
    try:
        # Step 1: Build main.tex from individual sections
        print("📋 Step 1: Building main.tex from sections...")
        main_tex_path = combine_tex_files("tex_files")
        
        print("\n" + "=" * 50)
        print("📄 Step 2: Compiling LaTeX to PDF...")
        
        # Step 2: Compile to PDF
        renderer = LaTeXToPDF()
        pdf_path = renderer.compile_latex_file(main_tex_path, ".")
        
        # Rename to better filename
        import os
        final_pdf = "ajin_frank_justin_resume.pdf"
        if os.path.exists(pdf_path) and pdf_path != final_pdf:
            if os.path.exists(final_pdf):
                os.remove(final_pdf)
            os.rename(pdf_path, final_pdf)
            pdf_path = final_pdf
        
        # Show final results
        file_size = os.path.getsize(pdf_path)
        
        print("\n" + "=" * 50)
        print("🎉 COMPLETE SUCCESS!")
        print("=" * 50)
        print(f"📋 Built from sections: 6 files")
        print(f"📄 Generated PDF: {pdf_path}")
        print(f"📊 File size: {file_size:,} bytes")
        print(f"🎯 Status: Ready for job applications!")
        print("\n🔍 What was built:")
        
        sections = ["head.tex", "heading.tex", "education.tex", "programming.tex", "experience.tex", "projects.tex"]
        for i, section in enumerate(sections, 1):
            print(f"   {i}. {section}")
        
        return pdf_path
        
    except Exception as e:
        print(f"\n❌ Error during build process: {e}")
        return None


if __name__ == "__main__":
    result = complete_resume_build()
    
    if result:
        print(f"\n✅ Success! Your resume is ready: {result}")
        sys.exit(0)
    else:
        print("\n❌ Build failed. Check the error messages above.")
        sys.exit(1)
