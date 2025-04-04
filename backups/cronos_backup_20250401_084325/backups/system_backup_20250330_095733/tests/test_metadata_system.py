import unittest
import pytest
from unittest.mock import Mock, patch
import os
import tempfile
import json
import time
from datetime import datetime, timedelta

from core.metadata.scanner import MetadataScanner
from core.metadata.tracker import UsageTracker
from core.metadata.organizer import FileOrganizer
from core.metadata.collector import DataCollector


class TestMetadataScanner(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.scanner = MetadataScanner()

        # Create test files
        self.test_files = {
            "test1.py": "import os\nimport sys\n",
            "test2.js": 'import React from "react";\n',
            "test3.ts": 'import { Component } from "@angular/core";\n',
        }

        for name, content in self.test_files.items():
            with open(os.path.join(self.temp_dir, name), "w") as f:
                f.write(content)

    def tearDown(self):
        for name in self.test_files:
            try:
                os.remove(os.path.join(self.temp_dir, name))
            except:
                pass
        os.rmdir(self.temp_dir)

    def test_scan_system(self):
        """Test system scanning functionality."""
        self.scanner.scan_system(self.temp_dir)
        self.assertEqual(len(self.scanner.metadata_db), len(self.test_files))

        for filepath in self.test_files:
            full_path = os.path.join(self.temp_dir, filepath)
            self.assertIn(full_path, self.scanner.metadata_db)

    def test_extract_imports(self):
        """Test import extraction from different file types."""
        python_imports = self.scanner._extract_imports(os.path.join(self.temp_dir, "test1.py"))
        js_imports = self.scanner._extract_imports(os.path.join(self.temp_dir, "test2.js"))
        ts_imports = self.scanner._extract_imports(os.path.join(self.temp_dir, "test3.ts"))

        self.assertIn("os", python_imports)
        self.assertIn("sys", python_imports)
        self.assertIn("react", js_imports)
        self.assertIn("@angular/core", ts_imports)

    def test_detect_subsystem(self):
        """Test subsystem detection."""
        test_paths = {
            "/core/metadata/test.py": "core",
            "/web/components/test.tsx": "web",
            "/QUANTUM_PROMPTS/test.md": "quantum_prompts",
            "/ETHIK/test.js": "ethik",
        }

        for path, expected in test_paths.items():
            detected = self.scanner._detect_subsystem(path)
            self.assertEqual(detected, expected)

    @pytest.mark.benchmark
    def test_scan_performance(self, benchmark):
        """Test scanning performance."""

        def scan():
            scanner = MetadataScanner()
            scanner.scan_system(self.temp_dir)

        # Should complete within 1 second for test directory
        result = benchmark(scan)
        assert result.seconds < 1.0


class TestUsageTracker(unittest.TestCase):
    def setUp(self):
        self.scanner = MetadataScanner()
        self.tracker = UsageTracker(self.scanner)

    def test_record_access(self):
        """Test file access recording."""
        test_file = "/test/file.py"
        self.tracker._record_access(test_file, "accessed")

        history = self.tracker.get_file_usage_history(test_file)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["type"], "accessed")

    def test_dependency_tracking(self):
        """Test dependency tracking."""
        test_file = "/test/file.py"
        test_deps = {"os", "sys"}

        self.tracker._update_file_dependencies(test_file, test_deps)
        cached_deps = self.tracker.dependency_cache.get(test_file, set())

        self.assertEqual(cached_deps, test_deps)

    @pytest.mark.benchmark
    def test_tracking_performance(self, benchmark):
        """Test tracking performance."""

        def track():
            for i in range(100):
                self.tracker._record_access(f"/test/file{i}.py", "accessed")

        # Should handle 100 events within 0.1 seconds
        result = benchmark(track)
        assert result.seconds < 0.1


class TestFileOrganizer(unittest.TestCase):
    def setUp(self):
        self.scanner = MetadataScanner()
        self.organizer = FileOrganizer(self.scanner)
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.temp_dir)

    def test_suggest_location(self):
        """Test location suggestion."""
        test_cases = {
            "/random/test.py": "/core/test.py",
            "/misc/component.tsx": "/web/components/component.tsx",
            "/docs/quantum.md": "/QUANTUM_PROMPTS/quantum.md",
        }

        for current, expected in test_cases.items():
            suggested = self.organizer._get_suggested_location(current)
            self.assertEqual(suggested, expected)

    def test_move_history(self):
        """Test move history tracking."""
        source = "/test/source.py"
        dest = "/core/dest.py"

        self.organizer._execute_moves({source: dest})
        history = self.organizer.move_history

        self.assertIn(source, history)
        self.assertEqual(history[source][-1]["destination"], dest)

    @pytest.mark.benchmark
    def test_organization_performance(self, benchmark):
        """Test organization performance."""

        def organize():
            self.organizer.organize_files(dry_run=True)

        # Should complete organization analysis within 0.5 seconds
        result = benchmark(organize)
        assert result.seconds < 0.5


class TestDataCollector(unittest.TestCase):
    def setUp(self):
        self.scanner = MetadataScanner()
        self.tracker = UsageTracker(self.scanner)
        self.organizer = FileOrganizer(self.scanner)
        self.collector = DataCollector(self.scanner, self.tracker, self.organizer)

    def test_collection_stats(self):
        """Test statistics collection."""
        stats = self.collector.get_collection_stats()

        required_metrics = {
            "total_files",
            "active_files",
            "subsystem_distribution",
            "dependency_count",
            "quantum_metrics",
        }

        self.assertTrue(all(metric in stats for metric in required_metrics))

    def test_real_time_updates(self):
        """Test real-time update generation."""
        updates = []

        def mock_callback(data):
            updates.append(data)

        self.collector.subscribe_updates(mock_callback)
        time.sleep(2)  # Wait for 2 updates

        self.assertGreaterEqual(len(updates), 2)
        self.assertNotEqual(updates[0], updates[1])  # Updates should be different

    @pytest.mark.benchmark
    def test_collector_performance(self, benchmark):
        """Test collector performance."""

        def collect():
            return self.collector.get_collection_stats()

        # Should generate stats within 0.1 seconds
        result = benchmark(collect)
        assert result.seconds < 0.1


if __name__ == "__main__":
    unittest.main()
