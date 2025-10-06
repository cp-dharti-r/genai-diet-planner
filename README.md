# 🥗 AI Diet Planner

A personalized diet planning application powered by AI that demonstrates advanced prompt engineering techniques and generates downloadable PDF diet plans.

## ✨ Features

### 🤖 AI Dietitian (Dr. Sarah Chen)
- **Role-Based Prompting**: AI acts as a real certified nutritionist with 15+ years of experience
- **Few-Shot Learning**: Guided conversation examples for natural interaction flow
- **Chain-of-Thought (CoT)**: Structured reasoning for profile extraction and meal planning
- **Personalized Approach**: Considers individual preferences, cultural background, and lifestyle

### 💬 Interactive Chat Interface
- Natural conversation with AI dietitian
- Automatic profile extraction from conversations
- Structured data collection using Pydantic models
- Real-time chat with context awareness

### 📊 Structured Data Extraction
- **User Profile**: Age, weight, goals, dietary restrictions, allergies, preferences
- **Lifestyle Information**: Activity level, daily routine, cooking skills, budget constraints
- **Cultural Considerations**: Food preferences, cultural background, dietary habits

### 🍽️ Personalized Diet Plans
- Weekly meal planning with daily breakdowns
- Nutritional calculations (calories, protein, carbs, fat)
- Meal-specific details (ingredients, instructions, prep time)
- Shopping lists and personalized recommendations

### 📄 Professional PDF Generation
- Beautiful, structured PDF documents
- User profile summary
- Complete weekly meal plans
- Shopping lists and recommendations
- Professional styling with ReportLab

## 🚀 Technical Implementation

### Prompt Engineering Techniques

#### 1. Role-Based Prompting
```python
# AI acts as Dr. Sarah Chen, certified clinical nutritionist
system_prompt = """You are Dr. Sarah Chen, a certified clinical nutritionist 
and registered dietitian with over 15 years of experience..."""
```

#### 2. Few-Shot Learning
```python
# Guided conversation examples
few_shot_examples = [
    {
        "user": "Hi, I want to lose weight",
        "assistant": "Hello! I'm Dr. Sarah Chen, and I'm here to help..."
    }
]
```

#### 3. Chain-of-Thought (CoT)
```python
# Structured reasoning for complex tasks
cot_prompt = """Let me think through this step by step:
1. First, I need to identify all the personal information mentioned
2. Then, I should categorize their preferences and restrictions
3. Next, I'll assess their lifestyle and routine patterns..."""
```

### Data Models (Pydantic)
- **UserProfile**: Comprehensive user information
- **MealPlan**: Individual meal details
- **DailyPlan**: Daily meal structure
- **WeeklyDietPlan**: Complete weekly plan

### PDF Generation (ReportLab)
- Professional document styling
- Structured layouts with tables and sections
- Custom fonts and colors
- Multi-page document generation

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/genai-diet-planner.git
cd genai-diet-planner
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
APP_TITLE=AI Diet Planner
APP_DESCRIPTION=Personalized diet planning with AI dietitian
```

### 4. Run the Application
```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📱 How to Use

### 1. Start a Conversation
- Begin chatting with Dr. Sarah Chen
- Share your health goals, preferences, and lifestyle
- The AI will ask targeted questions to understand your needs

### 2. Profile Extraction
- After sufficient conversation, your profile will be automatically extracted
- Review and confirm your extracted information
- All data is structured using Pydantic models

### 3. Diet Plan Generation
- Once your profile is complete, generate a personalized diet plan
- The AI uses Chain-of-Thought reasoning to create optimal meal plans
- Plans consider your preferences, restrictions, and lifestyle

### 4. Download PDF
- Generate a professional PDF of your complete diet plan
- Includes user profile, weekly meals, shopping lists, and recommendations
- Professional styling with ReportLab

## 🔧 Project Structure

```
genai-diet-planner/
├── app.py                 # Main Streamlit application
├── ai_dietitian.py        # AI service with prompt engineering
├── models.py              # Pydantic data models
├── pdf_generator.py       # PDF generation service
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

## 🧠 Prompt Engineering Deep Dive

### Role-Based Prompting
The AI dietitian maintains a consistent persona throughout the conversation:
- Professional credentials and experience
- Warm, empathetic communication style
- Evidence-based approach to nutrition
- Cultural sensitivity and inclusivity

### Few-Shot Examples
Pre-configured conversation examples guide the AI:
- Natural conversation flow
- Appropriate question sequencing
- Professional yet friendly tone
- Comprehensive information gathering

### Chain-of-Thought Reasoning
Complex tasks are broken down into logical steps:

#### Profile Extraction
1. Identify personal information mentioned
2. Categorize preferences and restrictions
3. Assess lifestyle and routine patterns
4. Determine goals and constraints

#### Meal Planning
1. Calculate caloric needs based on profile
2. Distribute calories across meals
3. Align foods with preferences and restrictions
4. Make plans practical for cooking skills
5. Incorporate cultural elements

## 📊 Data Flow

```
User Chat → AI Dietitian → Profile Extraction → Diet Plan Generation → PDF Creation
    ↓              ↓              ↓                ↓              ↓
Conversation → Structured → UserProfile → WeeklyDietPlan → Downloadable PDF
History      → Data      → Object      → Object        → Document
```

## 🎯 Learning Objectives

This project demonstrates:

1. **Advanced Prompt Engineering**
   - Role-based prompting for consistent AI behavior
   - Few-shot learning for guided conversations
   - Chain-of-Thought reasoning for complex tasks

2. **Structured Data Extraction**
   - Pydantic models for data validation
   - JSON extraction from natural language
   - Structured output from AI conversations

3. **PDF Generation**
   - ReportLab library usage
   - Professional document creation
   - Structured layout design

4. **AI Integration**
   - OpenAI API integration
   - Context-aware conversations
   - Multi-step AI workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT models
- Streamlit for the web application framework
- ReportLab for PDF generation capabilities
- Pydantic for data validation and serialization

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/genai-diet-planner/issues) page
2. Create a new issue with detailed information
3. Include error messages and system information

---

**Happy Diet Planning! 🥗✨**