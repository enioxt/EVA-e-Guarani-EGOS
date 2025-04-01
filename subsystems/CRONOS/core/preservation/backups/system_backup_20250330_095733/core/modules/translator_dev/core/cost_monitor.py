#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EVA & GUARANI Translator - Cost Monitor Module

This module provides cost monitoring for the OpenAI API, tracking usage and
implementing budget controls to help manage translation costs.
"""

import os
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field

# Setup logging
logger = logging.getLogger("cost_monitor")

def default_pricing() -> Dict[str, float]:
    """Default pricing for OpenAI models per 1K tokens"""
    return {
        "gpt-4o": 0.015,      # $0.015 per 1K tokens (average)
        "gpt-4": 0.03,        # $0.03 per 1K tokens (average)
        "gpt-3.5-turbo": 0.001  # $0.001 per 1K tokens (average)
    }

@dataclass
class CostControlConfig:
    """Configuration for cost control features"""
    enabled: bool = True
    monthly_budget: float = 5.0  # Default $5 monthly budget
    warn_at_percent: int = 80  # Warn at 80% of budget
    usage_file: str = "openai_usage.json"
    models_pricing: Dict[str, float] = field(default_factory=default_pricing)  # Price per 1K tokens
    
class CostMonitor:
    """Monitor and control costs for the OpenAI API"""
    
    def __init__(self, config: Optional[CostControlConfig] = None):
        """Initialize the cost monitor
        
        Args:
            config: Configuration for cost control
        """
        self.config = config or CostControlConfig()
        self.usage_data = self._load_usage_data()
        
    def _load_usage_data(self) -> Dict[str, Any]:
        """Load usage data from file
        
        Returns:
            Dictionary containing usage data
        """
        if not self.config.enabled:
            return {"enabled": False}
            
        # Default structure for usage data
        default_data = {
            "enabled": True,
            "monthly_budget": self.config.monthly_budget,
            "current_month": datetime.datetime.now().strftime("%Y-%m"),
            "months": {},
            "total_usage": {
                "cost": 0.0,
                "tokens": 0
            }
        }
        
        try:
            # Create directory if it doesn't exist
            usage_file = Path(self.config.usage_file)
            usage_file.parent.mkdir(parents=True, exist_ok=True)
            
            if usage_file.exists():
                with open(usage_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                # Ensure current month exists
                current_month = datetime.datetime.now().strftime("%Y-%m")
                if current_month not in data.get("months", {}):
                    data.setdefault("months", {})[current_month] = {
                        "cost": 0.0,
                        "tokens": 0,
                        "models": {}
                    }
                    
                data["current_month"] = current_month
                return data
            else:
                # Initialize with default data
                with open(usage_file, "w", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=2)
                return default_data
                
        except Exception as e:
            logger.error(f"Error loading usage data: {e}")
            return default_data
    
    def _save_usage_data(self) -> bool:
        """Save usage data to file
        
        Returns:
            True if successful, False otherwise
        """
        if not self.config.enabled:
            return True
            
        try:
            with open(self.config.usage_file, "w", encoding="utf-8") as f:
                json.dump(self.usage_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")
            return False
    
    def record_usage(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Record API usage and calculate cost
        
        Args:
            model: The model name (e.g., "gpt-3.5-turbo")
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost of this API call in USD
        """
        if not self.config.enabled:
            return 0.0
            
        # Determine cost based on model
        model_base_price = self.config.models_pricing.get(
            model, 
            self.config.models_pricing.get("gpt-3.5-turbo", 0.001)
        )
        
        # Calculate cost (simplified - in reality, input and output have different pricing)
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * model_base_price
        
        # Update usage data
        current_month = self.usage_data["current_month"]
        
        # Initialize if not exists
        if "months" not in self.usage_data:
            self.usage_data["months"] = {}
            
        if current_month not in self.usage_data["months"]:
            self.usage_data["months"][current_month] = {
                "cost": 0.0,
                "tokens": 0,
                "models": {}
            }
            
        month_data = self.usage_data["months"][current_month]
        
        # Update monthly totals
        month_data["cost"] += cost
        month_data["tokens"] += total_tokens
        
        # Update model-specific data
        month_data.setdefault("models", {})
        if model not in month_data["models"]:
            month_data["models"][model] = {
                "cost": 0.0,
                "tokens": 0,
                "calls": 0
            }
            
        model_data = month_data["models"][model]
        model_data["cost"] += cost
        model_data["tokens"] += total_tokens
        model_data["calls"] += 1
        
        # Update total usage
        self.usage_data.setdefault("total_usage", {"cost": 0.0, "tokens": 0})
        self.usage_data["total_usage"]["cost"] += cost
        self.usage_data["total_usage"]["tokens"] += total_tokens
        
        # Save updated data
        self._save_usage_data()
        
        # Check if we should warn about budget
        self._check_budget_warning()
        
        return cost
    
    def _check_budget_warning(self) -> bool:
        """Check if budget warning should be triggered
        
        Returns:
            True if warning was triggered, False otherwise
        """
        if not self.config.enabled or self.config.monthly_budget <= 0:
            return False
            
        current_month = self.usage_data["current_month"]
        month_data = self.usage_data["months"].get(current_month, {"cost": 0.0})
        
        current_cost = month_data.get("cost", 0.0)
        budget = self.config.monthly_budget
        
        # Calculate percentage of budget used
        percent_used = (current_cost / budget) * 100 if budget > 0 else 0
        
        # Warn if threshold exceeded
        if percent_used >= self.config.warn_at_percent:
            warning_msg = (
                f"⚠️ API BUDGET WARNING: ${current_cost:.2f} used "
                f"({percent_used:.1f}% of ${budget:.2f} monthly budget)"
            )
            logger.warning(warning_msg)
            
            # Critical warning if over budget
            if percent_used >= 100:
                critical_msg = (
                    f"🛑 BUDGET EXCEEDED: ${current_cost:.2f} used, "
                    f"which is ${current_cost - budget:.2f} over your "
                    f"${budget:.2f} monthly budget"
                )
                logger.critical(critical_msg)
            
            return True
            
        return False
        
    def get_current_usage(self) -> Dict[str, Any]:
        """Get current month's usage statistics
        
        Returns:
            Dictionary with usage statistics
        """
        if not self.config.enabled:
            return {"enabled": False, "cost": 0.0, "tokens": 0}
            
        current_month = self.usage_data["current_month"]
        month_data = self.usage_data["months"].get(current_month, {"cost": 0.0, "tokens": 0})
        
        usage = {
            "enabled": True,
            "current_month": current_month,
            "budget": self.config.monthly_budget,
            "cost": month_data.get("cost", 0.0),
            "tokens": month_data.get("tokens", 0),
            "percent_used": (month_data.get("cost", 0.0) / self.config.monthly_budget * 100 
                            if self.config.monthly_budget > 0 else 0),
            "models": month_data.get("models", {})
        }
        
        return usage
        
    def get_budget_remaining(self) -> float:
        """Get remaining budget for current month
        
        Returns:
            Remaining budget in USD
        """
        if not self.config.enabled or self.config.monthly_budget <= 0:
            return 0.0
            
        current_usage = self.get_current_usage()
        return max(0.0, self.config.monthly_budget - current_usage["cost"])
        
    def should_use_paid_api(self, estimated_tokens: int, model: str) -> Tuple[bool, str]:
        """Check if paid API should be used based on budget
        
        Args:
            estimated_tokens: Estimated number of tokens for the request
            model: Model to be used
            
        Returns:
            Tuple of (should_use_api, reason)
        """
        if not self.config.enabled:
            return True, "Cost monitoring disabled"
            
        # Get remaining budget
        remaining = self.get_budget_remaining()
        
        # Estimate cost of operation
        model_price = self.config.models_pricing.get(
            model, 
            self.config.models_pricing.get("gpt-3.5-turbo", 0.001)
        )
        estimated_cost = (estimated_tokens / 1000) * model_price
        
        # Prevent if we're over budget already
        current_usage = self.get_current_usage()
        if current_usage["percent_used"] >= 100:
            return False, f"Monthly budget of ${self.config.monthly_budget:.2f} exceeded"
            
        # Prevent if this operation would put us over budget
        if estimated_cost > remaining:
            return False, (
                f"Estimated cost ${estimated_cost:.4f} exceeds remaining "
                f"budget ${remaining:.2f}"
            )
            
        # Check if this would put us over warning threshold
        new_total = current_usage["cost"] + estimated_cost
        new_percent = (new_total / self.config.monthly_budget * 100
                      if self.config.monthly_budget > 0 else 0)
                      
        if (new_percent >= self.config.warn_at_percent and 
            current_usage["percent_used"] < self.config.warn_at_percent):
            logger.warning(
                f"⚠️ This translation will bring usage to {new_percent:.1f}% "
                f"of your ${self.config.monthly_budget:.2f} monthly budget"
            )
            
        return True, "Within budget limits" 