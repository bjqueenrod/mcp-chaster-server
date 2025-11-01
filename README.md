
# 🐍 Chaster Locks MCP Server - Python Edition

A modern **Model Context Protocol (MCP)** server built in Python with **FastAPI**, **Pydantic**, and **httpx** for the Chaster Locks API.

## ✨ Python Version Advantages

- 🚀 **FastAPI** - Native async performance with auto-generated documentation
- 🔒 **Pydantic V2** - Robust data validation and optimized serialization with Rust
- 🌐 **httpx** - Modern async HTTP client with automatic retry
- 🐍 **Python 3.11+** - Modern syntax and improved performance
- 📝 **Type hints** - Safer code with static checking
- 🛡️ **Pythonic error handling** - Intuitive exception management

## 📁 Python Project Structure

```
chaster-locks-mcp-server-python/
├── main.py               # Main FastAPI server with MCP routes
├── chaster_service.py    # Chaster API service with async httpx
├── requirements.txt      # Optimized Python dependencies
├── Dockerfile           # Python 3.11 slim Docker image
├── docker-compose.yml   # Orchestration with healthcheck
├── .env.example        # Python configuration template
└── README.md          # This documentation
```

## 🚀 Installation and Setup

### Prerequisites

- **Python 3.11+** (recommended)
- **Docker & Docker Compose** (optional but recommended)

### Method 1: Docker (Recommended)

```bash
# 1. Clone and configure
git clone <repo-url> chaster-mcp-python
cd chaster-mcp-python

# 2. Configuration
cp .env.example .env
# Edit .env with your tokens

# 3. Build and launch
docker-compose up -d

# 4. Verify status
curl http://localhost:3000/health
```

### Method 2: Local Installation

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configuration
cp .env.example .env
# Configure your tokens

# 4. Start server
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## 🔧 Configuration

### Environment Variables

```bash
# MCP Token (generate with: python -c "import secrets; print(secrets.token_hex(32))")
MCP_AUTH_TOKEN=your_64_char_hex_token

# Chaster API Token (from https://chaster.app/settings/developer)
CHASTER_API_TOKEN=your_chaster_api_token

# Server port (optional)
PORT=3000

# Environment (development for auto-reload and docs)
NODE_ENV=production
```

## 📡 API and Documentation

### Interactive Documentation

In development mode, FastAPI automatically generates documentation:

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

### Available Endpoints

- `GET /health` - Server health check
- `POST /mcp` - Main MCP endpoint (authenticated)

## 🔧 Available Chaster MCP Tools

The Python version supports all Chaster API tools:

### 📋 Lock Management
- `get_locks` - List with filters (active/archived/all)
- `get_lock_details` - Complete lock details
- `archive_lock` / `archive_lock_keyholder` - Archive locks
- `unlock_lock` - Permanent unlock

### ⚙️ Control and Modification
- `update_lock_time` - Duration modification
- `freeze_lock` - Freeze/unfreeze lock
- `update_lock_settings` - Display settings
- `convert_to_self_lock` - Convert to self-lock

### 📊 Information and Search
- `get_lock_combination` - Retrieve combination
- `get_lock_history` - Activity history
- `search_locks` - Advanced search with filters
- `trust_keyholder` - Mark keyholder as trusted

## 🧪 Testing and Validation

### Basic Tests

```bash
# Server health
curl http://localhost:3000/health

# MCP authentication test
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer YOUR_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list", 
    "params": {},
    "id": 1
  }'

# Chaster tool test
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer YOUR_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_locks",
      "arguments": {"status": "active"}
    },
    "id": 2
  }'
```

### Python Testing with pytest (optional)

```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Create test_main.py
pytest test_main.py -v
```

## 🐳 Useful Docker Commands

```bash
# Manual build with tag
docker build -t chaster-mcp-python .

# Run with environment variables
docker run -p 3000:3000 \
  -e MCP_AUTH_TOKEN=your_token \
  -e CHASTER_API_TOKEN=your_chaster_token \
  chaster-mcp-python

# Development with volume and reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Real-time logs
docker-compose logs -f chaster-mcp-python

# Shell into container
docker-compose exec chaster-mcp-python bash

# Complete cleanup
docker-compose down -v --remove-orphans
```

## 🔍 Monitoring and Debugging

### Structured Logs

The Python server produces detailed logs:

```bash
# Docker logs
docker-compose logs -f

# Chaster API specific logs
docker-compose logs | grep "Chaster API"

# Error logs only
docker-compose logs | grep "ERROR"
```

### Metrics and Health

```bash
# Health endpoint with system info
curl http://localhost:3000/health | jq

# Dependency check
pip check

# Environment info
python -c "import sys; print(sys.version)"
```

## 🏗️ Development and Extension

### Adding New Tools

1. **Add definition** in `get_available_tools()`
2. **Implement method** in `ChasterLocksService`
3. **Add case** in `call_tool()`
4. **Test** with curl or FastAPI docs

### MCP Response Structure

```python
def format_response(self, data: Any, message: str = "") -> Dict[str, Any]:
    return {
        "content": [
            {
                "type": "text", 
                "text": f"{message}\n\n{json.dumps(data, indent=2)}"
            }
        ]
    }
```

