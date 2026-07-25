import os
import re
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# List of common research report headings for auto-detection
REPORT_HEADINGS = {
    "introduction", "executive summary", "literature review", 
    "key findings", "benefits", "challenges", "analysis", 
    "future scope", "conclusion", "references", "summary", 
    "background", "methodology", "results", "discussion", 
    "recommendations", "overview", "objectives", "next steps"
}

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def check_if_heading(line):
    """
    Checks if a line of text is a section heading.
    Returns (is_heading, cleaned_text, level).
    """
    cleaned = line.strip()
    
    # Strip numbering prefixes (e.g., "1. Introduction" or "Section A: ")
    prefix_pattern = r'^(?:(?:[0-9]+(?:\.[0-9]+)*)|(?:[IVXLCDM]+)|(?:[A-Z]))[\s.:)-]+\s*'
    text_without_prefix = re.sub(prefix_pattern, '', cleaned, flags=re.IGNORECASE).strip()
    
    # Check if the text matches a known heading keyword
    if text_without_prefix.lower() in REPORT_HEADINGS:
        # Determine heading level based on sub-prefix (e.g., "1.2" is level 2)
        has_sub_prefix = re.match(r'^[0-9]+\.[0-9]+', cleaned)
        return True, text_without_prefix, (2 if has_sub_prefix else 1)
        
    # Check if the line is short, capitalized, and does not end with a period
    if len(cleaned) < 50 and cleaned and cleaned[0].isupper() and not cleaned.endswith('.'):
        return True, cleaned, 1
        
    return False, "", 0


def parse_report_text(report_text):
    """
    Parses the raw report text into structured elements (title, headings, lists, body text).
    This ensures consistent rendering across PDF and Word.
    """
    raw_lines = report_text.splitlines()
    
    title = ""
    start_index = 0
    
    # Extract the first non-empty line as the document title
    for i, line in enumerate(raw_lines):
        if line.strip():
            title = line.strip()
            start_index = i + 1
            break
            
    elements = []
    current_para_lines = []
    
    for line in raw_lines[start_index:]:
        stripped = line.strip()
        
        # Empty line ends the current body paragraph
        if not stripped:
            if current_para_lines:
                elements.append(('body', ' '.join(current_para_lines), 0))
                current_para_lines = []
            continue
            
        # Detect headings
        is_h, text, level = check_if_heading(stripped)
        if is_h:
            if current_para_lines:
                elements.append(('body', ' '.join(current_para_lines), 0))
                current_para_lines = []
            elements.append(('heading', text, level))
            continue
            
        # Detect bullet list items
        bullet_match = re.match(r'^[\-\*•]\s+(.*)$', stripped)
        if bullet_match:
            if current_para_lines:
                elements.append(('body', ' '.join(current_para_lines), 0))
                current_para_lines = []
            elements.append(('bullet', bullet_match.group(1).strip(), 1))
            continue
            
        # Detect numbered list items
        numbered_match = re.match(r'^(\d+|[a-zA-Z])[\.\)]\s+(.*)$', stripped)
        if numbered_match:
            if current_para_lines:
                elements.append(('body', ' '.join(current_para_lines), 0))
                current_para_lines = []
            prefix = f"{numbered_match.group(1)}. "
            elements.append(('numbered_list', prefix + numbered_match.group(2).strip(), 1))
            continue
            
        # Accumulate lines for a standard body paragraph
        current_para_lines.append(stripped)
        
    # Flush any remaining text in the buffer
    if current_para_lines:
        elements.append(('body', ' '.join(current_para_lines), 0))
        
    return title, elements


# =========================================================================
# PDF GENERATOR
# =========================================================================

