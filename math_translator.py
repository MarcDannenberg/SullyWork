# sully_engine/kernel_modules/math_translator.py
# 🔢 Symbolic-to-Mathematical Expression Translator

from typing import Dict, List, Any, Optional, Union, Tuple
import re
import json
import os
import random

class SymbolicMathTranslator:
    """
    Translates between symbolic/linguistic expressions and mathematical representations.
    
    This enhanced translator supports bidirectional translation (language to math, math to language),
    contextual interpretations, and multiple translation styles from formal to poetic.
    """

    def __init__(self, mapping_file: Optional[str] = None):
        """
        Initialize the translator with standard mappings or from a custom file.
        
        Args:
            mapping_file: Optional path to a JSON file with additional mappings
        """
        # Core symbolic mappings (concept to math notation)
        self.math_mappings = {
            # Abstract concepts
            "infinity": "∞",
            "infinite": "∞",
            "endless": "∞",
            "boundless": "∞",
            "forever": "∞",
            "eternity": "∞",
            
            # Change and movement
            "change": "d/dx",
            "derivative": "d/dx",
            "rate of change": "d/dx",
            "flow": "∇",
            "gradient": "∇",
            "direction": "→",
            "vector": "→",
            "movement": "→",
            
            # Integration and accumulation
            "sum": "∑",
            "summation": "∑",
            "series": "∑",
            "accumulation": "∫",
            "total": "∫",
            "area under curve": "∫",
            "integral": "∫",
            "area": "∫",
            
            # Growth and comparison
            "growth": "f'(x) > 0",
            "increase": "f'(x) > 0",
            "expand": "f'(x) > 0",
            "decrease": "f'(x) < 0",
            "shrink": "f'(x) < 0",
            "greater than": ">",
            "less than": "<",
            "equal to": "=",
            "equivalence": "≡",
            "approximately": "≈",
            
            # Balance and systems
            "equilibrium": "∇ · F = 0",
            "balance": "∇ · F = 0",
            "harmony": "∇ · F = 0",
            "system": "S = {x : P(x)}",
            "set": "S = {x : P(x)}",
            "collection": "{x₁, x₂, ..., xₙ}",
            
            # Logic and truth
            "therefore": "∴",
            "thus": "∴",
            "because": "∵",
            "since": "∵",
            "for all": "∀",
            "every": "∀",
            "each": "∀",
            "there exists": "∃",
            "exists": "∃",
            "some": "∃",
            "not": "¬",
            "contradiction": "⊥",
            "impossible": "⊥",
            "and": "∧",
            "or": "∨",
            "implies": "→",
            "if then": "→",
            
            # Relationships and structure
            "belongs to": "∈",
            "element of": "∈",
            "contains": "⊃",
            "subset": "⊂",
            "intersection": "∩",
            "overlap": "∩",
            "union": "∪",
            "combine": "∪",
            "join": "∪",
            "empty": "∅",
            "nothing": "∅",
            "void": "∅",
            
            # Quantum and uncertainty
            "uncertainty": "Δx · Δp ≥ ℏ/2",
            "wave function": "Ψ",
            "quantum": "ℏ",
            "planck": "ℏ",
            "probability": "P(A)",
            "chance": "P(A)",
            "likelihood": "P(A)",
            
            # Time and space
            "time": "t",
            "space": "s",
            "distance": "d",
            "position": "(x,y,z)",
            "location": "(x,y,z)",
            "spacetime": "(x,y,z,t)",
            
            # Constants and notable values
            "transcendental": "π, e, φ",
            "pi": "π",
            "golden ratio": "φ",
            "euler number": "e",
            "exponential": "e^x",
            "natural log": "ln(x)",
            "logarithm": "log₂(x)",
            
            # Physics
            "energy": "E = mc²",
            "mass": "m",
            "light": "c",
            "gravity": "G",
            "force": "F = ma",
            "acceleration": "a",
            "relativity": "E = mc²",
            
            # Complex and abstract
            "imaginary": "i",
            "complex": "a + bi",
            "fractal": "z ← z² + c",
            "recursion": "f(f(x))",
            "self-reference": "f(f)",
            "paradox": "P ⟺ ¬P",
            "contradiction": "A ∧ ¬A",
            
            # Additional domains
            "entropy": "S = k · ln(W)",
            "information": "I = -log₂(p)",
            "chaos": "xₙ₊₁ = r·xₙ·(1-xₙ)",
            "network": "G = (V, E)",
            "graph": "G = (V, E)",
            "cycle": "f(x+T) = f(x)"
        }
        
        # Enhanced mathematical notations (symbol to expanded form)
        self.expanded_math = {
            "∞": "infinity",
            "d/dx": "the derivative with respect to x",
            "∇": "the gradient operator",
            "→": "a vector or direction",
            "∑": "the sum of a series",
            "∫": "the integral of",
            "∇ · F = 0": "a system in equilibrium",
            "f'(x) > 0": "a function with positive derivative (increasing)",
            "f'(x) < 0": "a function with negative derivative (decreasing)",
            ">": "greater than",
            "<": "less than",
            "=": "equals",
            "≡": "is identical to",
            "≈": "is approximately equal to",
            "∴": "therefore",
            "∵": "because",
            "∀": "for all",
            "∃": "there exists",
            "¬": "not",
            "⊥": "contradiction",
            "∧": "and",
            "∨": "or",
            "∈": "belongs to the set",
            "⊂": "is a subset of",
            "⊃": "contains",
            "∩": "intersection",
            "∪": "union",
            "∅": "the empty set",
            "Ψ": "the wave function",
            "ℏ": "Planck's constant",
            "P(A)": "probability of event A",
            "π": "pi (approximately 3.14159)",
            "e": "Euler's number (approximately 2.71828)",
            "φ": "the golden ratio (approximately 1.61803)",
            "i": "the imaginary unit, sqrt(-1)",
            "E = mc²": "energy equals mass times the speed of light squared",
            "G = (V, E)": "a graph with vertices V and edges E"
        }
        
        # Translation styles
        self.translation_styles = {
            "formal": {
                "template": "{concept} can be formally represented as {symbol}.",
                "connectors": [
                    "which is expressed as",
                    "formally denoted as",
                    "symbolically represented by",
                    "mathematically equivalent to",
                    "denoted in formal notation as"
                ]
            },
            "intuitive": {
                "template": "Think of {symbol} as representing {concept}.",
                "connectors": [
                    "which intuitively captures",
                    "giving us a way to visualize",
                    "offering an intuitive representation of",
                    "providing a mental model for",
                    "helping us grasp the idea of"
                ]
            },
            "poetic": {
                "template": "The concept of {concept} unfolds into the symbolic rhythm of {symbol}.",
                "connectors": [
                    "dancing with the essence of",
                    "resonating with the meaning of",
                    "flowing into the symbolic realm of",
                    "transcending into the notation",
                    "echoing the pattern of"
                ]
            },
            "philosophical": {
                "template": "{symbol} emerges as the embodiment of {concept}, a bridge between thought and form.",
                "connectors": [
                    "revealing the deeper truth of",
                    "transcending the boundaries between",
                    "illuminating the essence of",
                    "dissolving the distinction between",
                    "unfolding the meaning within"
                ]
            },
            "pedagogical": {
                "template": "We can understand {concept} through the mathematical lens of {symbol}.",
                "connectors": [
                    "which helps students grasp",
                    "clarifying our understanding of",
                    "providing a structured way to approach",
                    "offering a framework for comprehending",
                    "building a foundation for exploring"
                ]
            }
        }
        
        # Domain-specific notation sets
        self.domain_notations = {
            "physics": {
                "force": "F = ma",
                "energy": "E = mc²",
                "work": "W = F·d",
                "power": "P = dW/dt",
                "momentum": "p = mv",
                "relativity": "E² = (mc²)² + (pc)²",
                "wave": "Ψ(x,t) = A·sin(kx - ωt)",
                "gravity": "F = G·(m₁m₂)/r²"
            },
            "calculus": {
                "derivative": "f'(x) = lim_{h→0} (f(x+h) - f(x))/h",
                "integral": "∫ab f(x)dx = F(b) - F(a)",
                "series": "∑n=0∞ aₙ",
                "taylor": "f(x) = ∑n=0∞ (f⁽ⁿ⁾(a)/n!)·(x-a)ⁿ"
            },
            "set_theory": {
                "union": "A ∪ B = {x : x ∈ A or x ∈ B}",
                "intersection": "A ∩ B = {x : x ∈ A and x ∈ B}",
                "complement": "Aᶜ = {x ∈ U : x ∉ A}",
                "power_set": "P(A) = {S : S ⊆ A}",
                "cardinality": "|A| = n"
            },
            "logic": {
                "conjunction": "A ∧ B",
                "disjunction": "A ∨ B",
                "implication": "A → B",
                "biconditional": "A ↔ B",
                "negation": "¬A",
                "universal": "∀x P(x)",
                "existential": "∃x P(x)"
            },
            "probability": {
                "probability": "P(A)",
                "conditional": "P(A|B) = P(A ∩ B)/P(B)",
                "bayes": "P(A|B) = P(B|A)·P(A)/P(B)",
                "independence": "P(A ∩ B) = P(A)·P(B)"
            },
            "quantum": {
                "uncertainty": "Δx·Δp ≥ ℏ/2",
                "schrodinger": "iℏ·∂Ψ/∂t = ĤΨ",
                "wavefunction": "Ψ(x,t)",
                "superposition": "|Ψ⟩ = α|0⟩ + β|1⟩"
            },
            "computation": {
                "algorithm": "O(n log n)",
                "recursion": "f(n) = f(n-1) + f(n-2)",
                "turing": "M = (Q, Σ, Γ, δ, q₀, F)",
                "boolean": "A ∧ (B ∨ C)"
            }
        }
        
        # Load additional mappings from file if provided
        if mapping_file and os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r', encoding='utf-8') as f:
                    additional_mappings = json.load(f)
                    self.math_mappings.update(additional_mappings)
            except Exception as e:
                print(f"Error loading additional mappings: {e}")

    def translate(self, phrase: str, style: str = "formal", domain: Optional[str] = None) -> Union[Dict[str, Any], str]:
        """
        Translates natural language into mathematical notation.
        
        Args:
            phrase: The text to translate
            style: Translation style (formal, intuitive, poetic, philosophical, pedagogical)
            domain: Optional domain focus (physics, calculus, set_theory, etc.)
            
        Returns:
            Either a dictionary with translation details or a formatted string
        """
        # Normalize inputs
        phrase_lower = phrase.lower()
        style = style.lower() if style else "formal"
        domain = domain.lower() if domain else None
        
        # Use domain-specific notation if requested
        active_mappings = self.math_mappings.copy()
        if domain and domain in self.domain_notations:
            active_mappings.update(self.domain_notations[domain])
        
        # Find matches in phrase
        matches = {}
        for word, symbol in active_mappings.items():
            if word in phrase_lower:
                matches[word] = symbol
        
        # If no direct matches, try to find related concepts
        if not matches:
            # Look for partial matches
            for word, symbol in active_mappings.items():
                words = word.split()
                if len(words) > 1:  # For multi-word concepts
                    # Check if at least half the words match
                    matching_words = sum(1 for w in words if w in phrase_lower)
                    if matching_words >= len(words) / 2:
                        matches[word] = symbol
                elif len(word) >= 5:  # For single longer words, check partial matches
                    # If the word is at least 5 chars, check if a substantial part appears
                    if word[:4] in phrase_lower:
                        matches[word] = symbol
        
        # Prepare the response
        if not matches:
            # Create a symbolic response even when no direct match
            explanation = self._generate_symbolic_reflection(phrase)
            return {
                "matches": {},
                "explanation": explanation
            }
        
        # Format the explanation based on the requested style
        explanation = self._format_translation(matches, style)
        
        # Return detailed or simple response
        return {
            "matches": matches,
            "explanation": explanation
        }

    def translate_to_text(self, math_expression: str, style: str = "formal") -> str:
        """
        Translates mathematical notation into natural language explanation.
        
        Args:
            math_expression: The mathematical expression to translate
            style: Translation style
            
        Returns:
            Natural language explanation
        """
        # Clean the expression
        expression = math_expression.strip()
        
        # Check for direct matches in expanded forms
        if expression in self.expanded_math:
            base_explanation = self.expanded_math[expression]
        else:
            # Look for symbols within the expression
            found_symbols = []
            explained_parts = []
            
            for symbol, explanation in self.expanded_math.items():
                if symbol in expression and len(symbol) > 1:  # Avoid single character false positives
                    found_symbols.append(symbol)
                    explained_parts.append(f"{symbol} represents {explanation}")
            
            if not found_symbols:
                # Check for individual symbols
                for symbol, explanation in self.expanded_math.items():
                    if len(symbol) == 1 and symbol in expression:
                        found_symbols.append(symbol)
                        explained_parts.append(f"{symbol} represents {explanation}")
            
            if explained_parts:
                base_explanation = "This expression contains " + ", ".join(explained_parts)
            else:
                base_explanation = "This is a mathematical expression that combines multiple symbolic elements."
        
        # Apply the requested style
        if style == "formal":
            return f"The expression {math_expression} represents {base_explanation}."
        elif style == "intuitive":
            return f"Think of {math_expression} as {base_explanation} in a more intuitive sense."
        elif style == "poetic":
            return f"The symbolic dance of {math_expression} reveals {base_explanation}, a pattern unfolding in the language of mathematics."
        elif style == "philosophical":
            return f"In the realm of symbolic thought, {math_expression} emerges as {base_explanation}, bridging the concrete and abstract."
        elif style == "pedagogical":
            return f"When teaching {math_expression}, we explain it as {base_explanation}, which helps build conceptual understanding."
        else:
            return f"{math_expression}: {base_explanation}"

    def _format_translation(self, matches: Dict[str, str], style: str) -> str:
        """
        Formats the translation results according to the requested style.
        
        Args:
            matches: Dictionary of concept to symbol matches
            style: Translation style
            
        Returns:
            Formatted explanation string
        """
        # Get style configuration
        style_config = self.translation_styles.get(style, self.translation_styles["formal"])
        template = style_config["template"]
        connectors = style_config["connectors"]
        
        # Format individual matches
        formatted_matches = []
        for concept, symbol in matches.items():
            formatted = template.format(concept=concept, symbol=symbol)
            formatted_matches.append(formatted)
        
        # Combine with appropriate connectors
        if len(formatted_matches) == 1:
            return formatted_matches[0]
        
        # Use connectors for multiple matches
        result = [formatted_matches[0]]
        for i in range(1, len(formatted_matches)):
            connector = random.choice(connectors)
            result.append(f"This {connector} {formatted_matches[i].lower()}")
        
        return " ".join(result)

    def _generate_symbolic_reflection(self, phrase: str) -> str:
        """
        Generates a symbolic reflection for phrases without direct matches.
        
        Args:
            phrase: The input phrase
            
        Returns:
            A symbolic reflection
        """
        reflections = [
            f"While there's no direct mathematical mapping for '{phrase}', it suggests a conceptual space where symbolic representation could emerge.",
            f"The phrase '{phrase}' transcends current symbolic notation, existing in the liminal space between language and mathematics.",
            f"'{phrase}' represents a concept that might be expressible through a combination of existing notations or a new symbolic framework.",
            f"In considering '{phrase}', we approach the boundary where language meets formalism, suggesting potential for new notation.",
            f"Though lacking a standardized notation, '{phrase}' invites us to consider how mathematical language might evolve to capture such concepts."
        ]
        return random.choice(reflections)

    def add_mapping(self, symbol_phrase: str, math_form: str, domain: Optional[str] = None) -> str:
        """
        Adds a new symbolic → math mapping at runtime.
        
        Args:
            symbol_phrase: The symbolic phrase to map
            math_form: The corresponding mathematical representation
            domain: Optional domain category
            
        Returns:
            Confirmation message
        """
        symbol_phrase = symbol_phrase.lower()
        
        # Add to appropriate dictionary
        if domain and domain in self.domain_notations:
            self.domain_notations[domain][symbol_phrase] = math_form
            return f"Domain-specific mapping added: '{symbol_phrase}' → '{math_form}' in {domain}"
        else:
            self.math_mappings[symbol_phrase] = math_form
            return f"Mapping added: '{symbol_phrase}' → '{math_form}'"

    def add_expanded_form(self, symbol: str, explanation: str) -> str:
        """
        Adds an expanded text explanation for a mathematical symbol.
        
        Args:
            symbol: The mathematical symbol or expression
            explanation: The natural language explanation
            
        Returns:
            Confirmation message
        """
        self.expanded_math[symbol] = explanation
        return f"Expanded form added: '{symbol}' → '{explanation}'"

    def save_mappings(self, filepath: str) -> str:
        """
        Saves all mappings to a JSON file.
        
        Args:
            filepath: Path to save the mappings
            
        Returns:
            Confirmation message
        """
        data = {
            "math_mappings": self.math_mappings,
            "expanded_math": self.expanded_math,
            "domain_notations": self.domain_notations
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return f"Mappings saved to {filepath}"
        except Exception as e:
            return f"Error saving mappings: {e}"

    def load_mappings(self, filepath: str) -> str:
        """
        Loads mappings from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Confirmation message
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if "math_mappings" in data:
                self.math_mappings.update(data["math_mappings"])
            if "expanded_math" in data:
                self.expanded_math.update(data["expanded_math"])
            if "domain_notations" in data:
                for domain, mappings in data["domain_notations"].items():
                    if domain in self.domain_notations:
                        self.domain_notations[domain].update(mappings)
                    else:
                        self.domain_notations[domain] = mappings
                        
            return f"Mappings loaded from {filepath}"
        except Exception as e:
            return f"Error loading mappings: {e}"

    def analyze_expression(self, math_expression: str) -> Dict[str, Any]:
        """
        Analyzes a mathematical expression to identify its components and structure.
        
        Args:
            math_expression: The mathematical expression to analyze
            
        Returns:
            Dictionary with analysis results
        """
        # Clean the expression
        expression = math_expression.strip()
        
        # Identify symbols present
        symbols = []
        for symbol in self.expanded_math:
            if len(symbol) > 1 and symbol in expression:  # Avoid single character false positives
                symbols.append({
                    "symbol": symbol,
                    "meaning": self.expanded_math[symbol]
                })
        
        # Look for individual symbols if none found
        if not symbols:
            for symbol in self.expanded_math:
                if len(symbol) == 1 and symbol in expression:
                    symbols.append({
                        "symbol": symbol,
                        "meaning": self.expanded_math[symbol]
                    })
        
        # Attempt to identify the domain
        possible_domains = []
        for domain, notations in self.domain_notations.items():
            domain_matches = 0
            for notation_key, notation_value in notations.items():
                if notation_value in expression:
                    domain_matches += 1
            
            if domain_matches > 0:
                possible_domains.append({
                    "domain": domain,
                    "confidence": min(domain_matches / len(notations) * 10, 1.0)
                })
        
        # Sort domains by confidence
        possible_domains.sort(key=lambda x: x["confidence"], reverse=True)
        
        # Return the analysis
        return {
            "expression": expression,
            "symbols_identified": symbols,
            "possible_domains": possible_domains,
            "complexity": len(expression) / 10  # Simple heuristic for complexity
        }


# Legacy method for backward compatibility
def translate(phrase):
    """
    Simple translation function for backward compatibility.
    """
    translator = SymbolicMathTranslator()
    result = translator.translate(phrase)
    return result["explanation"]


if __name__ == "__main__":
    # Example usage when run directly
    translator = SymbolicMathTranslator()
    
    # Test translations
    tests = [
        "The infinite sum approaches equilibrium",
        "The rate of change increases over time",
        "For all systems, there exists a state of balance",
        "The wave function collapses upon observation",
        "Knowledge increases entropy while decreasing uncertainty"
    ]
    
    print("=== Mathematical Translations ===")
    for test in tests:
        result = translator.translate(test)
        print(f"\nInput: {test}")
        print(f"Output: {result['explanation']}")
        print(f"Matches: {result['matches']}")
    
    # Test reverse translations
    math_tests = [
        "∇ · F = 0",
        "E = mc²",
        "P(A|B) = P(A ∩ B)/P(B)",
        "Δx·Δp ≥ ℏ/2"
    ]
    
    print("\n=== Natural Language Translations ===")
    for test in math_tests:
        result = translator.translate_to_text(test)
        print(f"\nInput: {test}")
        print(f"Output: {result}")