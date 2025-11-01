
import os
import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ChasterLocksService:
    """Service pour l'API Chaster Locks avec support asynchrone"""
    
    def __init__(self):
        self.base_url = "https://api.chaster.app"
        self.bearer_token = os.getenv("CHASTER_API_TOKEN")
        
        if not self.bearer_token:
            raise ValueError("CHASTER_API_TOKEN est requis dans les variables d'environnement")
        
        # Configuration du client HTTP asynchrone
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "User-Agent": "ChasterMCP-Python/1.0.0"
            }
        )
    
    async def __aenter__(self):
        """Support du context manager asynchrone"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fermeture propre du client HTTP"""
        await self.client.aclose()
    
    def format_response(self, data: Any, message: str = "") -> Dict[str, Any]:
        """Formater une réponse pour le protocole MCP"""
        response_text = message if message else "Données récupérées avec succès"
        if data:
            response_text += f"\n\n{json.dumps(data, indent=2, ensure_ascii=False)}"
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": response_text
                }
            ]
        }
    
    async def handle_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        """Gestionnaire générique pour les requêtes HTTP"""
        try:
            logger.info(f"📤 Chaster API: {method.upper()} {endpoint}")
            
            if method.upper() == "GET":
                response = await self.client.get(endpoint, params=data)
            elif method.upper() == "POST":
                response = await self.client.post(endpoint, json=data)
            elif method.upper() == "PUT":
                response = await self.client.put(endpoint, json=data)
            else:
                raise ValueError(f"Méthode HTTP non supportée: {method}")
            
            response.raise_for_status()
            
            logger.info(f"📥 Chaster API: {response.status_code} {endpoint}")
            return response.json() if response.content else {"success": True}
        
        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Erreur API Chaster: {e.response.status_code} {endpoint}")
            error_detail = "Erreur inconnue"
            try:
                error_detail = e.response.json().get("message", str(e))
            except:
                error_detail = str(e)
            raise Exception(f"Erreur API Chaster ({e.response.status_code}): {error_detail}")
        
        except httpx.RequestError as e:
            logger.error(f"❌ Erreur réseau: {str(e)}")
            raise Exception(f"Erreur réseau lors de la requête: {str(e)}")
    
    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Retourne la liste des outils disponibles pour MCP"""
        return [
            {
                "name": "get_locks",
                "description": "Récupérer les verrous utilisateur avec filtre de statut optionnel (active, archived, all). Par défaut: active",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "archived", "all"],
                            "default": "active",
                            "description": "Statut des verrous à récupérer"
                        }
                    }
                }
            },
            {
                "name": "get_lock_details",
                "description": "Obtenir les détails d'un verrou spécifique par son ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou à récupérer"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "archive_lock",
                "description": "Archiver un verrou (action du porteur)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou à archiver"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "archive_lock_keyholder",
                "description": "Archiver un verrou en tant que gardien de clé",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou à archiver"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "update_lock_time",
                "description": "Mettre à jour la durée d'un verrou (en secondes)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        },
                        "duration": {
                            "type": "number",
                            "description": "Nouvelle durée en secondes",
                            "minimum": 0
                        }
                    },
                    "required": ["lock_id", "duration"]
                }
            },
            {
                "name": "freeze_lock",
                "description": "Geler ou dégeler un verrou",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        },
                        "freeze": {
                            "type": "boolean",
                            "description": "True pour geler, False pour dégeler"
                        }
                    },
                    "required": ["lock_id", "freeze"]
                }
            },
            {
                "name": "unlock_lock",
                "description": "Déverrouiller définitivement un verrou",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou à déverrouiller"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "convert_to_self_lock",
                "description": "Convertir un verrou avec gardien en auto-verrou",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou à convertir"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "update_lock_settings",
                "description": "Mettre à jour les paramètres d'affichage et de comportement du verrou",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        },
                        "settings": {
                            "type": "object",
                            "properties": {
                                "display_remaining_time": {"type": "boolean"},
                                "limit_lock_time": {"type": "boolean"},
                                "hide_time_logs": {"type": "boolean"}
                            },
                            "description": "Nouveaux paramètres du verrou"
                        }
                    },
                    "required": ["lock_id", "settings"]
                }
            },
            {
                "name": "trust_keyholder",
                "description": "Marquer le gardien de clé comme fiable",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "get_lock_combination",
                "description": "Obtenir la combinaison du verrou si disponible",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "get_lock_history",
                "description": "Obtenir l'historique d'activité du verrou",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {
                            "type": "string",
                            "description": "ID du verrou"
                        },
                        "limit": {
                            "type": "number",
                            "description": "Nombre maximum d'entrées",
                            "default": 50
                        },
                        "offset": {
                            "type": "number",
                            "description": "Nombre d'entrées à ignorer",
                            "default": 0
                        }
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "search_locks",
                "description": "Rechercher des verrous avec des filtres avancés",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "archived", "all"],
                            "description": "Statut des verrous"
                        },
                        "role": {
                            "type": "string",
                            "enum": ["wearer", "keyholder"],
                            "description": "Rôle de l'utilisateur"
                        },
                        "search": {
                            "type": "string",
                            "description": "Terme de recherche"
                        }
                    }
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Exécuter un outil spécifique"""
        if args is None:
            args = {}
        
        try:
            if tool_name == "get_locks":
                return await self.get_locks(args.get("status", "active"))
            
            elif tool_name == "get_lock_details":
                return await self.get_lock_details(args["lock_id"])
            
            elif tool_name == "archive_lock":
                return await self.archive_lock(args["lock_id"])
            
            elif tool_name == "archive_lock_keyholder":
                return await self.archive_lock_keyholder(args["lock_id"])
            
            elif tool_name == "update_lock_time":
                return await self.update_lock_time(args["lock_id"], args["duration"])
            
            elif tool_name == "freeze_lock":
                return await self.freeze_lock(args["lock_id"], args["freeze"])
            
            elif tool_name == "unlock_lock":
                return await self.unlock_lock(args["lock_id"])
            
            elif tool_name == "convert_to_self_lock":
                return await self.convert_to_self_lock(args["lock_id"])
            
            elif tool_name == "update_lock_settings":
                return await self.update_lock_settings(args["lock_id"], args["settings"])
            
            elif tool_name == "trust_keyholder":
                return await self.trust_keyholder(args["lock_id"])
            
            elif tool_name == "get_lock_combination":
                return await self.get_lock_combination(args["lock_id"])
            
            elif tool_name == "get_lock_history":
                return await self.get_lock_history(
                    args["lock_id"], 
                    args.get("limit", 50), 
                    args.get("offset", 0)
                )
            
            elif tool_name == "search_locks":
                return await self.search_locks(args)
            
            else:
                raise ValueError(f"Outil inconnu: {tool_name}")
        
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'exécution de l'outil {tool_name}: {str(e)}")
            raise
    
    # Implémentations des méthodes API
    
    async def get_locks(self, status: str = "active") -> Dict[str, Any]:
        """Récupérer les verrous utilisateur"""
        params = {"status": status} if status != "active" else None
        data = await self.handle_request("GET", "/locks", params)
        return self.format_response(data, f"Trouvé {len(data)} verrous (statut: {status})")
    
    async def get_lock_details(self, lock_id: str) -> Dict[str, Any]:
        """Obtenir les détails d'un verrou"""
        data = await self.handle_request("GET", f"/locks/{lock_id}")
        return self.format_response(data, f"Détails du verrou {lock_id}")
    
    async def archive_lock(self, lock_id: str) -> Dict[str, Any]:
        """Archiver un verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/archive")
        return self.format_response(data, f"Verrou {lock_id} archivé avec succès")
    
    async def archive_lock_keyholder(self, lock_id: str) -> Dict[str, Any]:
        """Archiver un verrou en tant que gardien"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/archive/keyholder")
        return self.format_response(data, f"Verrou {lock_id} archivé par le gardien")
    
    async def update_lock_time(self, lock_id: str, duration: int) -> Dict[str, Any]:
        """Mettre à jour la durée du verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/update-time", {"duration": duration})
        return self.format_response(data, f"Durée du verrou {lock_id} mise à jour à {duration} secondes")
    
    async def freeze_lock(self, lock_id: str, freeze: bool) -> Dict[str, Any]:
        """Geler ou dégeler un verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/freeze", {"freeze": freeze})
        action = "gelé" if freeze else "dégelé"
        return self.format_response(data, f"Verrou {lock_id} {action} avec succès")
    
    async def unlock_lock(self, lock_id: str) -> Dict[str, Any]:
        """Déverrouiller un verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/unlock")
        return self.format_response(data, f"Verrou {lock_id} déverrouillé définitivement")
    
    async def convert_to_self_lock(self, lock_id: str) -> Dict[str, Any]:
        """Convertir en auto-verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/convert-to-self-lock")
        return self.format_response(data, f"Verrou {lock_id} converti en auto-verrou")
    
    async def update_lock_settings(self, lock_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Mettre à jour les paramètres du verrou"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/settings", settings)
        return self.format_response(data, f"Paramètres du verrou {lock_id} mis à jour")
    
    async def trust_keyholder(self, lock_id: str) -> Dict[str, Any]:
        """Faire confiance au gardien"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/trust-keyholder")
        return self.format_response(data, f"Gardien de clé marqué comme fiable pour le verrou {lock_id}")
    
    async def get_lock_combination(self, lock_id: str) -> Dict[str, Any]:
        """Obtenir la combinaison"""
        data = await self.handle_request("GET", f"/locks/{lock_id}/combination")
        return self.format_response(data, f"Combinaison pour le verrou {lock_id}")
    
    async def get_lock_history(self, lock_id: str, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Obtenir l'historique"""
        data = await self.handle_request("POST", f"/locks/{lock_id}/history", {"limit": limit, "offset": offset})
        return self.format_response(data, f"Historique du verrou {lock_id} ({len(data)} entrées)")
    
    async def search_locks(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Rechercher des verrous"""
        if filters is None:
            filters = {}
        data = await self.handle_request("POST", "/locks/search", filters)
        return self.format_response(data, f"Résultats de recherche: {len(data)} verrous trouvés")
