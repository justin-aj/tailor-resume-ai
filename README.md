# Tailor Resume AI

A professional AI-powered resume tailoring application with web interface and Windows service capability. Generate tailored prompts for AI services like ChatGPT, Claude, and Gemini to optimize your resume for specific job descriptions.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_App-green.svg)](https://flask.palletsprojects.com/)
[![LaTeX](https://img.shields.io/badge/LaTeX-pdflatex-green.svg)](https://www.latex-project.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

This project provides a web-based application for generating AI prompts to tailor your LaTeX resume to specific job descriptions. Features a clean web interface, file synchronization, and Windows service capability for 24/7 availability.

## ✨ Key Features

- 🌐 **Web Application**: Clean, responsive web interface
- 🤖 **AI Prompt Generation**: Creates complete prompts for ChatGPT, Claude, Gemini
- � **File Synchronization**: Bidirectional sync with local resume files
- � **Auto-Loading**: Pre-fills forms with your resume and CV data
- �️ **Windows Service**: Run as background service, auto-start with Windows
- 📱 **Mobile Friendly**: Responsive design works on all devices
- ⚡ **Real-time Updates**: Load from files or save to files with one click
- 🔧 **Easy Setup**: Simple batch file installation

## 📋 Requirements

- **Python**: 3.6 or higher
- **Flask**: Web framework (automatically installed)
- **pywin32**: Windows service support (for service installation)

## 🔧 Dependencies Installation

```bash
cd webapp
pip install -r requirements.txt
```

All required packages:
- Flask 2.3.3
- pywin32 (for Windows service functionality)

## 🚀 Quick Start

### 🌐 Web Application (Recommended)

**1. Install as Windows Service (One-Click Setup):**
```bash
cd webapp
# Right-click install_service.bat → "Run as administrator"
```
**2. Access your app:** http://localhost:5000

**That's it!** Your Resume Tailor AI is now running 24/7 as a Windows service.

### 💻 Manual Development Mode
```bash
cd webapp
python run.py
```

### 🎯 How It Works
1. **Enter job description** in the web form
2. **LaTeX resume loads automatically** from `data_science_resume.tex`
3. **Additional info loads automatically** from `resume.txt`
4. **Generate AI prompt** with one click
5. **Copy prompt** and paste into ChatGPT, Claude, or Gemini
6. **Get tailored resume** from your favorite AI service

## 🔧 Windows Service Installation (✅ TESTED & WORKING)

**The simplest way to host on Windows:**

1. **Navigate to the webapp folder**
2. **Right-click on `install_service.bat`**
3. **Select "Run as administrator"**
4. **Wait for completion**
5. **Access at http://localhost:5000**

**Features:**
- ✅ **Auto-starts with Windows**
- ✅ **Runs in background 24/7**
- ✅ **Network accessible** (configure firewall if needed)
- ✅ **Automatic logging** (`flask_service.log`)
- ✅ **Easy management** via Windows Services

**Service Management:**
```cmd
cd webapp
python flask_service.py start    # Start service
python flask_service.py stop     # Stop service  
python flask_service.py debug    # Check status
python flask_service.py remove   # Uninstall
```

## 📁 Project Structure

```
tailor-resume-ai/
├── 📁 .git/                     # Git repository
├── 📁 .venv/                    # Python virtual environment  
├── 📁 webapp/                   # 🌐 Web Application
│   ├── 📁 static/
│   │   ├── 📁 css/
│   │   │   └── 📄 style.css     # Application styles
│   │   └── 📁 js/
│   │       └── 📄 app.js        # Frontend JavaScript
│   ├── 📁 templates/
│   │   ├── 📄 index.html        # Main form interface
│   │   └── 📄 result.html       # Generated prompt display
│   ├── 📄 app.py                # 🔧 Main Flask application
│   ├── 📄 run.py                # 🎯 Application runner
│   ├── 📄 flask_service.py      # 🖥️ Windows service wrapper
│   ├── � install_service.bat   # ✅ One-click service installer
│   ├── 📄 install_service.ps1   # PowerShell installer
│   ├── 📄 uninstall_service.bat # Service remover
│   ├── 📄 test_app.bat          # Development tester
│   ├── 📄 requirements.txt      # Python dependencies
│   └── 📄 SERVICE_INSTALLATION.md # Installation guide
├── 📄 .gitignore                # Git ignore rules
├── 📄 data_science_resume.tex   # 📋 Your LaTeX resume
├── 📄 resume.txt                # 📄 Additional CV information
└── 📄 README.md                 # 📖 This documentation
```

## 🔧 API Reference

### Web Application Routes

- **`/`** - Main form interface with auto-loaded resume data
- **`/process`** - Generates AI prompt from form submission  
- **`/update-resume-txt`** - Loads content from `resume.txt`
- **`/update-latex-resume`** - Loads content from `data_science_resume.tex`
- **`/save-resume-txt`** - Saves form content to `resume.txt`
- **`/save-latex-resume`** - Saves form content to `data_science_resume.tex`

### Service Management Commands

```cmd
cd webapp
python flask_service.py install --startup auto  # Install service
python flask_service.py start                   # Start service
python flask_service.py stop                    # Stop service
python flask_service.py debug                   # Check status  
python flask_service.py remove                  # Uninstall service
```

## 🛠 Development Setup

### Local Development
```bash
git clone https://github.com/justin-aj/tailor-resume-ai.git
cd tailor-resume-ai/webapp
pip install -r requirements.txt
python run.py
```

### File Structure
- **`data_science_resume.tex`** - Your main LaTeX resume (auto-loaded)
- **`resume.txt`** - Additional CV information (auto-loaded)  
- **`webapp/`** - Complete web application
- **`webapp/static/`** - CSS, JavaScript, and assets
- **`webapp/templates/`** - HTML templates

### Features
- ✅ **Auto-loading** of resume files into web form
- ✅ **Bidirectional sync** - load from files or save to files
- ✅ **AI prompt generation** for ChatGPT, Claude, Gemini
- ✅ **Windows service** capability for 24/7 hosting
- ✅ **Responsive design** - works on desktop and mobile

## 📝 Resume Template

The project includes a professional LaTeX resume template (`tex_files/main.tex`) with:

- 📋 **Clean Layout**: Professional, ATS-friendly design
- 🔗 **Hyperlinks**: Clickable email, LinkedIn, GitHub links
- 📑 **Sections**: Education, Experience, Skills, Projects
- 🎨 **Formatting**: Custom commands for consistent styling
- 📱 **Mobile-Friendly**: Proper contact information layout

## 🔍 Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **Service won't install** | Not admin privileges | Run batch file as administrator |
| **Web app not accessible** | Service not running | Check `python flask_service.py debug` |
| **Files not loading** | File path issues | Ensure `resume.txt` and `data_science_resume.tex` exist |
| **Save buttons not working** | File permissions | Check write permissions on files |

## 📊 Application Features

- ✅ **Professional Web Interface**: Clean, responsive design
- ✅ **Auto-Loading Forms**: Pre-filled with your resume data  
- ✅ **File Synchronization**: Load from/save to resume files
- ✅ **AI Prompt Generation**: Optimized for ChatGPT, Claude, Gemini
- ✅ **Windows Service**: 24/7 background operation
- ✅ **Network Access**: Available on all network interfaces
- ✅ **Service Logging**: Detailed logs in `flask_service.log`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask web framework for the application backend
- Bootstrap for responsive web design  
- Font Awesome for clean iconography
- LaTeX resume template based on [Jake Gutierrez's template](https://github.com/sb2nov/resume)
- Built with Python and modern web technologies
- Windows service implementation using pywin32

## 📞 Support

If you encounter any issues:

1. Check that the Flask service is running (`python flask_service.py debug`)
2. Verify your resume files (`resume.txt`, `data_science_resume.tex`) exist
3. Check the service logs (`flask_service.log`) for error details
4. Ensure you have administrator privileges for service installation
5. Open an issue on GitHub with error details

---

**Built with ❤️ by [Ajin Frank Justin](https://github.com/justin-aj)**  
**September 2025** | **Version 2.0** | **Web Application with Windows Service**
