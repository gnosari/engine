"""Knowledge base loading functionality."""

import logging
from typing import List, Dict, Any, Optional

from ...knowledge import KnowledgeManager
from .knowledge_registry import KnowledgeRegistry


class KnowledgeLoader:
    """Handles loading and initialization of knowledge bases."""
    
    def __init__(self, knowledge_registry: KnowledgeRegistry = None):
        self.knowledge_registry = knowledge_registry or KnowledgeRegistry()
        self.knowledge_manager: Optional[KnowledgeManager] = None
        self.logger = logging.getLogger(__name__)
    
    def ensure_knowledge_manager(self):
        """Ensure knowledge manager is initialized."""
        if self.knowledge_manager is None:
            try:
                self.knowledge_manager = KnowledgeManager()
            except ImportError as e:
                self.logger.warning(f"Knowledge manager not available: {e}")
    
    async def load_knowledge_bases(self, knowledge_config: List[Dict[str, Any]]) -> None:
        """
        Load knowledge bases from configuration.
        
        Args:
            knowledge_config: List of knowledge base configurations from YAML
        """
        self.ensure_knowledge_manager()
        if self.knowledge_manager is None:
            self.logger.warning("Knowledge manager not available, skipping knowledge base loading")
            return
        
        for kb_config in knowledge_config:
            await self._load_single_knowledge_base(kb_config)
    
    async def _load_single_knowledge_base(self, kb_config: Dict[str, Any]) -> None:
        """Load a single knowledge base from configuration."""
        name = kb_config.get('name')
        kb_type = kb_config.get('type')
        kb_id = kb_config.get('id')
        
        if not kb_type:
            self.logger.warning(f"Invalid knowledge base configuration - missing type: {kb_config}")
            return
        
        # Use ID as the primary key, fallback to name if no ID is provided
        kb_key = kb_id if kb_id else name
        if not kb_key:
            self.logger.warning(f"Invalid knowledge base configuration - missing both id and name: {kb_config}")
            return
        
        # Store knowledge description if provided
        description = kb_config.get('description')
        if description:
            self.knowledge_registry.register_description(kb_key, description)
            self.logger.info(f"Stored description for knowledge base '{kb_key}': {description}")
        
        try:
            # Create knowledge base using ID as the key
            embedchain_config = kb_config.get('config')
            self.knowledge_manager.create_knowledge_base(kb_key, kb_type, config=embedchain_config)
            
            # Add data if specified
            data = kb_config.get('data')
            if data:
                await self._add_data_to_knowledge_base(kb_key, data)
            
            self.logger.info(f"Loaded knowledge base '{kb_key}' of type '{kb_type}'")
            
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base '{name}': {e}")
    
    async def _add_data_to_knowledge_base(self, kb_key: str, data: Any) -> None:
        """Add data to a knowledge base."""
        # Always treat data as a list for consistency
        if isinstance(data, list):
            data_list = data
        else:
            data_list = [data]
        
        # Add each data item to the knowledge base
        for item in data_list:
            await self.knowledge_manager.add_data_to_knowledge_base(kb_key, item)
    
    def add_knowledge_tools(self, agent_tools: List[str], knowledge_names: List[str]) -> List[str]:
        """
        Add knowledge query tools for specified knowledge bases to the agent's tool list.
        
        Args:
            agent_tools: Current list of agent tools
            knowledge_names: List of knowledge base names to add tools for
            
        Returns:
            Updated list of agent tools including knowledge query tools
        """
        if self.knowledge_manager is None:
            self.logger.warning("Knowledge manager not available, skipping knowledge tools")
            return agent_tools
        
        # Check if knowledge_query tool is already in the list
        if 'knowledge_query' not in agent_tools:
            agent_tools.append('knowledge_query')
            self.logger.info("Added knowledge_query tool to agent")
        
        return agent_tools