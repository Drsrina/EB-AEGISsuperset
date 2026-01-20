import os
import time
from celery.schedules import crontab
from cachelib.redis import RedisCache

# --- CONFIGURAÇÃO DE TIMEZONE (BRASIL) ---
os.environ['TZ'] = 'America/Sao_Paulo'
try:
    time.tzset()
except AttributeError:
    pass

# --- BRANDING (IDENTIDADE) ---
APP_NAME = "Aura Analytics"

# Le do Cloud Run Environment Variables
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SECRET_KEY = os.getenv('SECRET_KEY')

# --- LÓGICA DE CACHE HÍBRIDA (UPSTASH / REDIS / MEMÓRIA) ---
REDIS_URL = os.getenv('REDIS_URL')

if REDIS_URL:
    print(f"[Superset Config] REDIS_URL detectada. Configurando Cache e Celery...")
    
    # 1. Configuração padrão para Flask-Caching (Charts, Dashboards)
    CACHE_CONFIG = {
        'CACHE_TYPE': 'RedisCache',
        'CACHE_DEFAULT_TIMEOUT': 86400,
        'CACHE_KEY_PREFIX': 'superset_cache_',
        'CACHE_REDIS_URL': REDIS_URL,
    }
    DATA_CACHE_CONFIG = CACHE_CONFIG
    
    # 2. Configuração do Celery (Fila de Tarefas para SQL Lab Async)
    class CeleryConfig:
        broker_url = REDIS_URL
        imports = ("superset.sql_lab",)
        result_backend = REDIS_URL
        worker_prefetch_multiplier = 1
        task_acks_late = True
        
    CELERY_CONFIG = CeleryConfig
    
    print(f"[Superset Config] Redis configurado com sucesso para Cache e Celery.")

else:
    # Fallback para Memoria (Otimizado para 8GB RAM)
    print("[Superset Config] REDIS_URL NAO ENCONTRADA. Usando SimpleCache (RAM).")
    CACHE_CONFIG = {
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 86400,
        'CACHE_THRESHOLD': 50000
    }
    DATA_CACHE_CONFIG = CACHE_CONFIG
    CELERY_CONFIG = None

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

# --- FEATURE FLAGS (MODO POWERBI & ENTERPRISE) ---
FEATURE_FLAGS = {
    "DASHBOARD_NATIVE_FILTERS": True,
    "DASHBOARD_CROSS_FILTERS": True,
    "DRILL_TO_DETAIL": True,
    "DRILL_BY": True,
    "HORIZONTAL_FILTER_BAR": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "EMBEDDED_SUPERSET": True,
    "CSV_EXPORT": True,
    "ALLOW_FULL_CSV_EXPORT": True,
    "THUMBNAILS": False,
    "ALERT_REPORTS": False
}