# sully_engine/memory.py
# 🧠 Sully's Expansive Memory System with Associative Retrieval

from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple
import json
import os

class SullySearchMemory:
    """
    A sophisticated memory system for Sully that stores experiences, 
    queries, and knowledge with associative retrieval capabilities.
    """
    
    def __init__(self, memory_file: Optional[str] = None):
        """
        Initialize the memory system with optional persistent storage.
        
        Args:
            memory_file: Optional file path for persisting memory
        """
        self.storage = []
        self.associations = {}  # Maps concepts to relevant memory indices
        self.temporal_index = {}  # Organizes memories by time periods
        self.memory_file = memory_file
        
        # Load from file if provided and exists
        if memory_file and os.path.exists(memory_file):
            try:
                self._load_from_file()
            except Exception as e:
                print(f"Could not load memory file: {e}")

    def store_query(self, query: str, result: Any, metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Stores a symbolic query and its result in memory, with a timestamp.
        
        Args:
            query: The input query or stimulus
            result: The response or output
            metadata: Additional contextual information
            
        Returns:
            Index of the stored memory
        """
        timestamp = datetime.now()
        
        # Create memory entry
        entry = {
            "query": query,
            "result": result,
            "timestamp": timestamp.isoformat(),
            "type": "query",
        }
        
        # Add any additional metadata
        if metadata:
            entry["metadata"] = metadata
            
        # Store in main memory
        memory_index = len(self.storage)
        self.storage.append(entry)
        
        # Index by time period for temporal associations
        time_key = timestamp.strftime("%Y-%m-%d")
        if time_key not in self.temporal_index:
            self.temporal_index[time_key] = []
        self.temporal_index[time_key].append(memory_index)
        
        # Extract and index key concepts to build associations
        self._index_concepts(memory_index, query, result)
        
        # Save to persistent storage if configured
        if self.memory_file:
            self._save_to_file()
            
        return memory_index

    def store_experience(self, content: str, source: str, 
                        concepts: Optional[List[str]] = None,
                        importance: float = 0.5) -> int:
        """
        Stores a general experience or knowledge in memory.
        
        Args:
            content: The main content to remember
            source: Where the experience/knowledge came from
            concepts: Key concepts related to this memory
            importance: How important this memory is (0.0-1.0)
            
        Returns:
            Index of the stored memory
        """
        timestamp = datetime.now()
        
        # Create memory entry
        entry = {
            "content": content,
            "source": source,
            "timestamp": timestamp.isoformat(),
            "importance": importance,
            "type": "experience",
        }
        
        if concepts:
            entry["concepts"] = concepts
            
        # Store in main memory
        memory_index = len(self.storage)
        self.storage.append(entry)
        
        # Index by time period
        time_key = timestamp.strftime("%Y-%m-%d")
        if time_key not in self.temporal_index:
            self.temporal_index[time_key] = []
        self.temporal_index[time_key].append(memory_index)
        
        # Index by concepts
        if concepts:
            for concept in concepts:
                self._add_association(concept, memory_index)
        else:
            # Auto-extract concepts if none provided
            extracted_concepts = self._extract_key_concepts(content)
            for concept in extracted_concepts:
                self._add_association(concept, memory_index)
        
        # Save to persistent storage if configured
        if self.memory_file:
            self._save_to_file()
            
        return memory_index

    def _extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract potential key concepts from text.
        
        A more sophisticated implementation would use NLP.
        This simple version extracts capitalized terms and longer phrases.
        
        Args:
            text: Text to extract concepts from
            
        Returns:
            List of extracted concepts
        """
        import re
        
        # Extract capitalized terms (potential proper nouns/concepts)
        capitalized = re.findall(r'\b[A-Z][a-z]{3,}\b', text)
        
        # Extract potentially meaningful longer phrases
        phrases = re.findall(r'\b[a-z]{3,} [a-z]{3,}(?: [a-z]{3,})?\b', text.lower())
        
        # Combine and limit to reasonable number
        all_concepts = set(capitalized + phrases)
        return list(all_concepts)[:10]  # Limit to top 10

    def _add_association(self, concept: str, memory_index: int) -> None:
        """
        Add an association between a concept and a memory.
        
        Args:
            concept: The concept to associate
            memory_index: Index of the memory to associate with
        """
        concept_lower = concept.lower()
        if concept_lower not in self.associations:
            self.associations[concept_lower] = []
        
        if memory_index not in self.associations[concept_lower]:
            self.associations[concept_lower].append(memory_index)

    def _index_concepts(self, memory_index: int, query: str, result: Any) -> None:
        """
        Extract and index concepts from a query-result pair.
        
        Args:
            memory_index: Index of the memory to associate concepts with
            query: The query text
            result: The result data
        """
        # Extract concepts from query
        query_concepts = self._extract_key_concepts(query)
        
        # Extract concepts from result if it's a string
        result_concepts = []
        if isinstance(result, str):
            result_concepts = self._extract_key_concepts(result)
        elif isinstance(result, dict) and "response" in result:
            if isinstance(result["response"], str):
                result_concepts = self._extract_key_concepts(result["response"])
        
        # Combine unique concepts
        all_concepts = set(query_concepts + result_concepts)
        
        # Index all concepts
        for concept in all_concepts:
            self._add_association(concept, memory_index)

    def search(self, keyword: str, case_sensitive: bool = False, 
              limit: Optional[int] = None, include_associations: bool = True) -> Dict[int, Dict[str, Any]]:
        """
        Searches memory for entries containing the given keyword.

        Args:
            keyword: Term to search within memory
            case_sensitive: Whether to respect case during match
            limit: Max number of results to return
            include_associations: Whether to include associated memories
            
        Returns:
            Dictionary of indexed matches from memory
        """
        direct_matches = {}
        
        # Direct search in storage
        for i, entry in enumerate(self.storage):
            entry_matched = False
            
            # Check query field if it exists
            if "query" in entry:
                haystack = entry["query"] if case_sensitive else entry["query"].lower()
                needle = keyword if case_sensitive else keyword.lower()
                if needle in haystack:
                    direct_matches[i] = entry
                    entry_matched = True
            
            # Check result field if it exists and is a string
            if not entry_matched and "result" in entry:
                if isinstance(entry["result"], str):
                    haystack = entry["result"] if case_sensitive else entry["result"].lower()
                    needle = keyword if case_sensitive else keyword.lower()
                    if needle in haystack:
                        direct_matches[i] = entry
                        entry_matched = True
            
            # Check content field if it exists (for experience type memories)
            if not entry_matched and "content" in entry:
                haystack = entry["content"] if case_sensitive else entry["content"].lower()
                needle = keyword if case_sensitive else keyword.lower()
                if needle in haystack:
                    direct_matches[i] = entry
                    entry_matched = True
                    
            # Stop if we've reached the limit
            if limit and len(direct_matches) >= limit:
                break
        
        # If we don't need to include associations or have reached the limit, return
        if not include_associations or (limit and len(direct_matches) >= limit):
            return direct_matches
        
        # Search for associated memories
        matches = dict(direct_matches)  # Copy direct matches
        
        # Normalize keyword for association lookup
        needle = keyword.lower()
        
        # Look for exact concept matches in associations
        if needle in self.associations:
            # Add all associated memories, respecting the limit
            for memory_index in self.associations[needle]:
                if memory_index not in matches:
                    matches[memory_index] = self.storage[memory_index]
                    if limit and len(matches) >= limit:
                        break
        
        # Look for partial concept matches in associations
        if len(matches) < (limit or float('inf')):
            for concept, indices in self.associations.items():
                if needle in concept and concept != needle:
                    # Add associated memories, respecting the limit
                    for memory_index in indices:
                        if memory_index not in matches:
                            matches[memory_index] = self.storage[memory_index]
                            if limit and len(matches) >= limit:
                                break
                    if limit and len(matches) >= limit:
                        break
        
        return matches

    def get_temporal_context(self, timestamp_or_date: Union[str, datetime],
                           window_days: int = 1, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get memories from around a specific time, providing temporal context.
        
        Args:
            timestamp_or_date: Timestamp or date string to get context for
            window_days: Number of days before and after to include
            limit: Maximum number of memories to return
            
        Returns:
            List of memories within the temporal window
        """
        from datetime import datetime, timedelta
        
        # Parse timestamp if it's a string
        if isinstance(timestamp_or_date, str):
            try:
                target_date = datetime.fromisoformat(timestamp_or_date).date()
            except ValueError:
                # Try just the date portion if full ISO format fails
                try:
                    target_date = datetime.strptime(timestamp_or_date, "%Y-%m-%d").date()
                except ValueError:
                    return []  # Return empty list if unparseable
        else:
            target_date = timestamp_or_date.date()
        
        # Calculate window
        start_date = target_date - timedelta(days=window_days)
        end_date = target_date + timedelta(days=window_days)
        
        # Get all memory indices within window
        window_memories = []
        current_date = start_date
        while current_date <= end_date:
            date_key = current_date.strftime("%Y-%m-%d")
            if date_key in self.temporal_index:
                window_memories.extend(self.temporal_index[date_key])
            current_date += timedelta(days=1)
        
        # Return memories, with optional limit
        if limit:
            window_memories = window_memories[:limit]
        
        return [self.storage[idx] for idx in window_memories]

    def get_associated_memories(self, concept: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get memories associated with a particular concept.
        
        Args:
            concept: The concept to find associations for
            limit: Maximum number of memories to return
            
        Returns:
            List of memories associated with the concept
        """
        concept_lower = concept.lower()
        if concept_lower not in self.associations:
            return []
        
        indices = self.associations[concept_lower]
        if limit:
            indices = indices[:limit]
        
        return [self.storage[idx] for idx in indices]

    def find_connections(self, concept1: str, concept2: str) -> List[Dict[str, Any]]:
        """
        Find memories that connect two concepts.
        
        Args:
            concept1: First concept
            concept2: Second concept
            
        Returns:
            List of memories that reference both concepts
        """
        concept1_lower = concept1.lower()
        concept2_lower = concept2.lower()
        
        # Check if concepts exist in associations
        if concept1_lower not in self.associations or concept2_lower not in self.associations:
            return []
        
        # Find intersection of memory indices
        indices1 = set(self.associations[concept1_lower])
        indices2 = set(self.associations[concept2_lower])
        common_indices = indices1.intersection(indices2)
        
        # Return connected memories
        return [self.storage[idx] for idx in common_indices]

    def export_memory(self) -> List[Dict[str, Any]]:
        """
        Returns the entire memory as a list of entries (for JSON export).
        
        Returns:
            List of all memory entries
        """
        return self.storage

    def export_full_system(self) -> Dict[str, Any]:
        """
        Exports the complete memory system including associations and indices.
        
        Returns:
            Dictionary containing all memory system components
        """
        return {
            "storage": self.storage,
            "associations": self.associations,
            "temporal_index": self.temporal_index
        }

    def clear_memory(self) -> str:
        """
        Clears all stored memories and indices.
        
        Returns:
            Confirmation message
        """
        self.storage = []
        self.associations = {}
        self.temporal_index = {}
        
        # Clear persistent storage if configured
        if self.memory_file and os.path.exists(self.memory_file):
            try:
                os.remove(self.memory_file)
            except Exception as e:
                print(f"Could not remove memory file: {e}")
        
        return "[Memory system cleared]"

    def _save_to_file(self) -> None:
        """Save the memory system to a file."""
        if not self.memory_file:
            return
            
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.export_full_system(), f, indent=2)
        except Exception as e:
            print(f"Could not save memory to file: {e}")

    def _load_from_file(self) -> None:
        """Load the memory system from a file."""
        if not self.memory_file or not os.path.exists(self.memory_file):
            return
            
        try:
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Restore memory components
            if "storage" in data:
                self.storage = data["storage"]
            if "associations" in data:
                self.associations = data["associations"]
            if "temporal_index" in data:
                self.temporal_index = data["temporal_index"]
        except Exception as e:
            print(f"Could not load memory from file: {e}")

    def __len__(self) -> int:
        """Return the number of memories stored."""
        return len(self.storage)

    def summarize_by_time(self, period: str = "day") -> Dict[str, int]:
        """
        Summarize memory density by time period.
        
        Args:
            period: Time period grouping ('day', 'month', or 'year')
            
        Returns:
            Dictionary of period -> memory count
        """
        summary = {}
        
        for entry in self.storage:
            if "timestamp" not in entry:
                continue
                
            try:
                timestamp = datetime.fromisoformat(entry["timestamp"])
                
                if period == "day":
                    key = timestamp.strftime("%Y-%m-%d")
                elif period == "month":
                    key = timestamp.strftime("%Y-%m")
                elif period == "year":
                    key = timestamp.strftime("%Y")
                else:
                    key = timestamp.strftime("%Y-%m-%d")
                
                if key not in summary:
                    summary[key] = 0
                summary[key] += 1
            except ValueError:
                continue
                
        return summary