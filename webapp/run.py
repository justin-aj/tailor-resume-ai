#!/usr/bin/env python3
"""
Resume Tailor AI - Web Application Runner
Run this script to start the web application locally
"""

import os
import sys
from app import app

def main():
    """Main entry point for the web application"""
    
    print("🚀 Starting Resume Tailor AI - Prompt Generator")
    print("=" * 50)
    
    # Configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))  # Changed to 5000 to avoid conflict
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🌐 Server will start at: http://{host}:{port}")
    print(f"🔧 Debug mode: {'Enabled' if debug else 'Disabled'}")
    print("=" * 50)
    print("📋 How to use:")
    print("1. Open the URL above in your web browser")
    print("2. Enter your job description")
    print("3. Paste your LaTeX resume code")
    print("4. Add any additional information")
    print("5. Click 'Generate AI Prompt'")
    print("6. Copy the generated prompt")
    print("7. Paste it into ChatGPT, Claude, or your preferred AI service")
    print("=" * 50)
    print("🤖 Perfect for AI services like:")
    print("   • ChatGPT (https://chat.openai.com/)")
    print("   • Claude (https://claude.ai/)")
    print("   • Gemini (https://gemini.google.com/)")
    print("   • Perplexity (https://perplexity.ai/)")
    print("=" * 50)
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Goodbye! Thanks for using Resume Tailor AI")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
