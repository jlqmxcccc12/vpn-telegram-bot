from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from models import Server
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class ServerRepository:
    """Repository for WireGuard server operations."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, server_id: int) -> Server | None:
        """Get server by ID."""
        return await self.session.get(Server, server_id)
    
    async def get_by_host(self, host: str) -> Server | None:
        """Get server by hostname."""
        result = await self.session.execute(
            select(Server).where(Server.host == host)
        )
        return result.scalars().first()
    
    async def get_active_servers(self) -> list[Server]:
        """Get all active servers."""
        result = await self.session.execute(
            select(Server).where(Server.is_active == True)
        )
        return result.scalars().all()
    
    async def get_server_with_lowest_load(self) -> Server | None:
        """Get active server with lowest client count."""
        # This is simplified - in production, you'd want more sophisticated load balancing
        active_servers = await self.get_active_servers()
        if not active_servers:
            return None
        
        # Find server with fewest clients
        min_server = active_servers[0]
        for server in active_servers:
            current_clients = len(server.vpn_clients)
            min_clients = len(min_server.vpn_clients)
            if current_clients < min_clients and current_clients < server.max_clients:
                min_server = server
        
        return min_server if len(min_server.vpn_clients) < min_server.max_clients else None
    
    async def create(
        self,
        host: str,
        public_key: str,
        endpoint: str,
        endpoint_port: int = 51820,
        max_clients: int = 100
    ) -> Server:
        """Create new server."""
        server = Server(
            host=host,
            public_key=public_key,
            endpoint=endpoint,
            endpoint_port=endpoint_port,
            max_clients=max_clients,
            is_active=True
        )
        self.session.add(server)
        await self.session.flush()
        logger.info(f"Created server {server.id} on {host}")
        return server
