# 🚀 Quick Start Guide

Get your AI Diet Planner running in 5 minutes!

## ⚡ Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 2. Clone & Setup
```bash
git clone <your-repo-url>
cd genai-diet-planner
```

### 3. Run Setup Script
```bash
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Create .env template
- ✅ Run component tests

### 4. Configure API Key
Edit the `.env` file and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Launch Application
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` and start chatting with Dr. Sarah Chen!

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Create Environment File
```bash
cp env_example.txt .env
# Edit .env with your API key
```

### Run Tests
```bash
python demo.py
```

### Launch App
```bash
streamlit run app.py
```

## 🧪 Test Components

Run the demo script to test individual components:
```bash
python demo.py
```

This tests:
- ✅ Pydantic models
- ✅ AI Dietitian service
- ✅ PDF generation
- ✅ Data extraction

## 🎯 First Use

1. **Start Chatting**: Begin conversation with Dr. Sarah Chen
2. **Share Details**: Tell her about your goals, preferences, lifestyle
3. **Extract Profile**: Click "Extract Profile" after sufficient conversation
4. **Generate Plan**: Click "Generate Diet Plan" to create your personalized plan
5. **Download PDF**: Generate and download your complete diet plan

## 🆘 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Make sure you created a `.env` file
- Check that your API key is correct
- Restart the application after editing `.env`

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

**PDF generation fails**
- Ensure ReportLab is installed: `pip install reportlab`
- Check file permissions in your directory

**AI responses are slow**
- Verify your OpenAI API key is valid
- Check your OpenAI account usage/limits

### Get Help

1. Check the [README.md](README.md) for detailed documentation
2. Run `python demo.py` to test components
3. Check the console for error messages
4. Verify your OpenAI API key and account status

## 🎉 You're Ready!

Start your personalized nutrition journey with AI-powered diet planning! 🥗✨
