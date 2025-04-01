#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - Flask API for the Sandbox Environment
"""

import os
import sys
import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Flask configuration
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Allow cross-origin requests (CORS)
CORS(app)

# Path configuration to import core modules, if available
try:
    # Add project root directory to PYTHONPATH
    project_root = Path(__file__).resolve().parent.parent.parent.parent
    core_dir = project_root / "core"
    
    if core_dir.exists():
        sys.path.insert(0, str(project_root))
        
        # Try to import core modules
        # Define variables to avoid linter errors
        atlas_core = None
        nexus_core = None  # type: ignore
        cronos_core = None  # type: ignore
        ethik_core = None
        
        # Try to import each module separately
        try:
            from core.atlas import atlas_core
        except ImportError:
            pass
            
        try:
            from core.nexus import nexus_core  # type: ignore
        except ImportError:
            pass
            
        try:
            from core.cronos import cronos_core  # type: ignore
        except ImportError:
            pass
            
        try:
            from core.ethik import ethik_core
        except ImportError:
            pass
        
        # Check if any module was successfully imported
        MODULES_AVAILABLE = any([atlas_core, nexus_core, cronos_core, ethik_core])
        if MODULES_AVAILABLE:
            print("✓ EVA & GUARANI modules successfully imported")
        else:
            print("✗ Modules not found in core directory")
    else:
        MODULES_AVAILABLE = False
        print("✗ Core directory not found")
except Exception as e:
    MODULES_AVAILABLE = False
    print(f"✗ Error importing modules: {e}")

# Sample data when modules are not available
SAMPLE_DATA = {
    "atlas": {
        "name": "ATLAS",
        "description": "Systemic Cartography Module",
        "maps": [
            {"id": 1, "name": "Knowledge Map", "nodes": 42, "connections": 120},
            {"id": 2, "name": "Concept Map", "nodes": 18, "connections": 36}
        ]
    },
    "nexus": {
        "name": "NEXUS",
        "description": "Modular Analysis Module",
        "components": [
            {"id": 1, "name": "Code Analyzer", "quality": 0.92},
            {"id": 2, "name": "Pattern Detector", "quality": 0.89},
            {"id": 3, "name": "Module Connector", "quality": 0.95}
        ]
    },
    "cronos": {
        "name": "CRONOS",
        "description": "Evolutionary Preservation Module",
        "backups": [
            {"id": 1, "timestamp": "2023-09-15T14:30:00", "integrity": 0.99},
            {"id": 2, "timestamp": "2023-10-20T09:45:00", "integrity": 0.98}
        ]
    },
    "ethik": {
        "name": "ETHIK",
        "description": "Ethical Integration Module",
        "principles": [
            "Universal possibility of redemption",
            "Compassionate temporality",
            "Sacred privacy",
            "Universal accessibility",
            "Unconditional love"
        ]
    }
}

# Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    # Path to the frontend directory
    frontend_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "html_basic"
    return send_from_directory(directory=str(frontend_dir), path="index.html")

@app.route('/api/status')
def status():
    """Return API status and module availability"""
    return jsonify({
        "status": "online",
        "version": "1.0.0-sandbox",
        "modules": {
            "atlas": MODULES_AVAILABLE and atlas_core is not None,
            "nexus": MODULES_AVAILABLE and nexus_core is not None,
            "cronos": MODULES_AVAILABLE and cronos_core is not None,
            "ethik": MODULES_AVAILABLE and ethik_core is not None
        }
    })

@app.route('/api/atlas')
def atlas():
    """Returns data from the ATLAS module"""
    if MODULES_AVAILABLE and atlas_core:
        try:
            # In a real implementation, would call atlas_core here
            # return jsonify(atlas_core.get_maps())
            pass
        except Exception as e:
            return jsonify({"error": f"Error calling ATLAS module: {str(e)}"}), 500
    
    # Return sample data
    return jsonify(SAMPLE_DATA["atlas"])

@app.route('/api/nexus')
def nexus():
    """Returns data from the NEXUS module"""
    if MODULES_AVAILABLE and nexus_core:
        try:
            # In a real implementation, would call nexus_core here
            # return jsonify(nexus_core.get_components())
            pass
        except Exception as e:
            return jsonify({"error": f"Error calling NEXUS module: {str(e)}"}), 500
    
    # Return sample data
    return jsonify(SAMPLE_DATA["nexus"])

@app.route('/api/cronos')
def cronos():
    """Returns data from the CRONOS module"""
    if MODULES_AVAILABLE and cronos_core:
        try:
            # In a real implementation, would call cronos_core here
            # return jsonify(cronos_core.get_backups())
            pass
        except Exception as e:
            return jsonify({"error": f"Error calling CRONOS module: {str(e)}"}), 500
    
    # Return sample data
    return jsonify(SAMPLE_DATA["cronos"])

@app.route('/api/ethik')
def ethik():
    """Returns data from the ETHIK module"""
    if MODULES_AVAILABLE and ethik_core:
        try:
            # In a real implementation, would call ethik_core here
            # return jsonify(ethik_core.get_principles())
            pass
        except Exception as e:
            return jsonify({"error": f"Error calling ETHIK module: {str(e)}"}), 500
    
    # Return sample data
    return jsonify(SAMPLE_DATA["ethik"])

@app.route('/api/integrate', methods=['POST'])
def integrate():
    """Processes the received data through integrated modules"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    
    # In a real implementation, would process data with appropriate modules
    
    result = {
        "received": data,
        "processed": True,
        "timestamp": "2023-11-15T10:30:00",
        "message": "Data processed successfully"
    }
    
    return jsonify(result)

# Start the API if run directly
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"Starting EVA & GUARANI Sandbox API on {host}:{port}")
    app.run(host=host, port=port, debug=debug_mode)