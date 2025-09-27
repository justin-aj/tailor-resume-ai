import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

# Create Flask app with proper template and static folder paths for Vercel
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')
app.secret_key = 'yoyo_secret_key'  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def read_resume_txt():
    """Read content from resume.txt file"""
    try:
        # Go up one directory from api/ to webapp/ to find the file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resume.txt')
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

def read_data_science_resume_tex():
    """Read content from data_science_resume.tex file"""
    try:
        # Go up one directory from api/ to webapp/ to find the file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_science_resume.tex')
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

def write_resume_txt(content):
    """Write content to resume.txt file"""
    try:
        # Go up one directory from api/ to webapp/ to find the file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resume.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False

def write_data_science_resume_tex(content):
    """Write content to data_science_resume.tex file"""
    try:
        # Go up one directory from api/ to webapp/ to find the file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data_science_resume.tex')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False

class ResumeProcessor:
    def __init__(self):
        pass
    
    def generate_prompt(self, job_description, latex_resume, additional_info):
        """
        Generate the complete prompt with inputs filled in for AI services
        """
        # Generate the complete prompt
        prompt_template = """
            📄 Expert LaTeX Resume Optimizer & ATS Specialist

            You are a dual expert specializing in both LaTeX document formatting and ATS resume optimization. 
            Your expertise ensures that the revised resume maintains perfect LaTeX syntax while being optimized 
            for Applicant Tracking Systems (ATS) and tailored to the target job. The final output should be 
            a refined resume with flawless LaTeX formatting that integrates relevant keywords and skills from 
            the JD without making it look artificial or stuffed.

            Context: I am providing three documents:
            1. A target job description (JD) for the role I am applying to
            2. My current resume (in LaTeX format)
            3. Additional information about the job or the projects I have worked on

            Here are the inputs:
            ---------------------------------------------------------------------------------------------------
            JOB DESCRIPTION: 
            
            {job_description}
            ---------------------------------------------------------------------------------------------------
            OVERLEAF LATEX RESUME: 
            
            {latex_resume}
            ---------------------------------------------------------------------------------------------------
            ADDITIONAL CV/INFORMATION: 
            
            {additional_info}
            ---------------------------------------------------------------------------------------------------
            
            🔑 INSTRUCTIONS

            LaTeX Expertise & Formatting:
            • Maintain perfect LaTeX syntax throughout - ensure all commands are properly formatted
            • Preserve existing LaTeX document structure, packages, and environments
            • DO NOT change the existing LaTeX formatting style, template, or layout structure
            • Keep the current formatting patterns, spacing, fonts, and visual design intact
            • Use proper LaTeX escaping for special characters (ampersands, percentages, etc.)
            • Keep all braces, environments, and commands properly matched and nested
            • Maintain consistent formatting, spacing, and professional LaTeX styling as currently used

            Keyword Optimization:
            • Carefully analyze the job description and extract the most important hard skills, technical terms, 
              tools, certifications, and role-specific keywords.
            • Naturally integrate these keywords throughout the resume — especially in experience bullet points, 
              summary, and skills section — while maintaining readability and authenticity.
            • Place keywords in a way that ATS systems will parse correctly (e.g., within both Skills and Experience sections).

            Role Alignment:
            • Identify responsibilities and achievements from my current resume that most closely match the target role.
            • Rewrite bullet points to highlight quantifiable achievements, results, and leadership impact relevant to the new job.
            • Reorder or reframe content so the most role-aligned experiences are emphasized.

            ATS-Friendly Formatting:
            • Ensure the resume avoids formatting pitfalls that cause parsing errors (e.g., no tables, text boxes, 
              graphics, or headers/footers with critical info).
            • Use consistent bullet point formatting and standard section headers.
            • Maintain ATS-compatible LaTeX structure while ensuring proper formatting.

            Professional Voice & Impact:
            • Use strong action verbs (led, launched, optimized, delivered, drove, collaborated, etc.).
            • Focus on measurable outcomes where possible (e.g., "Increased revenue by 25%," "Improved efficiency by reducing processing time 30%").
            • Avoid vague or generic phrases (e.g., "responsible for," "worked on").

            Balance & Strategic Enhancement:
            • Do not keyword-stuff. Resume should read smoothly for a human recruiter.
            • If a skill or responsibility in the JOB DESCRIPTION somewhat relates to work you've done, you may phrase it 
              to suggest more direct familiarity, subtly emphasizing the connection.
            • For easily learnable skills or technologies mentioned in the JOB DESCRIPTION, you may include them in the 
              skills section or integrate them into relevant bullet points, implying proficiency. Exercise discretion.

            CRITICAL CONSTRAINTS:

            LaTeX Format Preservation: DO NOT modify the existing LaTeX template, formatting style, or visual layout. 
            Only update the CONTENT within the existing structure and formatting patterns.

            LaTeX Quality: The output must compile without errors and maintain professional LaTeX formatting standards.

            ATS & Hiring Manager Impact: The edits should make the resume an undeniable match for the job description, 
            using keywords and phrasing that resonate with both ATS systems and human reviewers.

            Maintain 1-Page Length: The edited resume MUST NOT exceed its current 1-page length.

            Concise Edits: Strategically modify, add, or remove bullet points, experiences, and projects to maximize 
            impact and alignment with the job description. Prioritize job-description-centric content.

            Avoid Line Expansion: Do not add new lines or sections if it causes the document to expand in length. 
            If new information is crucial, integrate it by replacing less relevant existing text.

            STRICT LINE CHARACTER LIMIT: Each line of LaTeX code, including spaces, must not exceed 100 characters. 
            This is critical to ensure proper formatting and prevent line breaks in the compiled PDF.

            LaTeX Special Characters: When using special characters in text within the LaTeX code, 
            ensure they are properly escaped to avoid LaTeX compilation errors.

            📌 DELIVERABLE

            Output the complete, revised LaTeX code that:
            • Compiles perfectly without any LaTeX errors
            • Highlights my most relevant achievements for the job
            • Passes ATS keyword scans effectively
            • Appeals to recruiters and hiring managers
            • Maintains professional formatting and readability
            • Stays within the 1-page constraint

            Please provide the revised LaTeX code for the resume.

            """
        
        # Fill in the template
        complete_prompt = prompt_template.format(
            job_description=job_description.strip(),
            latex_resume=latex_resume.strip(),
            additional_info=additional_info.strip() if additional_info.strip() else "None"
        )
        
        return {
            'success': True,
            'errors': [],
            'prompt': complete_prompt,
            'word_count': len(complete_prompt.split()),
            'char_count': len(complete_prompt)
        }

