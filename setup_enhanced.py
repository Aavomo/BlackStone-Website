#!/usr/bin/env python3
"""
Enhanced Website Setup Script for Blackstone EG & Partners
Installs dependencies and initializes the enhanced Flask application
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def print_banner():
    print("=" * 70)
    print("🚀 BLACKSTONE EG & PARTNERS - ENHANCED WEBSITE SETUP")
    print("=" * 70)
    print("🎯 Features: Database | Email | Admin Panel | Blog | Portfolio")
    print("📊 Analytics: Google Analytics | Facebook Pixel | SEO Optimized")
    print("🔧 Backend: Python Flask | SQLAlchemy | Email Integration")
    print("=" * 70)

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version compatible")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing enhanced dependencies...")
    
    try:
        # Install from requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_enhanced.txt"], 
                      check=True, capture_output=True)
        print("✅ Enhanced dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("🔄 Trying alternative installation...")
        
        # Try individual packages
        packages = [
            "Flask>=2.3.0",
            "Flask-SQLAlchemy>=3.0.0", 
            "Flask-Mail>=0.9.1",
            "Flask-Admin>=1.6.0",
            "Flask-WTF>=1.1.0",
            "WTForms>=3.0.0",
            "Flask-Migrate>=4.0.0",
            "Flask-Login>=0.6.0",
            "email-validator>=2.0.0",
            "python-dotenv>=1.0.0",
            "Pillow>=10.0.0"
        ]
        
        failed_packages = []
        for package in packages:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                              check=True, capture_output=True)
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError:
                failed_packages.append(package)
                print(f"❌ Failed to install {package}")
        
        if failed_packages:
            print(f"\n⚠️ Some packages failed to install: {failed_packages}")
            print("💡 Try installing them manually or check your internet connection")
            return False
        
        return True

def setup_environment():
    """Setup environment variables"""
    print("\n🔧 Setting up environment...")
    
    env_template = """# Blackstone EG & Partners Environment Configuration
# Database
DATABASE_URL=sqlite:///blackstone_eg.db

# Email Configuration (Configure for production)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@blackstoneegpartners.com

# Analytics (Optional - Add your IDs)
GOOGLE_ANALYTICS_ID=
FACEBOOK_PIXEL_ID=

# Security
SECRET_KEY=dev-key-change-in-production
FLASK_ENV=development
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_template)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️ .env file already exists")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'static/uploads',
        'static/uploads/logos',
        'static/uploads/blog', 
        'static/uploads/portfolio',
        'instance'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Created upload directories")

def test_enhanced_app():
    """Test if the enhanced app can be imported"""
    print("\n🧪 Testing enhanced application...")
    
    try:
        # Try importing the enhanced app
        sys.path.insert(0, os.getcwd())
        import app_enhanced
        print("✅ Enhanced app imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import enhanced app: {e}")
        return False

def show_setup_complete():
    """Show setup completion message"""
    print("\n" + "=" * 70)
    print("🎉 ENHANCED WEBSITE SETUP COMPLETE!")
    print("=" * 70)
    print("\n📋 NEXT STEPS:")
    print("\n1. 🚀 START THE ENHANCED WEBSITE:")
    print("   python app_enhanced.py")
    print("\n2. 🌐 ACCESS YOUR WEBSITE:")
    print("   Website: http://localhost:5000")
    print("   Admin Panel: http://localhost:5000/admin")
    print("\n3. 🔑 ADMIN LOGIN:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   ⚠️ CHANGE THIS PASSWORD IN PRODUCTION!")
    print("\n4. ⚙️ CONFIGURE EMAIL (Optional):")
    print("   Edit .env file with your SMTP settings")
    print("\n5. 📊 ADD ANALYTICS (Optional):")
    print("   Add Google Analytics ID and Facebook Pixel ID to .env")
    print("\n6. 🎨 CUSTOMIZE:")
    print("   - Upload your logo in Admin Panel")
    print("   - Add blog posts and portfolio items")
    print("   - Update company information")
    print("\n🔧 ENHANCED FEATURES INCLUDED:")
    print("✅ Database with Contact Forms, Blog, Portfolio")
    print("✅ Admin Panel for Content Management") 
    print("✅ Email Notifications")
    print("✅ SEO Optimization")
    print("✅ Google Analytics & Facebook Pixel Integration")
    print("✅ Responsive Design with Modern UI")
    print("✅ Blog System with Categories and Tags")
    print("✅ Portfolio Showcase with Filtering")
    print("✅ Contact Form with Validation")
    print("✅ Loading Animations and Smooth Scrolling")
    print("\n" + "=" * 70)

def show_help():
    """Show troubleshooting help"""
    print("\n🆘 TROUBLESHOOTING:")
    print("\n❌ If installation fails:")
    print("1. Check internet connection")
    print("2. Try: python -m pip install --upgrade pip")
    print("3. Use virtual environment: python -m venv venv")
    print("4. For Windows: pip install --trusted-host pypi.org [package]")
    print("\n❌ If app fails to start:")
    print("1. Check Python version (3.8+ required)")
    print("2. Install missing packages individually")
    print("3. Check file permissions")
    print("\n❌ If database issues:")
    print("1. Delete blackstone_eg.db and restart")
    print("2. Check write permissions in current directory")
    print("\n📧 Email Setup (Optional):")
    print("1. Use Gmail App Password (not regular password)")
    print("2. Enable 2FA and generate App Password")
    print("3. Update MAIL_USERNAME and MAIL_PASSWORD in .env")

def main():
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️ Some dependencies failed to install.")
        print("💡 You can try running the basic version: python app.py")
        show_help()
        return
    
    # Setup environment
    setup_environment()
    
    # Create directories
    create_directories()
    
    # Test enhanced app
    if not test_enhanced_app():
        print("\n⚠️ Enhanced app test failed.")
        print("💡 You can try running the basic version: python app.py")
        show_help()
        return
    
    # Show completion message
    show_setup_complete()

if __name__ == "__main__":
    main()