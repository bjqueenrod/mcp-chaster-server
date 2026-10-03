
import os
import json
import logging
from typing import Dict, Any, List, Optional, Union
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

from chaster_service import ChasterLocksService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for JSON-RPC validation
class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    method: str
    params: Optional[Union[Dict[str, Any], List[Any]]] = None
    id: Optional[Union[int, str]] = None

class JsonRpcResponse(BaseModel):
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[Union[int, str]] = None

class JsonRpcError(BaseModel):
    code: int
    message: str
    data: Optional[Any] = None

# FastAPI configuration with Swagger documentation
app = FastAPI(
    title="🔐 Chaster Locks MCP Server",
    description="""
    ## Model Context Protocol Server for Chaster Locks API

    This server implements the MCP (Model Context Protocol) to interact with the Chaster Locks API.

    ### Authentication
    - **Type**: Bearer Token (optional prefix)
    - **Header**: `Authorization: Bearer YOUR_MCP_TOKEN` or `Authorization: YOUR_MCP_TOKEN`
    - **Scope**: All `/mcp` routes require authentication

    ### Available Endpoints
    - **`/health`**: Server health check (no authentication required)
    - **`/mcp`**: Main MCP endpoint (authentication required)
    - **`/docs`**: This Swagger documentation
    - **`/redoc`**: Alternative ReDoc documentation

    ### MCP Protocol
    The server follows the JSON-RPC 2.0 standard with MCP methods:
    - `initialize` - Initialize MCP connection
    - `tools/list` - List available tools
    - `tools/call` - Execute a specific tool

    ### Available Chaster Tools
    86 complete tools covering the entire Chaster Public API:
    - **Locks** (18 tools): Management, control, history, extensions
    - **Lock Creation** (3 tools): Create, edit, from shared locks
    - **Profile** (7 tools): User profiles, badges, authentication
    - **Messaging** (9 tools): Conversations, messages, status
    - **Keyholder** (1 tool): Search locked users
    - **Shared Locks** (11 tools): Create, manage, favorites
    - **Public Locks** (4 tools): Browse, search, explore
    - **Session Offer** (7 tools): Keyholding offers management
    - **Blocks** (4 tools): Block/unblock users
    - **Extensions** (1 tool): Available extensions list
    - **Combinations** (2 tools): Image and code combinations
    - **Extensions - Penalties** (4 tools): Penalties management
    - **Extensions - Temporary Opening** (3 tools): Temporary combinations
    - **Extensions - Verification Picture** (2 tools): Verification pictures
    - **Files** (2 tools): Upload and retrieve files
    - **Users** (4 tools): Search and manage users
    - **Community Events** (2 tools): Events and tasks
    - **Settings** (1 tool): Application settings
    - **Reports** (1 tool): Create reports
    """,
    version="2.0.0",
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
            "description": "Production server"
        },
        {
            "url": "http://localhost:3000",
            "description": "Local development server"
        }
    ],
    docs_url="/docs",  # Enable Swagger UI
    redoc_url="/redoc",  # Enable ReDoc
    openapi_url="/openapi.json"  # OpenAPI specification URL
)

# Tags to organize endpoints in Swagger
tags_metadata = [
    {
        "name": "health",
        "description": "Server monitoring and health check endpoints"
    },
    {
        "name": "mcp",
        "description": "Model Context Protocol - Main endpoints (authentication required)"
    }
]

app.openapi_tags = tags_metadata

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication configuration
MCP_AUTH_TOKEN = os.getenv("MCP_AUTH_TOKEN")

if not MCP_AUTH_TOKEN:
    logger.error("MCP_AUTH_TOKEN not defined in environment variables")
    raise ValueError("MCP_AUTH_TOKEN is required")

# Debug: Log the expected token (first/last 4 chars only for security)
logger.info(f"🔑 Expected token: {MCP_AUTH_TOKEN[:4]}...{MCP_AUTH_TOKEN[-4:]}")

# Chaster service
chaster_service = ChasterLocksService()

def create_jsonrpc_response(result: Any = None, request_id: Optional[Union[int, str]] = None) -> JSONResponse:
    """Create a valid JSON-RPC response (success: `result` only, never `error`)"""
    return JSONResponse({"jsonrpc": "2.0", "id": request_id, "result": result if result is not None else {}})

def create_jsonrpc_error(code: int, message: str, request_id: Optional[Union[int, str]] = None, data: Any = None) -> JSONResponse:
    """Create a JSON-RPC error (error: `error` only, never `result`)"""
    error = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return JSONResponse({"jsonrpc": "2.0", "id": request_id, "error": error})

