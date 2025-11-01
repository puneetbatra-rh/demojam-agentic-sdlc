from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Config

Base = declarative_base()

class HomeLoanApplication(Base):
    """
    Model for home loan application.
    """
    __tablename__ = 'home_loan_applications'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone_number = Column(String(20), nullable=False)
    application_date = Column(DateTime, nullable=False)

    def __init__(self, customer_name, email, phone_number, application_date):
        self.customer_name = customer_name
        self.email = email
        self.phone_number = phone_number
        self.application_date = application_date

class Document(Base):
    """
    Model for document.
    """
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, nullable=False)
    document_type = Column(String(100), nullable=False)
    document_url = Column(String(200), nullable=False)

    def __init__(self, application_id, document_type, document_url):
        self.application_id = application_id
        self.document_type = document_type
        self.document_url = document_url

engine = create_engine(Config.get_db_url())
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)