#!/usr/bin/env python3
"""
CodePulse PDF Report Generator
Generates professional PDF reports from activity data
"""

import sqlite3
import json
from datetime import datetime, timedelta
from collections import Counter
import os
from config import get_db_path, DATA_DIR

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def get_db_connection():
    """Create a database connection"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_7day_stats():
    """Get last 7 days of statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    labels = []
    data = []
    total_minutes = 0
    all_languages = []
    session_count = 0
    
    # Get last 7 days of data
    for i in range(7, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        labels.append(date)
        
        # Query total duration for this date
        query = """
        SELECT COUNT(*) as count, SUM(duration_sec) as total_duration
        FROM sessions 
        WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ?
        """
        cursor.execute(query, (date,))
        row = cursor.fetchone()
        
        duration_minutes = 0
        count = 0
        if row:
            duration_minutes = (row['total_duration'] or 0) / 60.0
            count = row['count'] or 0
            total_minutes += duration_minutes
            session_count += count
        
        data.append(round(duration_minutes, 2))
        
        # Get languages used on this date
        query = """
        SELECT DISTINCT language FROM sessions
        WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ? AND language IS NOT NULL
        """
        cursor.execute(query, (date,))
        for row in cursor.fetchall():
            all_languages.append(row['language'])
    
    # Get top language
    top_language = Counter(all_languages).most_common(1)[0][0] if all_languages else "N/A"
    unique_languages = list(set(all_languages))
    
    conn.close()
    
    return {
        "labels": labels,
        "data": data,
        "total_minutes": round(total_minutes, 2),
        "total_sessions": session_count,
        "languages": unique_languages,
        "top_language": top_language
    }

def get_language_distribution():
    """Get today's language distribution"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    query = """
    SELECT language, SUM(duration_sec) as total_duration, COUNT(*) as count
    FROM sessions
    WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ? AND language IS NOT NULL
    GROUP BY language
    ORDER BY total_duration DESC
    """
    
    cursor.execute(query, (today,))
    rows = cursor.fetchall()
    
    data = []
    for row in rows:
        minutes = round((row['total_duration'] or 0) / 60.0, 2)
        data.append({
            "language": row['language'],
            "minutes": minutes,
            "sessions": row['count']
        })
    
    conn.close()
    return data

def get_top_projects():
    """Get top project folders"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        SUBSTR(file, 1, INSTR(file, '/') - 1) as folder,
        language,
        SUM(duration_sec) as total_duration,
        COUNT(*) as session_count
    FROM sessions
    WHERE file IS NOT NULL AND TRIM(file) != ''
    GROUP BY folder, language
    ORDER BY total_duration DESC
    LIMIT 10
    """
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    projects = []
    for row in rows:
        folder = row['folder'] if row['folder'] else "root"
        duration_minutes = round((row['total_duration'] or 0) / 60.0, 2)
        
        projects.append({
            "folder": folder,
            "language": row['language'] or "Unknown",
            "minutes": duration_minutes,
            "sessions": row['session_count']
        })
    
    conn.close()
    return projects

def generate_pdf(filename='codepulse_report_2025.pdf'):
    """Generate PDF report"""
    
    if not HAS_REPORTLAB:
        print("Error: reportlab not installed")
        print("Install with: pip install reportlab")
        return False
    
    try:
        # Get data
        stats = get_7day_stats()
        languages = get_language_distribution()
        projects = get_top_projects()
        
        # Create PDF in data/ directory
        os.makedirs(str(DATA_DIR), exist_ok=True)
        pdf_path = os.path.join(str(DATA_DIR), filename)
        doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                                 rightMargin=72, leftMargin=72,
                                 topMargin=72, bottomMargin=18)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        # Title
        elements.append(Paragraph("💻 CodePulse Activity Report", title_style))
        elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary Statistics
        elements.append(Paragraph("📊 Summary Statistics (Last 7 Days)", heading_style))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Focus Time', f"{stats['total_minutes']} minutes"],
            ['Total Sessions', f"{stats['total_sessions']} sessions"],
            ['Languages Used', f"{len(stats['languages'])} languages"],
            ['Top Language', stats['top_language']],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Daily Activity
        elements.append(Paragraph("📈 Daily Activity (Last 7 Days)", heading_style))
        
        daily_data = [['Date', 'Focus Time (minutes)']]
        for label, minutes in zip(stats['labels'], stats['data']):
            daily_data.append([label, f"{minutes} min"])
        
        daily_table = Table(daily_data, colWidths=[2*inch, 3*inch])
        daily_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(daily_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Language Distribution
        if languages:
            elements.append(Paragraph("💬 Language Distribution (Today)", heading_style))
            
            lang_data = [['Language', 'Duration', 'Sessions']]
            for lang in languages:
                lang_data.append([
                    lang['language'],
                    f"{lang['minutes']} min",
                    f"{lang['sessions']}"
                ])
            
            lang_table = Table(lang_data, colWidths=[2*inch, 2*inch, 1.5*inch])
            lang_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(lang_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Top Projects
        if projects:
            elements.append(Paragraph("📁 Top Projects", heading_style))
            
            proj_data = [['Folder', 'Language', 'Duration', 'Sessions']]
            for proj in projects[:10]:
                proj_data.append([
                    proj['folder'],
                    proj['language'],
                    f"{proj['minutes']} min",
                    f"{proj['sessions']}"
                ])
            
            proj_table = Table(proj_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
            proj_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#45B7D1')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            
            elements.append(proj_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Footer
        footer_text = f"CodePulse • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} • Offline-First Activity Tracker"
        elements.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )))
        
        # Build PDF
        doc.build(elements)
        
        print(f"✅ PDF Report generated: {pdf_path}")
        print(f"   File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

if __name__ == '__main__':
    print("CodePulse PDF Report Generator")
    print("=" * 50)
    
    if not HAS_REPORTLAB:
        print("\n⚠️  reportlab is not installed")
        print("Install it with: pip install reportlab")
        print("\nOnce installed, run this script again:")
        print("  python pdf_generator.py")
    else:
        print("\nGenerating PDF report...")
        if generate_pdf('codepulse_report_2025.pdf'):
            print("\n✅ Report ready!")
            print("   Open: codepulse_report_2025.pdf")
        else:
            print("\n❌ Failed to generate report")
