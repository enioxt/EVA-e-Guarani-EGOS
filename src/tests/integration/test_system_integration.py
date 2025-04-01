"""
EVA & GUARANI - System Integration Test Suite
Version: 1.0
Last Updated: 2025-03-30
"""

import pytest
import asyncio
from typing import Dict
from datetime import datetime

class TestSystemIntegration:
    """Test suite for system-wide integration testing."""
    
    @pytest.mark.asyncio
    async def test_roadmap_update_propagation(self, integrated_system: Dict):
        """Test that roadmap updates properly propagate through the system."""
        roadmap = integrated_system["roadmap"]
        visualizer = integrated_system["visualizer"]
        preservation = integrated_system["preservation"]
        
        # Create a test update
        update = {
            "component": "ATLAS",
            "progress": 0.75,
            "timestamp": datetime.now().isoformat()
        }
        
        # Process the update
        await roadmap.process_updates([update])
        
        # Verify visualization was updated
        viz_state = await visualizer.get_current_view()
        assert viz_state["components"]["ATLAS"]["progress"] == 0.75
        
        # Verify state was preserved
        preserved_state = await preservation.get_latest_state()
        assert preserved_state["components"]["ATLAS"]["progress"] == 0.75
        
    @pytest.mark.asyncio
    async def test_ethical_validation_integration(self, integrated_system: Dict):
        """Test that ethical validation is properly integrated with updates."""
        roadmap = integrated_system["roadmap"]
        validator = integrated_system["validator"]
        
        # Attempt an update with ethical implications
        update = {
            "component": "ETHIK",
            "action": "modify_core_values",
            "changes": ["add_principle: universal_respect"]
        }
        
        # Should trigger ethical validation
        validation_result = await validator.validate_update(update)
        assert validation_result.is_valid
        assert validation_result.ethical_score > 0.8
        
        # Process the update
        await roadmap.process_updates([update])
        
        # Verify the change was logged in metadata
        metadata = integrated_system["metadata"]
        logs = await metadata.get_ethical_validation_logs()
        assert any(log["action"] == "modify_core_values" for log in logs)
        
    @pytest.mark.asyncio
    async def test_modular_analysis_integration(self, integrated_system: Dict):
        """Test that modular analysis is properly integrated."""
        analyzer = integrated_system["analyzer"]
        roadmap = integrated_system["roadmap"]
        
        # Trigger system-wide analysis
        analysis_result = await analyzer.analyze_system_state()
        
        # Verify analysis results are properly integrated
        assert analysis_result.system_health > 0.7
        assert len(analysis_result.component_metrics) > 0
        
        # Verify analysis results are reflected in roadmap
        roadmap_state = await roadmap.get_current_state()
        assert roadmap_state["system_health"] == analysis_result.system_health
        
    @pytest.mark.asyncio
    async def test_concurrent_subsystem_operations(self, integrated_system: Dict):
        """Test system stability during concurrent operations."""
        roadmap = integrated_system["roadmap"]
        visualizer = integrated_system["visualizer"]
        analyzer = integrated_system["analyzer"]
        
        # Create concurrent operations
        tasks = [
            roadmap.process_updates([{"component": "NEXUS", "status": "active"}]),
            visualizer.generate_system_view(),
            analyzer.analyze_component("NEXUS")
        ]
        
        # Execute operations concurrently
        results = await asyncio.gather(*tasks)
        
        # Verify all operations completed successfully
        assert all(result is not None for result in results)
        assert len(results) == 3
        
    @pytest.mark.asyncio
    async def test_system_recovery_integration(self, integrated_system: Dict):
        """Test system's ability to recover from failures."""
        preservation = integrated_system["preservation"]
        roadmap = integrated_system["roadmap"]
        
        # Save current state
        original_state = await roadmap.get_current_state()
        
        # Simulate system crash
        await roadmap.simulate_crash()
        
        # Attempt recovery
        await roadmap.recover_from_crash()
        
        # Verify state was properly restored
        recovered_state = await roadmap.get_current_state()
        assert recovered_state == original_state
        
        # Verify all connections were restored
        assert await roadmap.verify_connections()
        
    @pytest.mark.asyncio
    async def test_performance_metrics_integration(self, integrated_system: Dict):
        """Test system-wide performance metrics collection and analysis."""
        analyzer = integrated_system["analyzer"]
        metadata = integrated_system["metadata"]
        
        # Collect performance metrics
        metrics = await analyzer.collect_performance_metrics()
        
        # Verify metrics are properly stored
        assert metrics["response_times"]["avg"] < 100  # ms
        assert metrics["memory_usage"]["percent"] < 80
        assert metrics["cpu_usage"]["percent"] < 70
        
        # Verify metrics are properly logged
        stored_metrics = await metadata.get_performance_logs()
        assert len(stored_metrics) > 0
        assert stored_metrics[-1]["timestamp"] is not None 