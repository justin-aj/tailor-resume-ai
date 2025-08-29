# LaTeX PDF Renderer for Resume Generation

A Python module that takes LaTeX resume data and renders professional PDF documents. This module is designed for the Tailor Resume AI project but can be used independently for any LaTeX to PDF conversion needs.

## Features

- **Template-based rendering**: Use Jinja2 templates with LaTeX
- **Direct LaTeX compilation**: Compile LaTeX strings directly to PDF
- **Multiple LaTeX engines**: Support for pdflatex, xelatex, and lualatex
- **Error handling**: Comprehensive error handling and logging
- **Sample templates**: Built-in basic resume template
- **Cross-platform**: Works on Windows, macOS, and Linux

## Prerequisites

### LaTeX Distribution Required

This module requires a LaTeX distribution to be installed on your system:

- **Windows**: [MiKTeX](https://miktex.org/) or [TeX Live](https://tug.org/texlive/)
- **macOS**: [MacTeX](https://tug.org/mactex/)
- **Linux**: TeX Live (usually available through package manager)

### Python Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install Jinja2 PyPDF2
```

## Quick Start

### Basic Usage

```python
from latex_pdf_renderer import LaTeXPDFRenderer, ResumeTemplateManager

# Create renderer
renderer = LaTeXPDFRenderer()

# Create template manager
template_manager = ResumeTemplateManager()

# Generate sample data
resume_data = template_manager.get_sample_resume_data()

# Create a basic template
template_manager.create_basic_template("templates/basic_resume.tex")

# Render PDF
pdf_path = renderer.render_resume(
    template_path="templates/basic_resume.tex",
    resume_data=resume_data,
    output_path="my_resume.pdf"
)

print(f"Resume generated: {pdf_path}")
```

### Direct LaTeX Rendering

```python
from latex_pdf_renderer import render_resume_from_latex

latex_content = r"""
\documentclass{article}
\begin{document}
\title{My Resume}
\author{John Doe}
\maketitle

\section{Experience}
Software Engineer at Tech Corp (2020-Present)

\end{document}
"""

pdf_path = render_resume_from_latex(latex_content, "resume.pdf")
```

## API Reference

### LaTeXPDFRenderer Class

The main class for handling LaTeX to PDF conversion.

#### Constructor

```python
LaTeXPDFRenderer(latex_engine="pdflatex", temp_dir=None)
```

**Parameters:**
- `latex_engine` (str): LaTeX engine to use ("pdflatex", "xelatex", "lualatex")
- `temp_dir` (str, optional): Custom temporary directory for compilation

#### Methods

##### `render_template(template_path, data)`

Render a Jinja2 LaTeX template with data.

**Parameters:**
- `template_path` (str): Path to the LaTeX template file
- `data` (dict): Data dictionary to populate the template

**Returns:** Rendered LaTeX content as string

##### `compile_latex_to_pdf(latex_content, output_path, cleanup=True)`

Compile LaTeX content to PDF.

**Parameters:**
- `latex_content` (str): LaTeX source content
- `output_path` (str): Path where PDF should be saved
- `cleanup` (bool): Whether to clean up temporary files

**Returns:** Path to generated PDF

##### `render_resume(template_path, resume_data, output_path)`

Complete workflow: render template and compile to PDF.

**Parameters:**
- `template_path` (str): Path to LaTeX template
- `resume_data` (dict): Resume data dictionary
- `output_path` (str): Output PDF path

**Returns:** Path to generated PDF

### ResumeTemplateManager Class

Helper class for managing templates and sample data.

#### Methods

##### `get_sample_resume_data()`

Returns a sample resume data structure that demonstrates the expected format.

##### `create_basic_template(template_path)`

Creates a basic LaTeX resume template at the specified path.

### Convenience Functions

#### `render_resume_from_template(template_path, resume_data, output_path, latex_engine="pdflatex")`

One-shot function to render a resume from a template.

#### `render_resume_from_latex(latex_content, output_path, latex_engine="pdflatex")`

One-shot function to render a PDF from LaTeX content.

## Resume Data Structure

The module expects resume data in the following format:

```python
{
    'personal_info': {
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '+1 (555) 123-4567',
        'address': '123 Main St, City, State 12345',
        'linkedin': 'linkedin.com/in/johndoe',
        'github': 'github.com/johndoe'
    },
    'summary': 'Professional summary text...',
    'experience': [
        {
            'title': 'Job Title',
            'company': 'Company Name',
            'location': 'City, State',
            'dates': 'Start - End',
            'achievements': ['Achievement 1', 'Achievement 2']
        }
    ],
    'education': [
        {
            'degree': 'Degree Name',
            'school': 'School Name',
            'location': 'City, State',
            'dates': 'Start - End',
            'gpa': '3.8/4.0'  # optional
        }
    ],
    'skills': {
        'programming': ['Python', 'JavaScript'],
        'frameworks': ['React', 'Django'],
        'databases': ['PostgreSQL', 'MongoDB'],
        'tools': ['Docker', 'Git']
    },
    'projects': [
        {
            'name': 'Project Name',
            'description': 'Project description',
            'technologies': ['Tech1', 'Tech2'],
            'url': 'project-url.com'  # optional
        }
    ]
}
```

## Template System

The module uses Jinja2 for template rendering with LaTeX-friendly delimiters:

- Variables: `\VAR{variable_name}`
- Blocks: `\BLOCK{for item in items}...\BLOCK{endfor}`
- Comments: `\#{comment}`
- Line statements: `%% statement`

### Example Template Snippet

```latex
\section{Experience}
\BLOCK{for exp in experience}
\subsection{\VAR{exp.title} -- \VAR{exp.company}}
\textit{\VAR{exp.location}} \hfill \VAR{exp.dates}
\begin{itemize}
\BLOCK{for achievement in exp.achievements}
\item \VAR{achievement}
\BLOCK{endfor}
\end{itemize}
\BLOCK{endfor}
```

## Error Handling

The module provides comprehensive error handling:

- **LaTeX Installation Check**: Verifies LaTeX engine availability
- **Compilation Errors**: Captures and reports LaTeX compilation errors
- **Template Errors**: Reports Jinja2 template rendering issues
- **File I/O Errors**: Handles file access and permission issues

## Logging

The module uses Python's logging system. Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Demo Script

Run the included demo script to test the module:

```bash
python demo.py
```

This will:
1. Create a sample template
2. Generate sample resume data
3. Render both template-based and direct LaTeX PDFs
4. Display the resume data structure

## Integration with Tailor Resume AI

This module is designed to integrate seamlessly with the Tailor Resume AI system:

1. **Input**: Receives structured resume data from the AI processing pipeline
2. **Templates**: Uses customizable LaTeX templates for different resume styles
3. **Output**: Generates ATS-friendly PDF resumes
4. **Customization**: Allows dynamic content based on job requirements

## Performance Considerations

- **Template Caching**: Templates are compiled once and reused
- **Temporary Files**: Automatic cleanup of compilation artifacts
- **Memory Usage**: Efficient handling of large resume datasets
- **Concurrent Processing**: Thread-safe for batch processing

## Troubleshooting

### Common Issues

1. **"LaTeX engine not found"**
   - Ensure LaTeX distribution is installed
   - Check that the LaTeX engine is in your PATH

2. **"Compilation failed"**
   - Check LaTeX syntax in your template
   - Ensure all required packages are available
   - Review compilation logs for specific errors

3. **"Template rendering failed"**
   - Verify template syntax and variable names
   - Check that all required data fields are provided

4. **"Permission denied"**
   - Ensure write permissions to output directory
   - Check that output file is not open in another application

### Getting Help

- Check the error logs for detailed information
- Enable debug logging for more verbose output
- Ensure all dependencies are properly installed
- Verify LaTeX installation with: `pdflatex --version`

## License

This module is part of the Tailor Resume AI project. See the main project repository for license information.