def create_pdf_styles():
    """
    Creates custom ParagraphStyles for the PDF report.
    """
    styles = {}
    primary_color = colors.HexColor('#1A365D')    # Navy
    secondary_color = colors.HexColor('#4A5568')  # Slate
    body_color = colors.HexColor('#2D3748')       # Charcoal
    
    styles['Title'] = ParagraphStyle(
        'ReportTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=TA_CENTER,
        spaceAfter=15
    )
    
    styles['Heading1'] = ParagraphStyle(
        'ReportHeading1',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    styles['Heading2'] = ParagraphStyle(
        'ReportHeading2',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    styles['BodyText'] = ParagraphStyle(
        'ReportBodyText',
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=body_color,
        spaceBefore=0,
        spaceAfter=8
    )
    
    styles['Bullet'] = ParagraphStyle(
        'ReportBullet',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=body_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceBefore=0,
        spaceAfter=4
    )
    
    styles['NumberedList'] = ParagraphStyle(
        'ReportNumberedList',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=body_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceBefore=0,
        spaceAfter=4
    )
    
    return styles


def draw_page_number(canvas, doc):
    """Draws a simple running page number in the footer."""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#718096'))
    canvas.drawRightString(doc.pagesize[0] - 54, 38, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf(report, filename):
    """
    Generates a professionally styled PDF report from raw text.
    """
    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = create_pdf_styles()
    title, elements = parse_report_text(report)
    
    story = []

    if title:
        story.append(Paragraph(html.escape(title), styles['Title']))
        story.append(Spacer(1, 15))

    for el_type, text, level in elements:
        # html.escape prevents XML parser issues in ReportLab Paragraphs
        escaped_text = html.escape(text)

        if el_type == 'heading':
            style_name = 'Heading1' if level == 1 else 'Heading2'
            story.append(Paragraph(escaped_text, styles[style_name]))
        elif el_type == 'bullet':
            story.append(Paragraph(f"&bull; {escaped_text}", styles['Bullet']))
        elif el_type == 'numbered_list':
            story.append(Paragraph(escaped_text, styles['NumberedList']))
        else:
            story.append(Paragraph(escaped_text, styles['BodyText']))

    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)
    print(f"PDF saved successfully at {filename}")


# =========================================================================
# DOCX GENERATOR
# =========================================================================

def generate_docx(report, filename):
    """
    Generates a professionally styled Word document (.docx) from raw text.
    """
    from docx import Document
    from docx.shared import Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH

    dir_name = os.path.dirname(filename)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    document = Document()

    color_primary = RGBColor(26, 54, 93)     # Navy
    color_secondary = RGBColor(74, 85, 104) # Slate
    color_body = RGBColor(45, 55, 72)       # Charcoal

    title, elements = parse_report_text(report)

    # 1. Document Title
    if title:
        title_p = document.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(24)
        
        run = title_p.add_run(title)
        run.font.name = 'Arial'
        run.font.size = Pt(24)
        run.bold = True
        run.font.color.rgb = color_primary

    # 2. Document Elements
    for el_type, text, level in elements:
        if el_type == 'heading':
            p = document.add_paragraph()
            p.paragraph_format.keep_with_next = True
            
            run = p.add_run(text)
            run.font.name = 'Arial'
            run.bold = True
            
            if level == 1:
                p.paragraph_format.space_before = Pt(16)
                p.paragraph_format.space_after = Pt(6)
                run.font.size = Pt(15)
                run.font.color.rgb = color_primary
            else:
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(4)
                run.font.size = Pt(12)
                run.font.color.rgb = color_secondary
                
        elif el_type in ('bullet', 'numbered_list'):
            # Use Word's built-in list styles
            style_name = 'List Bullet' if el_type == 'bullet' else 'List Number'
            p = document.add_paragraph(style=style_name)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            
            run = p.add_run(text)
            run.font.name = 'Arial'
            run.font.size = Pt(10.5)
            run.font.color.rgb = color_body
                
        else:
            p = document.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.line_spacing = 1.15
            
            run = p.add_run(text)
            run.font.name = 'Arial'
            run.font.size = Pt(10.5)
            run.font.color.rgb = color_body

    document.save(filename)
    print(f"DOCX saved successfully at {filename}")