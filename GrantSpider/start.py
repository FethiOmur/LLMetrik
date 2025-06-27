#!/usr/bin/env python3
"""
AMIF Grant Assistant - Quick Start Script
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def print_banner():
    """Prints the title banner"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 AMIF Grant Assistant                   ║
║              AI-Powered Grant Document Q&A System           ║
║                       Quick Start Script                    ║
╚══════════════════════════════════════════════════════════════╝
    """)

def get_correct_python_executable():
    """Detects the correct Python executable"""
    # First try the which python3 command
    try:
        result = subprocess.run(["which", "python3"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Try alternative paths
    possible_paths = [
        "/usr/bin/python3",
        "/opt/homebrew/bin/python3.11", 
        "/opt/homebrew/bin/python3",
        sys.executable
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return sys.executable  # Last resort

def check_prerequisites():
    """Checks prerequisites"""
    print("🔍 Checking prerequisites...")
    
    issues = []
    
    # .env file check
    env_file = Path(".env")
    if not env_file.exists():
        issues.append("❌ .env file not found")
        print("💡 Creating .env file...")
        create_env_template()
    else:
        print("✅ .env file exists")
    
    # Detect correct Python executable
    python_exec = get_correct_python_executable()
    
    # Dependencies check - use correct Python
    try:
        # Streamlit check
        result = subprocess.run([python_exec, "-c", "import streamlit"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Streamlit installed")
        else:
            issues.append("❌ Streamlit not installed")
    except Exception:
        issues.append("❌ Streamlit check failed")
    
    try:
        # LangChain check
        result = subprocess.run([python_exec, "-c", "import langchain"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ LangChain installed")
        else:
            issues.append("❌ LangChain not installed")
    except Exception:
        issues.append("❌ LangChain check failed")
    
    try:
        # ChromaDB check
        result = subprocess.run([python_exec, "-c", "import chromadb"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ChromaDB installed")
        else:
            issues.append("❌ ChromaDB not installed")
    except Exception:
        issues.append("❌ ChromaDB check failed")
    
    try:
        # OpenAI check
        result = subprocess.run([python_exec, "-c", "import openai"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ OpenAI installed")
        else:
            issues.append("❌ OpenAI not installed")
    except Exception:
        issues.append("❌ OpenAI check failed")
    
    # Database check
    db_path = Path("data/db")
    if db_path.exists() and any(db_path.iterdir()):
        print("✅ Vector database exists")
    else:
        issues.append("⚠️  Vector database empty or missing")
    
    # PDF files check
    pdf_path = Path("data/raw")
    if pdf_path.exists():
        pdf_count = len(list(pdf_path.glob("*.pdf")))
        if pdf_count > 0:
            print(f"✅ {pdf_count} PDF files found")
        else:
            issues.append("⚠️  No PDF files found")
    else:
        issues.append("❌ data/raw directory not found")
    
    return issues

def create_env_template():
    """Creates a sample .env file"""
    env_template = """# AMIF Grant Assistant - Environment Variables

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration  
OPENAI_MODEL=o4-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# Vector Database Configuration
CHROMA_PERSIST_DIRECTORY=data/db
CHROMA_COLLECTION_NAME=amif_documents

# Application Configuration
MAX_CHAT_HISTORY=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
MAX_SEARCH_RESULTS=8