### Custom Error Handling

```python
async def handle_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
    try:
        # Request logic
        response = await self.client.request(method, endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Specific HTTP error handling
        raise Exception(f"API Error ({e.response.status_code}): {e.response.text}")
```

## 🔒 Security and Best Practices

- ✅ **Bearer Authentication** required on `/mcp`
- ✅ **Pydantic Validation** of all JSON-RPC inputs
- ✅ **Configurable HTTP Timeouts** (default: 30s)
- ✅ **Non-root User** in Docker container
- ✅ **Environment Variables** for all secrets
- ✅ **CORS Configured** for web environments
- ✅ **Integrated Docker Health Checks**

## 🚀 Performance

### Python Optimizations
- **FastAPI async** - Concurrent request processing
- **httpx async** - Non-blocking HTTP client
- **Pydantic V2** - Ultra-fast validation with Rust
- **Python 3.11+** - 25% performance improvement

### Docker Optimizations
- **Python slim image** - 60% size reduction
- **Multi-stage build** - Dependency caching
- **Health checks** - Automatic restart if needed

## 🆚 Node.js vs Python Comparison

| Aspect | Node.js | Python |
|--------|---------|---------|
| **Performance** | Native Event Loop | FastAPI async (comparable) |
| **MCP Ecosystem** | Native | Adapted |
| **Readability** | Average | Excellent |
| **Validation** | Manual/joi | Pydantic integrated |
| **Documentation** | Manual Swagger | FastAPI auto |
| **Debugging** | Console/logs | Rich logs + pdb |

## 🤝 Support and Maintenance

