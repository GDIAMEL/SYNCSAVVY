import os
import json

# Create project structure
project_structure = {
    "freelancers_bot/": {
        "app.py": "# Main Flask application",
        "requirements.txt": "# Python dependencies",
        ".env.example": "# Environment variables template",
        "config.py": "# Application configuration",
        "models/": {
            "__init__.py": "",
            "client.py": "# Client model",
            "project.py": "# Project model", 
            "invoice.py": "# Invoice model",
            "contract.py": "# Contract model"
        },
        "services/": {
            "__init__.py": "",
            "mpesa_service.py": "# M-Pesa integration",
            "ai_service.py": "# AI email rewriter",
            "invoice_service.py": "# Invoice generation",
            "contract_service.py": "# Contract management"
        },
        "routes/": {
            "__init__.py": "",
            "dashboard.py": "# Dashboard routes",
            "payments.py": "# Payment routes",
            "clients.py": "# Client management",
            "projects.py": "# Project management"
        },
        "templates/": {
            "base.html": "# Base template",
            "dashboard.html": "# Dashboard template",
            "contracts/": {},
            "invoices/": {}
        },
        "static/": {
            "css/": {},
            "js/": {},
            "images/": {}
        }
    }
}

def create_directory_structure(structure, base_path=""):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if name.endswith("/"):
            os.makedirs(path, exist_ok=True)
            if isinstance(content, dict):
                create_directory_structure(content, path)
        else:
            with open(path, 'w') as f:
                f.write(content if isinstance(content, str) else "")

create_directory_structure(project_structure)
print("Project structure created successfully!")
