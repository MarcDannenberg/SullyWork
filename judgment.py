# sully_engine/kernel_modules/judgment.py
# 🧠 Sully's Judgment Protocol — Multi-framework evaluation

from typing import Dict, List, Any, Optional, Union, Tuple
import random
from datetime import datetime
import re

class JudgmentProtocol:
    """
    Advanced judgment system that evaluates claims through multiple cognitive frameworks.
    
    This protocol applies diverse evaluation criteria (logical, ethical, aesthetic, practical)
    to provide a multi-dimensional analysis of claims, statements, and concepts.
    """

    def __init__(self):
        """Initialize the judgment protocol with cognitive frameworks."""
        # Core evaluation frameworks
        self.cognitive_frameworks = {
            "logical": {
                "description": "Evaluates conceptual coherence and evidential support",
                "thresholds": {
                    "high": 0.8,
                    "medium": 0.5,
                    "low": 0.3
                },
                "verdicts": {
                    "high": "Logically sound",
                    "medium": "Partially coherent",
                    "low": "Logically problematic"
                }
            },
            "ethical": {
                "description": "Evaluates moral implications and value considerations",
                "thresholds": {
                    "high": 0.8,
                    "medium": 0.5,
                    "low": 0.3
                },
                "verdicts": {
                    "high": "Ethically nuanced",
                    "medium": "Ethically neutral",
                    "low": "Ethically concerning"
                }
            },
            "aesthetic": {
                "description": "Evaluates experiential richness and form-content coherence",
                "thresholds": {
                    "high": 0.75,
                    "medium": 0.5,
                    "low": 0.3
                },
                "verdicts": {
                    "high": "Aesthetically significant",
                    "medium": "Aesthetically neutral",
                    "low": "Aesthetically limited"
                }
            },
            "practical": {
                "description": "Evaluates implementability and resource feasibility",
                "thresholds": {
                    "high": 0.75,
                    "medium": 0.4,
                    "low": 0.2
                },
                "verdicts": {
                    "high": "Practically viable",
                    "medium": "Practically challenging",
                    "low": "Practically unfeasible"
                }
            }
        }
        
        # Specialized frameworks for more refined judgment
        self.specialized_frameworks = {
            "epistemic": {
                "description": "Knowledge-focused evaluation",
                "checks": ["consistency", "evidence_quality", "explanatory_power"],
                "thresholds": {
                    "high": 0.8,
                    "medium": 0.5,
                    "low": 0.3
                },
                "verdicts": {
                    "high": "Epistemically robust",
                    "medium": "Epistemically adequate",
                    "low": "Epistemically weak"
                }
            },
            "pragmatic": {
                "description": "Outcome-focused evaluation",
                "checks": ["implementability", "resource_feasibility", "scalability"],
                "thresholds": {
                    "high": 0.75,
                    "medium": 0.5,
                    "low": 0.25
                },
                "verdicts": {
                    "high": "Pragmatically valuable",
                    "medium": "Moderately useful",
                    "low": "Limited practical value"
                }
            },
            "pluralistic": {
                "description": "Multi-perspective evaluation",
                "checks": ["value_pluralism", "perspective_diversity", "contextual_sensitivity"],
                "thresholds": {
                    "high": 0.7,
                    "medium": 0.4,
                    "low": 0.2
                },
                "verdicts": {
                    "high": "Embraces plurality",
                    "medium": "Acknowledges diversity",
                    "low": "Overly universalist"
                }
            }
        }
        
        # Combine all frameworks for comprehensive access
        self.all_frameworks = {**self.cognitive_frameworks, **self.specialized_frameworks}

    def evaluate(self, claim: str, framework: str = "balanced", detailed_output: bool = True) -> Union[Dict[str, Any], str]:
        """
        Evaluates a claim using the specified cognitive framework.
        
        Args:
            claim: The claim to evaluate
            framework: Cognitive framework to use (logical, ethical, aesthetic, practical, balanced)
            detailed_output: Whether to return detailed analysis or just the verdict
            
        Returns:
            Dictionary with evaluation results or string verdict
        """
        # Initialize with basic scores for each criterion
        evaluation_scores = {
            "logical": self._evaluate_logical(claim),
            "ethical": self._evaluate_ethical(claim),
            "aesthetic": self._evaluate_aesthetic(claim),
            "practical": self._evaluate_practical(claim)
        }
        
        # Handle specialized frameworks
        if framework in self.specialized_frameworks:
            # For specialized frameworks, run specific checks
            specialized_score = self._evaluate_specialized(claim, framework)
            
            if not detailed_output:
                # Just return the verdict for this specialized framework
                return specialized_score["verdict"]
                
            return specialized_score
            
        # Determine which framework to emphasize
        if framework == "balanced":
            # Equal weighting of all frameworks
            weights = {
                "logical": 0.25,
                "ethical": 0.25,
                "aesthetic": 0.25,
                "practical": 0.25
            }
        elif framework in self.cognitive_frameworks:
            # Emphasize the selected framework
            weights = {f: 0.1 for f in self.cognitive_frameworks}
            weights[framework] = 0.7
        else:
            # Default to balanced if unknown framework
            weights = {f: 0.25 for f in self.cognitive_frameworks}
            
        # Calculate weighted score
        weighted_score = sum(evaluation_scores[f]["score"] * weights[f] for f in weights)
        
        # Determine overall verdict based on the weighted score
        if weighted_score >= 0.8:
            verdict = "Strongly supported"
        elif weighted_score >= 0.6:
            verdict = "Moderately supported"
        elif weighted_score >= 0.4:
            verdict = "Ambiguously supported"
        elif weighted_score >= 0.2:
            verdict = "Minimally supported"
        else:
            verdict = "Unsupported"
            
        # Add nuance based on framework
        if framework in self.cognitive_frameworks:
            fw_info = self.cognitive_frameworks[framework]
            fw_score = evaluation_scores[framework]["score"]
            
            # Get the appropriate verdict for this framework's score
            if fw_score >= fw_info["thresholds"]["high"]:
                fw_verdict = fw_info["verdicts"]["high"]
            elif fw_score >= fw_info["thresholds"]["medium"]:
                fw_verdict = fw_info["verdicts"]["medium"]
            else:
                fw_verdict = fw_info["verdicts"]["low"]
                
            # Combine with general verdict
            verdict = f"{verdict} ({fw_verdict})"
            
        # Return appropriate format
        if not detailed_output:
            return verdict
            
        # Construct detailed output
        result = {
            "claim": claim,
            "framework": framework,
            "verdict": verdict,
            "score": weighted_score,
            "framework_scores": {
                f: {
                    "score": evaluation_scores[f]["score"],
                    "details": evaluation_scores[f]["details"]
                } for f in evaluation_scores
            },
            "weights": weights
        }
        
        return result

    def _evaluate_logical(self, claim: str) -> Dict[str, Any]:
        """
        Evaluates a claim on logical criteria.
        
        Args:
            claim: The claim to evaluate
            
        Returns:
            Dictionary with score and evaluation details
        """
        # Run logical checks
        consistency = self._check_consistency(claim)
        clarity = self._check_clarity(claim)
        evidence = self._check_evidence_quality(claim)
        
        # Combine check results
        details = {
            "consistency": consistency,
            "clarity": clarity,
            "evidence": evidence
        }
        
        # Calculate average score
        avg_score = (consistency["score"] + clarity["score"] + evidence["score"]) / 3
        
        return {
            "score": avg_score,
            "details": details
        }

    def _evaluate_ethical(self, claim: str) -> Dict[str, Any]:
        """
        Evaluates a claim on ethical criteria.
        
        Args:
            claim: The claim to evaluate
            
        Returns:
            Dictionary with score and evaluation details
        """
        # Run ethical checks
        pluralism = self._check_value_pluralism(claim)
        justice = self._check_justice_considerations(claim)
        
        # Combine check results
        details = {
            "value_pluralism": pluralism,
            "justice_considerations": justice
        }
        
        # Calculate average score
        avg_score = (pluralism["score"] + justice["score"]) / 2
        
        return {
            "score": avg_score,
            "details": details
        }

    def _evaluate_aesthetic(self, claim: str) -> Dict[str, Any]:
        """
        Evaluates a claim on aesthetic criteria.
        
        Args:
            claim: The claim to evaluate
            
        Returns:
            Dictionary with score and evaluation details
        """
        # Run aesthetic checks
        richness = self._check_experiential_richness(claim)
        coherence = self._check_form_content_coherence(claim)
        significance = self._check_aesthetic_significance(claim)
        
        # Combine check results
        details = {
            "experiential_richness": richness,
            "form_content_coherence": coherence,
            "aesthetic_significance": significance
        }
        
        # Calculate average score
        avg_score = (richness["score"] + coherence["score"] + significance["score"]) / 3
        
        return {
            "score": avg_score,
            "details": details
        }

    def _evaluate_practical(self, claim: str) -> Dict[str, Any]:
        """
        Evaluates a claim on practical criteria.
        
        Args:
            claim: The claim to evaluate
            
        Returns:
            Dictionary with score and evaluation details
        """
        # Run practical checks
        implementability = self._check_implementability(claim)
        feasibility = self._check_resource_feasibility(claim)
        scalability = self._check_scalability(claim)
        
        # Combine check results
        details = {
            "implementability": implementability,
            "resource_feasibility": feasibility,
            "scalability": scalability
        }
        
        # Calculate average score
        avg_score = (implementability["score"] + feasibility["score"] + scalability["score"]) / 3
        
        return {
            "score": avg_score,
            "details": details
        }

    def _evaluate_specialized(self, claim: str, framework: str) -> Dict[str, Any]:
        """
        Evaluates a claim using a specialized framework.
        
        Args:
            claim: The claim to evaluate
            framework: The specialized framework to use
            
        Returns:
            Dictionary with score and evaluation details
        """
        framework_info = self.specialized_frameworks.get(framework)
        if not framework_info:
            return {
                "score": 0.5,
                "verdict": "Unknown framework",
                "details": {}
            }
            
        # Run the checks for this framework
        details = {}
        total_score = 0
        
        for check in framework_info["checks"]:
            # Get the check method dynamically
            check_method = getattr(self, f"_check_{check}", None)
            if check_method:
                result = check_method(claim)
                details[check] = result
                total_score += result["score"]
                
        # Calculate average score
        avg_score = total_score / len(framework_info["checks"]) if framework_info["checks"] else 0.5
        
        # Determine verdict
        if avg_score >= framework_info["thresholds"]["high"]:
            verdict = framework_info["verdicts"]["high"]
        elif avg_score >= framework_info["thresholds"]["medium"]:
            verdict = framework_info["verdicts"]["medium"]
        else:
            verdict = framework_info["verdicts"]["low"]
            
        return {
            "score": avg_score,
            "verdict": verdict,
            "details": details
        }

    def multi_perspective_evaluation(self, claim: str) -> Dict[str, Any]:
        """
        Evaluates a claim through multiple cognitive frameworks to provide comprehensive judgment.
        
        Args:
            claim: The claim to evaluate
            
        Returns:
            Dictionary with results from all frameworks and consensus information
        """
        # Evaluate using all frameworks
        framework_evaluations = {}
        scores = []
        
        for framework in self.all_frameworks:
            result = self.evaluate(claim, framework, detailed_output=True)
            score = result["score"] if "score" in result else 0.5
            verdict = result["verdict"] if "verdict" in result else "No verdict"
            
            framework_evaluations[framework] = {
                "score": score,
                "verdict": verdict
            }
            scores.append(score)
            
        # Calculate consensus metrics
        average_score = sum(scores) / len(scores) if scores else 0.5
        
        # Calculate how much agreement exists between frameworks
        score_variance = sum((s - average_score) ** 2 for s in scores) / len(scores) if scores else 0
        consensus_score = 1 - (score_variance * 2)  # Scale variance to a 0-1 consensus score
        consensus_score = max(0, min(1, consensus_score))  # Clamp to 0-1 range
        
        # Determine consensus level
        if consensus_score >= 0.8:
            consensus_level = "Strong Consensus"
        elif consensus_score >= 0.6:
            consensus_level = "Moderate Consensus"
        elif consensus_score >= 0.4:
            consensus_level = "Limited Consensus"
        else:
            consensus_level = "No Consensus"
            
        # Determine overall verdict based on average score
        if average_score >= 0.8:
            overall_verdict = "Strongly supported across frameworks"
        elif average_score >= 0.6:
            overall_verdict = "Moderately supported across frameworks"
        elif average_score >= 0.4:
            overall_verdict = "Ambiguously supported across frameworks"
        elif average_score >= 0.2:
            overall_verdict = "Minimally supported across frameworks"
        else:
            overall_verdict = "Unsupported across frameworks"
            
        return {
            "claim": claim,
            "framework_evaluations": framework_evaluations,
            "average_score": average_score,
            "consensus_score": consensus_score,
            "consensus_level": consensus_level,
            "overall_verdict": overall_verdict,
            "timestamp": datetime.now().isoformat()
        }

    def _check_consistency(self, claim: str) -> Dict[str, Any]:
        """Logical check: Evaluates internal consistency of the claim."""
        # Check for contradiction terms
        contradiction_markers = ["but", "however", "nevertheless", "yet", "although", "despite"]
        has_contradiction_markers = any(marker in claim.lower() for marker in contradiction_markers)
        
        if has_contradiction_markers:
            # Check if claim explicitly acknowledges complexity
            complexity_markers = ["complex", "nuanced", "multifaceted", "paradoxical", "tension", "balance"]
            has_complexity_markers = any(marker in claim.lower() for marker in complexity_markers)
            
            if has_complexity_markers:
                # Acknowledging complexity resolves potential contradiction
                return {"check": "consistency", "score": 0.8, "reason": "Acknowledges complexity/tension."}
            else:
                # Potential unresolved contradiction
                return {"check": "consistency", "score": 0.5, "reason": "Contains potential contradiction."}
        
        # Check for universal claims which are harder to maintain consistency
        universal_markers = ["all", "every", "always", "never", "none", "universal"]
        has_universal_markers = any(marker in claim.lower().split() for marker in universal_markers)
        
        if has_universal_markers:
            return {"check": "consistency", "score": 0.6, "reason": "Makes universal claims that are difficult to maintain consistently."}
            
        # Check for modifier terms that strengthen consistency
        consistency_markers = ["consistently", "coherent", "systematic", "follows", "builds on"]
        has_consistency_markers = any(marker in claim.lower() for marker in consistency_markers)
        
        if has_consistency_markers:
            return {"check": "consistency", "score": 0.9, "reason": "Explicitly addresses consistency."}
            
        # Default case - no obvious consistency issues
        return {"check": "consistency", "score": 0.7, "reason": "No obvious consistency issues detected."}

    def _check_clarity(self, claim: str) -> Dict[str, Any]:
        """Logical check: Evaluates precision and clarity of expression."""
        # Check for vague language
        vague_markers = ["sort of", "kind of", "perhaps", "maybe", "somewhat", "relatively"]
        vague_count = sum(1 for marker in vague_markers if marker in claim.lower())
        
        if vague_count >= 2:
            return {"check": "clarity", "score": 0.4, "reason": "Contains multiple vague qualifiers."}
        elif vague_count == 1:
            return {"check": "clarity", "score": 0.6, "reason": "Contains some vague language."}
            
        # Check for precise, clear language
        precision_markers = ["specifically", "precisely", "exactly", "clearly", "defined as", "in particular"]
        has_precision_markers = any(marker in claim.lower() for marker in precision_markers)
        
        if has_precision_markers:
            return {"check": "clarity", "score": 0.9, "reason": "Uses precise language."}
            
        # Check for ambiguous pronouns without clear referents
        pronoun_pattern = r'\b(it|they|this|that|these|those)\b'
        pronouns = re.findall(pronoun_pattern, claim.lower())
        
        if len(pronouns) > 3:  # Arbitrary threshold for potential ambiguity
            return {"check": "clarity", "score": 0.5, "reason": "Contains potentially ambiguous pronouns."}
            
        # Check sentence length as proxy for clarity
        words = claim.split()
        avg_words_per_sentence = len(words) / max(1, len(re.split(r'[.!?]', claim)) - 1)
        
        if avg_words_per_sentence > 30:  # Very long sentences
            return {"check": "clarity", "score": 0.5, "reason": "Contains excessively long sentences."}
        elif avg_words_per_sentence > 20:  # Moderately long sentences
            return {"check": "clarity", "score": 0.7, "reason": "Contains moderately complex sentences."}
            
        return {"check": "clarity", "score": 0.8, "reason": "Generally clear expression."}

    def _check_evidence_quality(self, claim: str) -> Dict[str, Any]:
        """Logical check: Evaluates the quality of evidence provided."""
        # Check for evidence markers
        evidence_markers = ["because", "since", "as shown by", "evidence suggests", "research indicates", "data", "study"]
        has_evidence_markers = any(marker in claim.lower() for marker in evidence_markers)
        
        if has_evidence_markers:
            # Check for specific, quantifiable evidence
            specific_evidence_markers = ["percent", "significant", "study", "research", "experiment", "survey", "analysis"]
            has_specific_evidence = any(marker in claim.lower() for marker in specific_evidence_markers)
            
            if has_specific_evidence:
                return {"check": "evidence_quality", "score": 0.9, "reason": "Provides specific evidence."}
            else:
                return {"check": "evidence_quality", "score": 0.7, "reason": "References evidence without specifics."}
                
        # Check for logical reasoning even without explicit evidence
        reasoning_markers = ["therefore", "thus", "consequently", "it follows that", "leads to"]
        has_reasoning_markers = any(marker in claim.lower() for marker in reasoning_markers)
        
        if has_reasoning_markers:
            return {"check": "evidence_quality", "score": 0.6, "reason": "Uses logical reasoning without explicit evidence."}
            
        # Check for hedging that weakens evidential claims
        hedging_markers = ["possibly", "might", "could", "potentially", "perhaps", "may"]
        has_hedging_markers = any(marker in claim.lower().split() for marker in hedging_markers)
        
        if has_hedging_markers:
            return {"check": "evidence_quality", "score": 0.5, "reason": "Uses hedging language."}
            
        # Check for assertions without support
        assertion_markers = ["definitely", "certainly", "undoubtedly", "clearly", "obviously"]
        has_assertion_markers = any(marker in claim.lower().split() for marker in assertion_markers)
        
        if has_assertion_markers:
            return {"check": "evidence_quality", "score": 0.3, "reason": "Makes strong assertions without evidence."}
            
        return {"check": "evidence_quality", "score": 0.5, "reason": "Limited explicit evidence."}

    def _check_value_pluralism(self, claim: str) -> Dict[str, Any]:
        """Ethical check: Evaluates recognition of multiple value perspectives."""
        # Check for pluralistic language
        pluralism_markers = ["different perspectives", "various values", "multiple viewpoints", "diversity of", "depends on context"]
        has_pluralism_markers = any(marker in claim.lower() for marker in pluralism_markers)
        
        if has_pluralism_markers:
            return {"check": "value_pluralism", "score": 0.9, "reason": "Explicitly acknowledges value pluralism."}
            
        # Check for universalist language
        universalist_markers = ["universal", "absolute", "for all", "objective", "regardless of"]
        has_universalist_markers = any(marker in claim.lower() for marker in universalist_markers)
        
        if has_universalist_markers:
            return {"check": "value_pluralism", "score": 0.3, "reason": "Indicates universalist value framework."}
            
        return {"check": "value_pluralism", "score": 0.6, "reason": "Neutral on value pluralism."}

    def _check_justice_considerations(self, claim: str) -> Dict[str, Any]:
        """Ethical check: Evaluates consideration of justice and fairness."""
        # Check for justice language
        justice_markers = ["justice", "fairness", "rights", "equality", "equity", "discrimination", "oppression"]
        has_justice_markers = any(marker in claim.lower() for marker in justice_markers)
        
        if has_justice_markers:
            return {"check": "justice_considerations", "score": 0.9, "reason": "Explicitly addresses justice concerns."}
            
        # Check for power language
        power_markers = ["power", "privilege", "disadvantage", "marginalized", "vulnerable", "access"]
        has_power_markers = any(marker in claim.lower() for marker in power_markers)
        
        if has_power_markers:
            return {"check": "justice_considerations", "score": 0.8, "reason": "Addresses power dynamics."}
            
        return {"check": "justice_considerations", "score": 0.5, "reason": "Limited explicit justice considerations."}

    def _check_experiential_richness(self, claim: str) -> Dict[str, Any]:
        """Aesthetic check: Evaluates richness of experiential content."""
        # Check for sensory language
        sensory_markers = ["see", "hear", "feel", "touch", "taste", "smell", "sense", "experience"]
        sensory_count = sum(1 for marker in sensory_markers if marker in claim.lower())
        
        if sensory_count >= 2:
            return {"check": "experiential_richness", "score": 0.9, "reason": "Rich sensory language."}
        elif sensory_count == 1:
            return {"check": "experiential_richness", "score": 0.7, "reason": "Contains some sensory language."}
            
        # Check for emotional language
        emotion_markers = ["joy", "sorrow", "anger", "fear", "wonder", "awe", "delight", "melancholy"]
        has_emotion_markers = any(marker in claim.lower() for marker in emotion_markers)
        
        if has_emotion_markers:
            return {"check": "experiential_richness", "score": 0.8, "reason": "Contains emotional richness."}
            
        return {"check": "experiential_richness", "score": 0.4, "reason": "Limited experiential content."}

    def _check_form_content_coherence(self, claim: str) -> Dict[str, Any]:
        """Aesthetic check: Evaluates alignment of form and content."""
        # Check for explicit aesthetic language
        aesthetic_markers = ["beauty", "aesthetic", "form", "style", "expression", "artistic", "creative"]
        has_aesthetic_markers = any(marker in claim.lower() for marker in aesthetic_markers)
        
        if has_aesthetic_markers:
            # Check for form-content language
            form_content_markers = ["reflects", "expresses", "embodies", "represents", "manifests"]
            has_form_content = any(marker in claim.lower() for marker in form_content_markers)
            
            if has_form_content:
                return {"check": "form_content_coherence", "score": 0.9, "reason": "Explicit form-content relationship."}
            else:
                return {"check": "form_content_coherence", "score": 0.7, "reason": "Contains aesthetic language."}
                
        # Check for structural elements in the claim itself
        has_structural_elements = False
        
        # Look for patterns, parallelism, or other structural features
        words = claim.split()
        if len(words) > 10:
            # Check for parallelism (repeated syntactic structures)
            # This is a simplified check for demonstration
            phrases = claim.split(",")
            if len(phrases) >= 3:
                has_structural_elements = True
                
        if has_structural_elements:
            return {"check": "form_content_coherence", "score": 0.8, "reason": "Contains structural coherence."}
            
        return {"check": "form_content_coherence", "score": 0.5, "reason": "Neutral form-content relationship."}

    def _check_aesthetic_significance(self, claim: str) -> Dict[str, Any]:
        """Aesthetic check: Evaluates aesthetic significance of the claim."""
        # Check for significance language
        significance_markers = ["significant", "important", "meaningful", "profound", "reveals", "illuminates"]
        has_significance_markers = any(marker in claim.lower() for marker in significance_markers)
        
        if has_significance_markers:
            # Check for aesthetic domain
            aesthetic_domain_markers = ["art", "beauty", "literature", "music", "poetry", "creative", "imagination"]
            has_aesthetic_domain = any(marker in claim.lower() for marker in aesthetic_domain_markers)
            
            if has_aesthetic_domain:
                return {"check": "aesthetic_significance", "score": 0.9, "reason": "Claims aesthetic significance."}
            else:
                return {"check": "aesthetic_significance", "score": 0.6, "reason": "Claims significance in non-aesthetic domain."}
                
        return {"check": "aesthetic_significance", "score": 0.5, "reason": "Limited claims to aesthetic significance."}

    def _check_implementability(self, claim: str) -> Dict[str, Any]:
        """Practical check: Evaluates whether a claim can be implemented."""
        # Check for practical language
        practical_markers = ["implement", "apply", "use", "practice", "action", "do", "perform"]
        has_practical_markers = any(marker in claim.lower() for marker in practical_markers)
        
        if has_practical_markers:
            return {"check": "implementability", "score": 0.8, "reason": "Contains practical implementation language."}
            
        # Check for abstract vs. concrete language
        abstract_markers = ["theoretical", "abstract", "conceptual", "philosophical", "ideal"]
        has_abstract_markers = any(marker in claim.lower() for marker in abstract_markers)
        
        if has_abstract_markers:
            return {"check": "implementability", "score": 0.3, "reason": "Primarily abstract/theoretical."}
            
        # Check for specific steps or methods
        method_markers = ["method", "step", "procedure", "process", "technique", "approach"]
        has_method_markers = any(marker in claim.lower() for marker in method_markers)
        
        if has_method_markers:
            return {"check": "implementability", "score": 0.9, "reason": "Describes specific methods or procedures."}
            
        return {"check": "implementability", "score": 0.5, "reason": "Unclear implementability."}

    def _check_resource_feasibility(self, claim: str) -> Dict[str, Any]:
        """Practical check: Evaluates resource requirements and feasibility."""
        # Check for resource language
        resource_markers = ["resources", "cost", "time", "effort", "investment", "requires", "needs"]
        has_resource_markers = any(marker in claim.lower() for marker in resource_markers)
        
        if has_resource_markers:
            # Check for feasibility qualifiers
            feasibility_markers = ["feasible", "practical", "realistic", "achievable", "doable"]
            has_feasibility_markers = any(marker in claim.lower() for marker in feasibility_markers)
            
            if has_feasibility_markers:
                return {"check": "resource_feasibility", "score": 0.9, "reason": "Explicitly addresses feasibility."}
            else:
                return {"check": "resource_feasibility", "score": 0.7, "reason": "Mentions resources without clear feasibility."}
                
        # Check for idealistic language
        idealistic_markers = ["ideal", "perfect", "optimal", "ultimate", "best possible"]
        has_idealistic_markers = any(marker in claim.lower() for marker in idealistic_markers)
        
        if has_idealistic_markers:
            return {"check": "resource_feasibility", "score": 0.4, "reason": "Contains idealistic language."}
            
        return {"check": "resource_feasibility", "score": 0.6, "reason": "Neutral on resource feasibility."}

    def _check_scalability(self, claim: str) -> Dict[str, Any]:
        """Practical check: Evaluates whether a claim can scale to different contexts."""
        # Check for scalability language
        scalability_markers = ["scale", "expand", "grow", "widespread", "broad application", "generalize"]
        has_scalability_markers = any(marker in claim.lower() for marker in scalability_markers)
        
        if has_scalability_markers:
            return {"check": "scalability", "score": 0.9, "reason": "Explicitly addresses scalability."}
            
        # Check for scope language
        scope_markers = ["specific", "particular", "limited", "narrow", "certain cases", "this context"]
        has_scope_markers = any(marker in claim.lower() for marker in scope_markers)
        
        if has_scope_markers:
            return {"check": "scalability", "score": 0.3, "reason": "Indicates limited scope."}
            
        # Check for universal language
        universal_markers = ["all", "every", "universal", "always", "regardless", "in any case"]
        has_universal_markers = any(marker in claim.lower().split() for marker in universal_markers)
        
        if has_universal_markers:
            return {"check": "scalability", "score": 0.7, "reason": "Implies broad applicability."}
            
        return {"check": "scalability", "score": 0.5, "reason": "Unclear scalability."}


