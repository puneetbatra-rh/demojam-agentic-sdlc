from flask import Flask, request, jsonify
from services import HomeLoanService, DocumentService
from config import Config

app = Flask(__name__)

@app.route('/applications', methods=['POST'])
def create_application():
    """
    Creates a new home loan application.

    Returns:
        JSON: Created application.
    """
    data = request.json
    application = HomeLoanService.create_application(data['customer_name'], data['email'], data['phone_number'])
    return jsonify({'id': application.id, 'customer_name': application.customer_name, 'email': application.email, 'phone_number': application.phone_number})

@app.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """
    Gets a home loan application by ID.

    Args:
        application_id (int): Application ID.

    Returns:
        JSON: Application.
    """
    application = HomeLoanService.get_application(application_id)
    if application:
        return jsonify({'id': application.id, 'customer_name': application.customer_name, 'email': application.email, 'phone_number': application.phone_number})
    return jsonify({'error': 'Application not found'}), 404

@app.route('/documents', methods=['POST'])
def create_document():
    """
    Creates a new document.

    Returns:
        JSON: Created document.
    """
    data = request.json
    document = DocumentService.create_document(data['application_id'], data['document_type'], data['document_url'])
    return jsonify({'id': document.id, 'application_id': document.application_id, 'document_type': document.document_type, 'document_url': document.document_url})

if __name__ == '__main__':
    app.run(debug=True)