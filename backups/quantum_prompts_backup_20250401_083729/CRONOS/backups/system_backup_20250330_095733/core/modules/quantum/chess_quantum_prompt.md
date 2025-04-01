---
metadata:
  api_endpoints: []
  author: EVA & GUARANI
  backup_required: true
  category: modules
  changelog: []
  dependencies:
  - QUANTUM_PROMPTS
  - BIOS-Q
  description: Component of the EVA & GUARANI Quantum Unified System
  documentation_quality: 0.95
  encoding: utf-8
  ethical_validation: true
  last_updated: '2025-03-29'
  related_files: []
  required: true
  review_status: approved
  security_level: 0.95
  simulation_capable: false
  status: active
  subsystem: MASTER
  test_coverage: 0.9
  translation_status: completed
  type: documentation
  version: '8.0'
  windows_compatibility: true
---
```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
  principles: []
  security_level: standard
  test_coverage: 0.0
  documentation_quality: 0.0
  ethical_validation: true
  windows_compatibility: true
  encoding: utf-8
  backup_required: false
  translation_status: pending
  api_endpoints: []
  related_files: []
  changelog: ''
  review_status: pending
```

```yaml
METADATA:
  type: documentation
  category: module
  subsystem: MASTER
  status: active
  required: false
  simulation_capable: true
  dependencies: []
  description: Component of the  subsystem
  author: EVA & GUARANI
  version: 1.0.0
  last_updated: '2025-03-29'
```

yaml
quantum_prompt:
  id: "QP-GAMES-CHESS-001"
  domain: "Strategy Games - Chess"
  version: "1.0"
  
  conceptual_core:
    fundamental_principle: "Simulated battle of strategy and tactics on a checkered board"
    condensed_definition: "Ancient strategy game for two players on an 8x8 board, where 16 pieces of different values and movements per player are manipulated with the aim of capturing the opponent's king (checkmate), combining short-term tactics and long-term strategies."
  
  structure:
    level_1:
      - concept: "Board"
        definition: "8x8 checkered surface alternating light and dark squares, designated by alphanumeric coordinates (a1-h8)"
        relations: ["Pieces", "Movements", "Position"]
      
      - concept: "Pieces"
        definition: "Set of 16 elements per player (white or black) with distinct movements and values"
        relations: ["Relative Value", "Movements", "Captures"]
        details:
          - "King (1): Moves one square in any direction, most important piece"
          - "Queen (9): Moves any number of squares in any direction, most powerful piece"
          - "Rook (5): Moves horizontally and vertically"
          - "Bishop (3): Moves diagonally"
          - "Knight (3): Moves in L (2+1), only piece that can jump over others"
          - "Pawn (1): Moves forward, captures diagonally, promotion upon reaching last rank"
      
      - concept: "Checkmate"
        definition: "Situation where the king is threatened (in check) and there is no legal move to escape"
        relations: ["Check", "King", "End of Game"]
      
      - concept: "Special Moves"
        definition: "Actions allowed in specific situations that transcend basic movements"
        relations: ["Castling", "En Passant", "Promotion"]
        details:
          - "Castling: Simultaneous move of the king and rook when both have not moved"
          - "En Passant: Special capture of a pawn that advanced two squares"
          - "Promotion: Transformation of the pawn upon reaching the last rank"
    
    level_2:
      - concept: "Phases of the Game"
        definition: "Temporal segments of the game with distinct characteristics and objectives"
        relations: ["Opening", "Middlegame", "Endgame"]
        details:
          - "Opening: Initial development of pieces and control of the center"
          - "Middlegame: Execution of strategic plans and tactical maneuvers"
          - "Endgame: Simplification of the board and exploitation of advantages"
      
      - concept: "Strategic Principles"
        definition: "Fundamental guidelines to guide decisions"
        relations: ["Control of the Center", "Development", "King Safety"]
        details:
          - "Control of the Center: Domination of central squares (d4, d5, e4, e5)"
          - "Development: Coordinated mobilization of pieces"
          - "King Safety: Protection of the monarch through castling and pawn structure"
          - "Pawn Structure: Organization that defines characteristics of the position"
          - "Piece Activity: Maximization of the influence of pieces on the board"
      
      - concept: "Tactical Elements"
        definition: "Short-term maneuvers exploiting specific conditions"
        relations: ["Fork", "Pin", "Discovered", "Sacrifice"]
        details:
          - "Fork: Simultaneous attack on two or more pieces"
          - "Pin: Attack on a valuable piece forcing it to expose a more valuable piece behind"
          - "Discovered Attack: Revelation of an attack by moving the front piece"
          - "Sacrifice: Material offering for positional or tactical gain"
          - "Combination: Forced sequence of moves with a defined advantage"
      
      - concept: "Notation"
        definition: "Standardized system for recording and communicating moves"
        relations: ["Algebraic Notation", "Recorded Games", "Analysis"]
        details:
          - "Algebraic Notation: Standard system using coordinates (e4, Nf3)"
          - "Special Symbols: Indicators for specific situations (+ for check, # for mate)"
    
    level_3:
      - concept: "Openings"
        definition: "Studied initial sequences with established nomenclature and theory"
        relations: ["Open Openings", "Closed Openings", "Gambits"]
        details:
          - "Ruy Lopez: 1.e4 e5 2.Nf3 Nc6 3.Bb5"
          - "Sicilian Defense: 1.e4 c5"
          - "King's Indian Defense: 1.d4 Nf6 2.c4 g6"
          - "Queen's Gambit: 1.d4 d5 2.c4"
      
      - concept: "Positional Evaluation"
        definition: "Systematic analysis of static and dynamic factors of the position"
        relations: ["Pawn Structure", "Space", "Piece Coordination"]
        details:
          - "Material: Balance of forces based on the relative value of pieces"
          - "King Safety: Vulnerability to attacks and mate"
          - "Pawn Structure: Formations, weaknesses, and strengths"
          - "Space: Territorial control and freedom of maneuver"
          - "Good vs. Bad Pieces: Evaluation of the functional quality of pieces"
      
      - concept: "Endgame Patterns"
        definition: "Typical endgame configurations with established methods"
        relations: ["Pawn Endgames", "Rook Endgames", "Minor Piece Endgames"]
        details:
          - "Opposition: Control of the distance between kings"
          - "Pawn Square: Determination of reach capacity"
          - "Rook and Pawn vs. Rook Endgame: Lucena and Philidor positions"
          - "King and Pawn vs. King Endgame: Calculation of critical tempos"
  
  interdisciplinary_connections:
    - domain: "Mathematics"
      connection_points: ["Geometry", "Combinatorics", "Game Theory"]
    
    - domain: "Psychology"
      connection_points: ["Decision Making", "Stress Management", "Metacognition"]
    
    - domain: "Computing"
      connection_points: ["Artificial Intelligence", "Search Algorithms", "Heuristic Evaluation"]
    
    - domain: "History"
      connection_points: ["Cultural Evolution", "Medieval Symbolism", "Cold War"]
  
  activation_triggers:
    - "chess"
    - "chess pieces"
    - "8x8 board"
    - "checkmate"
    - "check and mate"
    - "chess game"
    - "opening strategy"
    - "chess endgame"
    - "algebraic notation"
    - "Kasparov"
    - "Fischer"
    - "FIDE"
    - "Elo"
  
  metadata:
    original_source: "Compilation from multiple chess theory sources"
    reliability: "High"
    integration_date: "2024-03-15"
    last_update: "2024-03-15"