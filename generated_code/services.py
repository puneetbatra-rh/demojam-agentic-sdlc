from models import session, HomeLoanApplication, Document
from datetime import datetime

class HomeLoanService:
    """
    Service class for home loan application.
    """
    @staticmethod
    def create_application(customer_name, email, phone_number):
        """
        Creates a new home loan application.

        Args:
            customer_name (str): Customer name.
            email (str): Customer email.
            phone_number (str): Customer phone number.

        Returns:
            HomeLoanApplication: Created application.
        """
        application = HomeLoanApplication(customer_name, email, phone_number, datetime.now())
        session.add(application)
        session.commit()
        return application

    @staticmethod
    def get_application(application_id):
        """
        Gets a home loan application by ID.

        Args:
            application_id (int): Application ID.

        Returns:
            HomeLoanApplication: Application.
        """
        return session.query(HomeLoanApplication).filter_by(id=application_id).first()

    @staticmethod
    def update_application(application_id, customer_name=None, email=None, phone_number=None):
        """
        Updates a home loan application.

        Args:
            application_id (int): Application ID.
            customer_name (str, optional): Customer name. Defaults to None.
            email (str, optional): Customer email. Defaults to None.
            phone_number (str, optional): Customer phone number. Defaults to None.

        Returns:
            HomeLoanApplication: Updated application.
        """
        application = HomeLoanService.get_application(application_id)
        if application:
            if customer_name:
                application.customer_name = customer_name
            if email:
                application.email = email
            if phone_number:
                application.phone_number = phone_number
            session.commit()
        return application

class DocumentService:
    """
    Service class for document.
    """
    @staticmethod
    def create_document(application_id, document_type, document_url):
        """
        Creates a new document.

        Args:
            application_id (int): Application ID.
            document_type (str): Document type.
            document_url (str): Document URL.

        Returns:
            Document: Created document.
        """
        document = Document(application_id, document_type, document_url)
        session.add(document)
        session.commit()
        return document