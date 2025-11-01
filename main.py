
import os
import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

from chaster_service import ChasterLocksService

# Chargement des variables d'environnement
load_dotenv()

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modèles Pydantic pour la validation JSON-RPC
class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[int] = None

class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[int] = None

class JsonRpcError(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

# Configuration FastAPI avec documentation Swagger
app = FastAPI(
    title="🔐 Chaster Locks MCP Server",
    description="""
    ## Serveur Model Context Protocol pour l'API Chaster Locks
    
    Ce serveur implémente le protocole MCP (Model Context Protocol) pour interagir avec l'API Chaster Locks.
    
    ### Authentification
    - **Type**: Bearer Token
    - **Header**: `Authorization: Bearer YOUR_MCP_TOKEN`
    - **Scope**: Toutes les routes `/mcp` nécessitent une authentification
    
    ### Endpoints disponibles
    - **`/health`**: Vérification de l'état du serveur (sans authentification)
    - **`/mcp`**: Endpoint principal MCP (avec authentification)
    - **`/docs`**: Cette documentation Swagger
    - **`/redoc`**: Documentation alternative ReDoc
    
    ### Protocole MCP
    Le serveur suit le standard JSON-RPC 2.0 avec les méthodes MCP :
    - `initialize` - Initialisation de la connexion MCP
    - `tools/list` - Liste des outils disponibles  
    - `tools/call` - Exécution d'un outil spécifique
    
    ### Outils Chaster disponibles
    13 outils permettent d'interagir avec l'API Chaster :
    - Gestion des verrous (liste, détails, archivage)
    - Contrôle (gel/dégel, modification durée, déverrouillage)
    - Informations (historique, combinaison, recherche)
    """,
    version="1.0.0",
    contact={
        "name": "Chaster MCP Server",
        "url": "https://github.com/your-repo/chaster-mcp-server",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "https://mcpchaster.external.nahoj.net",
            "description": "Serveur de production"
        },
        {
            "url": "http://localhost:3000",
            "description": "Serveur de développement local"
        }
    ],
    docs_url="/docs",  # Active Swagger UI
    redoc_url="/redoc",  # Active ReDoc
    openapi_url="/openapi.json"  # URL de la spécification OpenAPI
)

# Tags pour organiser les endpoints dans Swagger
tags_metadata = [
    {
        "name": "health",
        "description": "Endpoints de monitoring et vérification du serveur"
    },
    {
        "name": "mcp", 
        "description": "Model Context Protocol - Endpoints principaux (authentification requise)"
    }
]

app.openapi_tags = tags_metadata

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de l'authentification
security = HTTPBearer()
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")

if not MCP_AUTH_TOKEN:
    logger.error("MCP_AUTH_TOKEN non défini dans les variables d'environnement")
    raise ValueError("MCP_AUTH_TOKEN est requis")

# Debug: Log the expected token (first/last 4 chars only for security)
logger.info(f"🔑 Token attendu: {MCP_AUTH_TOKEN[:4]}...{MCP_AUTH_TOKEN[-4:]}")

# Service Chaster
chaster_service = ChasterLocksService()

def create_jsonrpc_response(result: Any = None, request_id: Optional[int] = None) -> JsonRpcResponse:
    """Créer une réponse JSON-RPC valide"""
    return JsonRpcResponse(result=result, id=request_id)

def create_jsonrpc_error(code: int, message: str, request_id: Optional[int] = None, data: Any = None) -> JsonRpcResponse:
    """Créer une erreur JSON-RPC"""
    error = JsonRpcError(code=code, message=message, data=data)
    return JsonRpcResponse(error=error.dict(), id=request_id)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Vérifier le token d'authentification MCP"""
    received_token = credentials.credentials
    
    # Debug: Log received token (first/last 4 chars only for security)
    logger.info(f"🔍 Token reçu: {received_token[:4]}...{received_token[-4:]}")
    logger.info(f"🔍 Tokens identiques: {received_token == MCP_AUTH_TOKEN}")
    
    if received_token != MCP_AUTH_TOKEN:
        logger.warning("❌ Token d'authentification invalide")
        raise HTTPException(
            status_code=401,
            detail="Token d'authentification invalide"
        )
    
    logger.info("✅ Authentification réussie")
    return credentials

# Routes

