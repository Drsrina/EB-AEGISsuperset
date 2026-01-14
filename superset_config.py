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

# Tooltip ao passar o mouse sobre o logo
LOGO_TOOLTIP = "Aegis BI - Business Intelligence Platform"

# Texto que aparece à direita do logo (opcional - descomente se desejar usar)
# LOGO_RIGHT_TEXT = "BI Platform"

# ============================================================================
# TEMA CUSTOMIZADO - AEGIS BI
# Inspirado em estética moderna: glassmorphism, neon, gradientes purple/cyan
# ============================================================================

THEME_DEFAULT = {
    "token": {
        # === BRANDING ===
        "brandLogoAlt": "Aegis BI",
        "brandLogoUrl": "/static/assets/images/superset-logo-horiz.png",
        "brandLogoMargin": "18px 0",
        "brandLogoHref": "/",
        "brandLogoHeight": "24px",
        
        # === CORES PRINCIPAIS (Neon Purple/Cyan Theme) ===
        # Cor primária: Purple vibrante (inspirado no via-purple-900)
        "colorPrimary": "#a855f7",  # Purple-500 (cor principal de ações/botões)
        "colorLink": "#22d3ee",      # Cyan-400 (links e elementos interativos)
        
        # Cores de estado
        "colorSuccess": "#10b981",   # Green-500 (sucesso)
        "colorWarning": "#f59e0b",   # Amber-500 (avisos)
        "colorError": "#ec4899",     # Pink-500 (erros - neon pink)
        "colorInfo": "#06b6d4",      # Cyan-500 (informações)
        
        # Background e superfícies (Dark Mode)
        "colorBgBase": "#0f172a",        # Slate-900 (background principal escuro)
        "colorBgContainer": "#1e293b",   # Slate-800 (containers/cards)
        "colorBgElevated": "#334155",    # Slate-700 (elementos elevados)
        "colorBgLayout": "#0f172a",      # Slate-900 (layout geral)
        
        # Bordas e divisores
        "colorBorder": "#475569",        # Slate-600 (bordas sutis)
        "colorBorderSecondary": "#64748b", # Slate-500 (bordas secundárias)
        
        # Texto
        "colorText": "#f1f5f9",          # Slate-100 (texto principal - quase branco)
        "colorTextSecondary": "#cbd5e1",  # Slate-300 (texto secundário)
        "colorTextTertiary": "#94a3b8",   # Slate-400 (texto terciário)
        "colorTextQuaternary": "#64748b", # Slate-500 (texto desabilitado)
        
        # === TIPOGRAFIA ===
        # Fontes modernas e profissionais
        "fontUrls": [
            "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
            "https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap"
        ],
        "fontFamily": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif",
        "fontFamilyCode": "'Fira Code', 'Courier New', Consolas, Monaco, monospace",
        
        # Tamanhos de fonte
        "fontSizeXS": "10",
        "fontSizeSM": "12",
        "fontSize": "14",       # Base
        "fontSizeLG": "16",
        "fontSizeXL": "20",
        "fontSizeXXL": "28",
        
        # Pesos de fonte
        "fontWeightLight": "300",
        "fontWeightNormal": "400",
        "fontWeightStrong": "600",
        
        # === ESPAÇAMENTO E LAYOUT ===
        "borderRadius": "12",        # Border radius mais suave (12px)
        "borderRadiusLG": "16",      # Border radius grande para cards
        "borderRadiusSM": "8",       # Border radius pequeno
        
        # === EFEITOS E TRANSIÇÕES ===
        "transitionTiming": 0.3,     # Transições suaves
        
        # === SOMBRAS (Simulando glassmorphism) ===
        # Nota: Superset tem suporte limitado a sombras customizadas
        # A maioria dos efeitos virá do algoritmo dark + cores vibrantes
        
        # === OUTROS ===
        "brandIconMaxWidth": 37,
        
        # Spinner customizado (opcional)
        "brandSpinnerUrl": None,
        "brandSpinnerSvg": None,
    },
    
    # Usa o algoritmo DARK do Ant Design
    # Isso cria automaticamente variantes escuras de todos os componentes
    "algorithm": "dark",
}

# ============================================================================
# ESQUEMAS DE CORES CUSTOMIZADOS (Gradientes Neon)
# ============================================================================

EXTRA_CATEGORICAL_COLOR_SCHEMES = [
    {
        "id": "aegisNeonGradient",
        "description": "Aegis BI neon gradient color scheme with purple, cyan, and pink tones",
        "label": "Aegis Neon",
        "isDefault": True,
        "colors": [
            "#a855f7",  # Purple-500
            "#22d3ee",  # Cyan-400
            "#ec4899",  # Pink-500
            "#06b6d4",  # Cyan-500
            "#8b5cf6",  # Violet-500
            "#0ea5e9",  # Sky-500
            "#d946ef",  # Fuchsia-500
            "#14b8a6",  # Teal-500
            "#f472b6",  # Pink-400
            "#2dd4bf",  # Teal-400
            "#c084fc",  # Purple-400
            "#38bdf8",  # Sky-400
        ]
    },
    {
        "id": "aegisCool",
        "description": "Cool tones - cyan and blue focus",
        "label": "Aegis Cool",
        "isDefault": False,
        "colors": [
            "#06b6d4",  # Cyan-500
            "#0ea5e9",  # Sky-500
            "#3b82f6",  # Blue-500
            "#22d3ee",  # Cyan-400
            "#14b8a6",  # Teal-500
            "#6366f1",  # Indigo-500
            "#38bdf8",  # Sky-400
            "#2dd4bf",  # Teal-400
        ]
    },
]