- **Issues**: Check logs with `docker-compose logs -f`
- **Performance**: Use `htop` in container
- **Chaster API**: [Official Documentation](https://docs.chaster.app/api/)
- **FastAPI**: [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Version:** 1.0.0 | **License:** MIT | **Python:** 3.11+ | **FastAPI:** 0.104+

---

# 🐍 Serveur MCP Chaster Locks - Édition Python

Un serveur **Model Context Protocol (MCP)** moderne développé en Python avec **FastAPI**, **Pydantic** et **httpx** pour l'API Chaster Locks.

## ✨ Avantages de la version Python

- 🚀 **FastAPI** - Performance async native et documentation auto-générée
- 🔒 **Pydantic V2** - Validation de données robuste et sérialisation optimisée avec Rust
- 🌐 **httpx** - Client HTTP async moderne avec retry automatique
- 🐍 **Python 3.11+** - Syntaxe moderne et performances améliorées
- 📝 **Type hints** - Code plus sûr avec vérification statique
- 🛡️ **Gestion d'erreurs pythonique** - Exception handling intuitif

## 📁 Structure du projet Python

```
chaster-locks-mcp-server-python/
├── main.py               # Serveur FastAPI principal avec routes MCP
├── chaster_service.py    # Service API Chaster avec httpx async
├── requirements.txt      # Dépendances Python optimisées
├── Dockerfile           # Image Docker Python 3.11 slim
├── docker-compose.yml   # Orchestration avec healthcheck
├── .env.example        # Template configuration Python
└── README.md          # Cette documentation
```

## 🚀 Installation et démarrage

### Prérequis

- **Python 3.11+** (recommandé)
- **Docker & Docker Compose** (optionnel mais recommandé)

### Méthode 1: Docker (Recommandée)

```bash
# 1. Cloner et configurer
git clone <repo-url> chaster-mcp-python
cd chaster-mcp-python

# 2. Configuration
cp .env.example .env
# Éditer .env avec vos tokens

# 3. Build et lancement
docker-compose up -d

# 4. Vérifier le statut
curl http://localhost:3000/health
```

### Méthode 2: Installation locale

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Configuration
cp .env.example .env
# Configurer vos tokens

# 4. Lancer le serveur
python main.py

# Ou avec uvicorn directement
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

## 🔧 Configuration

### Variables d'environnement

```bash
# Token MCP (générer avec: python -c "import secrets; print(secrets.token_hex(32))")
MCP_AUTH_TOKEN=your_64_char_hex_token

# Token API Chaster (depuis https://chaster.app/settings/developer)
CHASTER_API_TOKEN=your_chaster_api_token

# Port du serveur (optionnel)
PORT=3000

# Environnement (development pour auto-reload et docs)
NODE_ENV=production
```

## 📡 API et Documentation

### Documentation interactive

En mode développement, FastAPI génère automatiquement la documentation :

- **Swagger UI**: http://localhost:3000/docs
- **ReDoc**: http://localhost:3000/redoc

### Endpoints disponibles

- `GET /health` - Vérification de santé du serveur
- `POST /mcp` - Endpoint principal MCP (authentifié)

## 🔧 Outils MCP Chaster disponibles

La version Python supporte tous les outils de l'API Chaster :

### 📋 Gestion des verrous
- `get_locks` - Liste avec filtres (active/archived/all)
- `get_lock_details` - Détails complets d'un verrou
- `archive_lock` / `archive_lock_keyholder` - Archivage
- `unlock_lock` - Déverrouillage définitif

### ⚙️ Contrôle et modification
- `update_lock_time` - Modification de durée
- `freeze_lock` - Gel/dégel du verrou
- `update_lock_settings` - Paramètres d'affichage
- `convert_to_self_lock` - Conversion en auto-verrou

### 📊 Informations et recherche
- `get_lock_combination` - Récupération de combinaison
- `get_lock_history` - Historique d'activités
- `search_locks` - Recherche avancée avec filtres
- `trust_keyholder` - Marquer gardien comme fiable

## 🧪 Tests et validation

### Tests de base

```bash
# Santé du serveur
curl http://localhost:3000/health

# Test authentification MCP
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer YOUR_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list", 
    "params": {},
    "id": 1
  }'

# Test d'un outil Chaster
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer YOUR_MCP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_locks",
      "arguments": {"status": "active"}
    },
    "id": 2
  }'
```

### Tests Python avec pytest (optionnel)

```bash
# Installer pytest
pip install pytest pytest-asyncio httpx

# Créer test_main.py
pytest test_main.py -v
```

## 🐳 Commandes Docker utiles

```bash
# Build manuel avec tag
docker build -t chaster-mcp-python .

# Lancement avec variables d'environnement
docker run -p 3000:3000 \
  -e MCP_AUTH_TOKEN=your_token \
  -e CHASTER_API_TOKEN=your_chaster_token \
  chaster-mcp-python

# Développement avec volume et reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Logs en temps réel
docker-compose logs -f chaster-mcp-python

# Shell dans le container
docker-compose exec chaster-mcp-python bash

# Nettoyage complet
docker-compose down -v --remove-orphans
```

## 🔍 Monitoring et debugging

### Logs structurés

Le serveur Python produit des logs détaillés :

```bash
# Logs Docker
docker-compose logs -f

# Logs spécifiques aux requêtes Chaster
docker-compose logs | grep "Chaster API"

# Logs d'erreurs seulement
docker-compose logs | grep "ERROR"
```

### Métriques et santé

```bash
# Endpoint de santé avec informations système
curl http://localhost:3000/health | jq

# Vérification des dépendances
pip check

# Informations sur l'environnement
python -c "import sys; print(sys.version)"
```

## 🏗️ Développement et extension

### Ajouter de nouveaux outils

1. **Ajouter la définition** dans `get_available_tools()`
2. **Implémenter la méthode** dans `ChasterLocksService`
3. **Ajouter le cas** dans `call_tool()`
4. **Tester** avec curl ou la documentation FastAPI

### Structure des réponses MCP

```python
def format_response(self, data: Any, message: str = "") -> Dict[str, Any]:
    return {
        "content": [
            {
                "type": "text", 
                "text": f"{message}\n\n{json.dumps(data, indent=2)}"
            }
        ]
    }
```

### Gestion d'erreurs personnalisée

```python
async def handle_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
    try:
        # Logique de requête
        response = await self.client.request(method, endpoint, json=data)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Gestion spécifique des erreurs HTTP
        raise Exception(f"Erreur API ({e.response.status_code}): {e.response.text}")
```

## 🔒 Sécurité et bonnes pratiques

- ✅ **Authentification Bearer** obligatoire sur `/mcp`
- ✅ **Validation Pydantic** de tous les inputs JSON-RPC
- ✅ **Timeouts HTTP** configurable (défaut: 30s)
- ✅ **Utilisateur non-root** dans le container Docker
- ✅ **Variables d'environnement** pour tous les secrets
- ✅ **CORS configuré** pour les environnements web
- ✅ **Health checks** Docker intégrés

## 🚀 Performance

### Optimisations Python
- **FastAPI async** - Traitement concurrent des requêtes
- **httpx async** - Client HTTP non-bloquant
- **Pydantic V2** - Validation ultra-rapide avec Rust
- **Python 3.11+** - Performances améliorées de 25%

### Optimisations Docker
- **Image Python slim** - Réduction de 60% de la taille
- **Multi-stage build** - Cache des dépendances
- **Health checks** - Redémarrage automatique si nécessaire

## 🆚 Comparaison Node.js vs Python

| Aspect | Node.js | Python |
|--------|---------|---------|
| **Performance** | Event Loop natif | FastAPI async (comparable) |
| **Écosystème MCP** | Natif | Adapté |
| **Lisibilité** | Moyenne | Excellente |
| **Validation** | Manuel/joi | Pydantic intégré |
| **Documentation** | Swagger manuel | FastAPI auto |
| **Debugging** | Console/logs | Rich logs + pdb |

## 🤝 Support et maintenance

- **Issues**: Vérifier les logs avec `docker-compose logs -f`
- **Performance**: Utiliser `htop` dans le container
- **API Chaster**: [Documentation officielle](https://docs.chaster.app/api/)
- **FastAPI**: [Documentation FastAPI](https://fastapi.tiangolo.com/)

---

**Version:** 1.0.0 | **Licence:** MIT | **Python:** 3.11+ | **FastAPI:** 0.104+
