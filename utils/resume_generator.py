# utils/resume_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import json
from datetime import datetime
from config import Config

def generate_resume_pdf(user_data, template='modern'):
    """Generate a resume PDF based on user data and selected template - ENGLISH ONLY"""
    
    # Create output directory if it doesn't exist
    output_dir = Config.UPLOAD_FOLDER
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = f"resume_{user_data['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    # Choose template - all templates generate English resumes
    if template == 'classic':
        return generate_classic_resume(user_data, filepath)
    elif template == 'compact':
        return generate_compact_resume(user_data, filepath)
    elif template == 'executive':
        return generate_executive_resume(user_data, filepath)
    else:  # modern (default)
        return generate_modern_resume(user_data, filepath)

def generate_modern_resume(user_data, filepath):
    """Generate modern style resume in English"""
    doc = SimpleDocTemplate(filepath, pagesize=letter, 
                          topMargin=0.5*inch, bottomMargin=0.5*inch,
                          leftMargin=0.5*inch, rightMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    
    # Custom styles for modern template
    styles.add(ParagraphStyle(
        name='TitleModern',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#007BFF'),
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeaderModern',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#007BFF'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='ProfessionalSummary',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    ))
    
    story = []
    
    # Header with blue accent
    full_name = user_data.get('full_name', 'Professional').upper()
    header_table_data = [
        [Paragraph(full_name, styles['TitleModern'])]
    ]
    header_table = Table(header_table_data, colWidths=[7.5*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#007BFF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [0, 0, 10, 10]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    
    # Contact Information
    contact_info = []
    if user_data.get('mobile'):
        contact_info.append(f"Mobile: {user_data['mobile']}")
    if user_data.get('email'):
        contact_info.append(f"Email: {user_data['email']}")
    if user_data.get('address'):
        contact_info.append(f"Address: {user_data['address']}")
    
    if contact_info:
        contact_text = " | ".join(contact_info)
        contact_paragraph = Paragraph(contact_text, styles['Normal'])
        story.append(contact_paragraph)
        story.append(Spacer(1, 15))
    
    # Professional Summary
    profession = user_data.get('profession', 'Professional')
    verification_data = user_data.get('verification_data', {})
    
    story.append(Paragraph('PROFESSIONAL SUMMARY', styles['SectionHeaderModern']))
    
    summary_parts = []
    if profession:
        summary_parts.append(f"Experienced {profession}")
    
    experience_years = verification_data.get('experience_years')
    if experience_years:
        summary_parts.append(f"with {experience_years} years of professional experience")
    
    specialization = verification_data.get('specialization')
    if specialization:
        summary_parts.append(f"specializing in {specialization}")
    
    skills = verification_data.get('skills') or verification_data.get('tools')
    if skills:
        summary_parts.append(f"skilled in {skills}")
    
    # Default summary if no specific data
    if not summary_parts:
        summary_parts.append(f"Professional {profession} with verified credentials and proven track record")
    
    summary = ". ".join(summary_parts) + "."
    story.append(Paragraph(summary, styles['ProfessionalSummary']))
    story.append(Spacer(1, 15))
    
    # Professional Details Table
    professional_data = []
    
    # Add profession-specific details
    for key, value in verification_data.items():
        if value and key not in ['experience_years']:  # experience handled in summary
            label = key.replace('_', ' ').title()
            professional_data.append([label, str(value)])
    
    if professional_data:
        story.append(Paragraph('PROFESSIONAL DETAILS', styles['SectionHeaderModern']))
        
        # Create table with professional details
        details_table = Table(professional_data, colWidths=[2*inch, 4*inch])
        details_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LINEBELOW', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f8f9fa')),
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 15))
    
    # Experience Summary
    if experience_years:
        story.append(Paragraph('EXPERIENCE SUMMARY', styles['SectionHeaderModern']))
        exp_text = f"<b>Total Experience:</b> {experience_years} years in {profession} field"
        story.append(Paragraph(exp_text, styles['Normal']))
        story.append(Spacer(1, 10))
    
    # Verification Status
    story.append(Paragraph('VERIFICATION STATUS', styles['SectionHeaderModern']))
    verification_status = [
        ["Identity", "Verified" if user_data.get('id_verified') else "Pending"],
        ["Professional Details", "Verified"],
        ["Mobile Number", "Verified"]
    ]
    
    status_table = Table(verification_status, colWidths=[2*inch, 1*inch])
    status_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007BFF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(status_table)
    story.append(Spacer(1, 10))
    
    # Footer note
    footer_note = Paragraph(
        "<i>This resume was generated using BlueCollarResume - Verified Professional Profile</i>",
        ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
    )
    story.append(footer_note)
    
    doc.build(story)
    return filepath

