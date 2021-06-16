class BaseConfig:
    DEBUG = True
    FLASK_DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    # SECURITY_REGISTER_URL = "/create_account"
    SECURITY_SEND_REGISTER_EMAIL = False
    FLASK_ADMIN_SWATCH = "cerulean"


class ProductionConfig(BaseConfig):
    DEBUG = False
    FLASK_ENV = "production"
    FLASK_DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
