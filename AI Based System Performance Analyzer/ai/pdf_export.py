"""
PDF Report Export Module
Exports system performance reports to PDF format
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime
import os

class PDFExporter:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center alignment
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            leading=14
        ))
    
    def export_report_to_pdf(self, report_text, output_file="System_Performance_Report.pdf"):
        """Export text report to PDF format"""
        try:
            # Ensure output directory exists
            os.makedirs("reports", exist_ok=True)
            output_path = os.path.join("reports", output_file)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for PDF content
            story = []
            
            # Add title
            title = Paragraph(
                "AI-Based System Performance Analyzer<br/>Performance Report",
                self.styles['CustomTitle']
            )
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Add generation date
            date_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            date_para = Paragraph(date_text, self.styles['CustomBody'])
            story.append(date_para)
            story.append(Spacer(1, 0.3*inch))
            
            # Parse and add report content
            lines = report_text.split('\n')
            current_section = []
            
            for line in lines:
                line = line.strip()
                
                if not line:
                    if current_section:
                        # Add accumulated section
                        section_text = '<br/>'.join(current_section)
                        story.append(Paragraph(section_text, self.styles['CustomBody']))
                        story.append(Spacer(1, 0.1*inch))
                        current_section = []
                    continue
                
                # Check for section headers
                if line.startswith('='):
                    if current_section:
                        section_text = '<br/>'.join(current_section)
                        story.append(Paragraph(section_text, self.styles['CustomBody']))
                        story.append(Spacer(1, 0.15*inch))
                        current_section = []
                    continue
                
                # Check for main headings
                if any(keyword in line.upper() for keyword in ['EXECUTIVE SUMMARY', 'SYSTEM METRICS', 'RISK ASSESSMENT', 
                                                                'RECOMMENDATIONS', 'INSIGHTS', 'END OF REPORT']):
                    if current_section:
                        section_text = '<br/>'.join(current_section)
                        story.append(Paragraph(section_text, self.styles['CustomBody']))
                        story.append(Spacer(1, 0.1*inch))
                        current_section = []
                    
                    # Add as heading
                    heading = Paragraph(line, self.styles['CustomHeading'])
                    story.append(heading)
                    story.append(Spacer(1, 0.1*inch))
                    continue
                
                # Check for subheadings
                if line.endswith(':') and len(line) < 50:
                    if current_section:
                        section_text = '<br/>'.join(current_section)
                        story.append(Paragraph(section_text, self.styles['CustomBody']))
                        story.append(Spacer(1, 0.05*inch))
                        current_section = []
                    
                    subheading = Paragraph(line, self.styles['CustomSubHeading'])
                    story.append(subheading)
                    continue
                
                # Regular content
                current_section.append(line)
            
            # Add remaining content
            if current_section:
                section_text = '<br/>'.join(current_section)
                story.append(Paragraph(section_text, self.styles['CustomBody']))
            
            # Build PDF
            doc.build(story)
            
            return {
                "success": True,
                "file_path": output_path,
                "message": f"PDF report generated successfully: {output_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Error generating PDF: {str(e)}"
            }
    
    def export_simple_pdf(self, content, output_file="Simple_Report.pdf"):
        """Export simple content to PDF"""
        try:
            os.makedirs("reports", exist_ok=True)
            output_path = os.path.join("reports", output_file)
            
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            story = []
            
            # Add content
            for line in content.split('\n'):
                if line.strip():
                    para = Paragraph(line.strip(), self.styles['Normal'])
                    story.append(para)
                    story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            return {"success": True, "file_path": output_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

def export_pdf(report_text, output_file="System_Performance_Report.pdf"):
    """Convenience function to export report to PDF"""
    exporter = PDFExporter()
    return exporter.export_report_to_pdf(report_text, output_file)
