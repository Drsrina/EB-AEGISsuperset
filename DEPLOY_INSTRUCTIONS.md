# Deploy do Apache Superset no Google Cloud Run

## 📋 Arquivos Criados

✅ **PASSO 1 - Dependências:**
- `requirements/google_cloud.txt` - Drivers para PostgreSQL (Supabase), BigQuery e Gunicorn

✅ **PASSO 2 - Configuração:**
- `docker/pythonpath_dev/superset_config.py` - Configuração do Superset com variáveis de ambiente

✅ **PASSO 3 - Dockerfile:**
- `Dockerfile.cloudrun` - Dockerfile otimizado baseado na imagem oficial do Superset

✅ **PASSO 4 - Script de Deploy:**
- `deploy-cloudrun.sh` - Script automatizado de build e deploy

---

## 🚀 Como Fazer o Deploy

### Pré-requisitos

1. **Google Cloud SDK instalado** e configurado
   ```bash
   gcloud auth login
   gcloud config set project SEU_PROJECT_ID
   ```

2. **Habilitar APIs necessárias:**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Credenciais do Supabase:**
   - Host
   - Porta (5432)
   - Database
   - Usuário
   - Senha

---

## 📝 Instruções de Deploy

### 1. Executar o Script de Deploy Interativo

O script `deploy.sh` solicitará as credenciais de forma interativa e segura.

No terminal, na raiz do projeto, execute:

```bash
# Dar permissão de execução ao script
chmod +x deploy.sh

# Executar o deploy
./deploy.sh
```

**O script irá:**
1. ✅ Solicitar a Connection String do Supabase (não fica salva em arquivos)
2. ✅ Gerar automaticamente um SECRET_KEY único (UUID)
3. ✅ Pedir confirmação antes de prosseguir
4. ✅ Fazer build da imagem usando Cloud Build
5. ✅ Fazer deploy no Cloud Run com todas as variáveis de ambiente
6. ✅ Exibir a URL do serviço e instruções de gestão de usuários

### 2. Informações Solicitadas Durante o Deploy

**Connection String do Supabase:**
```
postgresql://usuario:senha@host.supabase.co:5432/postgres
```

O script pedirá esta informação de forma interativa, garantindo que senhas não fiquem salvas em arquivos.

---

## 🔧 Configuração Pós-Deploy

### 1. Conectar ao BigQuery

Após o deploy, acesse o Superset e adicione uma nova conexão:

1. **Menu:** Data → Databases → + Database
2. **Tipo:** Google BigQuery
3. **SQLAlchemy URI:**
   ```
   bigquery://seu-project-id/seu-dataset
   ```

### 2. Credenciais de Admin

O script cria automaticamente um usuário admin com:
- **Usuário:** `admin`
- **Senha:** `admin`

⚠️ **IMPORTANTE:** Altere a senha imediatamente após o primeiro login!

---

## 👥 Gestão de Usuários

### Usuário Admin Inicial

O Superset cria automaticamente um usuário administrador no primeiro boot:

- 👤 **Usuário:** `admin`
- 🔑 **Senha:** `admin`

⚠️ **ALTERE A SENHA** imediatamente após o primeiro acesso!

---

### Criando Novos Usuários

#### 🖥️ MÉTODO 1 - Interface Web (RECOMENDADO)

1. Faça login no Superset
2. Vá em: **Settings → List Users**
3. Clique no botão **[+]** para adicionar novo usuário
4. Preencha os dados e selecione a Role apropriada:
   - **Admin**: acesso total ao sistema
   - **Alpha**: pode criar e editar dashboards
   - **Gamma**: apenas visualização

#### 💻 MÉTODO 2 - Linha de Comando (Avançado)

Se precisar criar usuários via CLI, você pode:

**Opção A - Criar Cloud Run Job:**

```bash
# Criar um job pontual para executar comandos
gcloud run jobs create create-superset-user \
  --image gcr.io/$PROJECT_ID/superset-prod \
  --region us-central1 \
  --set-env-vars "SQLALCHEMY_DATABASE_URI=<sua-uri>" \
  --set-env-vars "SECRET_KEY=<sua-secret-key>" \
  --command "superset" \
  --args "fab,create-admin,--username,novouser,--firstname,Nome,--lastname,Sobrenome,--email,user@example.com,--password,senhasegura"

# Executar o job
gcloud run jobs execute create-superset-user --region us-central1
```

**Opção B - Executar diretamente no container (requer configuração adicional):**

```bash
superset fab create-admin \
  --username novouser \
  --firstname Nome \
  --lastname Sobrenome \
  --email user@example.com \
  --password senhasegura
```

> [!NOTE]
> O método via Interface Web é mais simples e recomendado para a maioria dos casos.

---

## ⚙️ Configurações do Superset

### Variáveis de Ambiente Configuradas

| Variável | Valor | Descrição |
|----------|-------|-----------|
| `SQLALCHEMY_DATABASE_URI` | Sua connection string | Conexão com Supabase (PostgreSQL) |
| `SECRET_KEY` | UUID gerado automaticamente | Chave de segurança para sessões |
| `GUNICORN_CMD_ARGS` | `--timeout 120 --workers 2` | Configuração do servidor web |

### Configurações no superset_config.py

- ✅ **ENABLE_PROXY_FIX = True** - Obrigatório para Cloud Run/HTTPS
- ✅ **SimpleCache** - Cache em memória (sem Redis)
- ✅ **ROW_LIMIT = 5000** - Limite de linhas por query
- ✅ **Timeouts estendidos** - Para queries grandes no BigQuery

---

## 🔍 Monitoramento

### Ver logs do serviço:

```bash
gcloud run services logs read superset-prod --region us-central1
```

### Ver detalhes do serviço:

```bash
gcloud run services describe superset-prod --region us-central1
```

---

## 🛠️ Troubleshooting

### Problema: Timeout nas queries

Aumente o timeout no arquivo `deploy-cloudrun.sh`:

```bash
--set-env-vars "GUNICORN_CMD_ARGS=--timeout 300 --workers 2"
```

### Problema: Memória insuficiente

Aumente a memória no `deploy-cloudrun.sh`:

```bash
--memory 4Gi \
--cpu 4 \
```

### Problema: Erro de conexão com Supabase

Verifique se:
1. A connection string está correta
2. O IP do Cloud Run está liberado no Supabase (ou use `0.0.0.0/0` para testes)

---

## 📦 Estrutura dos Arquivos

```
EB-AEGISsuperset/
├── requirements/
│   └── google_cloud.txt          # Dependências GCP
├── docker/
│   └── pythonpath_dev/
│       └── superset_config.py    # Configuração do Superset
├── Dockerfile.cloudrun            # Dockerfile otimizado
├── deploy-cloudrun.sh             # Script de deploy automatizado
└── DEPLOY_INSTRUCTIONS.md         # Este arquivo
```

---

## 🎯 Próximos Passos

1. ✅ Execute o script `deploy-cloudrun.sh`
2. ✅ Acesse a URL fornecida ao final do deploy
3. ✅ Faça login com `admin/admin`
4. ✅ **ALTERE A SENHA** imediatamente
5. ✅ Configure a conexão com BigQuery
6. ✅ Comece a criar seus dashboards!

---

## 📞 Suporte

Para dúvidas sobre:
- **Cloud Run:** https://cloud.google.com/run/docs
- **Superset:** https://superset.apache.org/docs/intro
- **Supabase:** https://supabase.com/docs

---

**Criado por:** DevOps Engineer  
**Data:** 2026-01-13  
**Versão:** 1.0
