#!/bin/bash

# Script de Deploy do Apache Superset no Google Cloud Run
# Conectando ao Supabase (PostgreSQL) e BigQuery

set -e

echo "=========================================="
echo "Deploy do Superset no Google Cloud Run"
echo "=========================================="

# Obter o ID do projeto automaticamente
PROJECT_ID=$(gcloud config get-value project)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Erro: Não foi possível obter o PROJECT_ID."
    echo "Execute: gcloud config set project SEU_PROJECT_ID"
    exit 1
fi

echo "✅ PROJECT_ID: $PROJECT_ID"

# Variáveis de configuração
IMAGE_NAME="superset-prod"
REGION="us-central1"  # Ajuste conforme necessário
SERVICE_NAME="superset-prod"

# ==========================================
# PASSO 1: Build da imagem com Cloud Build
# ==========================================
echo ""
echo "🔨 Iniciando build da imagem com Cloud Build..."
gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --timeout=20m \
    -f Dockerfile.cloudrun \
    .

echo "✅ Build concluído com sucesso!"

# ==========================================
# PASSO 2: Deploy no Cloud Run
# ==========================================
echo ""
echo "🚀 Fazendo deploy no Cloud Run..."

# IMPORTANTE: Substitua os valores abaixo pelas suas credenciais reais
SQLALCHEMY_DATABASE_URI="postgresql://user:pass@host:5432/db"  # Substituir com Supabase
SECRET_KEY=$(uuidgen)  # Gera uma UUID automaticamente

echo "🔑 SECRET_KEY gerado: $SECRET_KEY"

gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8088 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --set-env-vars "SQLALCHEMY_DATABASE_URI=$SQLALCHEMY_DATABASE_URI" \
    --set-env-vars "SECRET_KEY=$SECRET_KEY" \
    --set-env-vars "GUNICORN_CMD_ARGS=--timeout 120 --workers 2"

echo ""
echo "=========================================="
echo "✅ Deploy concluído com sucesso!"
echo "=========================================="
echo ""
echo "🌐 URL do serviço:"
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'
echo ""
echo "⚠️  ATENÇÃO:"
echo "1. Atualize a variável SQLALCHEMY_DATABASE_URI com suas credenciais do Supabase"
echo "2. Salve o SECRET_KEY gerado em um local seguro"
echo "3. Para conectar ao BigQuery, adicione a connection string no Superset UI"
echo ""
