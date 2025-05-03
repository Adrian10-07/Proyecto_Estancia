class Config:
    DEBUG = False
    TESTING = False
    PDF_FOLDER = 'pdf_files'

class DevelopmentConfig(Config):
    DEBUG = True