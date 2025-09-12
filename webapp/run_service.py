#!/usr/bin/env python3
"""
Resume Tailor AI - Web Application Runner (Service Version)
Service-compatible version without Unicode characters
"""

import os
import sys
import logging
from app import app

# Configure logging for service
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flask_app.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    """Main entry point for the web application (service version)"""
    
    try:
        # Use ASCII-safe output for Windows service
        print("Starting Resume Tailor AI - Prompt Generator")
        print("=" * 50)
        
        # Configuration
        host = os.environ.get('FLASK_HOST', '0.0.0.0')
        port = int(os.environ.get('FLASK_PORT', 5000))
        debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'  # Default to False for service
        
        print(f"Server starting at: http://{host}:{port}")
        print(f"Debug mode: {'Enabled' if debug else 'Disabled'}")
        print("=" * 50)
        
        logging.info(f"Starting Flask app on {host}:{port}")
        logging.info(f"Debug mode: {debug}")
        
        # Start the Flask app
        app.run(host=host, port=port, debug=debug, use_reloader=False)  # No reloader in service
        
    except KeyboardInterrupt:
        print("\nService stopped by user")
        logging.info("Service stopped by keyboard interrupt")
    except Exception as e:
        error_msg = f"Error starting server: {e}"
        print(error_msg)
        logging.error(error_msg)
        sys.exit(1)

if __name__ == '__main__':
    main()
