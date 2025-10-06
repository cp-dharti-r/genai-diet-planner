import streamlit as st
import os
from datetime import datetime
from typing import List, Dict, Any
import json

from config import Config
from ai_dietitian import AIDietitian
from pdf_generator import DietPlanPDFGenerator
from models import UserProfile, WeeklyDietPlan

# Page configuration
st.set_page_config(
    page_title="AI Diet Planner",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .sidebar-header {
        font-size: 1.5rem;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f5e8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'diet_plan' not in st.session_state:
        st.session_state.diet_plan = None
    
    if 'conversation_complete' not in st.session_state:
        st.session_state.conversation_complete = False

def display_chat_message(role: str, content: str):
    """Display a chat message with appropriate styling"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong><br>{content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>Dr. Sarah Chen:</strong><br>{content}
        </div>
        """, unsafe_allow_html=True)

def display_user_profile(profile: UserProfile):
    """Display the extracted user profile"""
    st.subheader("📋 Your Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {profile.name}")
        st.write(f"**Age:** {profile.age} years")
        st.write(f"**Gender:** {profile.gender}")
        st.write(f"**Height:** {profile.height_cm} cm")
        st.write(f"**Current Weight:** {profile.weight_kg} kg")
    
    with col2:
        if profile.target_weight_kg:
            st.write(f"**Target Weight:** {profile.target_weight_kg} kg")
        st.write(f"**Goal:** {profile.goal.replace('_', ' ').title()}")
        st.write(f"**Activity Level:** {profile.activity_level.replace('_', ' ').title()}")
        st.write(f"**Cooking Skill:** {profile.cooking_skill}")
    
    if profile.dietary_restrictions and profile.dietary_restrictions != ["none"]:
        st.write(f"**Dietary Restrictions:** {', '.join(profile.dietary_restrictions)}")
    
    if profile.allergies:
        st.write(f"**Allergies:** {', '.join(profile.allergies)}")
    
    if profile.preferences:
        st.write(f"**Food Preferences:** {', '.join(profile.preferences)}")

def display_diet_plan_summary(plan: WeeklyDietPlan):
    """Display a summary of the generated diet plan"""
    st.subheader("🍽️ Your Weekly Diet Plan")
    
    # Weekly overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Calories", f"{plan.weekly_summary.get('total_calories', 'N/A')}")
    with col2:
        st.metric("Avg Protein", f"{plan.weekly_summary.get('avg_protein', 'N/A')}g")
    with col3:
        st.metric("Avg Carbs", f"{plan.weekly_summary.get('avg_carbs', 'N/A')}g")
    with col4:
        st.metric("Avg Fat", f"{plan.weekly_summary.get('avg_fat', 'N/A')}g")
    
    # Daily plans
    st.subheader("📅 Daily Meal Plans")
    for daily_plan in plan.daily_plans:
        with st.expander(f"{daily_plan.day} - {daily_plan.total_calories} calories"):
            for meal in daily_plan.meals:
                st.write(f"**{meal.meal_time.title()}:** {meal.meal_name}")
                st.write(f"*{meal.description}*")
                st.write(f"Calories: {meal.nutrition_info.get('calories', 'N/A')} | "
                        f"Protein: {meal.nutrition_info.get('protein', 'N/A')}g | "
                        f"Carbs: {meal.nutrition_info.get('carbs', 'N/A')}g | "
                        f"Fat: {meal.nutrition_info.get('fat', 'N/A')}g")
                st.write("---")
    
    # Shopping list
    if plan.shopping_list:
        st.subheader("🛒 Shopping List")
        shopping_text = "• " + "\n• ".join(plan.shopping_list)
        st.text_area("Items to buy:", shopping_text, height=150, disabled=True)
    
    # Recommendations
    if plan.recommendations:
        st.subheader("💡 Personalized Recommendations")
        for i, rec in enumerate(plan.recommendations, 1):
            st.write(f"{i}. {rec}")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🥗 AI Diet Planner</h1>', unsafe_allow_html=True)
    st.markdown("### Meet Dr. Sarah Chen, Your AI Nutritionist")
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">📊 Progress</div>', unsafe_allow_html=True)
        
        if st.session_state.user_profile:
            st.success("✅ Profile Extracted")
        else:
            st.info("⏳ Profile Pending")
        
        if st.session_state.diet_plan:
            st.success("✅ Diet Plan Generated")
        else:
            st.info("⏳ Diet Plan Pending")
        
        st.markdown("---")
        
        # Instructions
        st.markdown("### 💬 How to Use")
        st.markdown("""
        1. **Start chatting** with Dr. Sarah Chen
        2. **Share your details** - goals, preferences, lifestyle
        3. **Get your profile** extracted automatically
        4. **Receive personalized** diet plan
        5. **Download PDF** of your complete plan
        """)
        
        # Technical details
        st.markdown("---")
        st.markdown("### 🔧 Technical Features")
        st.markdown("""
        - **Role-Based Prompting**: AI acts as real dietitian
        - **Few-Shot Learning**: Guided conversation examples
        - **Chain-of-Thought**: Structured reasoning for planning
        - **Structured Output**: Pydantic models for data extraction
        - **PDF Generation**: Professional diet plan documents
        """)
    
    # Main content area
    if not st.session_state.conversation_complete:
        # Chat interface
        st.subheader("💬 Chat with Dr. Sarah Chen")
        st.markdown("""
        <div class="info-box">
            <strong>Welcome!</strong> I'm Dr. Sarah Chen, your AI nutritionist. 
            Let's start by understanding your health goals, lifestyle, and preferences. 
            I'll ask you some questions to create a personalized diet plan just for you.
        </div>
        """, unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            display_chat_message(message["role"], message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            display_chat_message("user", prompt)
            
            # Get AI response
            try:
                ai_dietitian = AIDietitian()
                response = ai_dietitian.chat(prompt, st.session_state.messages)
                
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                display_chat_message("assistant", response)
                
                # Check if we have enough information to extract profile
                if len(st.session_state.messages) >= 6 and not st.session_state.user_profile:
                    with st.spinner("Analyzing our conversation to create your profile..."):
                        profile = ai_dietitian.extract_user_profile(st.session_state.messages)
                        if profile:
                            st.session_state.user_profile = profile
                            st.success("✅ Profile extracted successfully!")
                            st.rerun()
                
            except Exception as e:
                st.error(f"Sorry, I encountered an error: {str(e)}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Extract Profile", disabled=not st.session_state.messages):
                try:
                    ai_dietitian = AIDietitian()
                    with st.spinner("Extracting your profile..."):
                        profile = ai_dietitian.extract_user_profile(st.session_state.messages)
                        if profile:
                            st.session_state.user_profile = profile
                            st.success("✅ Profile extracted successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Could not extract profile. Please continue the conversation.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            if st.button("📋 Generate Diet Plan", disabled=not st.session_state.user_profile):
                try:
                    ai_dietitian = AIDietitian()
                    with st.spinner("Creating your personalized diet plan..."):
                        plan = ai_dietitian.create_diet_plan(st.session_state.user_profile)
                        if plan:
                            st.session_state.diet_plan = plan
                            st.success("✅ Diet plan generated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Could not generate diet plan. Please try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col3:
            if st.button("✅ Complete Session", disabled=not st.session_state.diet_plan):
                st.session_state.conversation_complete = True
                st.rerun()
    
    else:
        # Display final results
        if st.session_state.user_profile and st.session_state.diet_plan:
            display_user_profile(st.session_state.user_profile)
            st.markdown("---")
            display_diet_plan_summary(st.session_state.diet_plan)
            
            # PDF download
            st.markdown("---")
            st.subheader("📄 Download Your Diet Plan")
            
            if st.button("🔄 Generate PDF"):
                try:
                    pdf_generator = DietPlanPDFGenerator()
                    with st.spinner("Generating PDF..."):
                        pdf_path = pdf_generator.generate_diet_plan_pdf(st.session_state.diet_plan)
                        
                        # Read the PDF file
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        
                        # Create download button
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=f"diet_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                        
                        # Clean up the temporary file
                        os.remove(pdf_path)
                        
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
            
            # Start over button
            if st.button("🔄 Start New Session"):
                st.session_state.messages = []
                st.session_state.user_profile = None
                st.session_state.diet_plan = None
                st.session_state.conversation_complete = False
                st.rerun()
        
        else:
            st.error("❌ Missing profile or diet plan. Please complete the session first.")
            if st.button("🔄 Start Over"):
                st.session_state.messages = []
                st.session_state.user_profile = None
                st.session_state.diet_plan = None
                st.session_state.conversation_complete = False
                st.rerun()

if __name__ == "__main__":
    try:
        Config.validate()
        main()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.markdown("""
        Please set up your environment variables:
        1. Create a `.env` file in the project root
        2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`
        3. Restart the application
        """)
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.markdown("Please check your configuration and try again.")
