import json
import openai
from typing import List, Dict, Any, Optional
from models import UserProfile, WeeklyDietPlan
from config import Config

class AIDietitian:
    """AI Dietitian service using various prompt engineering techniques"""
    
    def __init__(self):
        """Initialize the AI Dietitian with OpenAI configuration"""
        Config.validate()
        openai.api_key = Config.OPENAI_API_KEY
        self.model = Config.OPENAI_MODEL
        
        # Role-based system prompt
        self.system_prompt = self._get_system_prompt()
        
        # Few-shot examples for conversation
        self.few_shot_examples = self._get_few_shot_examples()
        
        # Chain-of-Thought reasoning prompts
        self.cot_prompts = self._get_cot_prompts()
    
    def _get_system_prompt(self) -> str:
        """Role-based system prompt defining the AI dietitian persona"""
        return """You are Dr. Sarah Chen, a certified clinical nutritionist and registered dietitian with over 15 years of experience. You specialize in creating personalized, evidence-based diet plans that consider individual preferences, cultural backgrounds, and lifestyle factors.

Your approach is:
- Warm, empathetic, and professional
- Evidence-based and scientifically sound
- Culturally sensitive and inclusive
- Practical and sustainable for real-life implementation
- Focused on long-term health outcomes

You should:
1. Ask thoughtful, targeted questions to understand the user's complete health profile
2. Provide clear, actionable advice
3. Consider medical conditions, allergies, and dietary restrictions
4. Offer practical meal suggestions that fit the user's lifestyle
5. Explain the reasoning behind your recommendations
6. Be encouraging and supportive throughout the conversation

Remember: You're not just providing meal plans; you're building a relationship and understanding the user's unique situation to create the most effective nutrition strategy."""
    
    def _get_few_shot_examples(self) -> List[Dict[str, str]]:
        """Few-shot examples to guide the conversation flow"""
        return [
            {
                "user": "Hi, I want to lose weight",
                "assistant": "Hello! I'm Dr. Sarah Chen, and I'm here to help you create a personalized weight loss plan. To get started, I'd like to understand your current situation better. Could you tell me:\n\n1. What's your current weight and height?\n2. How much weight would you like to lose?\n3. What's your typical daily routine like?\n4. Do you have any dietary restrictions or food allergies?\n5. What's your cooking experience level?\n\nThis will help me create a plan that fits your lifestyle and preferences."
            },
            {
                "user": "I'm 30, female, 5'6", 180 lbs, want to lose 30 lbs",
                "assistant": "Thank you for sharing those details! I can see you're looking to make a significant change, and I'm here to support you every step of the way. Let me ask a few more questions to create the most effective plan:\n\n1. What's your current activity level? (e.g., mostly sedentary, light exercise, moderate exercise)\n2. What's your typical work schedule and daily routine?\n3. Do you have any favorite foods or cuisines you'd like to include?\n4. Are there any foods you absolutely dislike?\n5. What's your experience with meal planning and cooking?\n6. Do you have any medical conditions or take medications that might affect your diet?\n\nBased on your stats, a healthy weight loss goal would be 1-2 pounds per week, which is sustainable and safe. This would take about 4-6 months to reach your goal weight of 150 lbs."
            },
            {
                "user": "I work 9-5, mostly sedentary, love Italian and Mexican food, beginner cook",
                "assistant": "Perfect! I can see you have a busy work schedule and enjoy flavorful cuisines. Let me gather a bit more information to tailor your plan:\n\n1. What time do you usually wake up and go to bed?\n2. Do you prefer to cook meals in advance or prepare them fresh each day?\n3. Are you open to trying new ingredients or do you prefer familiar foods?\n4. Do you have any food allergies or intolerances?\n5. What's your typical budget for groceries?\n\nBased on what you've shared, I'm thinking of a plan that includes:\n- Quick breakfast options for busy mornings\n- Make-ahead lunch ideas that travel well to work\n- Simple dinner recipes inspired by your favorite cuisines\n- Weekend meal prep strategies to set you up for success\n\nThis approach will help you stay on track even with your busy schedule while enjoying the foods you love!"
            }
        ]
    
    def _get_cot_prompts(self) -> Dict[str, str]:
        """Chain-of-Thought reasoning prompts for different tasks"""
        return {
            "profile_extraction": """Let me think through this step by step to extract the user's complete profile:

1. First, I need to identify all the personal information mentioned
2. Then, I should categorize their preferences and restrictions
3. Next, I'll assess their lifestyle and routine patterns
4. Finally, I'll determine their goals and constraints

Let me analyze the conversation systematically...""",
            
            "meal_planning": """Now let me think through creating a personalized meal plan:

1. Based on the user's profile, what are their caloric needs?
2. How should I distribute calories across meals given their routine?
3. What foods align with their preferences and restrictions?
4. How can I make the plan practical for their cooking skills?
5. What cultural elements should I incorporate?

Let me work through this systematically...""",
            
            "nutrition_calculation": """Let me calculate the nutritional requirements step by step:

1. First, I'll determine the Basal Metabolic Rate (BMR)
2. Then, I'll apply the activity multiplier
3. Next, I'll adjust for the weight goal (deficit/surplus)
4. Finally, I'll distribute macronutrients appropriately

Let me do the math..."""
        }
    
    def chat(self, message: str, conversation_history: List[Dict[str, str]]) -> str:
        """Main chat method with the AI dietitian"""
        # Build the conversation context
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add few-shot examples for context
        for example in self.few_shot_examples:
            messages.append({"role": "user", "content": example["user"]})
            messages.append({"role": "assistant", "content": example["assistant"]})
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again. Error: {str(e)}"
    
    def extract_user_profile(self, conversation_history: List[Dict[str, str]]) -> Optional[UserProfile]:
        """Extract structured user profile from conversation using Chain-of-Thought reasoning"""
        cot_prompt = self.cot_prompts["profile_extraction"]
        
        extraction_prompt = f"""Based on the conversation history below, extract the user's complete profile in a structured JSON format.

{cot_prompt}

Conversation History:
{json.dumps(conversation_history, indent=2)}

Please extract all available information and return ONLY a valid JSON object that matches this structure:
{{
    "name": "string",
    "age": integer,
    "gender": "string", 
    "height_cm": float,
    "weight_kg": float,
    "target_weight_kg": float or null,
    "activity_level": "sedentary|lightly_active|moderately_active|very_active|extremely_active",
    "goal": "weight_loss|weight_gain|maintenance|muscle_gain|general_health",
    "dietary_restrictions": ["list", "of", "restrictions"],
    "allergies": ["list", "of", "allergies"],
    "preferences": ["list", "of", "preferences"],
    "dislikes": ["list", "of", "dislikes"],
    "daily_routine": {{"key": "value"}},
    "cooking_skill": "string",
    "budget_constraint": "string" or null,
    "cultural_preferences": ["list", "of", "preferences"]
}}

If any information is not available, use null or empty arrays as appropriate. Return ONLY the JSON, no additional text."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data extraction specialist. Extract user information and return ONLY valid JSON."},
                    {"role": "user", "content": extraction_prompt}
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            content = response.choices[0].message.content.strip()
            # Clean up the response to extract just the JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            profile_data = json.loads(content)
            return UserProfile(**profile_data)
            
        except Exception as e:
            print(f"Error extracting user profile: {e}")
            return None
    
    def create_diet_plan(self, user_profile: UserProfile) -> Optional[WeeklyDietPlan]:
        """Create a personalized weekly diet plan using Chain-of-Thought reasoning"""
        cot_prompt = self.cot_prompts["meal_planning"]
        
        plan_prompt = f"""Create a personalized weekly diet plan for the user based on their profile.