@app.get(
    "/health",
    tags=["health"],
    summary="Vérification de l'état du serveur",
    description="Endpoint de monitoring qui retourne l'état du serveur, accessible sans authentification",
    response_description="Statut du serveur et informations de version"
)
@app.head("/health", tags=["health"], include_in_schema=False)
async def health_check():
    """Endpoint de vérification de santé (GET et HEAD supportés)"""
    return {
        "status": "ok",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0",
        "service": "chaster-locks-mcp-server",
        "python_version": "3.11+",
        "mcp_auth_configured": bool(MCP_AUTH_TOKEN),
        "chaster_auth_configured": bool(os.getenv("CHASTER_API_TOKEN"))
    }

@app.post(
    "/mcp",
    tags=["mcp"],
    summary="Endpoint principal MCP",
    description="""
    Endpoint principal pour les requêtes Model Context Protocol.
    
    **Authentification requise**: Bearer token dans le header Authorization
    
    **Méthodes MCP supportées**:
    - `initialize` - Initialisation de la connexion MCP
    - `tools/list` - Liste des 13 outils Chaster disponibles
    - `tools/call` - Exécution d'un outil avec ses paramètres
    
    **Format**: JSON-RPC 2.0
    """,
    response_description="Réponse JSON-RPC 2.0 selon la méthode appelée",
    responses={
        200: {
            "description": "Requête MCP traitée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "jsonrpc": "2.0",
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "serverInfo": {
                                "name": "chaster-locks-mcp-server",
                                "version": "1.0.0"
                            }
                        },
                        "id": 1
                    }
                }
            }
        },
        401: {
            "description": "Token d'authentification invalide ou manquant"
        },
        400: {
            "description": "Requête JSON-RPC malformée"
        }
    }
)
async def handle_mcp(
    request: JsonRpcRequest,
    credentials: HTTPAuthorizationCredentials = Depends(verify_token)
):
    """Endpoint principal MCP avec authentification"""
    
    logger.info(f"📡 Requête MCP: {request.method}")
    
    try:
        if request.method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {},
                    "logging": {}
                },
                "serverInfo": {
                    "name": "chaster-locks-mcp-server",
                    "version": "1.0.0",
                    "description": "Serveur MCP pour l'API Chaster Locks (Python)"
                }
            }
            return create_jsonrpc_response(result, request.id)
        
        elif request.method == "tools/list":
            tools = await chaster_service.get_available_tools()
            result = {"tools": tools}
            return create_jsonrpc_response(result, request.id)
        
        elif request.method == "tools/call":
            tool_name = request.params.get("name")
            tool_args = request.params.get("arguments", {})
            
            if not tool_name:
                return create_jsonrpc_error(
                    -32602, 
                    "Paramètres invalides: nom de l'outil manquant", 
                    request.id
                )
            
            result = await chaster_service.call_tool(tool_name, tool_args)
            return create_jsonrpc_response(result, request.id)
        
        else:
            return create_jsonrpc_error(-32601, "Méthode non trouvée", request.id)
    
    except Exception as e:
        logger.error(f"❌ Erreur MCP: {str(e)}")
        return create_jsonrpc_error(-32000, str(e), request.id)

# Gestionnaires d'erreurs corrigés
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Gestionnaire 404 personnalisé - retourne JSONResponse"""
    error_response = create_jsonrpc_error(
        -32601,
        "Endpoint non trouvé. Utilisez POST /mcp pour les opérations MCP ou GET /health pour le statut",
        None
    )
    return JSONResponse(
        status_code=404,
        content=error_response.dict()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Gestionnaire d'erreur global - retourne JSONResponse"""
    logger.error(f"❌ Erreur serveur: {str(exc)}")
    error_response = create_jsonrpc_error(-32000, "Erreur interne du serveur", None)
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    
    logger.info(f"🚀 Démarrage du serveur Chaster Locks MCP sur le port {port}")
    logger.info(f"📊 Santé: http://localhost:{port}/health")
    logger.info(f"🔗 Endpoint MCP: http://localhost:{port}/mcp")
    logger.info(f"📚 Documentation Swagger: http://localhost:{port}/docs")
    logger.info(f"📖 Documentation ReDoc: http://localhost:{port}/redoc")
    logger.info(f"🔐 Authentification: Token Bearer requis")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=os.getenv("NODE_ENV") == "development",
        log_level="info"
    )
