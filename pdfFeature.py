"""
pdf_export.py
PDF Export for Recipe App - Works with your exact format
"""

import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io
import re


def parse_instructions(instructions):
    """
    Convert instructions string to list
    
    Handles:
        "1. Step one\n2. Step two" → ["Step one", "Step two"]
    """
    if isinstance(instructions, list):
        return instructions
    
    if isinstance(instructions, str):
        # Split by newlines
        lines = instructions.strip().split('\n')
        
        # Remove empty lines and leading numbers
        steps = []
        for line in lines:
            line = line.strip()
            if line:
                # Remove leading "1.", "2.", etc.
                line = re.sub(r'^\d+\.\s*', '', line)
                if line:
                    steps.append(line)
        
        return steps
    
    return []


def export_recipe_to_pdf(recipe):
    """
    Create a beautifully formatted PDF from your recipe format
    
    Works with your exact recipe structure including:
    - id, name, cuisine, ingredients (list)
    - instructions (string with numbered steps)
    - cooking_time, prep_time, difficulty, servings
    - calories_per_serving, dietary_info, tips
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=26,
        textColor=colors.HexColor('#2E86AB'),
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#A23B72'),
        spaceBefore=20,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    )
    
    # Title
    story.append(Paragraph(recipe['name'], title_style))
    
    # Cuisine
    if 'cuisine' in recipe:
        story.append(Paragraph(f"{recipe['cuisine']} Cuisine", subtitle_style))
    
    # Info table (time, difficulty, servings, calories)
    info_data = []
    
    if 'prep_time' in recipe:
        info_data.append(['Prep Time:', recipe['prep_time']])
    if 'cooking_time' in recipe:
        info_data.append(['Cooking Time:', recipe['cooking_time']])
    if 'difficulty' in recipe:
        info_data.append(['Difficulty:', recipe['difficulty']])
    if 'servings' in recipe:
        info_data.append(['Servings:', str(recipe['servings'])])
    if 'calories_per_serving' in recipe:
        info_data.append(['Calories:', f"{recipe['calories_per_serving']} per serving"])
    
    if info_data:
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#555555')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
    
    # Dietary info
    if 'dietary_info' in recipe and recipe['dietary_info']:
        dietary_style = ParagraphStyle(
            'Dietary',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#888888'),
            leftIndent=10,
            spaceAfter=15
        )
        story.append(Paragraph(f"<i>Contains: {recipe['dietary_info']}</i>", dietary_style))
    
    # Ingredients Section
    story.append(Paragraph("Ingredients", heading_style))
    
    ingredients_data = [[f"☑  {ing}"] for ing in recipe['ingredients']]
    ingredients_table = Table(ingredients_data, colWidths=[5.5*inch])
    ingredients_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('LEFTPADDING', (0, 0), (-1, -1), 25),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9FA')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ]))
    story.append(ingredients_table)
    story.append(Spacer(1, 25))
    
    # Instructions Section
    story.append(Paragraph("Instructions", heading_style))
    
    # Parse instructions (convert string to list)
    instructions = parse_instructions(recipe['instructions'])
    
    for i, instruction in enumerate(instructions, 1):
        inst_style = ParagraphStyle(
            'Instruction',
            parent=styles['Normal'],
            fontSize=11,
            leftIndent=30,
            firstLineIndent=-15,
            leading=18,
            spaceAfter=12
        )
        story.append(Paragraph(f"<b>{i}.</b> {instruction}", inst_style))
    
    # Tips section
    if 'tips' in recipe and recipe['tips']:
        story.append(Spacer(1, 20))
        
        tips_heading = ParagraphStyle(
            'TipsHeading',
            parent=heading_style,
            fontSize=14,
            textColor=colors.HexColor('#F4A261')
        )
        story.append(Paragraph("💡 Chef's Tips", tips_heading))
        
        tips_style = ParagraphStyle(
            'Tips',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#555555'),
            leftIndent=20,
            rightIndent=20,
            leading=16,
            spaceBefore=10
        )
        
        # Add background box for tips
        tips_data = [[recipe['tips']]]
        tips_table = Table(tips_data, colWidths=[5.5*inch])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
            ('PADDING', (0, 0), (-1, -1), 15),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#555555')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#F4A261')),
        ]))
        story.append(tips_table)
    
    # Footer
    story.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#AAAAAA'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    
    buffer.seek(0)
    return buffer.getvalue()


def create_pdf_download_button(recipe, button_label="📄 Download as PDF"):
    """
    Create a Streamlit download button for recipe PDF
    
    Args:
        recipe (dict): Your recipe with the exact format you showed
        button_label (str): Button text
    
    Usage:
        create_pdf_download_button(recipe)
    """
    try:
        # Generate PDF
        pdf_bytes = export_recipe_to_pdf(recipe)
        
        # Create safe filename
        filename = recipe['name'].replace(' ', '_').replace('/', '-')
        # Remove special characters
        filename = re.sub(r'[^\w\-]', '', filename)
        filename = f"{filename}.pdf"
        
        # Download button
        st.download_button(
            label=button_label,
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
            type="primary",
            key=f"pdf_{recipe['name'].replace(' ', '_').lower()}" 
        )
    
    except KeyError as e:
        st.error(f"Missing recipe field: {e}")
        st.write("Recipe data:", recipe)
    
    except Exception as e:
        st.error(f"Error creating PDF: {e}")
        import traceback
        st.code(traceback.format_exc())


def export_multiple_recipes_to_pdf(recipes, collection_name="My Recipe Collection"):
    """
    Export multiple recipes to a single PDF
    
    Args:
        recipes (list): List of recipe dicts
        collection_name (str): Name for the collection
    
    Returns:
        bytes: PDF file content
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    styles = getSampleStyleSheet()
    story = []
    
    # Cover page
    cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Title'],
        fontSize=32,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(collection_name, cover_title))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"{len(recipes)} Delicious Recipes", styles['Heading2']))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y')}",
        styles['Normal']
    ))
    
    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    
    # Each recipe (simplified version for collection)
    for i, recipe in enumerate(recipes):
        # Title
        story.append(Paragraph(recipe['name'], styles['Title']))
        
        # Quick info
        if 'cuisine' in recipe:
            story.append(Paragraph(f"<i>{recipe['cuisine']} Cuisine</i>", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Ingredients
        story.append(Paragraph("Ingredients", styles['Heading2']))
        for ing in recipe['ingredients']:
            story.append(Paragraph(f"• {ing}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Instructions
        story.append(Paragraph("Instructions", styles['Heading2']))
        instructions = parse_instructions(recipe['instructions'])
        for j, inst in enumerate(instructions, 1):
            story.append(Paragraph(f"{j}. {inst}", styles['Normal']))
            story.append(Spacer(1, 4))
        
        # Page break between recipes (except last)
        if i < len(recipes) - 1:
            story.append(PageBreak())
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()