#!/usr/bin/env python3
"""
Setup script for AI Diet Planner
Helps users install dependencies and configure the environment
"""

import os
import sys
import subprocess
import platform

def print_header():
    """Print the application header"""
    print("🥗 AI Diet Planner - Setup Script")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   This application requires Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip not available. Please install pip first.")
        return False
    
    # Install requirements
    try:
        print("   Installing packages from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    print("\n🔧 Setting up environment configuration...")
    
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"   {env_file} already exists")
        return True
    
    # Create .env template
    env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Application Configuration
APP_TITLE=AI Diet Planner
APP_DESCRIPTION=Personalized diet planning with AI dietitian
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print(f"✅ Created {env_file} template")
        print("   Please edit this file and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Failed to create {env_file}: {e}")
        return False

def check_openai_key():
    """Check if OpenAI API key is configured"""
    print("\n🔑 Checking OpenAI API key...")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OpenAI API key not configured")
        print("   Please edit the .env file and add your API key")
        return False
    
    print("✅ OpenAI API key configured")
    return True

def run_tests():
    """Run component tests"""
    print("\n🧪 Running component tests...")
    
    try:
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print("   Check the output above for details")
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\n📋 Next Steps:")
    print("1. Edit the .env file with your OpenAI API key")
    print("2. Run the application: streamlit run app.py")
    print("3. Open your browser to http://localhost:8501")
    print("4. Start chatting with Dr. Sarah Chen!")
    print("\n📚 For more information, see README.md")
    print("=" * 50)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Check OpenAI key
    if not check_openai_key():
        print("\n⚠️  OpenAI API key not configured")
        print("   Please edit the .env file and add your API key")
        print("   Then run this setup script again")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("\n⚠️  Some tests failed")
        print("   The application may not work correctly")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
