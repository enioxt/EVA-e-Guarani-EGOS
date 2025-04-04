#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - ETHIK Validator
==============================

Real-time ethical validation and monitoring system.
Ensures continuous ethical compliance across all subsystems.

Version: 8.0.0
Ethical Awareness: 0.999
Love: 0.999
"""

import datetime
import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from koios.logger import KoiosLogger
from mycelium import Message, MyceliumClient


@dataclass
class ValidationRule:
    """Defines an ethical validation rule"""

    id: str
    name: str
    description: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    conditions: List[str]
    threshold: float
    action: str  # 'block', 'warn', 'log'
    created: datetime.datetime = field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class ValidationResult:
    """Result of a validation check"""

    rule_id: str
    timestamp: datetime.datetime
    is_valid: bool
    score: float
    details: str
    action_taken: str
    affected_components: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class EthikValidator:
    """Real-time ethical validation system - Adapted for Mycelium"""

    def __init__(
        self, config_path: Optional[Path] = None, mycelium_client: Optional[MyceliumClient] = None
    ):
        """Initialize the validator with configuration and Mycelium client.

        Args:
            config_path (Optional[Path]): Path to configuration file
            mycelium_client (Optional[MyceliumClient]): Mycelium client for messaging
        """
        self.logger = KoiosLogger.get_logger("ETHIK.Validator")
        self.mycelium = mycelium_client

        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize validation rules
        self.rules = self._load_validation_rules()

        # Initialize validation history
        self.validation_history = []
        self.max_history = self.config.get("max_history_size", 1000)

        # Setup Mycelium handlers if client provided
        if self.mycelium:
            self.topics = self.config["mycelium"]["topics"]
            self._setup_mycelium_handlers()

        self.logger.info("EthikValidator initialized")

    def _setup_mycelium_handlers(self):
        """Setup handlers for Mycelium messages."""

        @self.mycelium.subscribe(self.topics["validate_request"])
        async def handle_validation_request(message: Message):
            """Handle incoming validation requests."""
            try:
                self.logger.info(f"Received validation request: {message.id}")

                # Extract validation parameters
                action = message.data["action"]
                context = message.data.get("context", {})
                rules = message.data.get("rules", [])

                # Perform validation
                result = await self.validate_action(action, context, rules)

                # Publish result
                await self.mycelium.publish(
                    self.topics["validate_result"],
                    {
                        "request_id": message.id,
                        "action": action,
                        "valid": result.is_valid,
                        "score": result.score,
                        "details": result.details,
                        "timestamp": datetime.now().isoformat(),
                    },
                )

                # If validation failed, publish alert
                if not result.is_valid and result.severity >= self.config["alert_threshold"]:
                    await self._publish_alert(
                        "validation_failure",
                        f"Action '{action}' failed validation",
                        {
                            "action": action,
                            "score": result.score,
                            "details": result.details,
                            "severity": result.severity,
                        },
                    )

            except Exception as e:
                self.logger.error(f"Error handling validation request: {e}", exc_info=True)
                await self.mycelium.publish(
                    self.topics["validate_result"],
                    {"request_id": message.id, "status": "error", "error": str(e)},
                )

        @self.mycelium.subscribe(self.topics["rules_update"])
        async def handle_rules_update(message: Message):
            """Handle rule update requests."""
            try:
                self.logger.info(f"Received rules update request: {message.id}")

                # Update rules
                new_rules = message.data["rules"]
                self.rules.update(new_rules)

                # Publish confirmation
                await self.mycelium.publish(
                    self.topics["rules_status"],
                    {"request_id": message.id, "status": "success", "rules_count": len(self.rules)},
                )

            except Exception as e:
                self.logger.error(f"Error handling rules update: {e}", exc_info=True)
                await self.mycelium.publish(
                    self.topics["rules_status"],
                    {"request_id": message.id, "status": "error", "error": str(e)},
                )

    async def _publish_alert(self, alert_type: str, message: str, details: Dict[str, Any]):
        """Publish an alert through Mycelium."""
        if not self.mycelium:
            return

        try:
            await self.mycelium.publish(
                self.topics["alert"],
                {
                    "type": alert_type,
                    "message": message,
                    "details": details,
                    "timestamp": datetime.now().isoformat(),
                },
            )
        except Exception as e:
            self.logger.error(f"Failed to publish alert: {e}")

    def _load_config(self, config_path: Optional[Path]) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            "max_history_size": 1000,
            "alert_threshold": 0.7,
            "mycelium": {
                "topics": {
                    "validate_request": "ethik.validate.request",
                    "validate_result": "ethik.validate.result",
                    "rules_update": "ethik.rules.update",
                    "rules_status": "ethik.rules.status",
                    "alert": "ethik.alert",
                }
            },
        }

        if config_path and config_path.exists():
            try:
                with open(config_path) as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    self._deep_merge(default_config, loaded_config)
            except Exception as e:
                self.logger.error(f"Error loading config from {config_path}: {e}. Using defaults.")

        return default_config

    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """Recursively merge update dict into base dict."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def _load_rules(self):
        """Loads validation rules from the configured JSON file using the absolute path."""
        # Get the absolute path from the config (set by EthikService)
        rules_file_abs_path_str = self.config.get("rules_file")

        if not rules_file_abs_path_str:
            self.logger.error(
                "Absolute path for validation rules file not found in configuration."
            )  # Use self.logger
            self.rules.clear()
            return

        rules_path = Path(rules_file_abs_path_str)

        self.logger.info(
            f"Attempting to load validation rules from: {rules_path}"
        )  # Use self.logger
        if rules_path.exists() and rules_path.is_file():
            try:
                with open(rules_path, "r", encoding="utf-8") as f:
                    rules_data = json.load(f)

                self.rules.clear()  # Clear existing rules before loading
                # TODO: Validate rule structure before loading
                for rule_dict in rules_data.get("rules", []):
                    try:
                        # Convert timestamp strings back if needed, or adjust dataclass
                        # rule_dict['created'] = datetime.datetime.fromisoformat(
                        #     rule_dict['created'])
                        # rule_dict['last_updated'] = datetime.datetime.fromisoformat(
                        #     rule_dict['last_updated'])
                        rule = ValidationRule(**rule_dict)
                        self.rules[rule.id] = rule
                    except TypeError as te:
                        self.logger.error(
                            f"Error creating ValidationRule instance for rule ID "
                            f"'{rule_dict.get('id')}': Missing or invalid arguments - {te}",
                            exc_info=True,
                        )
                    except Exception as item_e:
                        self.logger.error(
                            f"Error parsing validation rule item {rule_dict.get('id')}: {item_e}",
                            exc_info=True,
                        )  # Use self.logger
                self.logger.info(
                    f"Loaded {len(self.rules)} validation rules from {rules_path.name}"
                )  # Use self.logger
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON in rules file: {rules_path}")  # Use self.logger
            except Exception as e:
                self.logger.error(
                    f"Error loading validation rules file {rules_path}: {e}", exc_info=True
                )  # Use self.logger
                self.rules.clear()  # Clear rules on error
        else:
            self.logger.warning(
                f"Validation rules file not found: {rules_path}. Validator will have no rules."
            )  # Use self.logger
            self.rules.clear()  # Ensure rules are empty if file not found

    async def start_monitoring(self):
        """Start real-time monitoring via Mycelium."""
        if self.monitoring_active:
            self.logger.warning("Monitoring is already active")  # Use self.logger
            return

        # Connect to Mycelium (Assuming interface instance exists)
        # Connection logic might live in the parent EthikService
        # await self.interface.connect(...)
        self.logger.info(
            "ETHIK Validator monitoring starting (Mycelium connection assumed active)..."
        )  # Use self.logger

        # Subscribe to relevant Mycelium topics
        # Example: Listen for events indicating actions to validate or status changes
        try:
            await self.interface.subscribe("event.*.action_proposed", self.handle_action_proposed)
            await self.interface.subscribe("event.*.status_update", self.handle_status_update)
            # Add other relevant subscriptions
            self.logger.info("Subscribed to relevant Mycelium topics.")  # Use self.logger
        except Exception as e:
            self.logger.error(
                f"Failed to subscribe to Mycelium topics: {e}", exc_info=True
            )  # Use self.logger
            # Decide if this is fatal for monitoring
            return

        self.monitoring_active = True
        # The _monitoring_loop (polling via WS) is likely replaced by event-driven handlers
        # self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        self.logger.info(
            "ETHIK Validator monitoring started (event-driven via Mycelium)."
        )  # Use self.logger

    async def stop_monitoring(self):
        """Stop real-time monitoring and disconnect from Mycelium."""
        if not self.monitoring_active:
            return

        self.logger.info("Stopping ETHIK Validator monitoring...")  # Use self.logger
        self.monitoring_active = False
        # Cancel any active validation tasks if necessary
        for task in self.active_validations.values():
            if task and not task.done():
                task.cancel()
        self.active_validations.clear()

        # Disconnect from Mycelium (Assuming interface instance exists)
        # Disconnection might be handled by parent EthikService
        # await self.interface.disconnect()
        self.logger.info(
            "ETHIK Validator monitoring stopped (Mycelium disconnection assumed handled)."
        )  # Use self.logger

    # Removed _monitoring_loop - replaced by event handlers
    # async def _monitoring_loop(self): ...

    # --- Mycelium Event Handlers (New) --- #
    async def handle_action_proposed(self, message: Dict[str, Any]):
        """Handle events indicating an action needs validation."""
        try:
            self.logger.info(
                f"Processing action proposal: {message.get('id', 'unknown')}"
            )  # Use self.logger

            # Extract action context from message
            payload = message.get("payload", {})
            action_context = {
                "action_type": payload.get("action_type"),
                "source_component": payload.get("source_component", "unknown"),
                "target_path": payload.get("target_path"),
                "timestamp": datetime.datetime.now().isoformat(),
                "message_id": message.get("id"),
                # Add any other relevant context from payload
            }

            # Validate action against all applicable rules
            validation_results = []
            for rule_id, rule in self.rules.items():
                if self._should_apply_rule(rule, action_context):
                    result = self._apply_rule(rule, action_context)
                    validation_results.append(result)
                    self._process_validation_result(result)

                    # If any rule indicates a block, stop processing further rules
                    if result.action_taken == "block":
                        break

            # Determine overall validation status
            is_valid = all(result.is_valid for result in validation_results)
            worst_action = max(
                [r.action_taken for r in validation_results],
                key=lambda x: {"log": 0, "warn": 1, "block": 2}.get(x, 0),
            )
            lowest_score = min([r.score for r in validation_results], default=1.0)

            # Prepare response message
            response = {
                "type": "validation_response",
                "reference_id": message.get("id"),
                "timestamp": datetime.datetime.now().isoformat(),
                "validation": {
                    "is_valid": is_valid,
                    "action": worst_action,
                    "score": lowest_score,
                    "results": [
                        {
                            "rule_id": r.rule_id,
                            "is_valid": r.is_valid,
                            "score": r.score,
                            "action": r.action_taken,
                            "details": r.details,
                        }
                        for r in validation_results
                    ],
                },
            }

            # Publish validation response
            await self.interface.publish(
                topic=f"response.validation.{message.get('id', 'unknown')}", message=response
            )

            # If action is blocked, also publish a block notification
            if worst_action == "block":
                await self.interface.publish(
                    topic="event.ethik.block",
                    message={
                        "reference_id": message.get("id"),
                        "reason": "; ".join(
                            r.details for r in validation_results if r.action_taken == "block"
                        ),
                        "timestamp": datetime.datetime.now().isoformat(),
                    },
                )

            self.logger.info(  # Use self.logger
                f"Action validation complete - ID: {message.get('id', 'unknown')}, "
                f"Valid: {is_valid}, Action: {worst_action}, Score: {lowest_score:.2f}"
            )

        except Exception as e:
            self.logger.error(
                f"Error handling action proposal: {e}", exc_info=True
            )  # Use self.logger
            # Send error response
            try:
                await self.interface.publish(
                    topic=f"response.validation.{message.get('id', 'unknown')}",
                    message={
                        "type": "validation_error",
                        "reference_id": message.get("id"),
                        "timestamp": datetime.datetime.now().isoformat(),
                        "error": str(e),
                    },
                )
            except Exception as pub_e:
                self.logger.error(f"Failed to publish error response: {pub_e}")  # Use self.logger

    async def handle_status_update(self, message: Dict[str, Any]):
        """Handle events about component status changes."""
        try:
            component = message.get("component")
            status = message.get("status", {})

            if not component:
                self.logger.warning(
                    "Received status update without component identifier"
                )  # Use self.logger
                return

            self.logger.debug(
                f"Processing status update for {component}: {status}"
            )  # Use self.logger

            # Update internal component status tracking if needed
            # This could trigger validation if certain status changes are concerning
            if status.get("health") == "critical" or status.get("errors"):
                # Create context for validation
                action_context = {
                    "action_type": "status_change",
                    "source_component": component,
                    "status": status,
                    "timestamp": datetime.datetime.now().isoformat(),
                }

                # Validate status change
                await self.validate_action(action_context, {})  # validate_action uses self.logger

        except Exception as e:
            self.logger.error(
                f"Error handling status update: {e}", exc_info=True
            )  # Use self.logger

    # -------------------------------------- #

    # --- Core Validation Logic (Needs Implementation) --- #
    def _should_apply_rule(self, rule: ValidationRule, context: Dict[str, Any]) -> bool:
        """Determine if a rule should be applied based on context."""
        try:
            # Check if action type matches any conditions
            action_type = context.get("action_type")
            if not action_type:
                return False

            # Check severity threshold from config
            ethical_threshold = self.config.get("validator_config", {}).get(
                "ethical_threshold", 0.7
            )
            if rule.threshold < ethical_threshold:
                return False

            # For critical severity rules, always apply
            if rule.severity == "critical":
                return True

            # For other severities, check context-specific conditions
            if rule.severity == "high":
                # Apply high severity rules if component is critical or action is risky
                return context.get("component_type") == "critical" or action_type in [
                    "file_write",
                    "config_change",
                    "system_update",
                ]

            # For medium/low severity, basic context check
            return bool(action_type and context.get("source_component"))

        except Exception as e:
            self.logger.error(f"Error in _should_apply_rule for {rule.id}: {e}")  # Use self.logger
            # Default to True for safety in case of evaluation error
            return True

    async def validate_action(
        self, action_context: Dict[str, Any], params: Dict[str, Any]
    ) -> ValidationResult:
        """Performs on-demand validation of a specific action."""
        self.logger.info(
            f"Validating action: {action_context.get('action_type')}"
        )  # Use self.logger

        try:
            # Track validation metrics
            start_time = datetime.datetime.now()
            validation_results = []

            # Apply all relevant rules
            for rule_id, rule in self.rules.items():
                if self._should_apply_rule(rule, action_context):
                    result = self._apply_rule(rule, action_context)
                    validation_results.append(result)

                    # Process result
                    self._process_validation_result(result)

                    # If critical rule is violated, stop processing
                    if not result.is_valid and rule.severity == "critical":
                        break

            # Calculate overall validation result
            is_valid = all(r.is_valid for r in validation_results) if validation_results else True
            worst_score = min((r.score for r in validation_results), default=1.0)
            worst_action = max(
                (r.action_taken for r in validation_results),
                key=lambda x: {"log": 0, "warn": 1, "block": 2}.get(x, 0),
                default="log",
            )

            # Combine details from all results
            details = "; ".join(r.details for r in validation_results)

            # Create final result
            final_result = ValidationResult(
                rule_id="validation_summary",
                timestamp=datetime.datetime.now(),
                is_valid=is_valid,
                score=worst_score,
                details=details or "No applicable rules found",
                action_taken=worst_action,
                affected_components=[action_context.get("source_component", "unknown")],
                metadata={
                    "validation_time": (datetime.datetime.now() - start_time).total_seconds(),
                    "rules_applied": len(validation_results),
                    "original_context": action_context,
                    "params": params,
                },
            )

            return final_result

        except Exception as e:
            self.logger.error(f"Error in validate_action: {e}", exc_info=True)  # Use self.logger
            # Return error result
            return ValidationResult(
                rule_id="validation_error",
                timestamp=datetime.datetime.now(),
                is_valid=False,
                score=0.0,
                details=f"Validation error: {str(e)}",
                action_taken="block",  # Default to block on error for safety
                affected_components=[action_context.get("source_component", "unknown")],
            )

    def _apply_rule(self, rule: ValidationRule, action_context: Dict[str, Any]) -> ValidationResult:
        """Apply a validation rule to a given action context."""
        timestamp = datetime.datetime.now()
        is_valid = True
        all_conditions_met = True
        details = f"Rule '{rule.name}' evaluated."
        score = 1.0  # Default score, assuming valid
        action_taken = "log"  # Default action

        try:
            # Evaluate all conditions defined in the rule
            # We provide the action_context dictionary to the eval environment
            # Restrict builtins for safety
            allowed_builtins = {
                "any": any,
                "all": all,
                "str": str,
                "int": int,
                "float": float,
                "list": list,
                "dict": dict,
                "set": set,
                "len": len,
                "in": lambda x, y: x in y,
                "True": True,
                "False": False,
                "None": None,
            }
            eval_globals = {"__builtins__": allowed_builtins, "action_context": action_context}

            for condition_str in rule.conditions:
                if not eval(condition_str, eval_globals):
                    all_conditions_met = False
                    break  # If one condition fails, the rule's premise might not apply

            # If all conditions evaluated to True, it means the rule's criteria are met.
            # For this type of rule (checking for forbidden actions),
            # meeting conditions means a violation.
            if all_conditions_met:
                is_valid = False  # Conditions met means violation for this rule type
                score = 0.0  # Score indicates violation
                action_taken = rule.action
                details = (
                    f"Rule '{rule.name}' violated. Conditions met: {rule.conditions}. "
                    f"Context: {action_context}"
                )

                # Log based on configured action
                if action_taken == "block":
                    self.logger.critical(
                        f"ETHICAL VIOLATION (BLOCK): Rule={rule.id}, Context={action_context}"
                    )
                elif action_taken == "warn":
                    self.logger.warning(
                        f"ETHICAL WARNING: Rule={rule.id}, Context={action_context}"
                    )
            else:
                # Conditions not met, rule doesn't trigger a violation
                details = f"Rule '{rule.name}' conditions not met. Context: {action_context}"

        except Exception as e:
            self.logger.error(
                f"Error evaluating rule {rule.id} conditions: {e}. Context: {action_context}",
                exc_info=True,
            )  # Use self.logger
            # Treat evaluation errors as potentially unsafe - perhaps default to warning?
            is_valid = False  # Be cautious
            score = 0.1  # Low score indicates error/uncertainty
            action_taken = "warn"  # Default to warning on error
            details = f"Error evaluating rule {rule.id}: {e}"

        # Log the outcome
        self.logger.debug(
            f"Validation result for rule '{rule.id}': IsValid={is_valid}, "
            f"Score={score:.2f}, Action={action_taken}, Details: {details}",
        )

        return ValidationResult(
            rule_id=rule.id,
            timestamp=timestamp,
            is_valid=is_valid,
            score=score,
            details=details,
            action_taken=action_taken,
            affected_components=[action_context.get("source_component", "unknown")],  # Example
        )

    async def _send_alert(self, result: ValidationResult):
        """Sends an alert via Mycelium if validation fails critically."""
        if not self.mycelium:
            return

        # Determine severity based on rule
        severity_level = result.metadata.get(
            "rule_severity", "medium"
        )  # Assume severity passed in metadata

        alert_config = self.config.get("alerting", {"level": "warning"})  # Default alert level
        should_alert = False
        if alert_config.get("level") == "critical" and severity_level == "critical":
            should_alert = True
        elif alert_config.get("level") == "high" and severity_level in ["critical", "high"]:
            should_alert = True
        elif alert_config.get("level") == "medium" and severity_level in [
            "critical",
            "high",
            "medium",
        ]:
            should_alert = True
        elif alert_config.get("level") == "low":  # Alert on everything if set to low
            should_alert = True

        if not result.is_valid and should_alert:
            try:
                await self.mycelium.publish(
                    topic=self.topics.get("alert", "ethik.alert"),  # Use configured topic
                    message={
                        "type": "validation_failure",
                        "rule_id": result.rule_id,
                        "timestamp": result.timestamp.isoformat(),
                        "details": result.details,
                        "score": result.score,
                        "severity": severity_level,  # Include severity
                        "affected_components": result.affected_components,
                    },
                )
                self.logger.info(f"Published validation failure alert for rule {result.rule_id}")
            except Exception as e:
                self.logger.error(
                    f"Failed to publish validation alert for rule {result.rule_id}: {e}"
                )

    def _process_validation_result(self, result: ValidationResult):
        """Processes a validation result, updating history and potentially triggering actions."""
        # Add to history
        self.validation_history.append(result)

        # Clean history if needed
        if len(self.validation_history) > self.max_history:
            self.validation_history.pop(0)

        # Log the result
        log_level = logging.INFO if result.is_valid else logging.WARNING
        self.logger.log(
            log_level,
            f"Validation Result for Rule '{result.rule_id}': "
            f"Valid={result.is_valid}, Score={result.score:.2f}, "
            f"Action={result.action_taken}, Details: {result.details}",
        )

        # --- Placeholder for triggering actions based on result.action_taken ---
        # if result.action_taken == 'block':
        #     self.logger.critical(f"BLOCK action triggered by rule {result.rule_id}")
        #     # Raise an exception or signal to block the operation?
        #     # This needs careful design based on how ETHIK integrates
        #     # raise EthicalViolationError(
        #     #     f"Action blocked by rule {result.rule_id}: "
        #     #     f"{result.details}")
        # elif result.action_taken == 'warn':
        #     self.logger.warning(
        #         f"WARN action triggered by rule {result.rule_id}: "
        #         f"{result.details}")
        #     # Potentially send a specific warning message via Mycelium?
        # ---------------------------------------------------------------------

        # --- Trigger Alert (moved to separate async function) ---
        # await self._send_alert(result) # Cannot call async from sync - needs rethink
        # Alerting might need to happen in the calling async context (e.g., handle_action_proposed)
        # or use asyncio.create_task if appropriate and safe.
        # For now, alerting is handled after validate_action call.
        # ----------------------------------------------------

        return result

    def add_rule(self, rule_dict: Dict[str, Any]):
        """Add or update a validation rule dynamically."""
        try:
            # Basic validation of rule_dict structure
            required_keys = [
                "id",
                "name",
                "description",
                "severity",
                "conditions",
                "threshold",
                "action",
            ]
            if not all(key in rule_dict for key in required_keys):
                raise ValueError(f"Rule dictionary missing required keys: {required_keys}")

            # Create ValidationRule instance
            rule_args = {k: v for k, v in rule_dict.items() if k not in ["created", "last_updated"]}
            rule = ValidationRule(**rule_args)
            rule.last_updated = datetime.datetime.now()  # Update timestamp

            self.rules[rule.id] = rule
            self.logger.info(f"Added/Updated validation rule: {rule.name} [{rule.id}]")
        except Exception as e:
            self.logger.error(
                f"Error adding/updating rule {rule_dict.get('id')}: {e}", exc_info=True
            )

    def get_validation_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent validation history."""
        return self.validation_history[-limit:]

    def get_component_health(self, component: str) -> Dict[str, Any]:
        """Assess the ethical health of a specific component based on history."""
        relevant_results = [
            r for r in self.validation_history if component in r.affected_components
        ]

        if not relevant_results:
            return {"status": "unknown", "message": "No validation history for component."}

        # Simple health calculation: ratio of valid results
        valid_count = sum(1 for r in relevant_results if r.is_valid)
        total_count = len(relevant_results)
        health_score = valid_count / total_count if total_count > 0 else 1.0

        status = (
            "healthy" if health_score >= 0.9 else ("warning" if health_score >= 0.7 else "critical")
        )

        return {
            "component": component,
            "status": status,
            "score": health_score,
            "valid_checks": valid_count,
            "total_checks": total_count,
            "recent_failures": [asdict(r) for r in relevant_results if not r.is_valid][
                -5:
            ],  # Last 5 failures
        }

    def remove_rule(self, rule_id: str):
        """Remove a validation rule dynamically."""
        if rule_id in self.rules:
            removed_rule_name = self.rules[rule_id].name
            del self.rules[rule_id]
            self.logger.info(f"Removed validation rule: {removed_rule_name} [{rule_id}]")
        else:
            self.logger.warning(f"Attempted to remove non-existent rule: {rule_id}")