{cot_prompt}

User Profile:
{user_profile.json(indent=2)}

Please create a complete weekly diet plan and return ONLY a valid JSON object that matches this structure:
{{
    "user_profile": {{...}},
    "daily_plans": [
        {{
            "day": "Monday",
            "meals": [
                {{
                    "meal_time": "breakfast",
                    "meal_name": "string",
                    "description": "string",
                    "ingredients": ["list", "of", "ingredients"],
                    "instructions": ["step", "by", "step", "instructions"],
                    "nutrition_info": {{"calories": integer, "protein": float, "carbs": float, "fat": float}},
                    "prep_time": "string",
                    "cooking_time": "string",
                    "difficulty": "string"
                }}
            ],
            "total_calories": integer,
            "total_protein": float,
            "total_carbs": float,
            "total_fat": float,
            "notes": "string"
        }}
    ],
    "weekly_summary": {{"total_calories": integer, "avg_protein": float, "avg_carbs": float, "avg_fat": float}},
    "recommendations": ["list", "of", "recommendations"],
    "shopping_list": ["list", "of", "items"],
    "created_date": "YYYY-MM-DD"
}}

Make the plan practical, culturally appropriate, and aligned with their goals and preferences. Return ONLY the JSON, no additional text."""

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a nutrition expert. Create personalized diet plans and return ONLY valid JSON."},
                    {"role": "user", "content": plan_prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content.strip()
            # Clean up the response to extract just the JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            
            plan_data = json.loads(content)
            return WeeklyDietPlan(**plan_data)
            
        except Exception as e:
            print(f"Error creating diet plan: {e}")
            return None
