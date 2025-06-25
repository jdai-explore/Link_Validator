"""
Debug launcher to catch startup errors and import issues
Run this instead of link_validator.py to see what's causing the crash
"""

import sys
import traceback

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import tkinter
        print("✅ tkinter - OK")
    except ImportError:
        missing_deps.append("tkinter")
        print("❌ tkinter - MISSING")
    
    try:
        import pandas
        print("✅ pandas - OK")
    except ImportError:
        missing_deps.append("pandas")
        print("❌ pandas - MISSING")
    
    try:
        import openpyxl
        print("✅ openpyxl - OK")
    except ImportError:
        missing_deps.append("openpyxl")
        print("❌ openpyxl - MISSING")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 - OK")
    except ImportError:
        missing_deps.append("beautifulsoup4")
        print("❌ beautifulsoup4 - MISSING")
    
    try:
        from urllib.parse import urlparse
        print("✅ urllib.parse - OK")
    except ImportError:
        missing_deps.append("urllib.parse")
        print("❌ urllib.parse - MISSING")
    
    return missing_deps

def check_local_modules():
    """Check if our local modules can be imported"""
    modules_status = {}
    
    try:
        import utils
        print("✅ utils.py - OK")
        modules_status['utils'] = True
    except Exception as e:
        print(f"❌ utils.py - ERROR: {e}")
        modules_status['utils'] = False
    
    try:
        import config
        print("✅ config.py - OK")
        modules_status['config'] = True
    except Exception as e:
        print(f"❌ config.py - ERROR: {e}")
        modules_status['config'] = False
    
    try:
        import logger
        print("✅ logger.py - OK")
        modules_status['logger'] = True
    except Exception as e:
        print(f"❌ logger.py - ERROR: {e}")
        modules_status['logger'] = False
    
    try:
        import exceptions
        print("✅ exceptions.py - OK")
        modules_status['exceptions'] = True
    except Exception as e:
        print(f"❌ exceptions.py - ERROR: {e}")
        modules_status['exceptions'] = False
    
    return modules_status

def safe_import_main():
    """Safely import and run the main application"""
    try:
        print("\n🔄 Attempting to import link_validator...")
        from link_validator import main
        print("✅ link_validator imported successfully")
        
        print("\n🚀 Starting application...")
        main()
        
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR during import/startup:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"\nFull traceback:")
        traceback.print_exc()
        
        print(f"\n💡 Possible solutions:")
        print(f"1. Install missing dependencies: pip install -r requirements.txt")
        print(f"2. Check that all .py files are in the same directory")
        print(f"3. Verify file permissions")
        print(f"4. Check Python version (requires 3.7+)")
        
        input("\nPress Enter to exit...")

def main():
    """Main debug function"""
    print("🔍 Link Validator Debug Launcher")
    print("=" * 50)
    
    print(f"\n📍 Python version: {sys.version}")
    print(f"📍 Python executable: {sys.executable}")
    print(f"📍 Current working directory: {sys.path[0]}")
    
    print(f"\n📦 Checking Dependencies...")
    print("-" * 30)
    missing_deps = check_dependencies()
    
    print(f"\n📄 Checking Local Modules...")
    print("-" * 30)
    modules_status = check_local_modules()
    
    if missing_deps:
        print(f"\n⚠️  MISSING DEPENDENCIES:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print(f"\n💿 Install with: pip install {' '.join(missing_deps)}")
        input("\nPress Enter to continue anyway or Ctrl+C to exit...")
    
    if not all(modules_status.values()):
        print(f"\n⚠️  LOCAL MODULE ISSUES:")
        for module, status in modules_status.items():
            if not status:
                print(f"   - {module}.py has import issues")
        input("\nPress Enter to continue anyway or Ctrl+C to exit...")
    
    print(f"\n" + "=" * 50)
    safe_import_main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n👋 Debug session cancelled by user")
    except Exception as e:
        print(f"\n\n💥 FATAL ERROR in debug launcher:")
        print(f"Error: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")