def generate_classic_resume(user_data, filepath):
    """Generate classic style resume in English"""
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Header
    story.append(Paragraph(user_data.get('full_name', 'Professional').upper(), styles['Title']))
    story.append(Spacer(1, 12))
    
    # Contact Info
    contact_lines = []
    if user_data.get('mobile'):
        contact_lines.append(f"Phone: {user_data['mobile']}")
    if user_data.get('email'):
        contact_lines.append(f"Email: {user_data['email']}")
    if user_data.get('address'):
        contact_lines.append(f"Address: {user_data['address']}")
    
    story.append(Paragraph(" | ".join(contact_lines), styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Professional Summary
    profession = user_data.get('profession', 'Professional')
    verification_data = user_data.get('verification_data', {})
    
    story.append(Paragraph('Professional Summary', styles['Heading2']))
    summary = f"Experienced {profession} with verified credentials and professional background."
    story.append(Paragraph(summary, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Professional Experience
    story.append(Paragraph('Professional Details', styles['Heading2']))
    
    for key, value in verification_data.items():
        if value:
            label = key.replace('_', ' ').title()
            story.append(Paragraph(f"<b>{label}:</b> {value}", styles['Normal']))
    
    story.append(Spacer(1, 15))
    
    # Verification Status
    story.append(Paragraph('Verification Status', styles['Heading2']))
    status = "Fully Verified" if user_data.get('id_verified') else "Verification Pending"
    story.append(Paragraph(f"<b>Status:</b> {status}", styles['Normal']))
    
    doc.build(story)
    return filepath

def generate_compact_resume(user_data, filepath):
    """Generate compact one-page resume in English"""
    doc = SimpleDocTemplate(filepath, pagesize=letter, 
                          topMargin=0.25*inch, bottomMargin=0.25*inch,
                          leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Compact header
    header_data = [
        [Paragraph("<b>" + user_data.get('full_name', 'Professional') + "</b>", styles['Normal']),
         Paragraph(user_data.get('profession', 'Professional'), styles['Normal'])],
        [Paragraph(user_data.get('mobile', ''), styles['Normal']),
         Paragraph(user_data.get('email', ''), styles['Normal'])]
    ]
    
    header_table = Table(header_data, colWidths=[3*inch, 3*inch])
    header_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, 0), 'Helvetica-Bold', 14),
        ('FONT', (1, 0), (1, 0), 'Helvetica', 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(header_table)
    story.append(Spacer(1, 15))
    
    # Quick summary
    verification_data = user_data.get('verification_data', {})
    if verification_data:
        story.append(Paragraph('<b>Key Qualifications</b>', styles['Normal']))
        for key, value in verification_data.items():
            if value and key in ['experience_years', 'specialization', 'license_number']:
                label = key.replace('_', ' ').title()
                story.append(Paragraph(f"• {label}: {value}", styles['Normal']))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph('<b>Status:</b> Verified Professional', styles['Normal']))
    
    doc.build(story)
    return filepath

def generate_executive_resume(user_data, filepath):
    """Generate executive style resume in English"""
    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Executive header
    story.append(Paragraph(user_data.get('full_name', 'EXECUTIVE PROFESSIONAL'), styles['Title']))
    story.append(Paragraph(user_data.get('profession', 'Senior Professional').upper(), styles['Heading2']))
    story.append(Spacer(1, 15))
    
    # Executive summary
    profession = user_data.get('profession', 'Professional')
    verification_data = user_data.get('verification_data', {})
    
    exec_summary = f"Accomplished {profession} with demonstrated expertise and verified professional credentials. "
    exec_summary += f"Bringing {verification_data.get('experience_years', 'extensive')} years of comprehensive experience "
    exec_summary += "and a proven track record of reliability and professional excellence."
    
    story.append(Paragraph('EXECUTIVE PROFILE', styles['Heading2']))
    story.append(Paragraph(exec_summary, styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Core competencies
    story.append(Paragraph('CORE COMPETENCIES', styles['Heading2']))
    
    competencies = []
    for key, value in verification_data.items():
        if value and key not in ['experience_years']:
            label = key.replace('_', ' ').title()
            competencies.append(f"• {label}: {value}")
    
    if competencies:
        for comp in competencies[:6]:  # Limit to 6 key competencies
            story.append(Paragraph(comp, styles['Normal']))
    
    story.append(Spacer(1, 15))
    
    # Professional verification
    story.append(Paragraph('PROFESSIONAL VERIFICATION', styles['Heading2']))
    verification_status = "FULLY VERIFIED" if user_data.get('id_verified') else "UNDER REVIEW"
    story.append(Paragraph(f"<b>Status:</b> {verification_status}", styles['Normal']))
    story.append(Paragraph("<b>Background Check:</b> Completed", styles['Normal']))
    story.append(Paragraph("<b>Identity Verification:</b> Confirmed", styles['Normal']))
    
    doc.build(story)
    return filepath