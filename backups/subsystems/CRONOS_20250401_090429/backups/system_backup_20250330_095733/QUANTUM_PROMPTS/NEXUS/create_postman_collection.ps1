# EVA & GUARANI - Postman Collection Creator
# This script creates a Postman collection with all the test endpoints

$collectionJson = @{
    info     = @{
        name        = "EVA & GUARANI Tests"
        description = "Collection of tests for EVA & GUARANI EGOS"
        schema      = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    }
    item     = @(
        @{
            name    = "Mycelium Network"
            request = @{
                method = "POST"
                header = @(@{
                        key   = "Content-Type"
                        value = "application/json"
                    })
                url    = @{
                    raw  = "{{baseUrl}}/mycelium/connect"
                    host = @("{{baseUrl}}")
                    path = @("mycelium", "connect")
                }
                body   = @{
                    mode = "raw"
                    raw  = '{
    "nodeId": "ATLAS-001",
    "nodeType": "visualization",
    "connections": ["NEXUS-001", "CRONOS-001"]
}'
                }
            }
        },
        @{
            name    = "ATLAS Visualization"
            request = @{
                method = "POST"
                header = @(@{
                        key   = "Content-Type"
                        value = "application/json"
                    })
                url    = @{
                    raw  = "{{baseUrl}}/atlas/visualize"
                    host = @("{{baseUrl}}")
                    path = @("atlas", "visualize")
                }
                body   = @{
                    mode = "raw"
                    raw  = '{
    "systemId": "SYS-001",
    "type": "system-map",
    "data": {
        "nodes": ["ATLAS", "NEXUS", "CRONOS"],
        "connections": [
            {"from": "ATLAS", "to": "NEXUS"},
            {"from": "NEXUS", "to": "CRONOS"}
        ]
    }
}'
                }
            }
        },
        @{
            name    = "CRONOS Timeline"
            request = @{
                method = "POST"
                header = @(@{
                        key   = "Content-Type"
                        value = "application/json"
                    })
                url    = @{
                    raw  = "{{baseUrl}}/cronos/timeline"
                    host = @("{{baseUrl}}")
                    path = @("cronos", "timeline")
                }
                body   = @{
                    mode = "raw"
                    raw  = '{
    "eventId": "EVT-001",
    "timestamp": "2025-03-28T12:00:00Z",
    "data": {
        "type": "system_update",
        "description": "ATLAS visualization completed"
    }
}'
                }
            }
        },
        @{
            name    = "NEXUS Analysis"
            request = @{
                method = "POST"
                header = @(@{
                        key   = "Content-Type"
                        value = "application/json"
                    })
                url    = @{
                    raw  = "{{baseUrl}}/nexus/analyze"
                    host = @("{{baseUrl}}")
                    path = @("nexus", "analyze")
                }
                body   = @{
                    mode = "raw"
                    raw  = '{
    "analysisId": "ANL-001",
    "data": {
        "type": "system_performance",
        "metrics": ["response_time", "memory_usage"]
    },
    "parameters": {
        "depth": "full",
        "coverage": true
    }
}'
                }
            }
        },
        @{
            name    = "ETHIK Validation"
            request = @{
                method = "POST"
                header = @(@{
                        key   = "Content-Type"
                        value = "application/json"
                    })
                url    = @{
                    raw  = "{{baseUrl}}/ethik/validate"
                    host = @("{{baseUrl}}")
                    path = @("ethik", "validate")
                }
                body   = @{
                    mode = "raw"
                    raw  = '{
    "actionId": "ACT-001",
    "context": {
        "action": "system_update",
        "impact_level": "medium",
        "affected_systems": ["ATLAS", "NEXUS"]
    },
    "parameters": {
        "validation_level": "strict"
    }
}'
                }
            }
        }
    )
    variable = @(
        @{
            key   = "baseUrl"
            value = "http://localhost:3000"
            type  = "string"
        }
    )
}

# Convert to JSON and save
$collectionJson | ConvertTo-Json -Depth 10 | Out-File -FilePath "EVA_GUARANI_Tests.postman_collection.json"

Write-Host "Collection file created successfully!"
Write-Host "To import into Postman:"
Write-Host "1. Open Postman"
Write-Host "2. Click 'Import' button"
Write-Host "3. Drag and drop the 'EVA_GUARANI_Tests.postman_collection.json' file"
Write-Host "4. Click 'Import' to confirm" 