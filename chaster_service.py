
import os
import json
import logging
from typing import Dict, Any, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ChasterLocksService:
    """Complete Chaster API Service with all 114 endpoints"""

    def __init__(self):
        self.base_url = "https://api.chaster.app"
        self.bearer_token = os.getenv("CHASTER_API_TOKEN")

        if not self.bearer_token:
            raise ValueError("CHASTER_API_TOKEN is required in environment variables")

        # Configure async HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {self.bearer_token}",
                "Content-Type": "application/json",
                "User-Agent": "ChasterMCP-Python/2.0.0"
            }
        )

    async def __aenter__(self):
        """Async context manager support"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean shutdown of HTTP client"""
        await self.client.aclose()

    def format_response(self, data: Any, message: str = "") -> Dict[str, Any]:
        """Format a response for MCP protocol"""
        response_text = message if message else "Data retrieved successfully"
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

    async def handle_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Generic handler for HTTP requests"""
        try:
            logger.info(f"📤 Chaster API: {method.upper()} {endpoint}")

            if method.upper() == "GET":
                response = await self.client.get(endpoint, params=params or data)
            elif method.upper() == "POST":
                response = await self.client.post(endpoint, json=data, params=params)
            elif method.upper() == "PUT":
                response = await self.client.put(endpoint, json=data, params=params)
            elif method.upper() == "PATCH":
                response = await self.client.patch(endpoint, json=data, params=params)
            elif method.upper() == "DELETE":
                response = await self.client.delete(endpoint, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            logger.info(f"📥 Chaster API: {response.status_code} {endpoint}")
            return response.json() if response.content else {"success": True}

        except httpx.HTTPStatusError as e:
            logger.error(f"❌ Chaster API error: {e.response.status_code} {endpoint}")
            error_detail = "Unknown error"
            try:
                error_detail = e.response.json().get("message", str(e))
            except:
                error_detail = str(e)
            raise Exception(f"Chaster API error ({e.response.status_code}): {error_detail}")

        except httpx.RequestError as e:
            logger.error(f"❌ Network error: {str(e)}")
            raise Exception(f"Network error during request: {str(e)}")

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """Return the complete list of 114 available tools for MCP"""
        return [
            # ==================== LOCKS ====================
            {
                "name": "get_locks",
                "description": "Retrieve user locks with optional status filter (active, archived, all). Default: active",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["active", "archived", "all"],
                            "default": "active",
                            "description": "Status of locks to retrieve"
                        }
                    }
                }
            },
            {
                "name": "get_lock_details",
                "description": "Get details of a specific lock by its ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "ID of the lock to retrieve"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "archive_lock",
                "description": "Archive a lock (wearer action)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "ID of the lock to archive"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "archive_lock_keyholder",
                "description": "Archive a lock as keyholder",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "ID of the lock to archive"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "update_lock_time",
                "description": "Update lock duration (in seconds)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "duration": {"type": "number", "description": "New duration in seconds", "minimum": 0}
                    },
                    "required": ["lock_id", "duration"]
                }
            },
            {
                "name": "freeze_lock",
                "description": "Freeze or unfreeze a lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "freeze": {"type": "boolean", "description": "True to freeze, False to unfreeze"}
                    },
                    "required": ["lock_id", "freeze"]
                }
            },
            {
                "name": "unlock_lock",
                "description": "Permanently unlock a lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "ID of the lock to unlock"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "convert_to_self_lock",
                "description": "Convert a keyholder lock to self-lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "ID of the lock to convert"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "update_lock_settings",
                "description": "Update lock display and behavior settings",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "settings": {
                            "type": "object",
                            "properties": {
                                "displayRemainingTime": {"type": "boolean"},
                                "hideTimeLogs": {"type": "boolean"}
                            },
                            "description": "New lock settings (use camelCase property names)"
                        }
                    },
                    "required": ["lock_id", "settings"]
                }
            },
            {
                "name": "update_max_limit_date",
                "description": "Increase the max limit date of a lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "max_limit_date": {"type": "string", "description": "New max limit date (ISO 8601 format)"}
                    },
                    "required": ["lock_id", "max_limit_date"]
                }
            },
            {
                "name": "trust_keyholder",
                "description": "Mark keyholder as trusted",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "get_lock_combination",
                "description": "Get lock combination if available",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "get_lock_history",
                "description": "Get lock activity history",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "limit": {"type": "number", "description": "Maximum number of entries", "default": 50},
                        "lastId": {"type": "string", "description": "Last entry ID for pagination"},
                        "extension": {"type": "string", "description": "Filter by extension slug"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "set_test_lock",
                "description": "Set an archived lock as a test lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "is_test_lock": {"type": "boolean", "description": "Whether this is a test lock"}
                    },
                    "required": ["lock_id", "is_test_lock"]
                }
            },
            {
                "name": "get_user_public_locks",
                "description": "Get public locks of a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "search_locks",
                "description": "Search locks with pagination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filterByArchivedLocks": {"type": "boolean"},
                        "limit": {"type": "number"},
                        "cursor": {"type": "string"}
                    }
                }
            },
            {
                "name": "get_lock_extension",
                "description": "Get information from an extension for a given lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "extension_id": {"type": "string", "description": "Extension ID"}
                    },
                    "required": ["lock_id", "extension_id"]
                }
            },
            {
                "name": "trigger_lock_extension_action",
                "description": "Trigger an action for a lock extension",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "extension_id": {"type": "string", "description": "Extension ID"},
                        "action_data": {"type": "object", "description": "Action data"}
                    },
                    "required": ["lock_id", "extension_id"]
                }
            },

            # ==================== LOCK CREATION ====================
            {
                "name": "create_lock",
                "description": "Create a new lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_data": {
                            "type": "object",
                            "description": "Lock configuration data"
                        }
                    },
                    "required": ["lock_data"]
                }
            },
            {
                "name": "edit_lock_extensions",
                "description": "Edit lock extensions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "extensions": {"type": "array", "description": "Extensions configuration"}
                    },
                    "required": ["lock_id", "extensions"]
                }
            },
            {
                "name": "create_lock_from_shared",
                "description": "Create a lock from a shared lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"},
                        "lock_data": {"type": "object", "description": "Additional lock data"}
                    },
                    "required": ["shared_lock_id"]
                }
            },

            # ==================== PROFILE ====================
            {
                "name": "get_user_profile_by_id",
                "description": "Find a user by their ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "get_user_profile",
                "description": "Find a user profile by username",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username"}
                    },
                    "required": ["username"]
                }
            },
            {
                "name": "get_user_profile_details",
                "description": "Find a user profile with detailed information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username"}
                    },
                    "required": ["username"]
                }
            },
            {
                "name": "get_badge_count",
                "description": "Get the user badge count",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "update_profile_from_auth",
                "description": "Update profile from the authentication server",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_auth_profile",
                "description": "Get logged user information",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "set_user_profile",
                "description": "Set the user profile",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "profile_data": {"type": "object", "description": "Profile data"}
                    },
                    "required": ["profile_data"]
                }
            },

            # ==================== MESSAGING ====================
            {
                "name": "find_conversation_by_user",
                "description": "Find conversation by user ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "create_conversation",
                "description": "Create a new conversation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to start conversation with"},
                        "message": {"type": "string", "description": "Initial message"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "get_conversations",
                "description": "Get list of conversations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "number", "description": "Maximum number of conversations"},
                        "offset": {"type": "number", "description": "Pagination offset"}
                    }
                }
            },
            {
                "name": "add_message",
                "description": "Add a new message to a conversation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "Conversation ID"},
                        "message": {"type": "string", "description": "Message content"}
                    },
                    "required": ["conversation_id", "message"]
                }
            },
            {
                "name": "get_conversation",
                "description": "Get a specific conversation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "Conversation ID"}
                    },
                    "required": ["conversation_id"]
                }
            },
            {
                "name": "set_conversation_status",
                "description": "Set conversation status (read/unread)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "Conversation ID"},
                        "status": {"type": "string", "description": "Status (read/unread)"}
                    },
                    "required": ["conversation_id", "status"]
                }
            },
            {
                "name": "set_conversation_unread",
                "description": "Set conversation unread status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "Conversation ID"},
                        "unread": {"type": "boolean", "description": "Unread status"}
                    },
                    "required": ["conversation_id", "unread"]
                }
            },
            {
                "name": "get_messages",
                "description": "Get messages in a conversation",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "conversation_id": {"type": "string", "description": "Conversation ID"},
                        "limit": {"type": "number", "description": "Maximum number of messages"},
                        "before": {"type": "string", "description": "Get messages before this ID"}
                    },
                    "required": ["conversation_id"]
                }
            },
            {
                "name": "get_ignored_users",
                "description": "Get list of ignored users in messaging",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== KEYHOLDER ====================
            {
                "name": "search_locked_users",
                "description": "Search locked users as keyholder",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "number", "description": "Maximum number of results"}
                    }
                }
            },

            # ==================== SHARED LOCKS ====================
            {
                "name": "get_shared_locks",
                "description": "Get all user shared locks",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "create_shared_lock",
                "description": "Create a new shared lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_data": {"type": "object", "description": "Shared lock configuration"}
                    },
                    "required": ["shared_lock_data"]
                }
            },
            {
                "name": "get_shared_lock",
                "description": "Get a specific shared lock by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "update_shared_lock",
                "description": "Update a shared lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"},
                        "shared_lock_data": {"type": "object", "description": "Updated data"}
                    },
                    "required": ["shared_lock_id", "shared_lock_data"]
                }
            },
            {
                "name": "archive_shared_lock",
                "description": "Archive a shared lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "get_shared_lock_tags",
                "description": "Get all shared lock tags",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_suggested_tags",
                "description": "Get suggested tags for a shared lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string", "description": "Lock description"}
                    }
                }
            },
            {
                "name": "check_favorite_shared_lock",
                "description": "Check if a shared lock is in user favorites",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "add_favorite_shared_lock",
                "description": "Add a shared lock to favorites",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "remove_favorite_shared_lock",
                "description": "Remove a shared lock from favorites",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "get_favorite_shared_locks",
                "description": "Get user favorite shared locks",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== PUBLIC LOCKS ====================
            {
                "name": "get_public_lock",
                "description": "Get a public shared lock by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "get_lock_image",
                "description": "Generate a shared lock image",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "shared_lock_id": {"type": "string", "description": "Shared lock ID"}
                    },
                    "required": ["shared_lock_id"]
                }
            },
            {
                "name": "search_public_locks",
                "description": "Search for public locks",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "tags": {"type": "array", "description": "Tags to filter by"},
                        "limit": {"type": "number", "description": "Maximum results"}
                    }
                }
            },
            {
                "name": "get_explore_categories",
                "description": "Get Explore page lock categories",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== SESSION OFFER ====================
            {
                "name": "create_keyholding_offer",
                "description": "Create a keyholding offer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "accept_keyholding_request",
                "description": "Accept a keyholding request",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "offer_token": {"type": "string", "description": "Offer token"}
                    },
                    "required": ["offer_token"]
                }
            },
            {
                "name": "get_keyholding_offer_status",
                "description": "Get keyholding offers status for a lock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "get_offer_public_info",
                "description": "Get public information of a lock from offer token",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "offer_token": {"type": "string", "description": "Offer token"}
                    },
                    "required": ["offer_token"]
                }
            },
            {
                "name": "respond_to_keyholding_offer",
                "description": "Accept or reject a keyholding offer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_request_id": {"type": "string", "description": "Session request ID"},
                        "accept": {"type": "boolean", "description": "Accept or reject"}
                    },
                    "required": ["session_request_id", "accept"]
                }
            },
            {
                "name": "archive_keyholding_offer",
                "description": "Archive a keyholding offer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_request_id": {"type": "string", "description": "Session request ID"}
                    },
                    "required": ["session_request_id"]
                }
            },
            {
                "name": "get_keyholding_requests",
                "description": "Get keyholding offers from wearers",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== BLOCKS ====================
            {
                "name": "get_blocked_users",
                "description": "Get list of blocked users",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "block_user",
                "description": "Block a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to block"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "get_block_interaction",
                "description": "Check block interaction with another user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "Target user ID"}
                    },
                    "required": ["user_id"]
                }
            },
            {
                "name": "unblock_user",
                "description": "Unblock a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "User ID to unblock"}
                    },
                    "required": ["user_id"]
                }
            },

            # ==================== EXTENSIONS ====================
            {
                "name": "get_extensions",
                "description": "Get the list of available extensions",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== COMBINATIONS ====================
            {
                "name": "upload_combination_image",
                "description": "Upload a combination image",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image_data": {"type": "string", "description": "Base64 encoded image"}
                    },
                    "required": ["image_data"]
                }
            },
            {
                "name": "create_code_combination",
                "description": "Create a code combination",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string", "description": "Combination code"}
                    },
                    "required": ["code"]
                }
            },

            # ==================== FILES ====================
            {
                "name": "upload_files",
                "description": "Upload attachments for messaging and posts",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "files": {"type": "array", "description": "Files to upload"}
                    },
                    "required": ["files"]
                }
            },
            {
                "name": "get_file",
                "description": "Get a file by its key",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_key": {"type": "string", "description": "File key"}
                    },
                    "required": ["file_key"]
                }
            },

            # ==================== USERS ====================
            {
                "name": "search_users",
                "description": "Search for users",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "number", "description": "Maximum results"}
                    }
                }
            },
            {
                "name": "search_user_by_username",
                "description": "Search a user by username",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string", "description": "Username"}
                    },
                    "required": ["username"]
                }
            },
            {
                "name": "search_user_by_discord",
                "description": "Search a user by Discord ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "discord_id": {"type": "string", "description": "Discord ID"}
                    },
                    "required": ["discord_id"]
                }
            },
            {
                "name": "update_current_user",
                "description": "Update current user information",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_data": {"type": "object", "description": "User data to update"}
                    },
                    "required": ["user_data"]
                }
            },

            # ==================== COMMUNITY EVENTS ====================
            {
                "name": "get_event_categories",
                "description": "Get community event categories",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_event_task_details",
                "description": "Get community event task details for a given day",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "string", "description": "Category ID"},
                        "day": {"type": "string", "description": "Day (ISO format)"}
                    }
                }
            },

            # ==================== SETTINGS ====================
            {
                "name": "get_app_settings",
                "description": "Get application settings",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== REPORTS ====================
            {
                "name": "create_report",
                "description": "Create a report for inappropriate content or behavior",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "report_data": {"type": "object", "description": "Report details"}
                    },
                    "required": ["report_data"]
                }
            },

            # ==================== EXTENSIONS - PENALTIES ====================
            {
                "name": "get_penalties",
                "description": "Get all available penalties",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "get_penalty_session",
                "description": "Get penalty session for a lock extension",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "extension_id": {"type": "string", "description": "Extension ID"}
                    },
                    "required": ["lock_id", "extension_id"]
                }
            },
            {
                "name": "search_penalty_periods",
                "description": "Search penalty periods for a lock extension",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "extension_id": {"type": "string", "description": "Extension ID"},
                        "filters": {"type": "object", "description": "Search filters"}
                    },
                    "required": ["lock_id", "extension_id"]
                }
            },
            {
                "name": "get_punishable_actions",
                "description": "Get all punishable actions",
                "inputSchema": {"type": "object", "properties": {}}
            },

            # ==================== EXTENSIONS - TEMPORARY OPENING ====================
            {
                "name": "get_temporary_combination",
                "description": "Get a lock combination for temporary opening",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            },
            {
                "name": "set_temporary_combination",
                "description": "Set a new combination for temporary opening",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "combination": {"type": "string", "description": "New combination"}
                    },
                    "required": ["lock_id", "combination"]
                }
            },
            {
                "name": "get_action_log_combination",
                "description": "Get combination from an action log",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "action_log_id": {"type": "string", "description": "Action log ID"}
                    },
                    "required": ["lock_id", "action_log_id"]
                }
            },

            # ==================== EXTENSIONS - VERIFICATION PICTURE ====================
            {
                "name": "submit_verification_picture",
                "description": "Submit a verification picture",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"},
                        "image_data": {"type": "string", "description": "Base64 encoded image"}
                    },
                    "required": ["lock_id", "image_data"]
                }
            },
            {
                "name": "get_verification_pictures",
                "description": "Get history of verification pictures",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "lock_id": {"type": "string", "description": "Lock ID"}
                    },
                    "required": ["lock_id"]
                }
            }
        ]

    async def call_tool(self, tool_name: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a specific tool"""
        if args is None:
            args = {}

        try:
            # ==================== LOCKS ====================
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
            elif tool_name == "update_max_limit_date":
                return await self.update_max_limit_date(args["lock_id"], args["max_limit_date"])
            elif tool_name == "trust_keyholder":
                return await self.trust_keyholder(args["lock_id"])
            elif tool_name == "get_lock_combination":
                return await self.get_lock_combination(args["lock_id"])
            elif tool_name == "get_lock_history":
                return await self.get_lock_history(
                    args["lock_id"],
                    args.get("limit", 50),
                    args.get("lastId"),
                    args.get("extension")
                )
            elif tool_name == "set_test_lock":
                return await self.set_test_lock(args["lock_id"], args["is_test_lock"])
            elif tool_name == "get_user_public_locks":
                return await self.get_user_public_locks(args["user_id"])
            elif tool_name == "search_locks":
                return await self.search_locks(args)
            elif tool_name == "get_lock_extension":
                return await self.get_lock_extension(args["lock_id"], args["extension_id"])
            elif tool_name == "trigger_lock_extension_action":
                return await self.trigger_lock_extension_action(
                    args["lock_id"],
                    args["extension_id"],
                    args.get("action_data", {})
                )

            # ==================== LOCK CREATION ====================
            elif tool_name == "create_lock":
                return await self.create_lock(args["lock_data"])
            elif tool_name == "edit_lock_extensions":
                return await self.edit_lock_extensions(args["lock_id"], args["extensions"])
            elif tool_name == "create_lock_from_shared":
                return await self.create_lock_from_shared(args["shared_lock_id"], args.get("lock_data", {}))

            # ==================== PROFILE ====================
            elif tool_name == "get_user_profile_by_id":
                return await self.get_user_profile_by_id(args["user_id"])
            elif tool_name == "get_user_profile":
                return await self.get_user_profile(args["username"])
            elif tool_name == "get_user_profile_details":
                return await self.get_user_profile_details(args["username"])
            elif tool_name == "get_badge_count":
                return await self.get_badge_count()
            elif tool_name == "update_profile_from_auth":
                return await self.update_profile_from_auth()
            elif tool_name == "get_auth_profile":
                return await self.get_auth_profile()
            elif tool_name == "set_user_profile":
                return await self.set_user_profile(args["profile_data"])

            # ==================== MESSAGING ====================
            elif tool_name == "find_conversation_by_user":
                return await self.find_conversation_by_user(args["user_id"])
            elif tool_name == "create_conversation":
                return await self.create_conversation(args["user_id"], args.get("message"))
            elif tool_name == "get_conversations":
                return await self.get_conversations(args.get("limit"), args.get("offset"))
            elif tool_name == "add_message":
                return await self.add_message(args["conversation_id"], args["message"])
            elif tool_name == "get_conversation":
                return await self.get_conversation(args["conversation_id"])
            elif tool_name == "set_conversation_status":
                return await self.set_conversation_status(args["conversation_id"], args["status"])
            elif tool_name == "set_conversation_unread":
                return await self.set_conversation_unread(args["conversation_id"], args["unread"])
            elif tool_name == "get_messages":
                return await self.get_messages(
                    args["conversation_id"],
                    args.get("limit"),
                    args.get("before")
                )
            elif tool_name == "get_ignored_users":
                return await self.get_ignored_users()

            # ==================== KEYHOLDER ====================
            elif tool_name == "search_locked_users":
                return await self.search_locked_users(args.get("query"), args.get("limit"))

            # ==================== SHARED LOCKS ====================
            elif tool_name == "get_shared_locks":
                return await self.get_shared_locks()
            elif tool_name == "create_shared_lock":
                return await self.create_shared_lock(args["shared_lock_data"])
            elif tool_name == "get_shared_lock":
                return await self.get_shared_lock(args["shared_lock_id"])
            elif tool_name == "update_shared_lock":
                return await self.update_shared_lock(args["shared_lock_id"], args["shared_lock_data"])
            elif tool_name == "archive_shared_lock":
                return await self.archive_shared_lock(args["shared_lock_id"])
            elif tool_name == "get_shared_lock_tags":
                return await self.get_shared_lock_tags()
            elif tool_name == "get_suggested_tags":
                return await self.get_suggested_tags(args.get("description"))
            elif tool_name == "check_favorite_shared_lock":
                return await self.check_favorite_shared_lock(args["shared_lock_id"])
            elif tool_name == "add_favorite_shared_lock":
                return await self.add_favorite_shared_lock(args["shared_lock_id"])
            elif tool_name == "remove_favorite_shared_lock":
                return await self.remove_favorite_shared_lock(args["shared_lock_id"])
            elif tool_name == "get_favorite_shared_locks":
                return await self.get_favorite_shared_locks()

            # ==================== PUBLIC LOCKS ====================
            elif tool_name == "get_public_lock":
                return await self.get_public_lock(args["shared_lock_id"])
            elif tool_name == "get_lock_image":
                return await self.get_lock_image(args["shared_lock_id"])
            elif tool_name == "search_public_locks":
                return await self.search_public_locks(
                    args.get("query"),
                    args.get("tags"),
                    args.get("limit")
                )
            elif tool_name == "get_explore_categories":
                return await self.get_explore_categories()

            # ==================== SESSION OFFER ====================
            elif tool_name == "create_keyholding_offer":
                return await self.create_keyholding_offer(args["lock_id"])
            elif tool_name == "accept_keyholding_request":
                return await self.accept_keyholding_request(args["offer_token"])
            elif tool_name == "get_keyholding_offer_status":
                return await self.get_keyholding_offer_status(args["lock_id"])
            elif tool_name == "get_offer_public_info":
                return await self.get_offer_public_info(args["offer_token"])
            elif tool_name == "respond_to_keyholding_offer":
                return await self.respond_to_keyholding_offer(args["session_request_id"], args["accept"])
            elif tool_name == "archive_keyholding_offer":
                return await self.archive_keyholding_offer(args["session_request_id"])
            elif tool_name == "get_keyholding_requests":
                return await self.get_keyholding_requests()

            # ==================== BLOCKS ====================
            elif tool_name == "get_blocked_users":
                return await self.get_blocked_users()
            elif tool_name == "block_user":
                return await self.block_user(args["user_id"])
            elif tool_name == "get_block_interaction":
                return await self.get_block_interaction(args["user_id"])
            elif tool_name == "unblock_user":
                return await self.unblock_user(args["user_id"])

            # ==================== EXTENSIONS ====================
            elif tool_name == "get_extensions":
                return await self.get_extensions()

            # ==================== COMBINATIONS ====================
            elif tool_name == "upload_combination_image":
                return await self.upload_combination_image(args["image_data"])
            elif tool_name == "create_code_combination":
                return await self.create_code_combination(args["code"])

            # ==================== FILES ====================
            elif tool_name == "upload_files":
                return await self.upload_files(args["files"])
            elif tool_name == "get_file":
                return await self.get_file(args["file_key"])

            # ==================== USERS ====================
            elif tool_name == "search_users":
                return await self.search_users(args.get("query"), args.get("limit"))
            elif tool_name == "search_user_by_username":
                return await self.search_user_by_username(args["username"])
            elif tool_name == "search_user_by_discord":
                return await self.search_user_by_discord(args["discord_id"])
            elif tool_name == "update_current_user":
                return await self.update_current_user(args["user_data"])

            # ==================== COMMUNITY EVENTS ====================
            elif tool_name == "get_event_categories":
                return await self.get_event_categories()
            elif tool_name == "get_event_task_details":
                return await self.get_event_task_details(args.get("category_id"), args.get("day"))

            # ==================== SETTINGS ====================
            elif tool_name == "get_app_settings":
                return await self.get_app_settings()

            # ==================== REPORTS ====================
            elif tool_name == "create_report":
                return await self.create_report(args["report_data"])

            # ==================== EXTENSIONS - PENALTIES ====================
            elif tool_name == "get_penalties":
                return await self.get_penalties()
            elif tool_name == "get_penalty_session":
                return await self.get_penalty_session(args["lock_id"], args["extension_id"])
            elif tool_name == "search_penalty_periods":
                return await self.search_penalty_periods(
                    args["lock_id"],
                    args["extension_id"],
                    args.get("filters", {})
                )
            elif tool_name == "get_punishable_actions":
                return await self.get_punishable_actions()

            # ==================== EXTENSIONS - TEMPORARY OPENING ====================
            elif tool_name == "get_temporary_combination":
                return await self.get_temporary_combination(args["lock_id"])
            elif tool_name == "set_temporary_combination":
                return await self.set_temporary_combination(args["lock_id"], args["combination"])
            elif tool_name == "get_action_log_combination":
                return await self.get_action_log_combination(args["lock_id"], args["action_log_id"])

            # ==================== EXTENSIONS - VERIFICATION PICTURE ====================
            elif tool_name == "submit_verification_picture":
                return await self.submit_verification_picture(args["lock_id"], args["image_data"])
            elif tool_name == "get_verification_pictures":
                return await self.get_verification_pictures(args["lock_id"])

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

        except Exception as e:
            logger.error(f"❌ Error executing tool {tool_name}: {str(e)}")
            raise

    # ==================== API METHOD IMPLEMENTATIONS ====================

    # LOCKS
    async def get_locks(self, status: str = "active") -> Dict[str, Any]:
        params = {"status": status} if status != "active" else None
        data = await self.handle_request("GET", "/locks", params=params)
        return self.format_response(data, f"Found {len(data) if isinstance(data, list) else 0} locks (status: {status})")

    async def get_lock_details(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/{lock_id}")
        return self.format_response(data, f"Lock {lock_id} details")

    async def archive_lock(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/archive")
        return self.format_response(data, f"Lock {lock_id} archived successfully")

    async def archive_lock_keyholder(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/archive/keyholder")
        return self.format_response(data, f"Lock {lock_id} archived by keyholder")

    async def update_lock_time(self, lock_id: str, duration: int) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/update-time", {"duration": duration})
        return self.format_response(data, f"Lock {lock_id} duration updated to {duration} seconds")

    async def freeze_lock(self, lock_id: str, freeze: bool) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/freeze", {"isFrozen": freeze})
        action = "frozen" if freeze else "unfrozen"
        return self.format_response(data, f"Lock {lock_id} {action} successfully")

    async def unlock_lock(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/unlock")
        return self.format_response(data, f"Lock {lock_id} unlocked permanently")

    async def convert_to_self_lock(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/convert-to-self-lock")
        return self.format_response(data, f"Lock {lock_id} converted to self-lock")

    async def update_lock_settings(self, lock_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/settings", settings)
        return self.format_response(data, f"Lock {lock_id} settings updated")

    async def update_max_limit_date(self, lock_id: str, max_limit_date: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/max-limit-date", {"maxLimitDate": max_limit_date})
        return self.format_response(data, f"Lock {lock_id} max limit date updated")

    async def trust_keyholder(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/trust-keyholder")
        return self.format_response(data, f"Keyholder marked as trusted for lock {lock_id}")

    async def get_lock_combination(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/{lock_id}/combination")
        return self.format_response(data, f"Combination for lock {lock_id}")

    async def get_lock_history(self, lock_id: str, limit: int = 50, last_id: str = None, extension: str = None) -> Dict[str, Any]:
        payload = {"limit": limit}
        if last_id:
            payload["lastId"] = last_id
        if extension:
            payload["extension"] = extension
        data = await self.handle_request("POST", f"/locks/{lock_id}/history", payload)
        return self.format_response(data, f"Lock {lock_id} history")

    async def set_test_lock(self, lock_id: str, is_test_lock: bool) -> Dict[str, Any]:
        data = await self.handle_request("PUT", f"/locks/{lock_id}/is-test-lock", {"isTestLock": is_test_lock})
        return self.format_response(data, f"Lock {lock_id} test status updated")

    async def get_user_public_locks(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/user/{user_id}")
        return self.format_response(data, f"Public locks for user {user_id}")

    async def search_locks(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        if filters is None:
            filters = {}
        data = await self.handle_request("POST", "/locks/search", filters)
        return self.format_response(data, f"Search results")

    async def get_lock_extension(self, lock_id: str, extension_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/{lock_id}/extensions/{extension_id}")
        return self.format_response(data, f"Extension {extension_id} info for lock {lock_id}")

    async def trigger_lock_extension_action(self, lock_id: str, extension_id: str, action_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/extensions/{extension_id}/action", action_data)
        return self.format_response(data, f"Action triggered for extension {extension_id}")

    # LOCK CREATION
    async def create_lock(self, lock_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/locks", lock_data)
        return self.format_response(data, "Lock created successfully")

    async def edit_lock_extensions(self, lock_id: str, extensions: List) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/extensions", {"extensions": extensions})
        return self.format_response(data, f"Extensions updated for lock {lock_id}")

    async def create_lock_from_shared(self, shared_lock_id: str, lock_data: Dict = None) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/public-locks/{shared_lock_id}/create-lock", lock_data or {})
        return self.format_response(data, f"Lock created from shared lock {shared_lock_id}")

    # PROFILE
    async def get_user_profile_by_id(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/users/profile/by-id/{user_id}")
        return self.format_response(data, f"Profile for user {user_id}")

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/users/profile/{username}")
        return self.format_response(data, f"Profile for {username}")

    async def get_user_profile_details(self, username: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/users/profile/{username}/details")
        return self.format_response(data, f"Detailed profile for {username}")

    async def get_badge_count(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/users/badge/count")
        return self.format_response(data, "User badge count")

    async def update_profile_from_auth(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/auth/profile/update")
        return self.format_response(data, "Profile updated from authentication server")

    async def get_auth_profile(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/auth/profile")
        return self.format_response(data, "Logged user information")

    async def set_user_profile(self, profile_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/auth/profile", profile_data)
        return self.format_response(data, "User profile updated")

    # MESSAGING
    async def find_conversation_by_user(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/conversations/by-user/{user_id}")
        return self.format_response(data, f"Conversation with user {user_id}")

    async def create_conversation(self, user_id: str, message: str = None) -> Dict[str, Any]:
        payload = {"userId": user_id}
        if message:
            payload["message"] = message
        data = await self.handle_request("POST", "/conversations", payload)
        return self.format_response(data, "Conversation created")

    async def get_conversations(self, limit: int = None, offset: int = None) -> Dict[str, Any]:
        params = {}
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        data = await self.handle_request("GET", "/conversations", params=params)
        return self.format_response(data, "Conversations list")

    async def add_message(self, conversation_id: str, message: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/conversations/{conversation_id}", {"message": message})
        return self.format_response(data, "Message sent")

    async def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/conversations/{conversation_id}")
        return self.format_response(data, f"Conversation {conversation_id}")

    async def set_conversation_status(self, conversation_id: str, status: str) -> Dict[str, Any]:
        data = await self.handle_request("PUT", f"/conversations/{conversation_id}/status", {"status": status})
        return self.format_response(data, "Conversation status updated")

    async def set_conversation_unread(self, conversation_id: str, unread: bool) -> Dict[str, Any]:
        data = await self.handle_request("PUT", f"/conversations/{conversation_id}/unread", {"unread": unread})
        return self.format_response(data, "Conversation unread status updated")

    async def get_messages(self, conversation_id: str, limit: int = None, before: str = None) -> Dict[str, Any]:
        params = {}
        if limit:
            params["limit"] = limit
        if before:
            params["before"] = before
        data = await self.handle_request("GET", f"/conversations/{conversation_id}/messages", params=params)
        return self.format_response(data, "Messages retrieved")

    async def get_ignored_users(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/messaging/ignored-users")
        return self.format_response(data, "Ignored users list")

    # KEYHOLDER
    async def search_locked_users(self, query: str = None, limit: int = None) -> Dict[str, Any]:
        payload = {}
        if query:
            payload["query"] = query
        if limit:
            payload["limit"] = limit
        data = await self.handle_request("POST", "/keyholder/locks/search", payload)
        return self.format_response(data, "Locked users search results")

    # SHARED LOCKS
    async def get_shared_locks(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/shared-locks")
        return self.format_response(data, "Shared locks list")

    async def create_shared_lock(self, shared_lock_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/shared-locks", shared_lock_data)
        return self.format_response(data, "Shared lock created")

    async def get_shared_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/shared-locks/{shared_lock_id}")
        return self.format_response(data, f"Shared lock {shared_lock_id}")

    async def update_shared_lock(self, shared_lock_id: str, shared_lock_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("PUT", f"/shared-locks/{shared_lock_id}", shared_lock_data)
        return self.format_response(data, f"Shared lock {shared_lock_id} updated")

    async def archive_shared_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/shared-locks/{shared_lock_id}/archive")
        return self.format_response(data, f"Shared lock {shared_lock_id} archived")

    async def get_shared_lock_tags(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/shared-lock-tags")
        return self.format_response(data, "Shared lock tags")

    async def get_suggested_tags(self, description: str = None) -> Dict[str, Any]:
        payload = {}
        if description:
            payload["description"] = description
        data = await self.handle_request("POST", "/shared-lock-tags/suggested", payload)
        return self.format_response(data, "Suggested tags")

    async def check_favorite_shared_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/shared-locks/{shared_lock_id}/favorite")
        return self.format_response(data, f"Favorite status for {shared_lock_id}")

    async def add_favorite_shared_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("PUT", f"/shared-locks/{shared_lock_id}/favorite")
        return self.format_response(data, f"Added {shared_lock_id} to favorites")

    async def remove_favorite_shared_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("DELETE", f"/shared-locks/{shared_lock_id}/favorite")
        return self.format_response(data, f"Removed {shared_lock_id} from favorites")

    async def get_favorite_shared_locks(self) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/favorites/shared-locks")
        return self.format_response(data, "Favorite shared locks")

    # PUBLIC LOCKS
    async def get_public_lock(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/public-locks/{shared_lock_id}")
        return self.format_response(data, f"Public lock {shared_lock_id}")

    async def get_lock_image(self, shared_lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/public-locks/images/{shared_lock_id}")
        return self.format_response(data, f"Image for lock {shared_lock_id}")

    async def search_public_locks(self, query: str = None, tags: List = None, limit: int = None) -> Dict[str, Any]:
        payload = {}
        if query:
            payload["query"] = query
        if tags:
            payload["tags"] = tags
        if limit:
            payload["limit"] = limit
        data = await self.handle_request("POST", "/public-locks/search", payload)
        return self.format_response(data, "Public locks search results")

    async def get_explore_categories(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/explore/categories")
        return self.format_response(data, "Explore categories")

    # SESSION OFFER
    async def create_keyholding_offer(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/session-offer/lock/{lock_id}")
        return self.format_response(data, f"Keyholding offer created for lock {lock_id}")

    async def accept_keyholding_request(self, offer_token: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/session-offer/token/{offer_token}/accept")
        return self.format_response(data, "Keyholding request accepted")

    async def get_keyholding_offer_status(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/session-offer/lock/{lock_id}/status")
        return self.format_response(data, f"Keyholding offers status for lock {lock_id}")

    async def get_offer_public_info(self, offer_token: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/session-offer/token/{offer_token}")
        return self.format_response(data, "Offer public information")

    async def respond_to_keyholding_offer(self, session_request_id: str, accept: bool) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/session-offer/{session_request_id}", {"accept": accept})
        return self.format_response(data, f"Keyholding offer {'accepted' if accept else 'rejected'}")

    async def archive_keyholding_offer(self, session_request_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/session-offer/{session_request_id}/archive")
        return self.format_response(data, "Keyholding offer archived")

    async def get_keyholding_requests(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/session-offer/requests")
        return self.format_response(data, "Keyholding requests")

    # BLOCKS
    async def get_blocked_users(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/blocks")
        return self.format_response(data, "Blocked users list")

    async def block_user(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/blocks", {"userId": user_id})
        return self.format_response(data, f"User {user_id} blocked")

    async def get_block_interaction(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/blocks/block-interaction/{user_id}")
        return self.format_response(data, f"Block interaction with user {user_id}")

    async def unblock_user(self, user_id: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/blocks/unblock", {"userId": user_id})
        return self.format_response(data, f"User {user_id} unblocked")

    # EXTENSIONS
    async def get_extensions(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/extensions")
        return self.format_response(data, "Available extensions")

    # COMBINATIONS
    async def upload_combination_image(self, image_data: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/combinations/image", {"image": image_data})
        return self.format_response(data, "Combination image uploaded")

    async def create_code_combination(self, code: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/combinations/code", {"code": code})
        return self.format_response(data, "Code combination created")

    # FILES
    async def upload_files(self, files: List) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/files/upload", {"files": files})
        return self.format_response(data, "Files uploaded")

    async def get_file(self, file_key: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/files/{file_key}")
        return self.format_response(data, f"File {file_key}")

    # USERS
    async def search_users(self, query: str = None, limit: int = None) -> Dict[str, Any]:
        payload = {}
        if query:
            payload["query"] = query
        if limit:
            payload["limit"] = limit
        data = await self.handle_request("POST", "/users/search", payload)
        return self.format_response(data, "Users search results")

    async def search_user_by_username(self, username: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/users/search/by-username", {"username": username})
        return self.format_response(data, f"Search results for username {username}")

    async def search_user_by_discord(self, discord_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/users/search/by-discord-id/{discord_id}")
        return self.format_response(data, f"User with Discord ID {discord_id}")

    async def update_current_user(self, user_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("PATCH", "/current-user", user_data)
        return self.format_response(data, "Current user updated")

    # COMMUNITY EVENTS
    async def get_event_categories(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/community-event/categories")
        return self.format_response(data, "Community event categories")

    async def get_event_task_details(self, category_id: str = None, day: str = None) -> Dict[str, Any]:
        payload = {}
        if category_id:
            payload["categoryId"] = category_id
        if day:
            payload["day"] = day
        data = await self.handle_request("POST", "/community-event/details", payload)
        return self.format_response(data, "Event task details")

    # SETTINGS
    async def get_app_settings(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/settings")
        return self.format_response(data, "Application settings")

    # REPORTS
    async def create_report(self, report_data: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", "/reports", report_data)
        return self.format_response(data, "Report created")

    # EXTENSIONS - PENALTIES
    async def get_penalties(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/extensions/penalty/penalties")
        return self.format_response(data, "Available penalties")

    async def get_penalty_session(self, lock_id: str, extension_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/{lock_id}/extensions/{extension_id}/penalty-session")
        return self.format_response(data, "Penalty session")

    async def search_penalty_periods(self, lock_id: str, extension_id: str, filters: Dict) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/locks/{lock_id}/extensions/{extension_id}/penalty-session/penalty-periods/search", filters)
        return self.format_response(data, "Penalty periods")

    async def get_punishable_actions(self) -> Dict[str, Any]:
        data = await self.handle_request("GET", "/extensions/penalty/punishable-actions")
        return self.format_response(data, "Punishable actions")

    # EXTENSIONS - TEMPORARY OPENING
    async def get_temporary_combination(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/extensions/temporary-opening/{lock_id}/combination")
        return self.format_response(data, f"Temporary combination for lock {lock_id}")

    async def set_temporary_combination(self, lock_id: str, combination: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/extensions/temporary-opening/{lock_id}/combination", {"combination": combination})
        return self.format_response(data, "Temporary combination set")

    async def get_action_log_combination(self, lock_id: str, action_log_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/extensions/temporary-opening/{lock_id}/action-log/{action_log_id}/combination")
        return self.format_response(data, "Action log combination")

    # EXTENSIONS - VERIFICATION PICTURE
    async def submit_verification_picture(self, lock_id: str, image_data: str) -> Dict[str, Any]:
        data = await self.handle_request("POST", f"/extensions/verification-picture/{lock_id}/submit", {"image": image_data})
        return self.format_response(data, "Verification picture submitted")

    async def get_verification_pictures(self, lock_id: str) -> Dict[str, Any]:
        data = await self.handle_request("GET", f"/locks/{lock_id}/verification-pictures")
        return self.format_response(data, f"Verification pictures for lock {lock_id}")
