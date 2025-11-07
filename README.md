
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

## 🔧 Available Chaster MCP Tools (86 Total)

The Python version now supports **ALL 86 Chaster Public API endpoints**!

> **Note**: The Chaster API has 114 total endpoints, but 28 are part of the Partner Extensions API specifically for extension developers. This server implements all 86 public user-facing endpoints.

### 📋 Locks (18 tools)
- `get_locks` - List locks with status filters
- `get_lock_details` - Complete lock details
- `archive_lock` / `archive_lock_keyholder` - Archive locks
- `unlock_lock` - Permanent unlock
- `update_lock_time` - Duration modification
- `freeze_lock` - Freeze/unfreeze lock
- `update_lock_settings` - Display settings
- `update_max_limit_date` - Increase max limit date
- `trust_keyholder` - Mark keyholder as trusted
- `get_lock_combination` - Retrieve combination
- `get_lock_history` - Activity history
- `set_test_lock` - Mark as test lock
- `get_user_public_locks` - Get user's public locks
- `search_locks` - Advanced search
- `get_lock_extension` - Extension information
- `trigger_lock_extension_action` - Trigger extension action
- `convert_to_self_lock` - Convert to self-lock

### 🔨 Lock Creation (3 tools)
- `create_lock` - Create a new lock
- `edit_lock_extensions` - Edit lock extensions
- `create_lock_from_shared` - Create from shared lock

### 👤 Profile (7 tools)
- `get_user_profile_by_id` - Get user by ID
- `get_user_profile` - Get user by username
- `get_user_profile_details` - Detailed profile
- `get_badge_count` - User badge count
- `update_profile_from_auth` - Update from auth server
- `get_auth_profile` - Logged user info
- `set_user_profile` - Update profile

### 💬 Messaging (9 tools)
- `find_conversation_by_user` - Find conversation
- `create_conversation` - Start new conversation
- `get_conversations` - List conversations
- `add_message` - Send message
- `get_conversation` - Get conversation details
- `set_conversation_status` - Update status
- `set_conversation_unread` - Set unread
- `get_messages` - Get messages
- `get_ignored_users` - List ignored users

### 🔑 Keyholder (1 tool)
- `search_locked_users` - Search locked users

### 🔓 Shared Locks (11 tools)
- `get_shared_locks` - List shared locks
- `create_shared_lock` - Create shared lock
- `get_shared_lock` - Get shared lock details
- `update_shared_lock` - Update shared lock
- `archive_shared_lock` - Archive shared lock
- `get_shared_lock_tags` - Get all tags
- `get_suggested_tags` - Get suggested tags
- `check_favorite_shared_lock` - Check favorite status
- `add_favorite_shared_lock` - Add to favorites
- `remove_favorite_shared_lock` - Remove from favorites
- `get_favorite_shared_locks` - List favorites

### 🌐 Public Locks (4 tools)
- `get_public_lock` - Get public lock
- `get_lock_image` - Generate lock image
- `search_public_locks` - Search public locks
- `get_explore_categories` - Explore categories

### 🤝 Session Offer (7 tools)
- `create_keyholding_offer` - Create offer
- `accept_keyholding_request` - Accept request
- `get_keyholding_offer_status` - Get status
- `get_offer_public_info` - Get offer info
- `respond_to_keyholding_offer` - Accept/reject
- `archive_keyholding_offer` - Archive offer
- `get_keyholding_requests` - List requests

### 🚫 Blocks (4 tools)
- `get_blocked_users` - List blocked users
- `block_user` - Block user
- `get_block_interaction` - Check block status
- `unblock_user` - Unblock user

### 🧩 Extensions (1 tool)
- `get_extensions` - List available extensions

### 🔢 Combinations (2 tools)
- `upload_combination_image` - Upload image
- `create_code_combination` - Create code

### ⚖️ Extensions - Penalties (4 tools)
- `get_penalties` - List penalties
- `get_penalty_session` - Get penalty session
- `search_penalty_periods` - Search periods
- `get_punishable_actions` - List actions

### 🔓 Extensions - Temporary Opening (3 tools)
- `get_temporary_combination` - Get combination
- `set_temporary_combination` - Set combination
- `get_action_log_combination` - Get from log

### 📸 Extensions - Verification Picture (2 tools)
- `submit_verification_picture` - Submit picture
- `get_verification_pictures` - Get history

### 📁 Files (2 tools)
- `upload_files` - Upload attachments
- `get_file` - Get file by key

### 👥 Users (4 tools)
- `search_users` - Search users
- `search_user_by_username` - Search by username
- `search_user_by_discord` - Search by Discord ID
- `update_current_user` - Update current user

### 🎉 Community Events (2 tools)
- `get_event_categories` - Event categories
- `get_event_task_details` - Task details

### ⚙️ Settings (1 tool)
- `get_app_settings` - Application settings

### 🚨 Reports (1 tool)
- `create_report` - Create report

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

**Version:** 2.0.0 | **License:** MIT | **Python:** 3.11+ | **FastAPI:** 0.104+

## 🆕 Version 2.0.0 - Complete API Coverage

**What's New:**
- ✨ **ALL 86 Chaster Public API endpoints** now implemented (was 13)
- 📦 **73 new tools** added covering:
  - Profile management and user search
  - Complete messaging system
  - Shared and public locks management
  - Keyholding offers and session management
  - User blocking and reporting
  - Extensions (penalties, temporary opening, verification)
  - File uploads and combinations
  - Community events
- 🏗️ **Maintained architecture**: Same async HTTP structure
- 🔄 **Backward compatible**: All original 13 tools work the same way
- 📚 **Complete documentation**: All tools documented in README and Swagger

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

**Version:** 2.0.0 | **Licence:** MIT | **Python:** 3.11+ | **FastAPI:** 0.104+

## 🆕 Version 2.0.0 - Couverture complète de l'API

**Nouveautés:**
- ✨ **TOUS les 86 endpoints de l'API publique Chaster** maintenant implémentés (était 13)
- 📦 **73 nouveaux outils** ajoutés couvrant:
  - Gestion des profils et recherche d'utilisateurs
  - Système de messagerie complet
  - Gestion des verrous partagés et publics
  - Offres de gardiennage et gestion de session
  - Blocage d'utilisateurs et signalements
  - Extensions (pénalités, ouverture temporaire, vérification)
  - Upload de fichiers et combinaisons
  - Événements communautaires
- 🏗️ **Architecture préservée**: Même structure HTTP async
- 🔄 **Rétrocompatible**: Les 13 outils originaux fonctionnent de la même manière
- 📚 **Documentation complète**: Tous les outils documentés dans README et Swagger
