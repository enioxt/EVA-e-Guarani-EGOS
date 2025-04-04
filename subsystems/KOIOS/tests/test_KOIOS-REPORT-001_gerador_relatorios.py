#!/usr/bin/env python3
"""
EVA & GUARANI EGOS - KOIOS Report Generator Tests
Version: 1.0.0
Last Updated: 2025-04-01
"""

import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ..core.KOIOS_REPORT_001_gerador_relatorios import ReportContext, ReportGenerator


# Test data
@pytest.fixture
def config():
    return {
        "integration": {
            "ci_cd": {
                "report_location": "/tmp/reports",
                "reporting": {"export_formats": ["markdown", "html", "json"]},
                "notifications": {
                    "slack": {
                        "enabled": True,
                        "channel": "#koios-validation",
                        "username": "KOIOS Validator",
                        "icon_emoji": ":robot_face:",
                        "templates": {
                            "success": "Validation passed with {warning_count} warnings",
                            "failure": "Validation failed with {error_count} errors",
                        },
                    },
                    "email": {
                        "enabled": True,
                        "smtp_server": "smtp.evaguarani.ai",
                        "from_address": "koios@evaguarani.ai",
                        "to_addresses": ["team@evaguarani.ai"],
                        "subject_prefix": "[KOIOS]",
                        "templates": {
                            "subject": "{prefix} Validation {status}: {error_count} errors, {warning_count} warnings"
                        },
                    },
                },
                "metrics": {
                    "statsd": {
                        "enabled": True,
                        "host": "localhost",
                        "port": 8125,
                        "prefix": "koios",
                    }
                },
            }
        }
    }


@pytest.fixture
def validation_results():
    return {
        "stats": {"files_analyzed": 100, "violations": {"error": 2, "warning": 5}},
        "violations": {
            "errors": [
                {"file": "file1.py", "message": "Invalid naming pattern"},
                {"file": "file2.py", "message": "Missing prefix"},
            ],
            "warnings": [
                {"file": "file3.py", "message": "Consider renaming"},
                {"file": "file4.py", "message": "Directory structure"},
                {"file": "file5.py", "message": "File organization"},
                {"file": "file6.py", "message": "Documentation format"},
                {"file": "file7.py", "message": "Code style"},
            ],
        },
    }


@pytest.fixture
def report_generator(config):
    return ReportGenerator(config)


@pytest.mark.asyncio
async def test_initialize(report_generator):
    """Test initialization of async clients."""
    with patch.dict(os.environ, {"SLACK_TOKEN": "test-token"}):
        await report_generator.initialize()
        assert report_generator.slack_client is not None
        assert report_generator.smtp_client is not None


@pytest.mark.asyncio
async def test_cleanup(report_generator):
    """Test cleanup of async clients."""
    report_generator.smtp_client = AsyncMock()
    await report_generator.cleanup()
    report_generator.smtp_client.quit.assert_called_once()


def test_prepare_context(report_generator, validation_results):
    """Test preparation of report context."""
    context = report_generator.prepare_context(validation_results)
    assert isinstance(context, ReportContext)
    assert context.stats == validation_results["stats"]
    assert context.violations == validation_results["violations"]
    assert len(context.summary["aspects"]) == 2
    assert context.quality_metrics["compliance_index"] == 93.0


def test_generate_summary(report_generator, validation_results):
    """Test summary generation from validation results."""
    summary = report_generator._generate_summary(validation_results)
    assert "Correção de erros de nomenclatura" in summary["aspects"]
    assert "Revisão de avisos de estrutura" in summary["aspects"]


def test_calculate_metrics(report_generator, validation_results):
    """Test calculation of quality metrics."""
    metrics = report_generator._calculate_metrics(validation_results)
    assert metrics["compliance_index"] == 93.0
    assert metrics["trend"]["value"] == "+2.3"
    assert metrics["complexity"] == "Baixa"
    assert metrics["maintainability"] == "Alta"


def test_generate_notes(report_generator, validation_results):
    """Test generation of additional notes."""
    notes = report_generator._generate_notes(validation_results)
    assert len(notes) == 3
    assert "A maioria das violações está concentrada em código novo" in notes
    assert "Melhorias significativas desde a última execução" in notes
    assert "Recomenda-se revisão do código antes do merge" in notes


@pytest.mark.asyncio
async def test_generate_reports(report_generator, validation_results, tmp_path):
    """Test generation of all report formats."""
    report_generator.artifacts_dir = tmp_path
    report_generator.templates_dir = Path(__file__).parent.parent / "templates"

    with patch("jinja2.Environment") as mock_env:
        mock_template = MagicMock()
        mock_template.render.return_value = "Test content"
        mock_env.return_value.get_template.return_value = mock_template

        reports = await report_generator.generate_reports(validation_results)

        assert "markdown" in reports
        assert "html" in reports
        assert "json" in reports
        assert reports["markdown"].exists()
        assert reports["html"].exists()
        assert reports["json"].exists()


@pytest.mark.asyncio
async def test_generate_markdown(report_generator, tmp_path):
    """Test generation of Markdown report."""
    report_generator.artifacts_dir = tmp_path
    context = MagicMock()

    with patch("jinja2.Environment") as mock_env:
        mock_template = MagicMock()
        mock_template.render.return_value = "# Test Report"
        mock_env.return_value.get_template.return_value = mock_template

        report_file = await report_generator.generate_markdown(context)
        assert report_file.exists()
        assert report_file.read_text() == "# Test Report"


@pytest.mark.asyncio
async def test_generate_html(report_generator, tmp_path):
    """Test generation of HTML report."""
    report_generator.artifacts_dir = tmp_path
    context = MagicMock()

    with patch("jinja2.Environment") as mock_env:
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_env.return_value.get_template.return_value = mock_template

        report_file = await report_generator.generate_html(context)
        assert report_file.exists()
        assert report_file.read_text() == "<html>Test</html>"


@pytest.mark.asyncio
async def test_generate_json(report_generator, validation_results, tmp_path):
    """Test generation of JSON report."""
    report_generator.artifacts_dir = tmp_path
    report_file = await report_generator.generate_json(validation_results)
    assert report_file.exists()
    with open(report_file) as f:
        data = json.load(f)
    assert data == validation_results


@pytest.mark.asyncio
async def test_send_slack_notification(report_generator):
    """Test sending Slack notification."""
    report_generator.slack_client = AsyncMock()
    context = MagicMock()
    context.stats = {"violations": {"error": 2, "warning": 5}}

    await report_generator.send_slack_notification(context)
    report_generator.slack_client.chat_postMessage.assert_called_once()


@pytest.mark.asyncio
async def test_send_email_notification(report_generator):
    """Test sending email notification."""
    report_generator.smtp_client = AsyncMock()
    context = MagicMock()
    context.stats = {"violations": {"error": 2, "warning": 5}}

    with patch("jinja2.Environment") as mock_env:
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Test</html>"
        mock_env.return_value.get_template.return_value = mock_template

        await report_generator.send_email_notification(context)
        report_generator.smtp_client.send_message.assert_called_once()


def test_update_metrics(report_generator):
    """Test updating metrics."""
    context = MagicMock()
    context.stats = {"violations": {"error": 2, "warning": 5}}
    report_generator.statsd = MagicMock()

    report_generator._update_metrics(context)
    report_generator.statsd.gauge.assert_called()
    report_generator.statsd.incr.assert_called_with("reports.generated")


# ✧༺❀༻∞ EVA & GUARANI ∞༺❀༻✧
