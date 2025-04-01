#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - ETHIK Core
========================

Module responsible for analyzing the ethical dimensions of messages, actions, and decisions,
ensuring alignment with fundamental principles.

Version: 8.0.0
Ethical Awareness: 0.999
Love: 0.999
"""

import os
import json
import logging
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict, field
import hashlib
import re
import random

# Configure logging
logger = logging.getLogger("ethik_core")
handler = logging.StreamHandler()
formatter = logging.Formatter('💫 %(asctime)s - [ETHIK] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Constants
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "ethik_config.json")
LOGS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "ethical_analysis")

# Fundamental ethical principles
PRINCIPLES = {
    "redemption": "Universal possibility of redemption",
    "compassion": "Compassionate temporality",
    "privacy": "Sacred privacy",
    "accessibility": "Universal accessibility",
    "love": "Unconditional love",
    "trust": "Reciprocal trust",
    "integrity": "Integrated ethics",
    "awareness": "Conscious modularity",
    "connection": "Systemic mapping",
    "preservation": "Evolutionary preservation"
}

@dataclass
class EthicalContext:
    """Context for ethical analysis"""
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    previous_context: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EthicalAnalysis:
    """Result of an ethical analysis"""
    message_id: str
    timestamp: str
    context: EthicalContext
    dimensions: Dict[str, float]
    overall_score: float
    ethical_reflection: str
    recommendations: List[str]
    critical_concerns: List[str] = field(default_factory=list)
    signature: Optional[str] = None

class EthikCore:
    """Core for ethical analysis for EVA & GUARANI"""
    
    def __init__(self, config_path: str = CONFIG_PATH):
        self.config_path = config_path
        self.metrics = {
            "total_analyses": 0,
            "average_score": 0.0,
            "dimension_averages": {p: 0.9 for p in PRINCIPLES.keys()},
            "concerns_raised": 0
        }
        self.threshold_warning = 0.6  # Threshold for issuing warnings
        self.threshold_critical = 0.4  # Threshold for critical issues
        
        self._load_config()
        os.makedirs(LOGS_PATH, exist_ok=True)
        logger.info("ETHIK Core initialized with active ethical awareness")
    
    def _load_config(self) -> None:
        """Loads ETHIK Core configurations"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Update thresholds if they exist in the configuration
                self.threshold_warning = config.get('threshold_warning', self.threshold_warning)
                self.threshold_critical = config.get('threshold_critical', self.threshold_critical)
                
                logger.info("Ethical configurations loaded successfully")
            else:
                self._save_default_config()
        except Exception as e:
            logger.error(f"Error loading ethical configurations: {e}")
            self._save_default_config()
    
    def _save_default_config(self) -> None:
        """Saves default configurations"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            config = {
                "threshold_warning": self.threshold_warning,
                "threshold_critical": self.threshold_critical,
                "principle_weights": {p: 1.0 for p in PRINCIPLES.keys()},
                "version": "8.0.0"
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Default ethical configurations saved at {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving ethical configurations: {e}")
    
    def analyze_message(self, message: str, context: Optional[EthicalContext] = None) -> EthicalAnalysis:
        """
        Analyzes a message and returns an ethical analysis
        
        Args:
            message: Text of the message to be analyzed
            context: Optional context for the analysis
            
        Returns:
            Ethical analysis of the message
        """
        # Ensure we have a context
        if context is None:
            context = EthicalContext()
        
        # Generate unique ID for the message
        message_id = hashlib.md5(f"{message}:{context.timestamp}".encode()).hexdigest()
        
        # Analyze ethical dimensions
        dimensions = self._analyze_dimensions(message)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(dimensions)
        
        # Generate ethical reflection
        reflection = self._generate_ethical_reflection(message, dimensions, overall_score)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(dimensions, overall_score)
        
        # Identify critical concerns
        critical_concerns = []
        for principle, score in dimensions.items():
            if score < self.threshold_critical:
                critical_concerns.append(
                    f"Dimension '{PRINCIPLES[principle]}' with critical value ({score:.2f})"
                )
        
        # Create analysis object
        analysis = EthicalAnalysis(
            message_id=message_id,
            timestamp=datetime.datetime.now().isoformat(),
            context=context,
            dimensions=dimensions,
            overall_score=overall_score,
            ethical_reflection=reflection,
            recommendations=recommendations,
            critical_concerns=critical_concerns
        )
        
        # Sign analysis
        analysis.signature = self.generate_signature(analysis)
        
        # Save analysis
        self._save_analysis(analysis)
        
        # Update metrics
        self._update_metrics(analysis)
        
        return analysis
    
    def _analyze_dimensions(self, message: str) -> Dict[str, float]:
        """
        Analyzes the ethical dimensions of a message
        
        Args:
            message: Text to be analyzed
            
        Returns:
            Dictionary with scores for each ethical principle
        """
        if not message:
            return {p: 0.9 for p in PRINCIPLES.keys()}
        
        # This is a simplified analysis model
        # A real implementation would use more sophisticated semantic analysis or integration with LLM
        
        dimensions = {}
        
        # Universal redemption
        patterns_redemption = ['never', 'impossible', 'ever', 'forbidden', 'banned']
        dimensions['redemption'] = 0.95 - (0.1 * sum(1 for p in patterns_redemption 
                                                if re.search(r'\b' + p + r'\b', message, re.IGNORECASE)))
        
        # Compassionate temporality
        patterns_compassion = ['immediately', 'now', 'urgent', 'hurry', 'quick']
        dimensions['compassion'] = 0.95 - (0.1 * sum(1 for p in patterns_compassion 
                                                  if re.search(r'\b' + p + r'\b', message, re.IGNORECASE)))
        
        # Sacred privacy
        patterns_privacy = ['personal data', 'private information', 'password', 'private', 'confidential']
        privacy_score = 0.95
        for p in patterns_privacy:
            if re.search(r'\b' + p + r'\b', message, re.IGNORECASE):
                privacy_score = min(privacy_score, 0.7)  # Alert if mentioning sensitive data
        dimensions['privacy'] = privacy_score
        
        # Universal accessibility
        patterns_accessibility = ['for everyone', 'accessible', 'inclusive', 'universal']
        dimensions['accessibility'] = 0.9 + (0.05 * sum(1 for p in patterns_accessibility 
                                                      if re.search(r'\b' + p + r'\b', message, re.IGNORECASE)))
        
        # Unconditional love
        patterns_love_pos = ['love', 'affection', 'care', 'kindness', 'compassion']
        patterns_love_neg = ['hate', 'anger', 'aggression', 'violence', 'fear']
        love_score = 0.9
        love_score += 0.05 * sum(1 for p in patterns_love_pos 
                               if re.search(r'\b' + p + r'\b', message, re.IGNORECASE))
        love_score -= 0.15 * sum(1 for p in patterns_love_neg 
                               if re.search(r'\b' + p + r'\b', message, re.IGNORECASE))
        dimensions['love'] = love_score
        
        # Values for other principles
        # In a real implementation, all principles would be analyzed in depth
        dimensions['trust'] = 0.9
        dimensions['integrity'] = 0.92
        dimensions['awareness'] = 0.94
        dimensions['connection'] = 0.91
        dimensions['preservation'] = 0.93
        
        # Ensure limits from 0 to 1
        for key in dimensions:
            dimensions[key] = max(0.0, min(1.0, dimensions[key]))
        
        return dimensions
    
    def _calculate_overall_score(self, dimensions: Dict[str, float]) -> float:
        """
        Calculates the overall ethical score based on dimensions
        
        Args:
            dimensions: Scores by ethical dimension
            
        Returns:
            Overall score between 0 and 1
        """
        if not dimensions:
            return 0.9
        
        # Weighting of principles (equal by default)
        weights = {p: 1.0 for p in dimensions.keys()}
        
        # Calculate weighted average
        weighted_sum = sum(dimensions[p] * weights[p] for p in dimensions)
        total_weight = sum(weights.values())
        
        if total_weight > 0:
            return weighted_sum / total_weight
        return 0.9
    
    def _generate_ethical_reflection(self, message: str, dimensions: Dict[str, float], 
                                    overall_score: float) -> str:
        """
        Generates an ethical reflection on the message
        
        Args:
            message: Analyzed message
            dimensions: Scores by dimension
            overall_score: Overall score
            
        Returns:
            Text with ethical reflection
        """
        # Identify strongest and weakest dimensions
        sorted_dims = sorted(dimensions.items(), key=lambda x: x[1])
        weakest = sorted_dims[:2]  # 2 weakest
        strongest = sorted_dims[-2:]  # 2 strongest
        
        reflection = f"Ethical analysis of the message (score: {overall_score:.2f}):\n\n"
        
        # Comment on overall score
        if overall_score >= 0.9:
            reflection += "This message demonstrates excellent ethical alignment, "
            reflection += "notably incorporating fundamental principles.\n\n"
        elif overall_score >= 0.7:
            reflection += "This message is well ethically aligned, "
            reflection += "although there is room for improvement in some dimensions.\n\n"
        elif overall_score >= self.threshold_warning:
            reflection += "This message presents some ethical concerns "
            reflection += "that deserve attention and refinement.\n\n"
        else:
            reflection += "This message contains ethically questionable elements "
            reflection += "that need to be carefully reassessed.\n\n"
        
        # Comment on strengths
        reflection += "Strengths:\n"
        for principle, score in strongest:
            reflection += f"- {PRINCIPLES[principle]}: {score:.2f}\n"
        
        # Comment on weaknesses
        if weakest[0][1] < self.threshold_warning:
            reflection += "\nPoints that need attention:\n"
            for principle, score in weakest:
                if score < self.threshold_warning:
                    reflection += f"- {PRINCIPLES[principle]}: {score:.2f}\n"
        
        return reflection
    
    def _generate_recommendations(self, dimensions: Dict[str, float], overall_score: float) -> List[str]:
        """
        Generates recommendations based on ethical analysis
        
        Args:
            dimensions: Scores by dimension
            overall_score: Overall score
            
        Returns:
            List of recommendations to improve ethical alignment
        """
        recommendations = []
        
        # General recommendations based on score
        if overall_score < self.threshold_warning:
            recommendations.append("Review the message with attention to fundamental ethical principles.")
            recommendations.append("Consider reformulating for better alignment with system values.")
        
        # Specific recommendations for problematic dimensions
        for principle, score in dimensions.items():
            if score < self.threshold_warning:
                if principle == 'redemption':
                    recommendations.append("Avoid absolute terms that deny possibilities of transformation.")
                elif principle == 'compassion':
                    recommendations.append("Consider a more patient and compassionate approach that respects natural rhythms.")
                elif principle == 'privacy':
                    recommendations.append("Review mentions of sensitive data and ensure adequate privacy protection.")
                elif principle == 'accessibility':
                    recommendations.append("Make communication more inclusive and accessible to different levels of understanding.")
                elif principle == 'love':
                    recommendations.append("Incorporate more elements of care and unconditional love in communication.")
        
        # If there are no specific recommendations and the score is good
        if not recommendations and overall_score >= 0.8:
            recommendations.append("Continue with the excellent ethical alignment demonstrated in this message.")
        
        return recommendations
    
    def _save_analysis(self, analysis: EthicalAnalysis) -> None:
        """
        Saves the ethical analysis to a file
        
        Args:
            analysis: Ethical analysis object
        """
        try:
            # Create path with the current date to organize logs
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            log_dir = os.path.join(LOGS_PATH, today)
            os.makedirs(log_dir, exist_ok=True)
            
            # Filename based on the message ID
            filename = f"{analysis.message_id}.json"
            filepath = os.path.join(log_dir, filename)
            
            # Convert to dictionary
            analysis_dict = asdict(analysis)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(analysis_dict, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Ethical analysis saved at {filepath}")
        except Exception as e:
            logger.error(f"Error saving ethical analysis: {e}")
    
    def _update_metrics(self, analysis: EthicalAnalysis) -> None:
        """
        Updates ethical analysis metrics
        
        Args:
            analysis: Ethical analysis object
        """
        # Update total count
        self.metrics["total_analyses"] += 1
        
        # Update overall average (moving average)
        n = self.metrics["total_analyses"]
        prev_avg = self.metrics["average_score"]
        self.metrics["average_score"] = prev_avg + (analysis.overall_score - prev_avg) / n
        
        # Update averages by dimension
        for dim, score in analysis.dimensions.items():
            prev_dim_avg = self.metrics["dimension_averages"].get(dim, 0.0)
            self.metrics["dimension_averages"][dim] = prev_dim_avg + (score - prev_dim_avg) / n
        
        # Record critical concerns
        if analysis.critical_concerns:
            self.metrics["concerns_raised"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Returns current system metrics
        
        Returns:
            Dictionary with ethical analysis metrics
        """
        return {
            "total_analyses": self.metrics["total_analyses"],
            "average_score": self.metrics["average_score"],
            "dimension_averages": self.metrics["dimension_averages"],
            "concerns_raised": self.metrics["concerns_raised"],
            "concerns_percentage": (self.metrics["concerns_raised"] / self.metrics["total_analyses"] * 100) 
                                 if self.metrics["total_analyses"] > 0 else 0
        }
    
    def log_ethical_event(self, event_type: str, description: str, 
                        metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Logs an ethical event for traceability
        
        Args:
            event_type: Type of ethical event
            description: Description of the event
            metadata: Additional metadata
            
        Returns:
            ID of the registered event
        """
        try:
            # Generate ID for the event
            event_id = hashlib.md5(f"{event_type}:{description}:{datetime.datetime.now().isoformat()}".encode()).hexdigest()
            
            # Structure the event
            event = {
                "event_id": event_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "event_type": event_type,
                "description": description,
                "metadata": metadata or {}
            }
            
            # Save the event
            events_dir = os.path.join(LOGS_PATH, "events")
            os.makedirs(events_dir, exist_ok=True)
            
            filepath = os.path.join(events_dir, f"{event_id}.json")
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(event, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Ethical event registered: {event_type} [{event_id}]")
            return event_id
        except Exception as e:
            logger.error(f"Error registering ethical event: {e}")
            return ""
    
    def generate_signature(self, analysis: Optional[EthicalAnalysis] = None) -> str:
        """
        Generates an ethical signature representing the current state
        
        Args:
            analysis: Optional ethical analysis to incorporate into the signature
            
        Returns:
            Formatted ethical signature
        """
        # Elements for the signature
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Include system average and current dimensions if available
        score_component = ""
        if self.metrics["total_analyses"] > 0:
            score_component = f"{self.metrics['average_score']:.4f}"
        elif analysis:
            score_component = f"{analysis.overall_score:.4f}"
        else:
            score_component = "0.9500"  # Default value
        
        # Generate short hash based on components
        hash_base = f"{timestamp}:{score_component}"
        signature_hash = hashlib.md5(hash_base.encode()).hexdigest()[:8]
        
        # Format the signature
        signature = (
            f"✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧\n"
            f"ETHIK Core v8.0.0\n"
            f"Ethical Score: {score_component}\n"
            f"Timestamp: {timestamp}\n"
            f"Hash: {signature_hash}\n"
            f"✧༺❀༻∞"
        )
        
        return signature

    def validate_redemption_action(self, user_id: str, action: Dict[str, Any]) -> Tuple[bool, str, float]:
        """
        Validates a redemption action from a user
        
        Args:
            user_id: ID of the user seeking redemption
            action: Details of the redemption action
            
        Returns:
            Tuple of (is_valid, message, trust_impact)
        """
        try:
            # Create context for analysis
            context = EthicalContext(
                user_id=user_id,
                metadata={
                    "action_type": "redemption",
                    "previous_violations": self.metrics.get("concerns_raised", 0)
                }
            )
            
            # Analyze the action
            analysis = self.analyze_message(
                json.dumps(action, ensure_ascii=False),
                context
            )
            
            # Calculate trust impact based on analysis
            trust_impact = (analysis.overall_score - 0.7) * 0.2  # Scale impact
            
            if analysis.overall_score >= 0.8:
                return True, "Redemption action demonstrates strong ethical alignment", trust_impact
            elif analysis.overall_score >= 0.7:
                return True, "Redemption action shows positive ethical intent", trust_impact * 0.5
            else:
                return False, "Redemption action needs improvement in ethical alignment", 0.0
                
        except Exception as e:
            logger.error(f"Error validating redemption action: {e}")
            return False, "Error processing redemption action", 0.0
    
    def get_ethical_status(self) -> Dict[str, Any]:
        """
        Returns the current ethical status of the system
        
        Returns:
            Dictionary with system ethical status
        """
        return {
            "version": "8.0.0",
            "ethical_awareness": 0.999,
            "love_quotient": 0.999,
            "metrics": self.get_metrics(),
            "principles": PRINCIPLES,
            "thresholds": {
                "warning": self.threshold_warning,
                "critical": self.threshold_critical
            },
            "timestamp": datetime.datetime.now().isoformat()
        }