@app.route('/')
def index():
    # Pre-fill with content from files
    additional_info = read_resume_txt()
    latex_resume = read_data_science_resume_tex()
    
    return render_template('index.html', 
                         additional_info=additional_info,
                         latex_resume=latex_resume)

@app.route('/process', methods=['POST'])
def process_resume():
    try:
        # Get form data
        job_description = request.form.get('job_description', '').strip()
        latex_resume = request.form.get('latex_resume', '').strip()
        additional_info = request.form.get('additional_info', '').strip()
        
        # Validation
        if not job_description:
            flash('Job description is required', 'error')
            return redirect(url_for('index'))
        
        if not latex_resume:
            flash('LaTeX resume is required', 'error')
            return redirect(url_for('index'))
        
        # Generate the complete prompt
        processor = ResumeProcessor()
        result = processor.generate_prompt(job_description, latex_resume, additional_info)
        
        # Return the generated prompt
        return render_template('result.html',
                             complete_prompt=result['prompt'],
                             word_count=result.get('word_count', 0),
                             char_count=result.get('char_count', 0),
                             job_description=job_description[:200] + "..." if len(job_description) > 200 else job_description)
    
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/update-resume-txt', methods=['GET'])
def update_resume_txt():
    """API endpoint to get updated content from resume.txt"""
    content = read_resume_txt()
    return jsonify({'content': content})

@app.route('/update-latex-resume', methods=['GET'])
def update_latex_resume():
    """API endpoint to get updated content from data_science_resume.tex"""
    content = read_data_science_resume_tex()
    return jsonify({'content': content})

@app.route('/save-resume-txt', methods=['POST'])
def save_resume_txt():
    """API endpoint to save content to resume.txt"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if write_resume_txt(content):
            return jsonify({'success': True, 'message': 'Content saved to resume.txt'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save content'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/save-latex-resume', methods=['POST'])
def save_latex_resume():
    """API endpoint to save content to data_science_resume.tex"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        
        if write_data_science_resume_tex(content):
            return jsonify({'success': True, 'message': 'Content saved to data_science_resume.tex'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save content'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

# For development
if __name__ == '__main__':
    app.run(debug=True)