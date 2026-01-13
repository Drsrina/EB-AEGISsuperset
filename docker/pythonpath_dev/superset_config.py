import os

# Configurações de Banco de Dados
# Supabase PostgreSQL connection string
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# Secret Key para segurança de sessões
SECRET_KEY = os.getenv('SECRET_KEY')

# Cache Configuration - SimpleCache para evitar dependência de Redis
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
}

# Proxy Fix - OBRIGATÓRIO para Cloud Run/HTTPS
ENABLE_PROXY_FIX = True

# Row Limit para queries
ROW_LIMIT = 5000

# Configurações de Logs
LOG_LEVEL = 'INFO'

# Feature Flags
FEATURE_FLAGS = {
    'ENABLE_TEMPLATE_PROCESSING': True,
}

# CORS Settings (ajuste conforme necessário)
# ENABLE_CORS = True
# CORS_OPTIONS = {
#     'supports_credentials': True,
#     'allow_headers': ['*'],
#     'resources': ['*'],
#     'origins': ['*']
# }

# Configurações de timeout
SUPERSET_WEBSERVER_TIMEOUT = 60

# BigQuery específico - permitir queries grandes
SQLLAB_TIMEOUT = 300
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300
