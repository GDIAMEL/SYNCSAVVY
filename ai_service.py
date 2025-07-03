# Create AI service for email rewriting and negotiation
ai_service_content = """
import openai
from config import Config

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def rewrite_email(self, original_email, tone="professional", purpose="general"):
        \"\"\"Rewrite email with specified tone and purpose\"\"\"
        try:
            tone_prompts = {
                "professional": "Rewrite this email in a professional, business-appropriate tone",
                "friendly": "Rewrite this email in a friendly, warm tone while maintaining professionalism",
                "assertive": "Rewrite this email in an assertive, confident tone",
                "diplomatic": "Rewrite this email in a diplomatic, tactful tone"
            }
            
            purpose_context = {
                "negotiation": "This email is for price negotiation. Make it persuasive but respectful.",
                "follow_up": "This is a follow-up email. Make it polite but persistent.",
                "proposal": "This is a project proposal. Make it compelling and professional.",
                "general": "This is a general business email."
            }
            
            prompt = f\"\"\"
            {tone_prompts.get(tone, tone_prompts["professional"])}
            
            Context: {purpose_context.get(purpose, purpose_context["general"])}
            
            Original email:
            {original_email}
            
            Rewritten email:
            \"\"\"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                temperature=0.7
            )
            
            return {
                "success": True,
                "rewritten_email": response.choices[0].text.strip(),
                "original_email": original_email
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def negotiate_price(self, current_price, client_budget, project_scope, justification=""):
        \"\"\"Generate negotiation response for price discussions\"\"\"
        try:
            prompt = f\"\"\"
            You are a professional freelancer negotiating a project price. Generate a diplomatic but firm response.
            
            Current Price: ${current_price}
            Client Budget: ${client_budget}
            Project Scope: {project_scope}
            Additional Justification: {justification}
            
            Generate a professional negotiation response that:
            1. Acknowledges the client's budget
            2. Explains the value you provide
            3. Offers alternatives if needed
            4. Maintains a positive relationship
            
            Response:
            \"\"\"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=400,
                temperature=0.6
            )
            
            return {
                "success": True,
                "negotiation_response": response.choices[0].text.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_contract_terms(self, project_type, duration, payment_terms, deliverables):
        \"\"\"Generate contract terms based on project details\"\"\"
        try:
            prompt = f\"\"\"
            Generate professional contract terms for a freelance project:
            
            Project Type: {project_type}
            Duration: {duration}
            Payment Terms: {payment_terms}
            Deliverables: {deliverables}
            
            Generate clear, professional contract terms covering:
            1. Scope of work
            2. Timeline and milestones
            3. Payment schedule
            4. Revision policy
            5. Termination clause
            6. Intellectual property rights
            
            Contract Terms:
            \"\"\"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=600,
                temperature=0.5
            )
            
            return {
                "success": True,
                "contract_terms": response.choices[0].text.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_client_communication(self, email_content):
        \"\"\"Analyze client communication for insights\"\"\"
        try:
            prompt = f\"\"\"
            Analyze this client communication and provide insights:
            
            Email Content: {email_content}
            
            Provide analysis on:
            1. Client's tone and mood
            2. Urgency level
            3. Potential concerns or issues
            4. Recommended response strategy
            5. Risk level (Low/Medium/High)
            
            Analysis:
            \"\"\"
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=300,
                temperature=0.4
            )
            
            return {
                "success": True,
                "analysis": response.choices[0].text.strip()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Initialize AI service
ai_service = AIService()
"""

with open("freelancers_bot/services/ai_service.py", "w") as f:
    f.write(ai_service_content)

print("AI service created!")
