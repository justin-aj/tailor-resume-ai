# Resume Tailor AI - Prompt Generator

A web-based tool that generates complete, formatted prompts for AI services to tailor your LaTeX resume to specific job descriptions with ATS optimization.

## 🎯 What This Tool Does

Instead of manually formatting your inputs every time, this tool:
1. **Takes your inputs** (job description, LaTeX resume, additional info)
2. **Validates your LaTeX** against ATS requirements (95-char lines, proper escaping)
3. **Generates a complete prompt** with your exact prompt template
4. **Provides easy copy-paste** functionality for AI services

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pdflatex (optional - only needed for validation features)
- Web browser

### Installation & Setup

1. **Navigate to the webapp directory:**
   ```bash
   cd webapp
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python run.py
   ```

4. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## 📋 How to Use

### Step 1: Input Your Data
- **Job Description**: Paste the complete job posting
- **LaTeX Resume**: Paste your complete LaTeX resume code  
- **Additional Information**: Add extra skills, projects, or experiences

### Step 2: Generate Prompt
- Click "Generate AI Prompt"
- The system validates your LaTeX against requirements
- Creates a complete prompt with your exact template

### Step 3: Copy & Use with AI
- Copy the generated prompt with one click
- Paste into ChatGPT, Claude, Gemini, or Perplexity
- Get your perfectly tailored resume LaTeX code back

## 🎯 Your Exact Prompt Template

The tool uses your precise prompt template:

```
You are an expert resume editor with a focus on conciseness and impact...

JOB DESCRIPTION: [Your job posting]

OVERLEAF LATEX RESUME: [Your LaTeX code]

ADDITIONAL CV/INFORMATION: [Your extra info or "None"]

[Complete instructions for strategic embellishment, ATS optimization, 
95-character limits, ampersand escaping, etc.]
```

## ✅ Features

### Current Features
- **LaTeX Validation**: Ensures 95-character line limits
- **Special Character Checking**: Validates ampersand escaping
- **Complete Prompt Generation**: Uses your exact template
- **One-Click Copy**: Easy clipboard functionality
- **AI Service Links**: Quick access to ChatGPT, Claude, etc.
- **Real-time Feedback**: Character and word counts
- **Clean Interface**: Modern, responsive design

### LaTeX Requirements Enforced
- **Line Length**: Maximum 95 characters per line
- **Special Characters**: Ampersands must be escaped as `\&`
- **Format Validation**: Checks for common LaTeX issues
- **ATS Compliance**: Ensures resume meets hiring system requirements

## 🤖 AI Service Integration

### Supported Services
- **ChatGPT** (https://chat.openai.com/)
- **Claude** (https://claude.ai/)
- **Gemini** (https://gemini.google.com/)
- **Perplexity** (https://perplexity.ai/)

### Workflow
1. Generate prompt in this tool
2. Copy the complete prompt
3. Open your preferred AI service
4. Paste and send the prompt
5. Receive tailored LaTeX resume code
6. Compile with your existing LaTeX system

## 📁 Project Structure

```
webapp/
├── app.py              # Main Flask application
├── run.py              # Application runner  
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Input form
│   └── result.html     # Generated prompt display
├── static/
│   ├── css/style.css   # Custom styles
│   └── js/app.js       # Frontend JavaScript
├── uploads/            # Temporary storage (unused)
└── output/             # Generated files (unused)
```

## ⚙️ Configuration

### Environment Variables
```bash
FLASK_HOST=127.0.0.1        # Server host
FLASK_PORT=5000             # Server port  
FLASK_DEBUG=True            # Debug mode
SECRET_KEY=your-secret-key  # Flask secret
```

### LaTeX Validation Rules
The tool enforces these constraints from your prompt:
- **STRICT LINE CHARACTER LIMIT**: Max 95 characters per line
- **LaTeX Special Characters**: Ampersands must be escaped (`\&`)
- **Single Page Format**: Validates against expansion
- **ATS Optimization**: Ensures compatibility requirements

## 🎯 Example Usage

### Sample Job Description Input:
```
Software Engineer - Full Stack
We are looking for a Python developer with experience in web frameworks, 
API development, and database management. React experience preferred.
```

### Sample LaTeX Resume Input:
```latex
\documentclass[letterpaper,11pt]{article}
\usepackage{latexsym}
\usepackage[empty]{fullpage}
% ... your complete LaTeX resume code
\begin{document}
\name{Your Name}
\section{Experience}
% ... your experience entries
\end{document}
```

### Generated Output:
A complete prompt with your exact template filled in, ready to paste into any AI service.

## 🔧 Development

### Adding New Features
1. **API Integration**: Could add direct AI service integration
2. **Template Library**: Multiple prompt templates
3. **Resume Templates**: Pre-built LaTeX templates
4. **History**: Save previous prompts

### Running in Development
```bash
export FLASK_DEBUG=True
python run.py
```

## �️ Troubleshooting

### Common Issues

1. **Line Length Validation Errors**
   ```
   Line 45 exceeds 95 characters (120 chars): \section{Experience}...
   ```
   **Solution**: Break long lines or shorten content

2. **Unescaped Ampersand Warnings**
   ```
   Line 12 may have unescaped ampersands: Machine Learning & AI
   ```
   **Solution**: Change `&` to `\&` in your LaTeX

3. **Flask Installation Issues**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## 🎯 Why This Approach Works

### Benefits of Prompt Generation vs Direct AI Integration
1. **Flexibility**: Use any AI service you prefer
2. **Control**: See exactly what prompt is sent
3. **Privacy**: Your data doesn't go through our servers
4. **Cost**: No API costs on our end
5. **Reliability**: Not dependent on specific AI service availability
6. **Customization**: Easy to modify the prompt template

### Perfect for Your Workflow
- **Consistent Results**: Same prompt format every time
- **Quick Iterations**: Fast prompt generation
- **Multiple Jobs**: Easy to generate prompts for different positions
- **Quality Control**: Validate LaTeX before sending to AI

## 📄 Next Steps

1. **Test with Sample Data**: Use the web interface with sample inputs
2. **Customize Prompt**: Modify the template in `app.py` if needed
3. **Create Shortcuts**: Bookmark your favorite AI services
4. **Build Resume Library**: Keep commonly used LaTeX templates ready

## 🎉 Success Metrics

After using this tool, you should have:
- ✅ Validated LaTeX code that meets all requirements
- ✅ Perfectly formatted prompts for AI services  
- ✅ Consistent results across different job applications
- ✅ Faster workflow from job posting to tailored resume
- ✅ ATS-optimized resumes that pass hiring system filters

---

**Perfect for**: Job seekers who want to leverage AI for resume tailoring while maintaining control over the process and ensuring ATS compliance.