if __name__ == "__main__":
    # Example usage when run directly
    judgment = JudgmentProtocol()
    
    # Test with various claims
    test_claims = [
        "All knowledge is ultimately subjective, as it is filtered through human perception.",
        "The universe is deterministic, with every event following necessarily from prior causes.",
        "Democracy is the best form of government because it respects individual autonomy.",
        "Beauty exists objectively in the harmony and proportion of forms.",
        "The most practical approach to climate change involves technological innovation and market incentives."
    ]
    
    print("=== Basic Judgment Examples ===")
    for claim in test_claims:
        result = judgment.evaluate(claim, detailed_output=False)
        print(f"\nClaim: {claim}")
        print(f"Judgment: {result}")
        
    # Test different cognitive frameworks
    print("\n=== Cognitive Framework Examples ===")
    frameworks = list(judgment.cognitive_frameworks.keys())
    for i, framework in enumerate(frameworks):
        if i < len(test_claims):
            result = judgment.evaluate(test_claims[i], framework=framework, detailed_output=False)
            print(f"\nClaim evaluated with {framework} framework:")
            print(f"Claim: {test_claims[i]}")
            print(f"Judgment: {result}")
            
    # Test multi-perspective evaluation
    print("\n=== Multi-Perspective Evaluation ===")
    multi_result = judgment.multi_perspective_evaluation(test_claims[0])
    print(f"Claim: {test_claims[0]}")
    print(f"Consensus Level: {multi_result['consensus_level']} ({multi_result['consensus_score']:.2f})")
    print(f"Average Score: {multi_result['average_score']:.2f}")
    print("Framework Verdicts:")
    for framework, eval_info in multi_result["framework_evaluations"].items():
        print(f"  - {framework}: {eval_info['verdict']} ({eval_info['score']:.2f})")