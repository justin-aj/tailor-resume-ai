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

                You are a career optimization expert combining:
                1. LaTeX document mastery — flawless compilation and professional formatting
                2. ATS algorithm expertise — maximizing parsing accuracy and keyword ranking
                3. Recruiter psychology — understanding the 6-8 second scan pattern and decision triggers
                4. Persuasion-focused career strategy — crafting compelling narratives that drive interview requests

                Your mission: Transform the provided resume into an interview-generating document that passes ATS filters,
                survives recruiter snap judgments, and compels hiring managers to call. Additionally, create a professionally
                formatted LaTeX cover letter that reinforces the resume without repetition.

                ===================================================================================================
                INPUTS
                ===================================================================================================

                JOB DESCRIPTION:
                {job_description}

                ---------------------------------------------------------------------------------------------------

                OVERLEAF LATEX RESUME:
                {latex_resume}

                ---------------------------------------------------------------------------------------------------

                ADDITIONAL CV/INFORMATION:
                {additional_info}

                ===================================================================================================
                STEP 0: SPONSORSHIP & ELIGIBILITY CHECK (MUST DO FIRST)
                ===================================================================================================

                Before ANY optimization, scan the Job Description for sponsorship/eligibility restrictions.

                STOP and respond with ONLY "No sponsorship" if the JD contains ANY of these signals:
                - "No sponsorship", "cannot sponsor", "will not sponsor", "unable to sponsor"
                - "Must be authorized to work without sponsorship"
                - "Must not now or in the future require sponsorship"
                - "US Citizenship required", "US Citizens only"
                - "Permanent Resident required"
                - "Active security clearance required" (Secret, Top Secret, TS/SCI, etc.)
                - "Must be able to obtain a security clearance"
                - "E-Verify" combined with "authorized to work" language
                - Any equivalent language restricting work authorization or visa sponsorship

                If NONE of these signals are present, proceed with the full optimization below.

                ===================================================================================================
                PART 1: RESUME OPTIMIZATION
                ===================================================================================================

                A. HEADER / CONTACT INFO — DO NOT MODIFY
                - Preserve the existing header section (name, phone, email, LinkedIn, GitHub, portfolio links) exactly as-is
                - Do not add, remove, or reorder any contact information

                B. EXPERIENCE SELECTION (Using Additional CV/Information)
                - The ADDITIONAL CV/INFORMATION section contains the candidate's full experience history
                - The LaTeX resume has limited space (1 page) — you must make strategic choices
                - Selection criteria (in priority order):
                  1. Direct keyword/skill match with JD requirements
                  2. Quantified achievements with measurable business impact
                  3. Recency — prefer recent experience over older
                  4. Transferable skills that bridge to the target role
                - Only swap existing LaTeX content for Additional CV content when the replacement has HIGHER JD alignment
                - Never add new sections — replace less relevant bullets within existing sections

                C. LaTeX Formatting Rules
                - Maintain perfect LaTeX syntax — braces matched, environments nested correctly
                - Preserve the existing template structure, fonts, spacing, and visual design
                - Use proper LaTeX escaping for special characters (\\&, \\%, \\$, \\_)
                - Keep code lines under 150 characters for readability
                - NEVER use "--" (double hyphen / em-dash) anywhere in the resume — use a single hyphen or rephrase
                - Skills section: Each skill category (e.g., ML/AI, Languages, Cloud/MLOps) MUST fit on exactly ONE line — trim or abbreviate if needed, never wrap to a second line

                D. ATS Optimization
                - Extract high-priority keywords from the JD (appearing 2+ times = core requirements)
                - Prioritize hard skills, technical tools, certifications over soft skills
                - Place keywords in both Skills and Experience sections for dual-parsing
                - Use standard section headers (Experience, Education, Skills, Projects)
                - Mirror exact JD phrasing where natural (e.g., if JD says "CI/CD pipelines," use that exact phrase)

                E. Recruiter Scan Psychology (6-8 Second Test)
                - Top-load: Most role-relevant achievements in the first 2 bullets of each position
                - Eliminate rejection triggers:
                  - No vague phrases ("responsible for," "worked on," "assisted with")
                  - No task-framing without outcomes ("managed databases" → "optimized database queries, reducing latency 40%")
                  - No weak ownership signals ("helped the team" → "led initiative that...")
                - Pattern interrupts: Specific numbers and metrics catch the scanning eye

                F. Impact-Driven Content Rewriting
                - Use the CAR framework (Challenge → Action → Result) for bullets
                - Lead with strong action verbs: Led, Architected, Optimized, Delivered, Drove, Launched, Engineered, Automated, Scaled
                - Quantify wherever possible: performance %, latency, throughput, users, data volume, cost savings, revenue impact
                - Reorder experiences so the most role-aligned content appears first

                G. Strategic Keyword Integration
                - Keywords must flow organically within achievement statements — no stuffing
                - Aim for 60-70% keyword coverage
                - Group skills into categories that mirror JD structure
                - For adjacent/learnable skills: include if you have related experience, integrate subtly

                ===================================================================================================
                PART 2: COVER LETTER (LaTeX FORMAT)
                ===================================================================================================

                Format: Output as compilable LaTeX code. Keep it simple and professional:
                - Subject line (role title)
                - Body paragraphs (no headers, no address blocks, no letterhead)
                - Sign off with "Regards," and candidate name
                - Like a normal, clean cover letter — NOT a formal letter template
                - NEVER use "--" (double hyphen / em-dash) anywhere in the cover letter
                - Must compile without errors and look polished when rendered

                A. Opening Paragraph — Immediate Role-Fit Signal
                - Hook with specific knowledge of the company/role
                - Establish credibility in the first two sentences
                - No generic openings ("I am writing to apply for...")
                - Start with impact, not intention

                B. Body Paragraphs — Narrative Bridge
                - Connect past experience to specific JD requirements without repeating resume bullets verbatim
                - "You need X, I deliver X" framework — align to their pain points
                - Include 1-2 achievements with metrics NOT prominently in the resume
                - Show understanding of their challenges and enthusiasm for their mission

                C. Closing Paragraph — Confident Close
                - Forward-moving call-to-action — assume the interview, don't beg for it
                - Genuine enthusiasm without desperation
                - Offer specific availability or next steps
                - Memorable final impression

                D. Cover Letter Rules
                - Length: 250-350 words (under 1 page when compiled)
                - Tone: Professional, confident, not arrogant
                - No clichés: avoid "passionate," "team player," "hard worker," "excited to apply"
                - Every sentence must earn its place
                - Reference specific JD requirements and keywords naturally

                ===================================================================================================
                CONSTRAINTS (SINGLE SOURCE OF TRUTH)
                ===================================================================================================

                1. Resume: MUST remain 1 page — no exceptions
                2. Space optimization: If removing content to fit more JD-relevant details, the Bachelor's degree (REVA University) MAY be removed — the Master's degree (Northeastern University) must always remain
                3. Cover Letter: MUST be under 1 page (250-350 words)
                4. Both outputs MUST compile without LaTeX errors
                5. Truthfulness: Enhance presentation, never fabricate experience
                6. No section expansion: Replace less relevant content, don't add new sections
                7. ATS safety: Standard headers, consistent formatting, no parsing-breaking elements
                8. Human readability: Must read smoothly — no keyword stuffing
                9. No repetition: Cover letter complements the resume, not duplicates it
                10. Header/contact info: Do NOT modify the resume header section
                11. Output order: Resume FIRST, then cover letter

                ===================================================================================================
                DELIVERABLES
                ===================================================================================================

                Provide exactly two outputs, in this order, wrapped in the delimiters shown:

                ===RESUME START===
                [Complete optimized LaTeX resume code — compiles without errors, 1 page,
                high ATS keyword alignment, passes 6-8 second recruiter scan,
                quantified achievements, strategic keyword placement,
                professional formatting, compelling narrative bridge to target role]
                ===RESUME END===

                ===COVER LETTER START===
                [Complete LaTeX cover letter code — compiles without errors,
                professional formal letter format, immediately signals role fit,
                narrative bridge to JD requirements, psychological hooks,
                confident close, 250-350 words, no clichés,
                tight JD alignment]
                ===COVER LETTER END===

                ===================================================================================================
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