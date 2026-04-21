# 🚀 Azure DevOps Demo — CI/CD with GitHub Actions

A simple Python/Flask REST API deployed to **Azure App Service** via a fully automated **GitHub Actions** pipeline.

---

## 📁 Project Structure

```
azure-devops-project/
├── app/
│   ├── app.py               # Flask application
│   └── requirements.txt     # Python dependencies
├── tests/
│   └── test_app.py          # Unit tests
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
├── Dockerfile               # Container definition
└── README.md
```

---

## 🔁 CI/CD Pipeline Flow

```
Push to main
     ↓
[Job 1] Run Tests (pytest)
     ↓ (if tests pass)
[Job 2] Build Docker image → Push to Azure Container Registry
     ↓
[Job 3] Deploy to Azure App Service → Health check
```

---

## ⚙️ Azure Setup (One-Time)

### Step 1 — Create Azure Resources

```bash
# Login
az login

# Create resource group
az group create --name rg-devops-demo --location eastus

# Create Azure Container Registry
az acr create --resource-group rg-devops-demo \
  --name <YOUR_ACR_NAME> --sku Basic --admin-enabled true

# Create App Service plan
az appservice plan create --name asp-devops-demo \
  --resource-group rg-devops-demo --sku F1 --is-linux

# Create Web App (linked to ACR)
az webapp create --resource-group rg-devops-demo \
  --plan asp-devops-demo --name <YOUR_APP_NAME> \
  --deployment-container-image-name <YOUR_ACR_NAME>.azurecr.io/azure-devops-demo:latest
```

### Step 2 — Get ACR Credentials

```bash
az acr credential show --name <YOUR_ACR_NAME>
```

### Step 3 — Create Azure Service Principal (for GitHub Actions to deploy)

```bash
az ad sp create-for-rbac \
  --name "github-actions-deploy" \
  --role contributor \
  --scopes /subscriptions/<SUB_ID>/resourceGroups/rg-devops-demo \
  --json-auth
```
Copy the entire JSON output — this is your `AZURE_CREDENTIALS` secret.

---

## 🔐 GitHub Secrets to Add

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `ACR_LOGIN_SERVER` | `<yourname>.azurecr.io` |
| `ACR_USERNAME` | from `az acr credential show` |
| `ACR_PASSWORD` | from `az acr credential show` |
| `AZURE_CREDENTIALS` | full JSON from service principal |
| `AZURE_WEBAPP_NAME` | your App Service name |

---

## 🧪 Run Tests Locally

```bash
pip install -r app/requirements.txt
pytest tests/ -v
```

## 🐳 Run with Docker Locally

```bash
docker build -t azure-devops-demo .
docker run -p 8000:8000 azure-devops-demo
# Visit: http://localhost:8000
```

---

## 🌐 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Home — app status |
| `GET /health` | Health check |
| `GET /info` | App environment info |
