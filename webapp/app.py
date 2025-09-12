import os
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'yoyo_secret_key'  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def read_resume_txt():
    """Read content from resume.txt file"""
    try:
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
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resume.txt')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception:
        return False

def write_data_science_resume_tex(content):
    """Write content to data_science_resume.tex file"""
    try:
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
            You are an expert resume editor with a focus on conciseness and impact. 
            Your primary goal is to tailor a resume to a specific job description so 
            effectively that a hiring manager would think: "Wow, this resume perfectly 
            fits what we are looking for!" You must also optimize the resume for 
            Applicant Tracking Systems (ATS).

            Your task is to edit the resume, ensuring it remains a single page in length.

            Here are the inputs:

            JOB DESCRIPTION: {job_description}

            OVERLEAF LATEX RESUME: {latex_resume}

            ADDITIONAL CV/INFORMATION: {additional_info}

            Your goal is to edit the OVERLEAF LATEX RESUME to highlight the most relevant 
            experiences, skills, and achievements for the JOB DESCRIPTION.

            STRATEGIC EMBELLISHMENT GUIDELINES:

            Relatable Experience: If a skill or responsibility in the JOB DESCRIPTION 
            somewhat relates to work you've done, you may phrase it in the resume to 
            suggest a more direct familiarity or experience, subtly emphasizing the 
            connection.

            Easily Learnable Skills: If there are non-complex skills or technologies 
            mentioned in the JOB DESCRIPTION that you believe I can learn quickly, 
            you may include them in your skills section or subtly integrate them into 
            relevant bullet points, implying proficiency. Exercise discretion 
            and avoid misrepresenting core competencies.

            CRITICAL CONSTRAINTS:

            Hiring Manager's Impression & ATS Optimization: The edits should make the 
            resume an undeniable match for the job description, using keywords and 
            phrasing that resonate with both human reviewers & ATS.

            Maintain 1-Page Length: The edited resume MUST NOT exceed its current 
            1-page length.

            Concise Edits: Strategically modify, add, or remove bullet points, 
            experiences, and projects to maximize impact and alignment with the 
            job description. Prioritize job-description-centric content.

            Avoid Line Expansion: Do not add new lines or sections if it causes the 
            document to expand in length. If new information is crucial, integrate it 
            by replacing less relevant existing text, ensuring the line count and 
            overall visual length remain the same. Prioritize editing within existing 
            text blocks.

            STRICT LINE CHARACTER LIMIT: Each line of LaTeX code, including spaces, 
            must not exceed 95 characters. This is a critical constraint to ensure 
            proper formatting and prevent line breaks in the compiled PDF.

            LaTeX Special Characters: When using the ampersand symbol (&) in text 
            within the LaTeX code, you must escape it with a backslash (\) 
            (i.e., use \&). This is crucial to avoid LaTeX compilation errors.

            LaTeX Format: Provide the complete, edited LaTeX code.

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

if __name__ == '__main__':
    # Run the app - configuration will be handled by run.py
    app.run(debug=False, host='0.0.0.0', port=5000)
