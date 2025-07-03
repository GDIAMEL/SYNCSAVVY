# Create main Flask application
app_content = """
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os

from config import Config
from models import db, Client, Project, Invoice, Contract
from services.mpesa_service import mpesa_service
from services.ai_service import ai_service
from services.invoice_service import invoice_service
from services.contract_service import contract_service

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    \"\"\"Main dashboard\"\"\"
    try:
        # Get dashboard statistics
        total_clients = Client.query.count()
        total_projects = Project.query.count()
        active_projects = Project.query.filter_by(status='active').count()
        pending_invoices = Invoice.query.filter_by(status='sent').count()
        overdue_invoices = Invoice.query.filter(
            Invoice.status != 'paid',
            Invoice.due_date < datetime.now().date()
        ).count()
        
        # Recent activity
        recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
        recent_invoices = Invoice.query.order_by(Invoice.created_at.desc()).limit(5).all()
        
        # Calculate total revenue
        total_revenue = db.session.query(db.func.sum(Invoice.total_amount)).filter_by(status='paid').scalar() or 0
        pending_revenue = db.session.query(db.func.sum(Invoice.total_amount)).filter_by(status='sent').scalar() or 0
        
        dashboard_data = {
            'stats': {
                'total_clients': total_clients,
                'total_projects': total_projects,
                'active_projects': active_projects,
                'pending_invoices': pending_invoices,
                'overdue_invoices': overdue_invoices,
                'total_revenue': total_revenue,
                'pending_revenue': pending_revenue
            },
            'recent_projects': [project.to_dict() for project in recent_projects],
            'recent_invoices': [invoice.to_dict() for invoice in recent_invoices]
        }
        
        return render_template('dashboard.html', data=dashboard_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients')
def clients():
    \"\"\"Clients management page\"\"\"
    try:
        clients = Client.query.order_by(Client.created_at.desc()).all()
        clients_data = [client.to_dict() for client in clients]
        return render_template('clients.html', clients=clients_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clients/add', methods=['POST'])
def add_client():
    \"\"\"Add new client\"\"\"
    try:
        data = request.get_json()
        
        # Check if client already exists
        existing_client = Client.query.filter_by(email=data['email']).first()
        if existing_client:
            return jsonify({'error': 'Client with this email already exists'}), 400
        
        # Create new client
        client = Client(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            company=data.get('company'),
            address=data.get('address')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Client added successfully',
            'client': client.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/projects')
def projects():
    \"\"\"Projects management page\"\"\"
    try:
        projects = Project.query.order_by(Project.created_at.desc()).all()
        projects_data = []
        
        for project in projects:
            project_dict = project.to_dict()
            project_dict['client_name'] = project.client.name if project.client else 'Unknown'
            projects_data.append(project_dict)
        
        return render_template('projects.html', projects=projects_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/projects/add', methods=['POST'])
def add_project():
    \"\"\"Add new project\"\"\"
    try:
        data = request.get_json()
        
        project = Project(
            title=data['title'],
            description=data.get('description'),
            client_id=data['client_id'],
            budget=data.get('budget'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else None,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            status=data.get('status', 'pending')
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project added successfully',
            'project': project.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/invoices')
def invoices():
    \"\"\"Invoices management page\"\"\"
    try:
        invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
        invoices_data = []
        
        for invoice in invoices:
            invoice_dict = invoice.to_dict()
            invoice_dict['client_name'] = invoice.client.name if invoice.client else 'Unknown'
            invoices_data.append(invoice_dict)
        
        return render_template('invoices.html', invoices=invoices_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/invoices/create', methods=['POST'])
def create_invoice():
    \"\"\"Create new invoice\"\"\"
    try:
        data = request.get_json()
        
        # Calculate totals
        totals = invoice_service.calculate_totals(data['amount'], data.get('tax_rate', 0.16))
        
        # Create invoice
        invoice = Invoice(
            invoice_number=invoice_service.generate_invoice_number(),
            client_id=data['client_id'],
            project_id=data.get('project_id'),
            amount=totals['amount'],
            tax_amount=totals['tax_amount'],
            total_amount=totals['total_amount'],
            currency=data.get('currency', 'KES'),
            due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date() if data.get('due_date') else None,
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Invoice created successfully',
            'invoice': invoice.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/invoices/<int:invoice_id>/pdf')
def generate_invoice_pdf(invoice_id):
    \"\"\"Generate invoice PDF\"\"\"
    try:
        invoice = Invoice.query.get_or_404(invoice_id)
        client = invoice.client
        
        # Generate PDF
        result = invoice_service.generate_invoice_pdf(
            invoice.to_dict(),
            client.to_dict()
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Invoice PDF generated successfully',
                'file_path': result['file_path']
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/payments/mpesa/stk-push', methods=['POST'])
def mpesa_stk_push():
    \"\"\"Initiate M-Pesa STK Push payment\"\"\"
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['phone_number', 'amount', 'invoice_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get invoice details
        invoice = Invoice.query.get(data['invoice_id'])
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        # Initiate STK Push
        callback_url = f"{request.host_url}payments/mpesa/callback"
        
        result = mpesa_service.stk_push(
            phone_number=data['phone_number'],
            amount=data['amount'],
            account_reference=invoice.invoice_number,
            transaction_desc=f"Payment for invoice {invoice.invoice_number}",
            callback_url=callback_url
        )
        
        if 'error' not in result:
            return jsonify({
                'success': True,
                'message': 'STK Push initiated successfully',
                'checkout_request_id': result.get('CheckoutRequestID'),
                'response_code': result.get('ResponseCode')
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/payments/mpesa/callback', methods=['POST'])
def mpesa_callback():
    \"\"\"Handle M-Pesa payment callback\"\"\"
    try:
        data = request.get_json()
        
        # Process callback data
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        
        if result_code == 0:  # Success
            # Extract transaction details
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            
            transaction_id = None
            phone_number = None
            amount = None
            
            for item in callback_metadata:
                if item.get('Name') == 'MpesaReceiptNumber':
                    transaction_id = item.get('Value')
                elif item.get('Name') == 'PhoneNumber':
                    phone_number = item.get('Value')
                elif item.get('Name') == 'Amount':
                    amount = item.get('Value')
            
            # Update invoice status
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            # You'll need to store checkout_request_id when initiating STK push
            # For now, we'll just log the successful payment
            
            return jsonify({
                'success': True,
                'message': 'Payment processed successfully',
                'transaction_id': transaction_id
            })
        else:
            # Payment failed
            return jsonify({
                'success': False,
                'message': 'Payment failed',
                'result_code': result_code
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai/rewrite-email', methods=['POST'])
def rewrite_email():
    \"\"\"AI email rewriter\"\"\"
    try:
        data = request.get_json()
        
        result = ai_service.rewrite_email(
            original_email=data['email'],
            tone=data.get('tone', 'professional'),
            purpose=data.get('purpose', 'general')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ai/negotiate-price', methods=['POST'])
def negotiate_price():
    \"\"\"AI price negotiation\"\"\"
    try:
        data = request.get_json()
        
        result = ai_service.negotiate_price(
            current_price=data['current_price'],
            client_budget=data['client_budget'],
            project_scope=data['project_scope'],
            justification=data.get('justification', '')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contracts')
def contracts():
    \"\"\"Contracts management page\"\"\"
    try:
        contracts = Contract.query.order_by(Contract.created_at.desc()).all()
        contracts_data = []
        
        for contract in contracts:
            contract_dict = contract.to_dict()
            contract_dict['client_name'] = contract.client.name if contract.client else 'Unknown'
            contracts_data.append(contract_dict)
        
        return render_template('contracts.html', contracts=contracts_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contracts/create', methods=['POST'])
def create_contract():
    \"\"\"Create new contract\"\"\"
    try:
        data = request.get_json()
        
        # Get client and project data
        client = Client.query.get(data['client_id'])
        project = Project.query.get(data.get('project_id')) if data.get('project_id') else None
        
        # Generate contract content
        contract_content = contract_service.generate_contract_content(
            client_data=client.to_dict(),
            project_data=project.to_dict() if project else data,
            template_type=data.get('template_type', 'consulting')
        )
        
        if contract_content['success']:
            # Create contract record
            contract = Contract(
                contract_number=contract_content['contract_number'],
                client_id=data['client_id'],
                project_id=data.get('project_id'),
                title=data.get('title', 'Service Agreement'),
                content=contract_content['content'],
                value=data.get('value', 0)
            )
            
            db.session.add(contract)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Contract created successfully',
                'contract': contract.to_dict()
            })
        else:
            return jsonify({'error': contract_content['error']}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/contracts/<int:contract_id>/pdf')
def generate_contract_pdf(contract_id):
    \"\"\"Generate contract PDF\"\"\"
    try:
        contract = Contract.query.get_or_404(contract_id)
        
        # Generate PDF
        result = contract_service.generate_contract_pdf(contract.to_dict())
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Contract PDF generated successfully',
                'file_path': result['file_path']
            })
        else:
            return jsonify({'error': result['error']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/templates/contracts')
def get_contract_templates():
    \"\"\"Get available contract templates\"\"\"
    try:
        templates = contract_service.get_contract_templates_list()
        return jsonify({
            'success': True,
            'templates': templates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
"""

with open("freelancers_bot/app.py", "w") as f:
    f.write(app_content)

print("Main Flask application created!")
