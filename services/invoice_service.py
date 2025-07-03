# Create invoice service
invoice_service_content = """
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import os

class InvoiceService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
    
    def generate_invoice_number(self):
        \"\"\"Generate unique invoice number\"\"\"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f"INV-{timestamp}"
    
    def generate_invoice_pdf(self, invoice_data, client_data, save_path=None):
        \"\"\"Generate PDF invoice\"\"\"
        try:
            # Create filename if not provided
            if not save_path:
                save_path = f"invoice_{invoice_data['invoice_number']}.pdf"
            
            # Create PDF document
            doc = SimpleDocTemplate(save_path, pagesize=letter)
            story = []
            
            # Title
            title = Paragraph(f"<b>INVOICE #{invoice_data['invoice_number']}</b>", self.styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Invoice details
            invoice_details = [
                ['Invoice Date:', datetime.now().strftime('%Y-%m-%d')],
                ['Due Date:', invoice_data.get('due_date', 'N/A')],
                ['Status:', invoice_data.get('status', 'Draft').upper()]
            ]
            
            details_table = Table(invoice_details, colWidths=[2*inch, 3*inch])
            details_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(details_table)
            story.append(Spacer(1, 20))
            
            # Client information
            client_info = Paragraph(f"<b>Bill To:</b><br/>"
                                  f"{client_data.get('name', 'N/A')}<br/>"
                                  f"{client_data.get('email', 'N/A')}<br/>"
                                  f"{client_data.get('company', '')}<br/>"
                                  f"{client_data.get('address', '')}", self.styles['Normal'])
            story.append(client_info)
            story.append(Spacer(1, 20))
            
            # Invoice items
            items_data = [
                ['Description', 'Quantity', 'Rate', 'Amount']
            ]
            
            # Add invoice items (you can customize this based on your needs)
            items_data.append([
                invoice_data.get('description', 'Freelance Services'),
                '1',
                f"KES {invoice_data.get('amount', 0):,.2f}",
                f"KES {invoice_data.get('amount', 0):,.2f}"
            ])
            
            items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(items_table)
            story.append(Spacer(1, 20))
            
            # Total
            total_data = [
                ['Subtotal:', f"KES {invoice_data.get('amount', 0):,.2f}"],
                ['Tax:', f"KES {invoice_data.get('tax_amount', 0):,.2f}"],
                ['Total:', f"KES {invoice_data.get('total_amount', 0):,.2f}"]
            ]
            
            total_table = Table(total_data, colWidths=[4*inch, 2*inch])
            total_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ]))
            story.append(total_table)
            story.append(Spacer(1, 20))
            
            # Payment instructions
            payment_info = Paragraph(f"<b>Payment Instructions:</b><br/>"
                                   f"• M-Pesa: Send payment to [Your M-Pesa Number]<br/>"
                                   f"• Bank Transfer: [Your Bank Details]<br/>"
                                   f"• Reference: {invoice_data['invoice_number']}<br/>"
                                   f"<br/>"
                                   f"<b>Notes:</b><br/>"
                                   f"{invoice_data.get('notes', 'Thank you for your business!')}", 
                                   self.styles['Normal'])
            story.append(payment_info)
            
            # Build PDF
            doc.build(story)
            
            return {
                'success': True,
                'file_path': save_path,
                'message': 'Invoice PDF generated successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def calculate_totals(self, amount, tax_rate=0.16):
        \"\"\"Calculate invoice totals including tax\"\"\"
        tax_amount = amount * tax_rate
        total_amount = amount + tax_amount
        
        return {
            'amount': amount,
            'tax_amount': tax_amount,
            'total_amount': total_amount
        }
    
    def get_overdue_invoices(self, invoices):
        \"\"\"Get list of overdue invoices\"\"\"
        current_date = datetime.now().date()
        overdue = []
        
        for invoice in invoices:
            if (invoice.get('status') != 'paid' and 
                invoice.get('due_date') and 
                datetime.strptime(invoice.get('due_date'), '%Y-%m-%d').date() < current_date):
                overdue.append(invoice)
        
        return overdue
    
    def send_payment_reminder(self, invoice_data, client_data):
        \"\"\"Generate payment reminder message\"\"\"
        try:
            days_overdue = (datetime.now().date() - 
                          datetime.strptime(invoice_data.get('due_date'), '%Y-%m-%d').date()).days
            
            if days_overdue > 0:
                urgency = "URGENT: " if days_overdue > 30 else ""
                message = f\"\"\"{urgency}Payment Reminder
                
Dear {client_data.get('name', 'Valued Client')},

This is a friendly reminder that Invoice #{invoice_data['invoice_number']} 
for KES {invoice_data.get('total_amount', 0):,.2f} was due on {invoice_data.get('due_date')}.

The invoice is now {days_overdue} days overdue.

Please process the payment at your earliest convenience.

Payment Options:
• M-Pesa: [Your M-Pesa Number]
• Bank Transfer: [Your Bank Details]
• Reference: {invoice_data['invoice_number']}

Thank you for your prompt attention to this matter.

Best regards,
[Your Name]
\"\"\"
                return {
                    'success': True,
                    'message': message,
                    'days_overdue': days_overdue
                }
            else:
                return {
                    'success': False,
                    'message': 'Invoice is not overdue'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Initialize service
invoice_service = InvoiceService()
"""

with open("freelancers_bot/services/invoice_service.py", "w") as f:
    f.write(invoice_service_content)

print("Invoice service created!")
