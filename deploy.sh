#!/bin/bash

# Script de Deploy Interativo do Apache Superset no Google Cloud Run
# Conectando ao Supabase (PostgreSQL) e BigQuery

set -e

echo "=========================================="
echo "Deploy do Superset no Google Cloud Run"
echo "=========================================="
echo ""

# Obter o ID do projeto automaticamente
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Erro: Não foi possível obter o PROJECT_ID."
    echo "Execute: gcloud config set project SEU_PROJECT_ID"
    exit 1
fi

echo "✅ PROJECT_ID: $PROJECT_ID"
echo ""

# Variáveis de configuração
IMAGE_NAME="superset-prod"
REGION="us-central1"
SERVICE_NAME="superset-prod"

# ==========================================
# COLETA DE INFORMAÇÕES DO USUÁRIO
# ==========================================

echo "📋 Configuração de Credenciais"
echo "----------------------------------------"
echo ""

# Solicitar Connection String do Supabase
echo "🔐 Cole a URI de conexão do Supabase (PostgreSQL):"
echo "Formato: postgresql://usuario:senha@host.supabase.co:5432/postgres"
echo ""
read -p "URI do Supabase: " DB_URI

if [ -z "$DB_URI" ]; then
    echo "❌ Erro: URI do banco de dados não pode estar vazia!"
    exit 1
fi

echo ""
echo "✅ URI configurada!"
echo ""

# Gerar SECRET_KEY automaticamente
echo "🔑 Gerando SECRET_KEY aleatória..."

# Tentar usar uuidgen, se não existir, gerar manualmente
if command -v uuidgen &> /dev/null; then
    GENERATED_SECRET=$(uuidgen)
elif command -v python3 &> /dev/null; then
    GENERATED_SECRET=$(python3 -c "import uuid; print(str(uuid.uuid4()))")
else
    # Fallback: usar openssl para gerar string aleatória
    GENERATED_SECRET=$(openssl rand -hex 32)
fi

echo "✅ SECRET_KEY gerado: $GENERATED_SECRET"
echo ""
echo "⚠️  IMPORTANTE: Salve esta SECRET_KEY em local seguro!"
echo "   Você precisará dela se fizer redeploy ou backup."
echo ""

# Confirmação antes de prosseguir
read -p "Deseja prosseguir com o deploy? (s/n): " CONFIRM

if [ "$CONFIRM" != "s" ] && [ "$CONFIRM" != "S" ]; then
    echo "❌ Deploy cancelado pelo usuário."
    exit 0
fi

echo ""

# ==========================================
# PASSO 1: Build da imagem com Cloud Build
# ==========================================
echo "=========================================="
echo "🔨 PASSO 1: Build da Imagem"
echo "=========================================="
echo ""

gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --timeout=20m \
    -f Dockerfile.cloudrun \
    .

echo ""
echo "✅ Build concluído com sucesso!"
echo ""

# ==========================================
# PASSO 2: Deploy no Cloud Run
# ==========================================
echo "=========================================="
echo "🚀 PASSO 2: Deploy no Cloud Run"
echo "=========================================="
echo ""

gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8088 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 600 \
    --set-env-vars "SQLALCHEMY_DATABASE_URI=$DB_URI" \
    --set-env-vars "SECRET_KEY=$GENERATED_SECRET" \
    --set-env-vars "GUNICORN_CMD_ARGS=--timeout 120 --workers 2"

echo ""
echo "=========================================="
echo "✅ DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=========================================="
echo ""

# Obter URL do serviço
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo "🌐 URL do Superset:"
echo "   $SERVICE_URL"
echo ""

# ==========================================
# INSTRUÇÕES DE GESTÃO DE USUÁRIOS
# ==========================================
echo "=========================================="
echo "👥 GESTÃO DE USUÁRIOS"
echo "=========================================="
echo ""
echo "📌 USUÁRIO ADMIN INICIAL:"
echo "   O Superset cria automaticamente um usuário administrador:"
echo ""
echo "   👤 Usuário: admin"
echo "   🔑 Senha: admin"
echo ""
echo "   ⚠️  ALTERE A SENHA IMEDIATAMENTE após o primeiro login!"
echo ""
echo "----------------------------------------"
echo "📝 CRIANDO NOVOS USUÁRIOS:"
echo "----------------------------------------"
echo ""
echo "🖥️  MÉTODO 1 - Interface Web (RECOMENDADO):"
echo ""
echo "   1. Faça login no Superset: $SERVICE_URL"
echo "   2. Vá em: Settings → List Users"
echo "   3. Clique no botão [+] para adicionar novo usuário"
echo "   4. Preencha os dados e selecione a Role apropriada:"
echo "      • Admin: acesso total"
echo "      • Alpha: pode criar e editar dashboards"
echo "      • Gamma: apenas visualização"
echo ""
echo "----------------------------------------"
echo ""
echo "💻 MÉTODO 2 - Linha de Comando (Avançado):"
echo ""
echo "   Se precisar criar usuários via CLI, conecte ao container:"
echo ""
echo "   # Obter nome do serviço"
echo "   gcloud run services list --region $REGION"
echo ""
echo "   # Executar comando no container (requer configuração de job)"
echo "   # Exemplo de criação de usuário:"
echo "   superset fab create-admin \\"
echo "     --username novouser \\"
echo "     --firstname Nome \\"
echo "     --lastname Sobrenome \\"
echo "     --email user@example.com \\"
echo "     --password senhasegura"
echo ""
echo "   Nota: Este método requer criar um Cloud Run Job ou"
echo "   executar diretamente no container. Prefira a Interface Web."
echo ""
echo "=========================================="
echo "🔧 PRÓXIMOS PASSOS"
echo "=========================================="
echo ""
echo "1. ✅ Acesse: $SERVICE_URL"
echo "2. ✅ Login com: admin / admin"
echo "3. ⚠️  ALTERE A SENHA DO ADMIN"
echo "4. ✅ Configure conexão com BigQuery:"
echo "      Data → Databases → + Database"
echo "      Tipo: Google BigQuery"
echo "      URI: bigquery://seu-project-id/seu-dataset"
echo "5. ✅ Crie novos usuários via Settings → List Users"
echo "6. ✅ Comece a criar seus dashboards!"
echo ""
echo "=========================================="
echo "📊 INFORMAÇÕES DE DEPLOYMENT"
echo "=========================================="
echo ""
echo "Project ID: $PROJECT_ID"
echo "Service: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: gcr.io/$PROJECT_ID/$IMAGE_NAME"
echo "URL: $SERVICE_URL"
echo ""
echo "SECRET_KEY: $GENERATED_SECRET"
echo ""
echo "⚠️  Guarde a SECRET_KEY em local seguro!"
echo ""
echo "=========================================="
echo "📞 Suporte e Documentação"
echo "=========================================="
echo ""
echo "• Cloud Run: https://cloud.google.com/run/docs"
echo "• Superset: https://superset.apache.org/docs/intro"
echo "• Supabase: https://supabase.com/docs"
echo ""
echo "🎉 Deploy finalizado com sucesso!"
echo ""
