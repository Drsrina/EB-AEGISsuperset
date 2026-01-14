import os

# Le do Cloud Run Environment Variables
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# Cache na RAM (SimpleCache)
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_THRESHOLD': 500
}
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

ENABLE_PROXY_FIX = True
ROW_LIMIT = 5000
SUPERSET_WEBSERVER_TIMEOUT = 120

# ============================================================================
# CUSTOMIZAÇÃO DE BRANDING - AEGIS BI
# ============================================================================

# Nome da aplicação (usado em títulos, mensagens e nomenclatura interna)
APP_NAME = "Aegis BI"

# Customização do tema padrão (texto alternativo do logo)
THEME_DEFAULT = {
    "token": {
        "brandLogoAlt": "Aegis BI",
    }
}

# Tooltip ao passar o mouse sobre o logo (opcional)
LOGO_TOOLTIP = "Aegis BI - Business Intelligence Platform"

# Texto que aparece à direita do logo (opcional - descomente se desejar usar)
# LOGO_RIGHT_TEXT = "BI Platform"