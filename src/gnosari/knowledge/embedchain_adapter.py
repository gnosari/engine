"""
Embedchain adapter for integrating Embedchain knowledge bases with Gnosari.
"""

import logging
from typing import Any, Dict, List, Optional

from .base import BaseKnowledgeBase, KnowledgeResult, KnowledgeProvider
from ..core.exceptions import KnowledgeError


class EmbedchainKnowledgeBase(BaseKnowledgeBase):
    """
    Embedchain implementation of the knowledge base interface.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Embedchain knowledge base.
        
        Args:
            name: Knowledge base name
            config: Optional Embedchain configuration
        """
        super().__init__(name, config)
        self.embedchain_app = None
        self.logger = logging.getLogger(__name__)
    
    async def initialize(self) -> None:
        """Initialize the Embedchain application."""
        if self._initialized:
            return
        
        try:
            from embedchain import App
            
            # Create Embedchain app with configuration (only if config is provided)
            embedchain_config = self.config.get('embedchain')
            if embedchain_config:
                self.embedchain_app = App.from_config(config=embedchain_config)
            else:
                self.embedchain_app = App()
            
            self._initialized = True
            self.logger.info(f"Initialized Embedchain knowledge base '{self.name}'")
            
        except ImportError:
            raise KnowledgeError("Embedchain not installed. Install with: pip install embedchain")
        except Exception as e:
            raise KnowledgeError(f"Failed to initialize Embedchain knowledge base '{self.name}': {e}")
    
    async def add_data(self, data: str, source: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add data to the Embedchain knowledge base.
        
        Args:
            data: Data content or URL to add
            source: Source identifier
            metadata: Optional metadata
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Check if knowledge base already has data (optimization from old implementation)
            try:
                if hasattr(self.embedchain_app, 'db') and hasattr(self.embedchain_app.db, 'count') and self.embedchain_app.db.count() > 0:
                    self.logger.info(f"Knowledge base '{self.name}' already has data. Skipping addition of: {data}")
                    return
            except Exception as check_error:
                # If check fails, proceed with adding (fallback)
                self.logger.debug(f"Could not check existing data: {check_error}")
            
            self.logger.info(f'Adding data to knowledge base {self.name}: {data}')
            
            # Check if this is a directory type and needs special loader
            kb_type = self.config.get('type', '').lower()
            if kb_type == 'directory':
                # Import directory loader
                from embedchain.loaders.directory_loader import DirectoryLoader
                
                # Get directory-specific configuration
                loader_config = self.config.get('loader_config', {})
                # Set defaults for directory loading
                if 'recursive' not in loader_config:
                    loader_config['recursive'] = True
                if 'extensions' not in loader_config:
                    loader_config['extensions'] = ['.txt', '.md', '.py', '.yaml', '.yml', '.json']
                
                loader = DirectoryLoader(config=loader_config)
                self.embedchain_app.add(data, loader=loader)
            else:
                # Use the old approach: just call add() without data_type
                # Let Embedchain auto-detect the data type
                self.embedchain_app.add(data)
            
            self.logger.debug(f"Added data to Embedchain knowledge base '{self.name}': {source}")
            
        except Exception as e:
            raise KnowledgeError(f"Failed to add data to knowledge base '{self.name}': {e}")
    
    async def query(self, query: str, max_results: int = 5) -> List[KnowledgeResult]:
        """
        Query the Embedchain knowledge base.
        
        Args:
            query: Query string
            max_results: Maximum number of results
            
        Returns:
            List of knowledge results
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            # Query Embedchain
            response = self.embedchain_app.search(query)

            self.logger.debug(f"Embedchain search response type: {type(response)}")
            self.logger.debug(f"Embedchain knowledge base '{self.name}' response: {response}")
            
            # Handle different response formats from Embedchain
            results = []
            
            if isinstance(response, str):
                # Single string response
                results = [
                    KnowledgeResult(
                        content=response,
                        source=self.name,
                        score=1.0,
                        metadata={'query': query}
                    )
                ]
            elif isinstance(response, list):
                # List of results
                for i, item in enumerate(response):
                    if isinstance(item, str):
                        # List of strings
                        results.append(
                            KnowledgeResult(
                                content=item,
                                source=f"{self.name}#{i}",
                                score=1.0,
                                metadata={'query': query, 'index': i}
                            )
                        )
                    elif isinstance(item, dict):
                        # List of dictionaries (more structured results)
                        content = item.get('content', str(item))
                        source = item.get('source', f"{self.name}#{i}")
                        score = item.get('score', 1.0)
                        metadata = item.get('metadata', {})
                        metadata.update({'query': query, 'index': i})
                        
                        results.append(
                            KnowledgeResult(
                                content=content,
                                source=source,
                                score=score,
                                metadata=metadata
                            )
                        )
                    else:
                        # Convert other types to string
                        results.append(
                            KnowledgeResult(
                                content=str(item),
                                source=f"{self.name}#{i}",
                                score=1.0,
                                metadata={'query': query, 'index': i}
                            )
                        )
            else:
                # Convert other types to string
                results = [
                    KnowledgeResult(
                        content=str(response),
                        source=self.name,
                        score=1.0,
                        metadata={'query': query}
                    )
                ]

            return results[:max_results]
            
        except Exception as e:
            raise KnowledgeError(f"Failed to query knowledge base '{self.name}': {e}")
    
    async def delete_data(self, source: str) -> bool:
        """
        Delete data from the Embedchain knowledge base.
        
        Args:
            source: Source identifier
            
        Returns:
            True if data was deleted
        """
        # Embedchain doesn't have a direct delete method in the basic interface
        # This would need to be implemented based on the specific Embedchain version
        self.logger.warning(f"Delete operation not implemented for Embedchain knowledge base '{self.name}'")
        return False
    
    async def cleanup(self) -> None:
        """Clean up Embedchain resources."""
        if self.embedchain_app:
            # Embedchain cleanup if available
            self.embedchain_app = None
        self._initialized = False


class EmbedchainProvider(KnowledgeProvider):
    """
    Provider for creating Embedchain knowledge bases.
    """
    
    def create_knowledge_base(
        self, 
        name: str, 
        kb_type: str, 
        config: Optional[Dict[str, Any]] = None
    ) -> BaseKnowledgeBase:
        """
        Create an Embedchain knowledge base.
        
        Args:
            name: Knowledge base name
            kb_type: Type (should be supported by Embedchain)
            config: Optional configuration
            
        Returns:
            EmbedchainKnowledgeBase instance
        """
        # Create the full config including the type
        full_config = config or {}
        full_config['type'] = kb_type
        
        return EmbedchainKnowledgeBase(name, full_config)
    
    def get_supported_types(self) -> List[str]:
        """
        Get supported knowledge base types.
        
        Returns:
            List of supported types
        """
        return [
            'website',
            'documents', 
            'text',
            'pdf',
            'web_page',
            'youtube_video',
            'github_repo',
            'sitemap',
            'directory'
        ]