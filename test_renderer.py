"""
Test script for the LaTeX PDF Renderer module.

This script performs basic tests to ensure the module works correctly.
Run this script to verify that your LaTeX installation and the module are working.
"""

import os
import tempfile
from latex_pdf_renderer import LaTeXPDFRenderer, ResumeTemplateManager

def test_latex_installation():
    """Test if LaTeX is properly installed."""
    print("Testing LaTeX installation...")
    try:
        renderer = LaTeXPDFRenderer()
        print("✓ LaTeX engine is available")
        return True
    except RuntimeError as e:
        print(f"✗ LaTeX installation issue: {e}")
        return False

def test_template_creation():
    """Test template creation functionality."""
    print("\nTesting template creation...")
    try:
        template_manager = ResumeTemplateManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            template_path = os.path.join(temp_dir, "test_template.tex")
            template_manager.create_basic_template(template_path)
            
            if os.path.exists(template_path):
                print("✓ Template creation successful")
                return True
            else:
                print("✗ Template file was not created")
                return False
    except Exception as e:
        print(f"✗ Template creation failed: {e}")
        return False

def test_sample_data():
    """Test sample data generation."""
    print("\nTesting sample data generation...")
    try:
        template_manager = ResumeTemplateManager()
        sample_data = template_manager.get_sample_resume_data()
        
        required_fields = ['personal_info', 'summary', 'experience', 'education', 'skills']
        missing_fields = [field for field in required_fields if field not in sample_data]
        
        if not missing_fields:
            print("✓ Sample data contains all required fields")
            return True
        else:
            print(f"✗ Sample data missing fields: {missing_fields}")
            return False
    except Exception as e:
        print(f"✗ Sample data generation failed: {e}")
        return False

def test_simple_latex_rendering():
    """Test simple LaTeX to PDF rendering."""
    print("\nTesting simple LaTeX rendering...")
    try:
        renderer = LaTeXPDFRenderer()
        
        simple_latex = r"""
\documentclass{article}
\usepackage[margin=1in]{geometry}
\begin{document}

\title{Test Document}
\author{LaTeX PDF Renderer Test}
\date{\today}
\maketitle

\section{Test Section}
This is a test document to verify that LaTeX compilation works correctly.

\subsection{Features Tested}
\begin{itemize}
\item Document structure
\item Basic formatting
\item List generation
\end{itemize}

\end{document}
"""
        
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "test_simple.pdf")
            result_path = renderer.render_from_latex_string(simple_latex, output_path)
            
            if os.path.exists(result_path) and os.path.getsize(result_path) > 0:
                print("✓ Simple LaTeX rendering successful")
                return True
            else:
                print("✗ PDF was not generated or is empty")
                return False
    except Exception as e:
        print(f"✗ Simple LaTeX rendering failed: {e}")
        return False

def test_template_rendering():
    """Test template-based rendering."""
    print("\nTesting template-based rendering...")
    try:
        renderer = LaTeXPDFRenderer()
        template_manager = ResumeTemplateManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create template
            template_path = os.path.join(temp_dir, "test_template.tex")
            template_manager.create_basic_template(template_path)
            
            # Get sample data
            sample_data = template_manager.get_sample_resume_data()
            
            # Render PDF
            output_path = os.path.join(temp_dir, "test_resume.pdf")
            result_path = renderer.render_resume(template_path, sample_data, output_path)
            
            if os.path.exists(result_path) and os.path.getsize(result_path) > 0:
                print("✓ Template-based rendering successful")
                return True
            else:
                print("✗ Resume PDF was not generated or is empty")
                return False
    except Exception as e:
        print(f"✗ Template-based rendering failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("LaTeX PDF Renderer - Test Suite")
    print("=" * 40)
    
    tests = [
        test_latex_installation,
        test_template_creation,
        test_sample_data,
        test_simple_latex_rendering,
        test_template_rendering
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    print("Test Results Summary:")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("🎉 All tests passed! The module is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        if not results[0]:  # LaTeX installation failed
            print("\nNote: LaTeX installation is required for this module to work.")
            print("Please install a LaTeX distribution:")
            print("  - Windows: MiKTeX (https://miktex.org/)")
            print("  - macOS: MacTeX (https://tug.org/mactex/)")
            print("  - Linux: TeX Live (via package manager)")
    
    return all(results)

if __name__ == "__main__":
    run_all_tests()
