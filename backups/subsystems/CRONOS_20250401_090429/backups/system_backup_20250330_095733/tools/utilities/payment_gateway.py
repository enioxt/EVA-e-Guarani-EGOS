#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Payment Gateway
====================================

This module implements a payment gateway for the Telegram bot EVA & GUARANI,
allowing payments via PIX and cryptocurrencies and managing the FREEMIUM credit system.

Author: EVA & GUARANI
Version: 2.0
"""

import os
import json
import time
import logging
import hashlib
import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

# Logging configuration
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/payment_gateway.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("payment_gateway")

class PaymentGateway:
    """
    Payment gateway for the Telegram bot EVA & GUARANI.
    Manages payments, user tiers, usage limits, and credit system.
    """
    
    def __init__(self, config_path: str = "config/payment_config.json"):
        """
        Initializes the payment gateway.
        
        Args:
            config_path: Path to the configuration file.
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Ensure initial_credits_value exists in the configuration
        if "initial_credits_value" not in self.config:
            self.config["initial_credits_value"] = 10  # Default initial credits value
            logger.info(f"Initial credits value set to {self.config['initial_credits_value']}")
        
        # Create directory to store payment records
        os.makedirs("data/payments", exist_ok=True)
        
        # Load existing payments
        self.payments = self._load_payments()
        
        logger.info("PaymentGateway initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.
        
        Returns:
            Dictionary with the configurations or a default dictionary in case of error.
        """
        default_config = {
            "pix": {
                "key": "10689169663",
                "name": "Enio Batista Fernandes Rocha",
                "enabled": True
            },
            "crypto": {
                "btc": {
                    "address": "bc1qy9vr32f2hsjyapt3jz7fen6g0lxrehrqahwj3m",
                    "network": "Bitcoin (Segwit)",
                    "enabled": True
                },
                "sol": {
                    "address": "2iWboZwTkJ5ofCB2wXApa5ReeyJwUFRXrBgHyFRSy6a1",
                    "network": "Solana",
                    "enabled": True
                },
                "eth": {
                    "address": "0xa858F22c8C1f3D5059D101C0c7666Ed0C2BF53ac",
                    "network": "Ethereum (BASE chain)",
                    "enabled": True
                }
            },
            "usage_limits": {
                "free_tier": {
                    "messages_per_day": 20,
                    "api_calls_per_day": 10,
                    "special_calls_per_day": 5,
                    "internet_calls_per_day": 5,
                    "recharge_amount": 5.0  # In reais
                },
                "supporter_tier": {
                    "messages_per_day": 100,
                    "api_calls_per_day": 50,
                    "min_payment": 5.0,  # In reais
                    "special_calls_per_day": 20,
                    "internet_calls_per_day": 20
                },
                "premium_tier": {
                    "messages_per_day": 500,
                    "api_calls_per_day": 250,
                    "min_payment": 20.0,  # In reais
                    "special_calls_per_day": 100,
                    "internet_calls_per_day": 100
                }
            },
            "upgrade_message": "Thank you for considering upgrading your plan! The FREEMIUM system offers access to more features and higher usage limits with payments starting from R$ 5.00.",
            "freemium_enabled": True,
            "pricing": {
                "credits_per_recharge": 10
            },
            "initial_credits_value": 5
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            else:
                # Create default configuration file
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
                logger.info(f"Default configuration file created at {self.config_path}")
                return default_config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return default_config
    
    def _load_payments(self) -> Dict[str, Any]:
        """
        Loads the payment records.
        
        Returns:
            Dictionary with the registered payments.
        """
        payments_path = "data/payments/payments.json"
        default_payments = {
            "users": {},
            "transactions": [],
            "usage_tracking": {}
        }
        
        try:
            if os.path.exists(payments_path):
                with open(payments_path, "r", encoding="utf-8") as f:
                    payments = json.load(f)
                
                # Add credits field if it doesn't exist
                for user_id, user_data in payments.get("users", {}).items():
                    if "credits" not in user_data:
                        user_data["credits"] = {
                            "special_calls": self.config["initial_credits_value"],
                            "internet_calls": self.config["initial_credits_value"],
                            "last_reset": datetime.datetime.now().isoformat()
                        }
                
                # Add usage tracking field if it doesn't exist
                if "usage_tracking" not in payments:
                    payments["usage_tracking"] = {}
                
                logger.info(f"Payments loaded from {payments_path}")
                return payments
            else:
                # Create default payments file
                with open(payments_path, "w", encoding="utf-8") as f:
                    json.dump(default_payments, f, indent=2, ensure_ascii=False)
                logger.info(f"Default payments file created at {payments_path}")
                return default_payments
        except Exception as e:
            logger.error(f"Error loading payments: {e}")
            return default_payments
    
    def _save_payments(self) -> bool:
        """
        Saves the payment records.
        
        Returns:
            True if saved successfully, False otherwise.
        """
        payments_path = "data/payments/payments.json"
        try:
            with open(payments_path, "w", encoding="utf-8") as f:
                json.dump(self.payments, f, indent=2, ensure_ascii=False)
            logger.info(f"Payments saved at {payments_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving payments: {e}")
            return False
    
    def register_payment(self, user_id: int, amount: float, currency: str, 
                        payment_method: str, transaction_id: str = "") -> bool:
        """
        Registers a received payment.
        
        Args:
            user_id: User ID on Telegram.
            amount: Payment amount.
            currency: Currency (BRL, BTC, SOL, ETH).
            payment_method: Payment method (pix, crypto).
            transaction_id: Transaction ID (optional).
            
        Returns:
            True if registered successfully, False otherwise.
        """
        try:
            # Generate transaction ID if not provided
            if not transaction_id:
                transaction_id = hashlib.md5(f"{user_id}_{time.time()}".encode()).hexdigest()
            
            # Create transaction record
            transaction = {
                "id": transaction_id,
                "user_id": user_id,
                "amount": amount,
                "currency": currency,
                "payment_method": payment_method,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "completed"
            }
            
            # Add to transaction list
            self.payments["transactions"].append(transaction)
            
            # Update user record
            if str(user_id) not in self.payments["users"]:
                self.payments["users"][str(user_id)] = {
                    "total_paid": 0.0,
                    "payments_count": 0,
                    "last_payment": None,
                    "tier": "free_tier",
                    "credits": {
                        "special_calls": self.config["initial_credits_value"],
                        "internet_calls": self.config["initial_credits_value"],
                        "last_reset": datetime.datetime.now().isoformat()
                    }
                }
            
            # Update user statistics
            user_data = self.payments["users"][str(user_id)]
            user_data["total_paid"] += amount
            user_data["payments_count"] += 1
            user_data["last_payment"] = datetime.datetime.now().isoformat()
            
            # Update user tier based on total paid
            if user_data["total_paid"] >= self.config["usage_limits"]["premium_tier"]["min_payment"]:
                user_data["tier"] = "premium_tier"
            elif user_data["total_paid"] >= self.config["usage_limits"]["supporter_tier"]["min_payment"]:
                user_data["tier"] = "supporter_tier"
            
            # Add credits based on the amount paid
            credits_to_add = int((amount / self.config["usage_limits"]["free_tier"]["recharge_amount"]) * 
                                self.config["pricing"]["credits_per_recharge"])
            
            if "credits" not in user_data:
                user_data["credits"] = {
                    "special_calls": self.config["initial_credits_value"],
                    "internet_calls": self.config["initial_credits_value"],
                    "last_reset": datetime.datetime.now().isoformat()
                }
            
            user_data["credits"]["special_calls"] += credits_to_add
            user_data["credits"]["internet_calls"] += credits_to_add
            
            # Save changes
            self._save_payments()
            
            logger.info(f"Payment registered: {transaction_id} from {user_id} amounting to {amount} {currency}")
            return True
        except Exception as e:
            logger.error(f"Error registering payment: {e}")
            return False
    
    def get_user_tier(self, user_id: int) -> str:
        """
        Gets the current tier of the user.
        
        Args:
            user_id: User ID on Telegram.
            
        Returns:
            Tier name (free_tier, supporter_tier, premium_tier).
        """
        if str(user_id) not in self.payments["users"]:
            return "free_tier"
        
        return self.payments["users"][str(user_id)]["tier"]
    
    def get_user_limits(self, user_id: int) -> Dict[str, int]:
        """
        Gets the usage limits for the user based on their tier.
        
        Args:
            user_id: User ID on Telegram.
            
        Returns:
            Dictionary with the usage limits.
        """
        tier = self.get_user_tier(user_id)
        return self.config["usage_limits"][tier]
    
    def check_user_usage(self, user_id: int, usage_type: str) -> bool:
        """
        Checks if the user still has available usage for the specified type.
        
        Args:
            user_id: User ID on Telegram.
            usage_type: Type of usage (messages, special_calls, internet_calls).
            
        Returns:
            True if the user still has available usage, False otherwise.
        """
        try:
            # Check if the FREEMIUM system is enabled
            if not self.config.get("freemium_enabled", False):
                return True
            
            # If it's a basic message, check daily limit
            if usage_type == "messages":
                return self._check_daily_message_limit(user_id)
            
            # If it's a special or internet call, check credits
            if usage_type in ["special_calls", "internet_calls"]:
                return self._check_credits(user_id, usage_type)
            
            # For other types, allow
            return True
        except Exception as e:
            logger.error(f"Error checking usage for user {user_id}: {e}")
            # In case of error, allow usage to not block the user
            return True
    
    def _check_daily_message_limit(self, user_id: int) -> bool:
        """
        Checks if the user still has available messages for the day.
        
        Args:
            user_id: User ID on Telegram.
            
        Returns:
            True if the user still has available messages, False otherwise.
        """
        try:
            # Get user's tier and limits
            tier = self.get_user_tier(user_id)
            limits = self.get_user_limits(user_id)
            
            # Get today's message count
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            user_id_str = str(user_id)
            
            if "usage_tracking" not in self.payments:
                self.payments["usage_tracking"] = {}
            
            if user_id_str not in self.payments["usage_tracking"]:
                self.payments["usage_tracking"][user_id_str] = {}
            
            if today not in self.payments["usage_tracking"][user_id_str]:
                self.payments["usage_tracking"][user_id_str][today] = {
                    "messages": 0,
                    "special_calls": 0,
                    "internet_calls": 0
                }
            
            # Check if limit exceeded
            daily_usage = self.payments["usage_tracking"][user_id_str][today]
            if daily_usage["messages"] >= limits["messages_per_day"]:
                return False
            
            # Increment message count
            daily_usage["messages"] += 1
            self._save_payments()
            
            return True
        except Exception as e:
            logger.error(f"Error checking daily message limit for {user_id}: {e}")
            # In case of error, allow usage to not block the user
            return True
    
    def _check_credits(self, user_id: int, credit_type: str) -> bool:
        """
        Checks if the user has available credits for the specified type.
        
        Args:
            user_id: User ID on Telegram.
            credit_type: Type of credit (special_calls, internet_calls).
            
        Returns:
            True if the user has available credits, False otherwise.
        """
        try:
            user_id_str = str(user_id)
            
            # Check if the user exists
            if user_id_str not in self.payments["users"]:
                # Create record for new user
                self.payments["users"][user_id_str] = {
                    "total_paid": 0.0,
                    "payments_count": 0,
                    "last_payment": None,
                    "tier": "free_tier",
                    "credits": {
                        "special_calls": self.config["initial_credits_value"],
                        "internet_calls": self.config["initial_credits_value"],
                        "last_reset": datetime.datetime.now().isoformat()
                    }
                }
                self._save_payments()
            
            # Check if the credits field exists
            if "credits" not in self.payments["users"][user_id_str]:
                self.payments["users"][user_id_str]["credits"] = {
                    "special_calls": self.config["initial_credits_value"],
                    "internet_calls": self.config["initial_credits_value"],
                    "last_reset": datetime.datetime.now().isoformat()
                }
                self._save_payments()
            
            # Check if there are available credits
            credits = self.payments["users"][user_id_str]["credits"]
            if credits[credit_type] <= 0:
                return False
            
            # Decrement credit
            credits[credit_type] -= 1
            
            # Register usage
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            if "usage_tracking" not in self.payments:
                self.payments["usage_tracking"] = {}
            
            if user_id_str not in self.payments["usage_tracking"]:
                self.payments["usage_tracking"][user_id_str] = {}
            
            if today not in self.payments["usage_tracking"][user_id_str]:
                self.payments["usage_tracking"][user_id_str][today] = {
                    "messages": 0,
                    "special_calls": 0,
                    "internet_calls": 0
                }
            
            self.payments["usage_tracking"][user_id_str][today][credit_type] += 1
            self._save_payments()
            
            return True
        except Exception as e:
            logger.error(f"Error checking credits for {user_id}: {e}")
            # In case of error, allow usage to not block the user
            return True
    
    def get_user_credits(self, user_id: int) -> Dict[str, int]:
        """
        Gets the user's available credits.
        
        Args:
            user_id: User ID on Telegram.
            
        Returns:
            Dictionary with the available credits.
        """
        try:
            user_id_str = str(user_id)
            
            # Check if the user exists
            if user_id_str not in self.payments["users"]:
                # Return default credits for new users
                return {
                    "special_calls": self.config.get("initial_credits_value", 10),
                    "internet_calls": self.config.get("initial_credits_value", 10)
                }
            
            # Check if the credits field exists
            if "credits" not in self.payments["users"][user_id_str]:
                self.payments["users"][user_id_str]["credits"] = {
                    "special_calls": self.config.get("initial_credits_value", 10),
                    "internet_calls": self.config.get("initial_credits_value", 10),
                    "last_reset": datetime.datetime.now().isoformat()
                }
                self._save_payments()
            
            # Return available credits
            credits = self.payments["users"][user_id_str]["credits"]
            return {
                "special_calls": credits.get("special_calls", self.config.get("initial_credits_value", 10)),
                "internet_calls": credits.get("internet_calls", self.config.get("initial_credits_value", 10))
            }
        except Exception as e:
            logger.error(f"Error getting credits for user {user_id}: {e}")
            # In case of error, return default credits
            return {
                "special_calls": self.config.get("initial_credits_value", 10),
                "internet_calls": self.config.get("initial_credits_value", 10)
            }
    
    def reset_daily_credits(self, user_id: int) -> bool:
        """
        Resets the user's daily credits.
        
        Args:
            user_id: User ID on Telegram