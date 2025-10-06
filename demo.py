#!/usr/bin/env python3
"""
Demo script for testing AI Dietitian and PDF generation components
Run this to test the core functionality without the Streamlit interface
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_dietitian():
    """Test the AI Dietitian service"""
    print("🧪 Testing AI Dietitian Service...")
    
    try:
        from ai_dietitian import AIDietitian
        
        # Initialize AI dietitian
        ai_dietitian = AIDietitian()
        print("✅ AI Dietitian initialized successfully")
        
        # Test conversation
        conversation = [
            {"role": "user", "content": "Hi, I'm Sarah, 28 years old, female, 5'5", 160 lbs, want to lose 20 lbs"},
            {"role": "assistant", "content": "Hello Sarah! I'm Dr. Chen, your nutritionist. Tell me more about your lifestyle."},
            {"role": "user", "content": "I work 9-5, mostly sedentary, love Mediterranean food, beginner cook, no allergies"},
            {"role": "assistant", "content": "Great! What's your typical daily routine and food preferences?"},
            {"role": "user", "content": "Wake up 7 AM, breakfast at 8, lunch at 1 PM, dinner at 7 PM. Love fish, vegetables, pasta. Hate spicy food."}
        ]
        
        # Test profile extraction
        print("\n🔍 Testing profile extraction...")
        profile = ai_dietitian.extract_user_profile(conversation)
        
        if profile:
            print("✅ Profile extracted successfully!")
            print(f"   Name: {profile.name}")
            print(f"   Age: {profile.age}")
            print(f"   Goal: {profile.goal}")
            print(f"   Activity Level: {profile.activity_level}")
            print(f"   Cooking Skill: {profile.cooking_skill}")
            
            # Test diet plan generation
            print("\n🍽️ Testing diet plan generation...")
            plan = ai_dietitian.create_diet_plan(profile)
            
            if plan:
                print("✅ Diet plan generated successfully!")
                print(f"   Days planned: {len(plan.daily_plans)}")
                print(f"   Total calories (weekly): {plan.weekly_summary.get('total_calories', 'N/A')}")
                print(f"   Shopping list items: {len(plan.shopping_list)}")
                
                return profile, plan
            else:
                print("❌ Failed to generate diet plan")
                return profile, None
        else:
            print("❌ Failed to extract profile")
            return None, None
            
    except Exception as e:
        print(f"❌ Error testing AI Dietitian: {e}")
        return None, None

def test_pdf_generation(profile, plan):
    """Test the PDF generation service"""
    print("\n🧪 Testing PDF Generation Service...")
    
    try:
        from pdf_generator import DietPlanPDFGenerator
        
        if not profile or not plan:
            print("❌ Cannot test PDF generation without profile and plan")
            return False
        
        # Initialize PDF generator
        pdf_generator = DietPlanPDFGenerator()
        print("✅ PDF Generator initialized successfully")
        
        # Generate PDF
        print("📄 Generating PDF...")
        pdf_path = pdf_generator.generate_diet_plan_pdf(plan)
        
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF generated successfully!")
            print(f"   File: {pdf_path}")
            print(f"   Size: {file_size} bytes")
            
            # Clean up
            os.remove(pdf_path)
            print("   Temporary file cleaned up")
            return True
        else:
            print("❌ PDF file not found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing PDF generation: {e}")
        return False

def test_models():
    """Test the Pydantic models"""
    print("🧪 Testing Pydantic Models...")
    
    try:
        from models import UserProfile, ActivityLevel, Goal, DietaryRestriction
        
        # Test model creation
        test_profile = UserProfile(
            name="Test User",
            age=30,
            gender="female",
            height_cm=165.0,
            weight_kg=70.0,
            target_weight_kg=65.0,
            activity_level=ActivityLevel.MODERATELY_ACTIVE,
            goal=Goal.WEIGHT_LOSS,
            dietary_restrictions=[DietaryRestriction.NONE],
            allergies=[],
            preferences=["Mediterranean", "vegetables"],
            dislikes=["spicy food"],
            daily_routine={"wake_up": "7:00 AM", "bedtime": "10:00 PM"},
            cooking_skill="intermediate",
            budget_constraint=None,
            cultural_preferences=["Mediterranean"]
        )
        
        print("✅ UserProfile model created successfully")
        print(f"   Name: {test_profile.name}")
        print(f"   Goal: {test_profile.goal}")
        print(f"   Activity Level: {test_profile.activity_level}")
        
        # Test JSON serialization
        json_data = test_profile.json()
        print("✅ JSON serialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 AI Diet Planner - Component Testing Demo")
    print("=" * 50)
    
    # Check environment
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please create a .env file with your OpenAI API key")
        return
    
    print("✅ Environment variables loaded")
    
    # Test components
    models_ok = test_models()
    profile, plan = test_ai_dietitian()
    pdf_ok = test_pdf_generation(profile, plan)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"   Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"   AI Dietitian: {'✅ PASS' if profile and plan else '❌ FAIL'}")
    print(f"   PDF Generation: {'✅ PASS' if pdf_ok else '❌ FAIL'}")
    
    if models_ok and profile and plan and pdf_ok:
        print("\n🎉 All components working correctly!")
        print("   You can now run the full application with: streamlit run app.py")
    else:
        print("\n⚠️  Some components failed. Check the error messages above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
