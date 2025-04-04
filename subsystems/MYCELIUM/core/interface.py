# subsystems/MYCELIUM/core/interface.py

"""Defines the MyceliumInterface class for subsystems to interact with the network."""

import asyncio
import logging
from datetime import datetime  # Added missing import
from typing import Any, Callable, Coroutine, Dict, List, Optional

from .network import MyceliumNetwork

# Forward declaration for type hinting
# from .network import MyceliumNetwork

logger = logging.getLogger(__name__)


class MyceliumInterface:
    """Interface for subsystems to interact with the Mycelium Network (Asyncio implementation)."""

    def __init__(self, network_instance: "MyceliumNetwork", node_id: str):
        if network_instance is None:
            # This should be handled by the system initializing the interface (e.g., BIOS-Q)
            raise ValueError("Network instance cannot be None")
        self.network = network_instance
        self.node_id = node_id
        # Dictionary to store Futures waiting for responses, keyed by correlation_id
        self._response_waiters: Dict[str, asyncio.Future] = {}
        logger.debug(f"MyceliumInterface initialized for node: {self.node_id}")

    async def connect(self, node_type: str, version: str, capabilities: List[str]) -> bool:
        """Registers the subsystem node with the network."""
        logger.info(f"Node {self.node_id} connecting to Mycelium Network...")
        # Called by the subsystem during its initialization
        success = await self.network.register_node(self.node_id, node_type, version, capabilities)
        if success:
            # Register handler for incoming responses directed to this node
            await self.network.register_response_handler(self.node_id, self._handle_response)
        return success

    async def disconnect(self) -> bool:
        """Deregisters the subsystem node."""
        logger.info(f"Node {self.node_id} disconnecting from Mycelium Network...")
        # Called during subsystem shutdown
        # Cancel any pending response futures
        for future in list(self._response_waiters.values()):  # Iterate over a copy
            if not future.done():
                future.cancel("Node disconnecting")  # Use cancel with message

        # Remove response handler
        await self.network.remove_response_handler(self.node_id)
        # Remove node from network
        success = await self.network.remove_node(self.node_id)
        self.node_id = None  # Clear node id after disconnection
        return success

    async def send_request(
        self, target_node: str, topic: str, payload: Dict[str, Any], timeout: int = 10
    ) -> Dict[str, Any]:
        """Sends a request and waits for a response.

        Args:
            target_node: The ID of the target node.
            topic: The specific request topic (e.g., 'request.nexus.analyze_module').
            payload: The data for the request.
            timeout: Maximum seconds to wait for a response.

        Returns:
            The payload of the response message.

        Raises:
            asyncio.TimeoutError: If no response is received within the timeout.
            ConnectionAbortedError: If the node disconnects while waiting.
            Exception: If the response payload indicates an error status or other processing error.
        """
        if not self.node_id:
            raise ConnectionAbortedError("Cannot send request, node is disconnected.")

        correlation_id = self.network.generate_uuid()  # Network should provide UUID generation
        future = asyncio.Future()
        self._response_waiters[correlation_id] = future

        message = {
            "header": {
                "message_id": self.network.generate_uuid(),
                "correlation_id": correlation_id,
                "timestamp": datetime.now().isoformat(),
                "sender_node": self.node_id,
                "target_node": target_node,
                "topic": topic,
                "message_type": "REQUEST",
                "priority": "MEDIUM",
                "version": "1.0",
            },
            "payload": payload,
        }

        logger.debug(
            f"[{self.node_id}] Sending request {correlation_id} to {target_node} on topic {topic}"
        )
        await self.network.route_message(message)  # Network handles routing via asyncio

        try:
            # Wait for the future to be set by _handle_response
            response_payload = await asyncio.wait_for(future, timeout=timeout)
            logger.debug(f"[{self.node_id}] Received response for {correlation_id}")
            if isinstance(response_payload, Exception):  # Check if an exception was set
                raise response_payload
            if response_payload.get("status") == "ERROR":
                # Raise a specific exception type if possible
                raise Exception(
                    f"Error response from {target_node}: "
                    f"{response_payload.get('error_message', 'Unknown error')}"
                )
            return response_payload
        except asyncio.CancelledError:
            logger.warning(f"[{self.node_id}] Request {correlation_id} cancelled.")
            # Reraise CancelledError if needed, or handle as ConnectionAbortedError
            raise ConnectionAbortedError(
                f"Request {correlation_id} cancelled due to node disconnection."
            )
        except asyncio.TimeoutError:
            logger.error(
                f"[{self.node_id}] Timeout waiting for response {correlation_id} "
                f"from {target_node} on topic {topic}"
            )
            raise  # Reraise TimeoutError
        finally:
            # Clean up future if it still exists (might be removed by disconnect)
            self._response_waiters.pop(correlation_id, None)

    async def _handle_response(self, message: Dict[str, Any]):
        """Internal method called by the network to resolve a response future."""
        correlation_id = message["header"]["correlation_id"]
        if correlation_id in self._response_waiters:
            future = self._response_waiters.pop(
                correlation_id
            )  # Remove here to prevent setting twice
            if not future.done():
                logger.debug(f"[{self.node_id}] Handling response for {correlation_id}")
                # Check for errors in the response payload before setting result
                payload = message["payload"]
                # We set the payload directly; the waiting task will check the status
                future.set_result(payload)
            else:
                logger.warning(
                    f"[{self.node_id}] Future for correlation_id {correlation_id} was already done."
                )
        else:
            logger.warning(
                f"[{self.node_id}] Received response for unknown/timed-out/cancelled "
                f"correlation_id: {correlation_id}"
            )

    async def publish_event(self, topic: str, payload: Dict[str, Any]):
        """Publishes an event to a topic."""
        if not self.node_id:
            raise ConnectionAbortedError("Cannot publish event, node is disconnected.")

        message = {
            "header": {
                "message_id": self.network.generate_uuid(),
                "correlation_id": None,
                "timestamp": datetime.now().isoformat(),
                "sender_node": self.node_id,
                "target_node": "TOPIC_TARGET",  # Indicate topic-based routing
                "topic": topic,
                "message_type": "EVENT",
                "priority": "MEDIUM",
                "version": "1.0",
            },
            "payload": payload,
        }
        logger.debug(f"[{self.node_id}] Publishing event to topic {topic}")
        await self.network.route_message(message)  # Network distributes to subscribers

    async def subscribe(self, topic: str, callback_function: Callable[[Dict[str, Any]], Coroutine]):
        """Subscribes to a topic, providing an async callback function.
        The callback will receive the full message dictionary.
        """
        if not self.node_id:
            raise ConnectionAbortedError("Cannot subscribe, node is disconnected.")
        # Network stores subscription: topic -> list[(node_id, callback)]
        logger.info(f"[{self.node_id}] Subscribing to topic: {topic}")
        await self.network.add_subscription(topic, self.node_id, callback_function)

    async def report_health(self, status: str, details: Optional[Dict[str, Any]] = None):
        """Reports the node's health status to the network."""
        if not self.node_id:
            # Maybe just log a warning instead of raising an error?
            logger.warning("Cannot report health, node is disconnected.")
            return

        payload = {"node_id": self.node_id, "status": status, "details": details or {}}
        logger.debug(f"[{self.node_id}] Reporting health: {status}")
        await self.publish_event(topic="event.mycelium.health_report", payload=payload)

    # TODO: Add methods for register_file, get_network_status, get_node_status if needed
    # These might be better suited for a dedicated admin/KOIOS interface

    async def register_file(
        self, file_path: str, file_type: str, connections: Dict[str, Any], version: str
    ) -> Dict[str, Any]:
        """Register a file in the network with its connections."""
        return {
            "file_path": file_path,
            "file_type": file_type,
            "connections": connections,
            "version": version,
        }
