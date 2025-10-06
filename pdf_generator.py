from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from typing import List, Dict, Any
import os
from datetime import datetime
from models import WeeklyDietPlan, UserProfile, DailyPlan, MealPlan

class DietPlanPDFGenerator:
    """PDF generator for diet plans using ReportLab"""
    
    def __init__(self):
        """Initialize the PDF generator with styles"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Subtitle style
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'CustomSection',
            parent=self.styles['Heading3'],
            fontSize=16,
            spaceAfter=15,
            textColor=colors.darkblue
        )
        
        # Normal text style
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        # Meal name style
        self.meal_style = ParagraphStyle(
            'CustomMeal',
            parent=self.styles['Heading4'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.darkred
        )
    
    def generate_diet_plan_pdf(self, diet_plan: WeeklyDietPlan, output_path: str = None) -> str:
        """Generate a comprehensive PDF diet plan"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"diet_plan_{timestamp}.pdf"
        
        # Create the PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add title page
        story.extend(self._create_title_page(diet_plan.user_profile))
        story.append(PageBreak())
        
        # Add user profile summary
        story.extend(self._create_profile_summary(diet_plan.user_profile))
        story.append(PageBreak())
        
        # Add weekly overview
        story.extend(self._create_weekly_overview(diet_plan))
        story.append(PageBreak())
        
        # Add daily meal plans
        for daily_plan in diet_plan.daily_plans:
            story.extend(self._create_daily_plan(daily_plan))
            story.append(PageBreak())
        
        # Add shopping list
        story.extend(self._create_shopping_list(diet_plan.shopping_list))
        story.append(PageBreak())
        
        # Add recommendations
        story.extend(self._create_recommendations(diet_plan.recommendations))
        
        # Build the PDF
        doc.build(story)
        return output_path
    
    def _create_title_page(self, user_profile: UserProfile) -> List:
        """Create the title page of the PDF"""
        elements = []
        
        # Main title
        title = Paragraph("Personalized Diet Plan", self.title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph(f"Created for {user_profile.name}", self.subtitle_style)
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Creation date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y')}"
        date_para = Paragraph(date_text, self.normal_style)
        elements.append(date_para)
        elements.append(Spacer(1, 0.5*inch))
        
        # User info table
        user_info = [
            ["Name:", user_profile.name],
            ["Age:", f"{user_profile.age} years"],
            ["Gender:", user_profile.gender],
            ["Height:", f"{user_profile.height_cm} cm"],
            ["Current Weight:", f"{user_profile.weight_kg} kg"],
            ["Target Weight:", f"{user_profile.target_weight_kg} kg" if user_profile.target_weight_kg else "Not specified"],
            ["Goal:", user_profile.goal.replace('_', ' ').title()],
            ["Activity Level:", user_profile.activity_level.replace('_', ' ').title()]
        ]
        
        user_table = Table(user_info, colWidths=[2*inch, 3*inch])
        user_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(user_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_profile_summary(self, user_profile: UserProfile) -> List:
        """Create the user profile summary section"""
        elements = []
        
        # Section header
        header = Paragraph("Your Profile Summary", self.section_style)
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Dietary restrictions
        if user_profile.dietary_restrictions and user_profile.dietary_restrictions != ["none"]:
            restrictions_text = f"<b>Dietary Restrictions:</b> {', '.join(user_profile.dietary_restrictions)}"
            elements.append(Paragraph(restrictions_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Allergies
        if user_profile.allergies:
            allergies_text = f"<b>Food Allergies:</b> {', '.join(user_profile.allergies)}"
            elements.append(Paragraph(allergies_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Preferences
        if user_profile.preferences:
            preferences_text = f"<b>Food Preferences:</b> {', '.join(user_profile.preferences)}"
            elements.append(Paragraph(preferences_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Dislikes
        if user_profile.dislikes:
            dislikes_text = f"<b>Foods to Avoid:</b> {', '.join(user_profile.dislikes)}"
            elements.append(Paragraph(dislikes_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        # Cooking skill
        cooking_text = f"<b>Cooking Skill Level:</b> {user_profile.cooking_skill}"
        elements.append(Paragraph(cooking_text, self.normal_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Cultural preferences
        if user_profile.cultural_preferences:
            cultural_text = f"<b>Cultural Preferences:</b> {', '.join(user_profile.cultural_preferences)}"
            elements.append(Paragraph(cultural_text, self.normal_style))
            elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _create_weekly_overview(self, diet_plan: WeeklyDietPlan) -> List:
        """Create the weekly overview section"""
        elements = []
        
        # Section header
        header = Paragraph("Weekly Overview", self.section_style)
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Weekly summary table
        summary_data = [
            ["Metric", "Value"],
            ["Total Calories (weekly)", f"{diet_plan.weekly_summary.get('total_calories', 'N/A')}"],
            ["Average Protein (g/day)", f"{diet_plan.weekly_summary.get('avg_protein', 'N/A')}"],
            ["Average Carbs (g/day)", f"{diet_plan.weekly_summary.get('avg_carbs', 'N/A')}"],
            ["Average Fat (g/day)", f"{diet_plan.weekly_summary.get('avg_fat', 'N/A')}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        return elements
    
    def _create_daily_plan(self, daily_plan: DailyPlan) -> List:
        """Create a daily meal plan section"""
        elements = []
        
        # Day header
        day_header = Paragraph(f"{daily_plan.day}", self.subtitle_style)
        elements.append(day_header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Daily nutrition summary
        nutrition_data = [
            ["Calories", "Protein (g)", "Carbs (g)", "Fat (g)"],
            [str(daily_plan.total_calories), str(daily_plan.total_protein), 
             str(daily_plan.total_carbs), str(daily_plan.total_fat)]
        ]
        
        nutrition_table = Table(nutrition_data, colWidths=[1.25*inch, 1.25*inch, 1.25*inch, 1.25*inch])
        nutrition_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(nutrition_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Meals
        for meal in daily_plan.meals:
            elements.extend(self._create_meal_section(meal))
            elements.append(Spacer(1, 0.1*inch))
        
        # Daily notes
        if daily_plan.notes:
            notes_text = f"<b>Notes:</b> {daily_plan.notes}"
            elements.append(Paragraph(notes_text, self.normal_style))
        
        return elements
    
    def _create_meal_section(self, meal: MealPlan) -> List:
        """Create a meal section"""
        elements = []
        
        # Meal header
        meal_header = Paragraph(f"{meal.meal_time.title()}: {meal.meal_name}", self.meal_style)
        elements.append(meal_header)
        
        # Meal description
        if meal.description:
            desc_para = Paragraph(meal.description, self.normal_style)
            elements.append(desc_para)
        
        # Ingredients
        if meal.ingredients:
            ingredients_text = f"<b>Ingredients:</b> {', '.join(meal.ingredients)}"
            elements.append(Paragraph(ingredients_text, self.normal_style))
        
        # Instructions
        if meal.instructions:
            instructions_text = "<b>Instructions:</b>"
            elements.append(Paragraph(instructions_text, self.normal_style))
            for i, instruction in enumerate(meal.instructions, 1):
                instruction_para = Paragraph(f"{i}. {instruction}", self.normal_style)
                elements.append(instruction_para)
        
        # Nutrition info
        if meal.nutrition_info:
            nutrition_text = f"<b>Nutrition:</b> {meal.nutrition_info.get('calories', 'N/A')} cal, " \
                           f"{meal.nutrition_info.get('protein', 'N/A')}g protein, " \
                           f"{meal.nutrition_info.get('carbs', 'N/A')}g carbs, " \
                           f"{meal.nutrition_info.get('fat', 'N/A')}g fat"
            elements.append(Paragraph(nutrition_text, self.normal_style))
        
        # Prep and cooking time
        time_text = f"<b>Prep Time:</b> {meal.prep_time} | <b>Cooking Time:</b> {meal.cooking_time} | <b>Difficulty:</b> {meal.difficulty}"
        elements.append(Paragraph(time_text, self.normal_style))
        
        return elements
    
    def _create_shopping_list(self, shopping_list: List[str]) -> List:
        """Create the shopping list section"""
        elements = []
        
        # Section header
        header = Paragraph("Shopping List", self.section_style)
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Shopping list items
        if shopping_list:
            for item in shopping_list:
                item_para = Paragraph(f"• {item}", self.normal_style)
                elements.append(item_para)
        else:
            no_items = Paragraph("No shopping list items available.", self.normal_style)
            elements.append(no_items)
        
        return elements
    
    def _create_recommendations(self, recommendations: List[str]) -> List:
        """Create the recommendations section"""
        elements = []
        
        # Section header
        header = Paragraph("Personalized Recommendations", self.section_style)
        elements.append(header)
        elements.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        if recommendations:
            for i, recommendation in enumerate(recommendations, 1):
                rec_para = Paragraph(f"{i}. {recommendation}", self.normal_style)
                elements.append(rec_para)
                elements.append(Spacer(1, 0.1*inch))
        else:
            no_recs = Paragraph("No specific recommendations available.", self.normal_style)
            elements.append(no_recs)
        
        return elements
