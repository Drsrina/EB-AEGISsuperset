import os
import time

# --- CONFIGURAÇÃO DE TIMEZONE (BRASIL) ---
# Força o container a usar o horário de Brasília para logs e agendamentos
os.environ['TZ'] = 'America/Sao_Paulo'
try:
    time.tzset()
except AttributeError:
    pass # Windows nao suporta tzset, mas no Linux/Docker funciona

# Le do Cloud Run Environment Variables
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# Cache na RAM (SimpleCache) - Economia de custo (sem Redis)
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_THRESHOLD': 500
}
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

ENABLE_PROXY_FIX = True
ROW_LIMIT = 5000

# --- TIMEOUTS (CRÍTICO PARA BIGQUERY) ---
SUPERSET_WEBSERVER_TIMEOUT = 120
SQLLAB_ASYNC_TIME_LIMIT_SEC = 300 # 5 minutos para queries SQL Lab
SQLLAB_TIMEOUT = 300

# --- FEATURE FLAGS (MODO POWERBI) ---
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True, # Ativa filtros laterais (Periodo, Dropdown)
    "DASHBOARD_CROSS_FILTERS": True,  # Permite clicar no grafico p/ filtrar
    "DRILL_TO_DETAIL": True,          # Drill down para ver linhas
    "DRILL_BY": True,                 # Drill down por hierarquia
    "HORIZONTAL_FILTER_BAR": True,    # Barra de filtros moderna
    "ENABLE_TEMPLATE_PROCESSING": True, # Permite Jinja no SQL Lab
    "THUMBNAILS": False,              # Desliga thumbnails (exige Redis/Workers)
    "ALERT_REPORTS": False            # Desliga alertas (exige Redis/Workers)
}