async def verify_token(request: Request):
    """Verify MCP authentication token (supports both 'Bearer TOKEN' and 'TOKEN' formats)"""
    # Get Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        logger.warning("❌ Missing Authorization header")
        raise HTTPException(
            status_code=401,
            detail="Missing authentication token"
        )

    # Extract token (handle both "Bearer TOKEN" and "TOKEN" formats)
    received_token = auth_header.strip()
    if received_token.lower().startswith("bearer "):
        received_token = received_token[7:].strip()  # Remove "Bearer " prefix

    # Debug: Log received token (first/last 4 chars only for security)
    if len(received_token) >= 8:
        logger.info(f"🔍 Received token: {received_token[:4]}...{received_token[-4:]}")
    else:
        logger.info(f"🔍 Received token: [too short]")

    logger.info(f"🔍 Tokens match: {received_token == MCP_AUTH_TOKEN}")

    if received_token != MCP_AUTH_TOKEN:
        logger.warning("❌ Invalid authentication token")
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )

    logger.info("✅ Authentication successful")
    return received_token

# Routes

@app.get(
    "/health",
    tags=["health"],
    summary="Server health check",
    description="Monitoring endpoint that returns server status, accessible without authentication",
    response_description="Server status and version information"
)
@app.head("/health", tags=["health"], include_in_schema=False)
async def health_check():
    """Health check endpoint (GET and HEAD supported)"""
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
    summary="Main MCP endpoint",
    description="""
    Main endpoint for Model Context Protocol requests.

    **Authentication required**: Bearer token in Authorization header

    **Supported MCP methods**:
    - `initialize` - Initialize MCP connection
    - `tools/list` - List of the 13 available Chaster tools
    - `tools/call` - Execute a tool with its parameters

    **Format**: JSON-RPC 2.0
    """,
    response_description="JSON-RPC 2.0 response based on the method called",
    responses={
        200: {
            "description": "MCP request processed successfully",
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
            "description": "Invalid or missing authentication token"
        },
        400: {
            "description": "Malformed JSON-RPC request"
        }
    }
)
async def handle_mcp(
    rpc_request: JsonRpcRequest,
    request: Request,
    token: str = Depends(verify_token)
):
    """Main MCP endpoint with authentication"""

    logger.info(f"📡 MCP request: {rpc_request.method}")

    # Notifications get no JSON-RPC response body (HTTP 202 per MCP streamable-HTTP)
    if rpc_request.method.startswith("notifications/"):
        return Response(status_code=202)

    params = rpc_request.params if isinstance(rpc_request.params, dict) else {}

    try:
        if rpc_request.method == "initialize":
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
                    "version": "2.0.0",
                    "description": "Complete MCP Server for Chaster Public API - All 86 user endpoints (Python)"
                }
            }
            return create_jsonrpc_response(result, rpc_request.id)

        elif rpc_request.method == "tools/list":
            tools = await chaster_service.get_available_tools()
            result = {"tools": tools}
            return create_jsonrpc_response(result, rpc_request.id)

        elif rpc_request.method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            if not tool_name:
                return create_jsonrpc_error(
                    -32602,
                    "Invalid parameters: tool name missing",
                    rpc_request.id
                )

            result = await chaster_service.call_tool(tool_name, tool_args)
            return create_jsonrpc_response(result, rpc_request.id)

        elif rpc_request.method == "ping":
            return create_jsonrpc_response({}, rpc_request.id)

        elif rpc_request.method == "resources/list":
            return create_jsonrpc_response({"resources": []}, rpc_request.id)

        elif rpc_request.method == "prompts/list":
            return create_jsonrpc_response({"prompts": []}, rpc_request.id)

        else:
            return create_jsonrpc_error(-32601, "Method not found", rpc_request.id)

    except Exception as e:
        logger.error(f"❌ MCP error: {str(e)}")
        return create_jsonrpc_error(-32000, str(e), rpc_request.id)

# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler - returns JSONResponse"""
    error_response = create_jsonrpc_error(
        -32601,
        "Endpoint not found. Use POST /mcp for MCP operations or GET /health for status",
        None
    )
    return JSONResponse(
        status_code=404,
        content=error_response.dict()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global error handler - returns JSONResponse"""
    logger.error(f"❌ Server error: {str(exc)}")
    error_response = create_jsonrpc_error(-32000, "Internal server error", None)
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))

    logger.info(f"🚀 Starting Chaster Locks MCP server on port {port}")
    logger.info(f"📊 Health: http://localhost:{port}/health")
    logger.info(f"🔗 MCP endpoint: http://localhost:{port}/mcp")
    logger.info(f"📚 Swagger documentation: http://localhost:{port}/docs")
    logger.info(f"📖 ReDoc documentation: http://localhost:{port}/redoc")
    logger.info(f"🔐 Authentication: Bearer token required")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Production mode only
        log_level="info"
    )
