#!/usr/bin/env python3
"""
AMIF Grant Assistant - Main Entry Point
"""

import sys
import os
import argparse
from typing import Optional

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_environment():
    """Checks environment variables"""
    try:
        from config.settings import settings
        return True
    except Exception as e:
        print(f"❌ Environment variable error: {e}")
        print("💡 Please create .env file and add required API keys")
        return False

def run_web_app():
    """Starts Flask web interface"""
    print("🌐 Starting web interface...")
    from interfaces.web_app import app
    app.run(host='0.0.0.0', port=3000, debug=True)

def run_streamlit():
    """Starts Streamlit web interface"""
    print("🌐 Starting Streamlit web interface...")
    os.system("streamlit run streamlit_app.py")

def run_ingestion(pdf_dir: str = "data/raw"):
    """Starts PDF ingestion process"""
    print(f"📂 Loading PDFs: {pdf_dir}")
    try:
        from ingestion import run_full_ingestion
        success = run_full_ingestion(data_dir=pdf_dir)
        if success:
            print("✅ PDF upload successful!")
        else:
            print("❌ PDF upload failed!")
    except Exception as e:
        print(f"❌ Ingestion error: {e}")

def show_status():
    """Shows system status"""
    try:
        from ingestion.vector_store import get_collection_info
        
        print("\n📊 SYSTEM STATUS")
        print("=" * 50)
        
        info = get_collection_info()
        
        print(f"🗃️  Database: {info.get('collection_name', 'N/A')}")
        print(f"📄 Document count: {info.get('document_count', 0):,}")
        print(f"📁 Directory: {info.get('persist_directory', 'N/A')}")
        
        # Check PDF files
        pdf_count = len([f for f in os.listdir("data/raw") if f.endswith('.pdf')])
        print(f"📑 Raw PDF count: {pdf_count}")
        
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Status information could not be retrieved: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="AMIF Grant Assistant - AI Powered Grant Document Q&A System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
  python main.py                    # Flask web interface (default)
  python main.py --streamlit        # Streamlit web interface
  python main.py --ingest           # Load PDFs to database
  python main.py --status           # Show system status
        """
    )
    
    parser.add_argument(
        '--interface', '-i',
        choices=['web', 'streamlit'],
        default='web',
        help='Interface to use (default: web)'
    )
    
    parser.add_argument(
        '--web',
        action='store_true',
        help='Start Flask web interface (default)'
    )
    
    parser.add_argument(
        '--streamlit', 
        action='store_true',
        help='Start Streamlit web interface'
    )
    
    parser.add_argument(
        '--ingest',
        action='store_true',
        help='Load PDF files to database'
    )
    
    parser.add_argument(
        '--pdf-dir',
        default='data/raw',
        help='Directory containing PDF files (default: data/raw)'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status'
    )
    
    args = parser.parse_args()
    
    # Environment check
    if not check_environment():
        return 1
    
    # Run appropriate function based on arguments
    try:
        if args.ingest:
            run_ingestion(args.pdf_dir)
        elif args.status:
            show_status()
        elif args.streamlit or args.interface == 'streamlit':
            run_streamlit()
        else:
            # Default: Flask web interface
            run_web_app()
            
    except KeyboardInterrupt:
        print("\n👋 Program terminated!")
        return 0
    except Exception as e:
        print(f"❌ Program error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 