# Logging
LOG_LEVEL=INFO
"""
    
    with open(".env", "w", encoding="utf-8") as f:
        f.write(env_template)
    
    print("📝 .env file created. Please add your API keys!")

def show_quick_start_menu():
    """Shows the quick start menu"""
    print("\n🚀 QUICK START MENU")
    print("=" * 50)
    print("1. 🌐 Streamlit Web Interface (Recommended)")
    print("2. 💻 Advanced CLI Interface")
    print("3. 🔧 Simple CLI Interface")
    print("4. 📂 PDF Upload (Ingestion)")
    print("5. 📊 System Status")
    print("6. ❓ Help")
    print("7. 🚪 Exit")
    print("=" * 50)

def handle_user_choice(choice: str):
    """Handles user choice"""
    if choice == '1':
        print("🌐 Starting Streamlit...")
        os.system("python main.py --streamlit")
    
    elif choice == '2':
        print("💻 Starting Advanced CLI...")
        os.system("python main.py --cli")
    
    elif choice == '3':
        print("🔧 Starting Simple CLI...")
        os.system("python main.py --simple")
    
    elif choice == '4':
        print("📂 Starting PDF upload...")
        os.system("python main.py --ingest")
    
    elif choice == '5':
        print("📊 Checking system status...")
        os.system("python main.py --status")
    
    elif choice == '6':
        show_help()
    
    elif choice == '7':
        print("👋 Goodbye!")
        sys.exit(0)
    
    else:
        print("❌ Invalid selection! Please enter a number between 1-7.")

def show_help():
    """Shows help information"""
    print("\n📚 HELP INFORMATION")
    print("=" * 60)
    print("🌐 Streamlit Web Interface:")
    print("   • Most user-friendly interface")
    print("   • Works in web browser")
    print("   • Drag-and-drop file upload")
    print("   • Visual result display")
    print()
    print("💻 Advanced CLI Interface:")
    print("   • Terminal-based")
    print("   • Detailed source information")
    print("   • Advanced commands")
    print("   • LangGraph-based")
    print()
    print("🔧 Simple CLI Interface:")
    print("   • For quick testing")
    print("   • Minimal interface")
    print("   • Basic Q&A")
    print()
    print("📂 PDF Upload:")
    print("   • Adds new PDF files to the system")
    print("   • Processes PDFs from data/raw folder")
    print("   • Updates vector database")
    print("=" * 60)

def run_diagnostic():
    """Runs detailed system diagnostics"""
    print("\n🔍 DETAILED SYSTEM DIAGNOSTICS")
    print("=" * 60)
    
    # Detect correct Python executable
    python_exec = get_correct_python_executable()
    
    # Python information
    print(f"🐍 Python: {sys.version}")
    print(f"📁 Python executable: {python_exec}")
    print(f"📂 Working directory: {os.getcwd()}")
    
    print("\n📦 INSTALLED PACKAGES:")
    print("-" * 30)
    
    # Check critical packages
    critical_packages = [
        "streamlit", "langchain", "chromadb", "openai", 
        "langchain-openai", "langchain-chroma", "python-dotenv"
    ]
    
    for package in critical_packages:
        try:
            result = subprocess.run([python_exec, "-c", f"import {package}; print(f'{package}: INSTALLED')"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ {package}")
            else:
                print(f"❌ {package}: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {package}: {str(e)}")
    
    print("\n📁 CHECK PROJECT STRUCTURE:")
    print("-" * 30)
    
    # Check critical directories
    critical_dirs = [
        "agents", "config", "graph", "ingestion", "interfaces", 
        "memory", "chains", "utils", "data", "data/db", "data/raw"
    ]
    
    for dir_name in critical_dirs:
        if os.path.exists(dir_name):
            if dir_name == "data/db":
                files = os.listdir(dir_name) if os.path.isdir(dir_name) else []
                print(f"✅ {dir_name}/ ({len(files)} files)")
            elif dir_name == "data/raw":
                pdf_files = [f for f in os.listdir(dir_name) if f.endswith('.pdf')] if os.path.isdir(dir_name) else []
                print(f"✅ {dir_name}/ ({len(pdf_files)} PDFs)")
            else:
                print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ missing")
    
    print("\n🔧 CRITICAL FILES:")
    print("-" * 30)
    
    critical_files = [
        ".env", "requirements.txt", "main.py", "start.py", 
        "streamlit_app.py", "config/settings.py", "config/models.py"
    ]
    
    for file_name in critical_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} ({size} bytes)")
        else:
            print(f"❌ {file_name} missing")
    
    # Environment variables check
    print("\n🔐 ENVIRONMENT VARIABLES:")
    print("-" * 30)
    
    if os.path.exists(".env"):
        try:
            with open(".env", "r") as f:
                env_content = f.read()
                if "OPENAI_API_KEY=your_openai_api_key_here" in env_content:
                    print("⚠️  OpenAI API key not configured yet")
                elif "OPENAI_API_KEY=" in env_content:
                    print("✅ OpenAI API key appears to be configured")
                else:
                    print("❌ API key not found in .env file")
        except Exception as e:
            print(f"❌ .env file couldn't be read: {e}")
    
    print("\n💾 DATABASE STATUS:")
    print("-" * 30)
    
    db_path = Path("data/db")
    if db_path.exists():
        try:
            # Check ChromaDB files
            chroma_file = db_path / "chroma.sqlite3"
            if chroma_file.exists():
                size_mb = chroma_file.stat().st_size / (1024*1024)
                print(f"✅ ChromaDB: {size_mb:.1f}MB")
            else:
                print("❌ ChromaDB file not found")
            
            # Count collection directories
            collections = [d for d in db_path.iterdir() if d.is_dir()]
            print(f"📁 Collection count: {len(collections)}")
            
        except Exception as e:
            print(f"❌ Database check failed: {e}")
    else:
        print("❌ Database directory not found")
    
    print("=" * 60)

def launch_streamlit():
    """Starts the Streamlit application"""
    print("\n🌐 Starting Streamlit application...")
    try:
        os.system(f"{sys.executable} -m streamlit run streamlit_app.py")
    except Exception as e:
        print(f"❌ Streamlit could not be started: {e}")

def launch_flask_app():
    """Starts the Flask web application"""
    print("\n🌐 Starting Flask web application...")
    print("📍 Address: http://localhost:3000")
    print("🎨 Loading modern web interface...")
    try:
        # Go to interfaces directory and run web_app.py
        os.chdir("interfaces")
        import subprocess
        subprocess.run([sys.executable, "web_app.py"])
    except Exception as e:
        print(f"❌ Flask application could not be started: {e}")
        print("💡 Trying alternative solution...")
        try:
            os.system(f"{sys.executable} web_app.py")
        except Exception as e2:
            print(f"❌ Alternative solution also failed: {e2}")
        finally:
            # Return to main directory
            os.chdir("..")

def show_system_status():
    """Shows system status"""
    print("\n📊 SYSTEM STATUS")
    print("=" * 30)
    
    # Detect correct Python executable
    python_exec = get_correct_python_executable()
    
    # Quick checks
    print("🔧 Basic Checks:")
    
    # Python version
    print(f"🐍 Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Dependencies
    deps_ok = True
    for dep in ["streamlit", "langchain", "chromadb", "openai"]:
        try:
            result = subprocess.run([python_exec, "-c", f"import {dep}"], 
                                  capture_output=True, text=True, timeout=3)
            if result.returncode == 0:
                print(f"✅ {dep}")
            else:
                print(f"❌ {dep}")
                deps_ok = False
        except:
            print(f"❌ {dep}")
            deps_ok = False
    
    # Database
    if Path("data/db").exists() and any(Path("data/db").iterdir()):
        print("✅ Database")
    else:
        print("❌ Database")
    
    # PDFs
    pdf_count = len(list(Path("data/raw").glob("*.pdf"))) if Path("data/raw").exists() else 0
    print(f"📄 PDF Files: {pdf_count}")
    
    # Overall status
    if deps_ok and Path("data/db").exists() and pdf_count > 0:
        print("\n🎉 System ready! All components working.")
    else:
        print("\n⚠️  Some issues detected. Use option '4' for detailed analysis.")

def main():
    """Main function - Directly starts Flask web application"""
    print_banner()
    
    # Check prerequisites
    issues = check_prerequisites()
    
    if issues:
        print("\n⚠️  Detected issues:")
        for issue in issues:
            print(f"  {issue}")
        
        # Stop if there are critical errors
        if any("❌" in issue for issue in issues):
            print("\n❌ Critical errors exist. Please resolve issues and try again.")
            print("💡 For help: python install.sh")
            return
    
    print(f"\n✅ System ready! Starting web application...")
    
    # Start Flask web application directly
    launch_flask_app()

if __name__ == "__main__":
    main() 