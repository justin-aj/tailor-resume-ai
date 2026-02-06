import os
import sys
import asyncio
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Create Flask app with proper template and static folder paths for Vercel
app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')
app.secret_key = 'yoyo_secret_key'  
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Import scraper (will be available after installation)
try:
    from scraper import JobScraper
    SCRAPER_AVAILABLE = True
except ImportError:
    SCRAPER_AVAILABLE = False
    print("Warning: Scraper module not available. Install required packages: pip install -r scraper_requirements.txt")

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
                Expert LaTeX Resume Optimizer, ATS Specialist & Cover Letter Strategist

                You are a quadruple-threat career optimization expert combining:
                1. LaTeX document mastery - ensuring flawless compilation and professional formatting
                2. ATS algorithm expertise - maximizing parsing accuracy and keyword ranking
                3. Recruiter psychology knowledge - understanding the 6-8 second scan pattern and decision triggers
                4. Persuasion-focused career strategy - crafting compelling narratives that drive interview requests

                Your mission: Transform the provided resume into an undeniable interview-generating document that passes ATS filters, 
                survives recruiter snap judgments, and compels hiring managers to call. Additionally, create a psychologically 
                compelling cover letter that reinforces the resume without repetition and creates urgency to interview.

                ---------------------------------------------------------------------------------------------------
                INPUTS
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

                PART 1: RESUME OPTIMIZATION INSTRUCTIONS

                1. LaTeX Excellence & Formatting Integrity
                - Maintain perfect LaTeX syntax - all commands properly formatted, braces matched, environments nested correctly
                - Preserve the existing template structure, fonts, spacing, and visual design
                - Use proper LaTeX escaping for special characters (\&, \%, \$, \_, \#)
                - Ensure the output compiles without errors
                - Keep code lines reasonably readable (120-150 characters) without sacrificing syntax correctness

                2. ATS Algorithm Optimization
                - Extract high-priority keywords from the JD (those appearing 2+ times are likely core requirements)
                - Prioritize hard skills, technical tools, certifications, and role-specific terminology over soft skills
                - Place keywords strategically in both Skills and Experience sections for dual-parsing
                - Use standard section headers that ATS systems reliably parse (Experience, Education, Skills, Projects)
                - Avoid formatting pitfalls: no tables, text boxes, graphics, or critical info in headers/footers
                - Mirror exact phrasing from JD where natural (e.g., if JD says "CI/CD pipelines," use that exact phrase)

                3. Recruiter Scan Psychology (6-8 Second Test)
                - Top-load impact: Place the most role-relevant achievements in the first 2 bullets of each position
                - Visual hierarchy: Ensure the most important information is scannable at a glance
                - Eliminate rejection triggers:
                - Remove vague phrases ("responsible for," "worked on," "assisted with")
                - Remove task-framing without outcomes ("managed databases" → "optimized database queries, reducing latency 40%")
                - Remove lack of ownership signals ("helped the team" → "led initiative that...")
                - Create pattern interrupts: Specific numbers and metrics catch the scanning eye

                4. Impact-Driven Content Rewriting
                - Use the CAR framework (Challenge → Action → Result) for bullet points
                - Lead with strong action verbs: Led, Architected, Optimized, Delivered, Drove, Launched, Engineered, Automated, Scaled
                - Include quantifiable outcomes wherever possible:
                - Performance improvements (%, latency, throughput)
                - Scale indicators (users, data volume, transactions)
                - Efficiency gains (time saved, cost reduced)
                - Business impact (revenue, adoption, reliability)
                - Reorder experiences so the most role-aligned content appears first and most prominently

                5. Strategic Keyword Integration
                - Natural weaving: Keywords must flow organically within achievement statements
                - Density balance: Aim for 60-70% keyword coverage without stuffing
                - Skill section optimization: Group skills into categories that mirror JD structure
                - For adjacent/learnable skills mentioned in JD: Include if you have related experience or can quickly demonstrate proficiency – integrate subtly to imply familiarity

                6. Narrative Alignment & Credibility Signals
                - Create a clear story arc that bridges past experience to the target role
                - Highlight transferable achievements that demonstrate capability for JD responsibilities
                - Include credibility markers: company names, technologies, scale of impact
                - Ensure every bullet answers "so what?" - why should the hiring manager care?

                ---------------------------------------------------------------------------------------------------

                PART 2: COVER LETTER STRATEGY INSTRUCTIONS

                1. Immediate Role-Fit Signal (Opening Paragraph)
                - Open with a hook that demonstrates specific knowledge of the company/role
                - Establish credibility within the first two sentences - mention a relevant achievement or qualification
                - Avoid generic openings ("I am writing to apply for...")
                - Create pattern interrupt: Start with impact, not intention

                2. Narrative Bridge (Body Paragraphs)
                - Connect past experience to specific JD requirements without repeating resume bullets verbatim
                - Use the "You need X, I deliver X" framework - align your experience to their pain points
                - Include 1-2 specific achievements with metrics that aren't prominently featured in the resume
                - Demonstrate understanding of their challenges and how you solve them
                - Show enthusiasm for the specific company/mission - not just the role

                3. Psychological Hooks That Increase Interview Probability
                - Social proof: Reference recognizable companies, technologies, or scale of impact
                - Specificity: Concrete numbers and outcomes signal competence
                - Future value framing: Show what you will accomplish, not just what you have done
                - Curiosity gap: Hint at deeper expertise worth exploring in an interview
                - Loss aversion: Subtly imply what they'd miss by not interviewing you

                4. Confident Close (Final Paragraph)
                - End with a forward-moving call-to-action - assume the interview, don't beg for it
                - Express genuine enthusiasm without desperation
                - Offer specific availability or next steps
                - Leave them with a memorable final impression

                5. Cover Letter Rules
                - Length: Strictly under one page (250-350 words ideal)
                - Tone: Professional but compelling - confident, not arrogant
                - No generic fluff: Every sentence must earn its place
                - No clichés: Avoid "passionate," "team player," "hard worker," "excited to apply"
                - ATS-safe formatting: Simple structure, no tables or graphics
                - Tight JD alignment: Reference specific requirements and keywords naturally

                ---------------------------------------------------------------------------------------------------

                CRITICAL CONSTRAINTS

                Resume Page Length: MUST remain 1 page - no exceptions
                Cover Letter Length: MUST be under 1 page (250-350 words)
                LaTeX Compilation: Resume must compile without errors
                Truthfulness: Enhance presentation, but do not fabricate experience
                No Line Expansion: Replace less relevant content rather than adding new sections
                ATS Safety: Standard headers, consistent formatting, no parsing-breaking elements
                Human Readability: Must read smoothly for recruiters – no keyword stuffing
                No Repetition: Cover letter must complement resume, not duplicate it

                ---------------------------------------------------------------------------------------------------

                DELIVERABLES

                Provide two complete outputs:

                ---------------------------------------------------------------------------------------------------

                OUTPUT 1: Optimized LaTeX Resume

                Provide the complete revised LaTeX code that:
                - Compiles perfectly without any LaTeX errors
                - Achieves high ATS keyword alignment with the target JD
                - Passes the 6-8 second recruiter scan test with role-fit clarity
                - Highlights quantified achievements relevant to the position
                - Uses strategic keyword placement for both ATS and human readers
                - Maintains professional formatting and visual appeal
                - Stays strictly within 1 page
                - Creates a compelling narrative bridge between current experience and target role

                ---------------------------------------------------------------------------------------------------

                OUTPUT 2: Strategic Cover Letter

                Provide the complete cover letter (ready to submit) that:
                - Immediately signals role fit and credibility in the opening
                - Creates a narrative bridge between candidate experience and role requirements
                - Uses psychological hooks that increase interview probability
                - Reinforces resume claims without repetition
                - Ends with a confident, forward-moving call-to-action
                - Is under one page (250-350 words)
                - Uses professional but compelling tone - no generic fluff or clichés
                - Is ATS-safe in formatting
                - Aligns tightly to the job description

                ---------------------------------------------------------------------------------------------------
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

@app.route('/scraper')
def scraper():
    """Job URL scraper page"""
    return render_template('scraper.html')

@app.route('/api/scrape-job', methods=['POST'])
def scrape_job():
    """API endpoint to scrape a job description from URL"""
    if not SCRAPER_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Scraper not available. Please install required packages: pip install -r scraper_requirements.txt'
        }), 500
    
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Run async scraper using context manager
        async def scrape():
            async with JobScraper() as scraper:
                return await scraper.scrape(url)
        
        result = asyncio.run(scrape())
        
        if result.success:
            return jsonify({
                'success': True,
                'title': result.job_title or 'Job Posting',
                'company': result.company_name,
                'location': result.location,
                'description': result.to_resume_prompt(),
                'url': url
            })
        else:
            return jsonify({
                'success': False,
                'error': result.error or 'Unknown error occurred'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate-prompt', methods=['POST'])
def generate_prompt_api():
    """API endpoint to generate prompt for a scraped job"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '').strip()
        
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description is required'}), 400
        
        # Get default resume data
        latex_resume = read_data_science_resume_tex()
        additional_info = read_resume_txt()
        
        if not latex_resume:
            return jsonify({'success': False, 'error': 'LaTeX resume file not found'}), 400
        
        # Generate the complete prompt
        processor = ResumeProcessor()
        result = processor.generate_prompt(job_description, latex_resume, additional_info)
        
        return jsonify({
            'success': True,
            'prompt': result['prompt'],
            'word_count': result.get('word_count', 0),
            'char_count': result.get('char_count', 0)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# For development
if __name__ == '__main__':
    app.run(debug=True)