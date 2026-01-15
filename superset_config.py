import os
import time

# --- CONFIGURAÇÃO DE TIMEZONE (BRASIL) ---
os.environ['TZ'] = 'America/Sao_Paulo'
try:
    time.tzset()
except AttributeError:
    pass

# Le do Cloud Run Environment Variables
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# --- LÓGICA DE CACHE HÍBRIDA (UPSTASH / REDIS / MEMÓRIA) ---
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL:
    # Upstash geralmente exige SSL (rediss://), verificamos isso
    is_ssl = 'rediss://' in REDIS_URL
    
    CACHE_CONFIG = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 86400, # 24 horas
        'CACHE_KEY_PREFIX': 'superset_results_',
        'CACHE_REDIS_URL': REDIS_URL,
    }
    # Configuracao especifica para Data Cache (Queries)
    DATA_CACHE_CONFIG = CACHE_CONFIG
    print(f"Usando Redis Cache (SSL={is_ssl})")
else:
    # Fallback para Memoria (Otimizado para 8GB RAM)
    CACHE_CONFIG = {
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 86400,
        'CACHE_THRESHOLD': 50000 # Aguenta muito mais objetos na RAM agora
    }
    DATA_CACHE_CONFIG = CACHE_CONFIG
    print("Usando SimpleCache (Memoria Volatil)")

# Aplica a mesma logica para filtros e metadados
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

ENABLE_PROXY_FIX = True

# --- LIMITES AUMENTADOS (HARDWARE 8GB) ---
ROW_LIMIT = 50000  # Aumentado de 5k para 50k
SAMPLES_ROW_LIMIT = 1000 # Amostragem SQL Lab

# --- TIMEOUTS (CRÍTICO PARA BIGQUERY/MYSQL LENTOS) ---
SUPERSET_WEBSERVER_TIMEOUT = 300 # 5 min
SQLLAB_ASYNC_TIME_LIMIT_SEC = 600
SQLLAB_TIMEOUT = 600

# --- FEATURE FLAGS (MODO POWERBI) ---
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DRILL_TO_DETAIL": True,
    "DRILL_BY": True,
    "HORIZONTAL_FILTER_BAR": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "THUMBNAILS": False,
    "ALERT_REPORTS": False
}