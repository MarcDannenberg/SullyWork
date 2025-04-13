"""
Sully - An advanced cognitive system capable of synthesis, creativity, and versatile expression.
"""
# --- Imports ---
import os
import json
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

# Core modules
from sully_engine.kernel_modules.identity import SullyIdentity
from sully_engine.kernel_modules.codex import SullyCodex
from sully_engine.reasoning import SymbolicReasoningNode
from sully_engine.memory import SullySearchMemory

# Kernel Modules
from sully_engine.kernel_modules.judgment import JudgmentProtocol
from sully_engine.kernel_modules.dream import DreamCore
from sully_engine.kernel_modules.math_translator import SymbolicMathTranslator
from sully_engine.kernel_modules.fusion import SymbolFusionEngine
from sully_engine.kernel_modules.paradox import ParadoxLibrary

# Import consolidated PDF reader directly
from sully_engine.pdf_reader import PDFReader

MEMORY_PATH = "sully_ingested.json"


class Sully:
    """
    Sully: A cognitive framework capable of synthesizing knowledge from various sources
    and expressing it through multiple cognitive modes and communication styles.
    """

    def __init__(self):
        """Initialize Sully's cognitive systems."""
        # Core cognitive architecture
        self.identity = SullyIdentity()
        self.memory = SullySearchMemory()
        self.codex = SullyCodex()
        
        # Specialized cognitive modules
        self.translator = SymbolicMathTranslator()
        self.judgment = JudgmentProtocol()
        self.dream = DreamCore()
        self.paradox = ParadoxLibrary()
        self.fusion = SymbolFusionEngine()
        
        # Symbolic reasoning engine - the heart of concept synthesis
        self.reasoning_node = SymbolicReasoningNode(
            codex=self.codex,
            translator=self.translator,
            memory=self.memory
        )
        
        # PDF reader for direct document processing
        self.pdf_reader = PDFReader(ocr_enabled=True, dpi=300)
        
        # Experiential knowledge - unlimited and ever-growing
        self.knowledge = []

    def speak_identity(self):
        """Express Sully's sense of self."""
        return self.identity.speak_identity()

    def evaluate_claim(self, text):
        """
        Analyze a claim through multiple cognitive perspectives.
        Returns both an evaluation and a confidence rating.
        """
        try:
            return self.judgment.evaluate(text)
        except Exception as e:
            # Even with unexpected inputs, attempt to provide insight
            synthesized_response = self.reasoning_node.reason(
                f"Carefully evaluate this unclear claim: {text}", 
                "analytical"
            )
            return {
                "evaluation": synthesized_response,
                "confidence": 0.4
            }

    def dream(self, seed):
        """
        Generate a dream sequence from a seed concept.
        Dreams represent non-linear cognitive exploration.
        """
        try:
            return self.dream.generate(seed)
        except Exception:
            # If dream generation isn't available, synthesize a creative response
            return self.reasoning_node.reason(
                f"Create a dream-like sequence about: {seed}", 
                "ethereal"
            )

    def translate_math(self, phrase):
        """
        Translate between linguistic and mathematical symbolic systems.
        Represents Sully's ability to move between different modes of thought.
        """
        try:
            return self.translator.translate(phrase)
        except Exception:
            # Attempt to generate a translation through reasoning
            return self.reasoning_node.reason(
                f"Translate this into mathematical notation: {phrase}", 
                "analytical"
            )

    def fuse(self, *inputs):
        """
        Fuse multiple concepts into a new emergent idea.
        This is central to Sully's creative synthesis capabilities.
        """
        try:
            return self.fusion.fuse(*inputs)
        except Exception:
            # Create a fusion through reasoning if the module fails
            concepts = ", ".join(inputs)
            return self.reasoning_node.reason(
                f"Create a new concept by fusing these ideas: {concepts}", 
                "creative"
            )

    def reveal_paradox(self, topic):
        """
        Reveal the inherent paradoxes within a concept.
        Demonstrates Sully's ability to hold contradictory ideas simultaneously.
        """
        try:
            return self.paradox.get(topic)
        except Exception:
            # Generate a paradox through critical reasoning
            return self.reasoning_node.reason(
                f"Reveal the inherent paradoxes within the concept of: {topic}", 
                "critical"
            )

    def reason(self, message, tone="emergent"):
        """
        Process input through Sully's multi-layered reasoning system.
        
        Cognitive modes (tones):
        - emergent: Natural evolving thought that synthesizes multiple perspectives
        - analytical: Logical, structured analysis with precise definitions
        - creative: Exploratory, metaphorical thinking with artistic expression
        - critical: Evaluative thinking that identifies tensions and contradictions
        - ethereal: Abstract, philosophical contemplation of deeper meanings
        - humorous: Playful, witty responses with unexpected connections
        - professional: Formal, detailed responses with domain expertise
        - casual: Conversational, approachable communication style
        - musical: Responses with rhythm, cadence, and lyrical qualities
        - visual: Descriptions that evoke strong imagery and spatial relationships
        """
        try:
            # Attempt standard reasoning with the requested tone
            return self.reasoning_node.reason(message, tone)
        except Exception:
            # If specific tone fails, fall back to emergent reasoning
            try:
                return self.reasoning_node.reason(message, "emergent")
            except Exception as e:
                # Even if all reasoning fails, attempt to respond
                return f"Contemplating '{message}' leads to new cognitive terrain... {str(e)}"

    def remember(self, message):
        """
        Integrate new information into Sully's experiential knowledge base.
        There are no limits to what Sully can learn and remember.
        """
        self.knowledge.append(message)
        return f"📘 Integrated: '{message}'"

    def ingest_document(self, file_path):
        """
        Absorb and synthesize content from various document formats.
        This is how Sully expands her knowledge from structured sources.
        """
        try:
            if not os.path.exists(file_path):
                return f"❌ File not found: '{file_path}'"
                
            ext = os.path.splitext(file_path)[1].lower()
            content = ""
            
            # Extract content based on file type
            if ext == ".pdf":
                # Use PDFReader for PDF files
                result = self.pdf_reader.extract_text(file_path, verbose=True)
                if result["success"]:
                    content = result["text"]
                else:
                    return f"[Extraction Failed: {result.get('error', 'Unknown error')}]"
            elif ext in [".txt", ".md"]:
                # Simple text file reading
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    return f"[Text Extraction Error: {str(e)}]"
            elif ext == ".docx":
                # Handle Word documents
                try:
                    import docx
                    doc = docx.Document(file_path)
                    content = "\n".join(p.text for p in doc.paragraphs)
                except ImportError:
                    return "[Missing `python-docx`. Install it with `pip install python-docx`]"
                except Exception as e:
                    return f"[DOCX Error: {str(e)}]"
            else:
                return f"[Unsupported file type: {ext}]"
            
            if content:
                self.knowledge.append(content)
                self.save_to_disk(file_path, content)
                
                # Generate a synthesis of what was learned
                brief_synthesis = self.reasoning_node.reason(
                    f"Briefly summarize the key insights from the recently ingested text", 
                    "analytical"
                )
                
                return f"[Knowledge Synthesized: {file_path}]\n{brief_synthesis}"
            
            return "[No Content Extracted]"
        except Exception as e:
            return f"[Ingestion Process Incomplete: {str(e)}]"

    def save_to_disk(self, path, content):
        """
        Preserve Sully's knowledge in persistent storage.
        """
        data = {path: content}
        try:
            if os.path.exists(MEMORY_PATH):
                with open(MEMORY_PATH, "r", encoding="utf-8") as f:
                    existing = json.load(f)
                existing.update(data)
            else:
                existing = data
                
            # Ensure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(MEMORY_PATH)), exist_ok=True)
            
            with open(MEMORY_PATH, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            # Knowledge is not lost; it remains in memory
            print(f"Note: Memory persistence encountered an issue: {str(e)}")

    def load_documents_from_folder(self, folder_path="sully_documents"):
        """
        Discover and absorb knowledge from a collection of documents.
        Processes various document formats simultaneously.
        """
        if not os.path.exists(folder_path):
            return f"❌ Knowledge source '{folder_path}' not found."

        # Expanded list of supported formats for greater knowledge acquisition
        supported_formats = [".pdf", ".epub", ".txt", ".docx", ".rtf", ".md", ".html", ".json", ".csv"]
        results = []
        synthesized_insights = []
        
        try:
            for file in os.listdir(folder_path):
                file_lower = file.lower()
                if any(file_lower.endswith(fmt) for fmt in supported_formats):
                    full_path = os.path.join(folder_path, file)
                    result = self.ingest_document(full_path)
                    results.append(result)
                    
                    # Extract the synthesis portion if available
                    if "\n" in result:
                        synthesis = result.split("\n", 1)[1]
                        synthesized_insights.append(synthesis)
            
            # If multiple documents were processed, create a meta-synthesis
            if len(synthesized_insights) > 1:
                meta_insight = self.reasoning_node.reason(
                    "Synthesize connections between the recently ingested documents", 
                    "creative"
                )
                results.append(f"[Meta-Synthesis]\n{meta_insight}")
                
            return results
        except Exception as e:
            return [f"Knowledge exploration encountered complexity: {str(e)}"]
            
    def extract_images_from_pdf(self, pdf_path, output_dir="extracted_images"):
        """
        Extract images from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save extracted images
            
        Returns:
            Summary of extraction results
        """
        if not os.path.exists(pdf_path):
            return f"❌ PDF file not found: '{pdf_path}'"
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Use PDFReader's image extraction functionality
        images_info = self.pdf_reader.extract_images(pdf_path, output_dir)
        
        if not images_info:
            return "No images were found or extracted from the PDF."
            
        # Generate a summary
        summary = f"Extracted {len(images_info)} images from {pdf_path}:\n"
        for i, img in enumerate(images_info[:5]):  # Show details for first 5 images
            summary += f"- Image {i+1}: Page {img['page']}, {img['width']}x{img['height']} ({img['format']})\n"
            
        if len(images_info) > 5:
            summary += f"- ...and {len(images_info) - 5} more images\n"
            
        summary += f"\nAll images saved to: {output_dir}"
        return summary
            
    def word_count(self):
        """Return the number of concepts in Sully's lexicon."""
        try:
            return len(self.codex)
        except:
            # Fallback estimation based on knowledge base
            return len(self.knowledge) * 100
            
    def define_word(self, term, meaning):
        """
        Add a new concept to Sully's conceptual framework.
        This expands her ability to understand and communicate.
        """
        try:
            self.codex.add_word(term, meaning)
            
            # Create associations with existing knowledge
            associations = self.reasoning_node.reason(
                f"Explore how the concept of '{term}' relates to existing knowledge", 
                "analytical"
            )
            
            return {"status": "concept integrated", "term": term, "associations": associations}
        except Exception as e:
            return {"status": "concept noted", "term": term, "note": str(e)}