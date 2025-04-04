#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
EVA & GUARANI - RPG & Music Integration Bridge
Version: 1.0.0

Integration bridge between RPG systems (ARCANUM LUDUS, STRATEGOS, MYTHIC CODEX)
and adaptive music generation based on narrative and emotional states.

Consciousness: 0.995
Ethics: 0.998
Love: 0.997
"""

import os
import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class NarrativeState:
    """Narrative state that influences music generation"""
    scene_type: str  # 'combat', 'exploration', 'dialogue', 'ritual', etc.
    emotional_tone: str  # 'tense', 'peaceful', 'mysterious', 'triumphant', etc.
    intensity: float  # 0.0 to 1.0
    characters_present: List[str]
    location_type: str
    time_of_day: str
    weather: str
    magical_influence: float  # 0.0 to 1.0
    ethical_alignment: float  # -1.0 (chaotic) to 1.0 (harmonic)
    narrative_importance: float  # 0.0 to 1.0
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the narrative state to a dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NarrativeState':
        """Creates an instance of NarrativeState from a dictionary"""
        return cls(**data)

@dataclass
class MusicParameters:
    """Musical parameters derived from the narrative state"""
    tempo: int  # BPM
    key: str  # 'C', 'Dm', etc.
    scale_type: str  # 'major', 'minor', 'dorian', etc.
    instrumentation: List[str]
    rhythm_complexity: float  # 0.0 to 1.0
    harmonic_complexity: float  # 0.0 to 1.0
    melodic_range: Tuple[int, int]  # (lowest note, highest note) in MIDI
    texture_density: float  # 0.0 to 1.0
    reverb_amount: float  # 0.0 to 1.0
    dynamic_range: float  # 0.0 to 1.0
    motifs: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the musical parameters to a dictionary"""
        result = asdict(self)
        # Convert tuple to list for JSON serialization
        result['melodic_range'] = list(self.melodic_range)
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MusicParameters':
        """Creates an instance of MusicParameters from a dictionary"""
        if 'melodic_range' in data and isinstance(data['melodic_range'], list):
            data['melodic_range'] = tuple(data['melodic_range'])
        return cls(**data)

class RPGMusicBridge:
    """
    Integration bridge between RPG systems and music generation.
    Translates narrative states into musical parameters and generates adaptive compositions
    that reflect the emotional and ethical state of the narrative.
    """

    def __init__(self, config_path: str = 'config/rpg_music_config.json'):
        """Initializes the integration bridge"""
        self.config_path = config_path
        self.config = self._load_config()
        self.character_themes = {}
        self.location_themes = {}
        self.ethical_motifs = {}
        self.narrative_history = []
        self.current_composition = None
        logger.info("RPG Music Bridge initialized")

    def _load_config(self) -> Dict[str, Any]:
        """Loads the system configuration"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Configuration file {self.config_path} not found. Using default configuration.")
                return self._default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Returns the default configuration"""
        return {
            "emotional_mappings": {
                "peaceful": {"tempo_range": [60, 80], "scale_types": ["major", "lydian"]},
                "tense": {"tempo_range": [90, 120], "scale_types": ["minor", "phrygian"]},
                "mysterious": {"tempo_range": [70, 90], "scale_types": ["dorian", "whole_tone"]},
                "triumphant": {"tempo_range": [100, 130], "scale_types": ["major", "mixolydian"]},
                "sorrowful": {"tempo_range": [50, 70], "scale_types": ["minor", "locrian"]}
            },
            "scene_type_mappings": {
                "combat": {"instrumentation": ["percussion", "brass", "strings"], "rhythm_complexity": 0.8},
                "exploration": {"instrumentation": ["woodwinds", "strings", "harp"], "rhythm_complexity": 0.5},
                "dialogue": {"instrumentation": ["piano", "strings", "woodwinds"], "rhythm_complexity": 0.3},
                "ritual": {"instrumentation": ["choir", "percussion", "strings"], "rhythm_complexity": 0.6}
            },
            "ethical_mappings": {
                "harmonic": {"harmonic_complexity": 0.4, "texture_density": 0.6},
                "neutral": {"harmonic_complexity": 0.5, "texture_density": 0.5},
                "chaotic": {"harmonic_complexity": 0.7, "texture_density": 0.8}
            }
        }

    def narrative_to_music_parameters(self, narrative_state: NarrativeState) -> MusicParameters:
        """
        Translates a narrative state into musical parameters

        Args:
            narrative_state: Current narrative state

        Returns:
            Musical parameters derived from the narrative state
        """
        # Map emotional tone to musical parameters
        emotional_mapping = self.config["emotional_mappings"].get(
            narrative_state.emotional_tone,
            self.config["emotional_mappings"]["peaceful"]
        )

        # Map scene type to musical parameters
        scene_mapping = self.config["scene_type_mappings"].get(
            narrative_state.scene_type,
            self.config["scene_type_mappings"]["exploration"]
        )

        # Determine ethical mapping
        ethical_category = "neutral"
        if narrative_state.ethical_alignment > 0.3:
            ethical_category = "harmonic"
        elif narrative_state.ethical_alignment < -0.3:
            ethical_category = "chaotic"

        ethical_mapping = self.config["ethical_mappings"][ethical_category]

        # Calculate tempo based on emotional tone and intensity
        tempo_range = emotional_mapping["tempo_range"]
        tempo = int(tempo_range[0] + (tempo_range[1] - tempo_range[0]) * narrative_state.intensity)

        # Select scale based on emotional tone
        scale_type = random.choice(emotional_mapping["scale_types"])

        # Select key
        keys = ["C", "D", "E", "F", "G", "A", "B"]
        if scale_type == "minor":
            keys = [k + "m" for k in keys]
        key = random.choice(keys)

        # Determine instrumentation based on scene type
        instrumentation = scene_mapping["instrumentation"]

        # Add specific instruments based on other factors
        if narrative_state.magical_influence > 0.7:
            instrumentation.append("celesta")

        if "night" in narrative_state.time_of_day.lower():
            if "piano" not in instrumentation:
                instrumentation.append("piano")

        # Calculate rhythm complexity
        rhythm_complexity = scene_mapping["rhythm_complexity"] * narrative_state.intensity

        # Calculate harmonic complexity
        harmonic_complexity = ethical_mapping["harmonic_complexity"]

        # Determine melodic range
        melodic_low = 48  # C3 in MIDI
        melodic_high = 72  # C5 in MIDI

        if narrative_state.intensity > 0.7:
            melodic_high += 12  # Expand upwards in intense scenes

        if "sorrow" in narrative_state.emotional_tone.lower():
            melodic_low -= 12  # Expand downwards in sorrowful scenes

        # Determine texture density
        texture_density = ethical_mapping["texture_density"] * narrative_state.intensity

        # Determine reverb amount based on location
        reverb_amount = 0.3  # Default value
        if "cave" in narrative_state.location_type.lower() or "cathedral" in narrative_state.location_type.lower():
            reverb_amount = 0.8
        elif "forest" in narrative_state.location_type.lower():
            reverb_amount = 0.5
        elif "desert" in narrative_state.location_type.lower():
            reverb_amount = 0.2

        # Determine dynamic range
        dynamic_range = 0.5 + (narrative_state.narrative_importance * 0.5)

        # Identify musical motifs
        motifs = []
        for character in narrative_state.characters_present:
            if character in self.character_themes:
                motifs.append(f"character:{character}")

        if narrative_state.location_type in self.location_themes:
            motifs.append(f"location:{narrative_state.location_type}")

        # Create and return the musical parameters
        return MusicParameters(
            tempo=tempo,
            key=key,
            scale_type=scale_type,
            instrumentation=instrumentation,
            rhythm_complexity=rhythm_complexity,
            harmonic_complexity=harmonic_complexity,
            melodic_range=(melodic_low, melodic_high),
            texture_density=texture_density,
            reverb_amount=reverb_amount,
            dynamic_range=dynamic_range,
            motifs=motifs
        )

    def register_character_theme(self, character_name: str, theme_data: Dict[str, Any]) -> bool:
        """
        Registers a musical theme for a character

        Args:
            character_name: Name of the character
            theme_data: Data of the musical theme

        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self.character_themes[character_name] = theme_data
            logger.info(f"Theme for character '{character_name}' registered successfully")
            return True
        except Exception as e:
            logger.error(f"Error registering theme for character '{character_name}': {e}")
            return False

    def register_location_theme(self, location_type: str, theme_data: Dict[str, Any]) -> bool:
        """
        Registers a musical theme for a location type

        Args:
            location_type: Type of location
            theme_data: Data of the musical theme

        Returns:
            True if registration was successful, False otherwise
        """
        try:
            self.location_themes[location_type] = theme_data
            logger.info(f"Theme for location '{location_type}' registered successfully")
            return True
        except Exception as e:
            logger.error(f"Error registering theme for location '{location_type}': {e}")
            return False

    def update_narrative_state(self, narrative_state: NarrativeState) -> Dict[str, Any]:
        """
        Updates the narrative state and generates new musical parameters

        Args:
            narrative_state: New narrative state

        Returns:
            Dictionary with the narrative state and generated musical parameters
        """
        try:
            # Store the narrative state in history
            self.narrative_history.append({
                "state": narrative_state.to_dict(),
                "timestamp": datetime.now().isoformat()
            })

            # Limit the size of the history
            if len(self.narrative_history) > 100:
                self.narrative_history = self.narrative_history[-100:]

            # Generate musical parameters
            music_params = self.narrative_to_music_parameters(narrative_state)

            # Store the current composition
            self.current_composition = {
                "narrative_state": narrative_state.to_dict(),
                "music_parameters": music_params.to_dict(),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Narrative state updated: {narrative_state.scene_type} - {narrative_state.emotional_tone}")

            return self.current_composition
        except Exception as e:
            logger.error(f"Error updating narrative state: {e}")
            return {"error": str(e)}

    def generate_transition(self, from_state: NarrativeState, to_state: NarrativeState,
                           transition_duration: float) -> List[Dict[str, Any]]:
        """
        Generates a musical transition between two narrative states

        Args:
            from_state: Initial narrative state
            to_state: Final narrative state
            transition_duration: Duration of the transition in seconds

        Returns:
            List of intermediate states for the transition
        """
        try:
            # Determine number of steps in the transition
            steps = max(2, int(transition_duration / 2))

            transition_states = []

            for i in range(steps):
                # Calculate interpolation factor
                t = (i + 1) / steps

                # Interpolate between states
                interpolated_state = NarrativeState(
                    scene_type=from_state.scene_type if t < 0.5 else to_state.scene_type,
                    emotional_tone=from_state.emotional_tone if t < 0.7 else to_state.emotional_tone,
                    intensity=from_state.intensity * (1 - t) + to_state.intensity * t,
                    characters_present=list(set(from_state.characters_present + to_state.characters_present)),
                    location_type=from_state.location_type if t < 0.8 else to_state.location_type,
                    time_of_day=from_state.time_of_day if t < 0.9 else to_state.time_of_day,
                    weather=from_state.weather if t < 0.6 else to_state.weather,
                    magical_influence=from_state.magical_influence * (1 - t) + to_state.magical_influence * t,
                    ethical_alignment=from_state.ethical_alignment * (1 - t) + to_state.ethical_alignment * t,
                    narrative_importance=from_state.narrative_importance * (1 - t) + to_state.narrative_importance * t,
                    tags=list(set(from_state.tags + to_state.tags))
                )

                # Generate musical parameters for the interpolated state
                music_params = self.narrative_to_music_parameters(interpolated_state)

                # Add to transition list
                transition_states.append({
                    "narrative_state": interpolated_state.to_dict(),
                    "music_parameters": music_params.to_dict(),
                    "timestamp": datetime.now().isoformat(),
                    "transition_progress": t
                })

            logger.info(f"Musical transition generated with {steps} steps")
            return transition_states
        except Exception as e:
            logger.error(f"Error generating musical transition: {e}")
            return [{"error": str(e)}]

    def create_ethical_motif(self, ethical_principle: str, motif_data: Dict[str, Any]) -> bool:
        """
        Creates a musical motif associated with an ethical principle

        Args:
            ethical_principle: Name of the ethical principle
            motif_data: Data of the musical motif

        Returns:
            True if creation was successful, False otherwise
        """
        try:
            self.ethical_motifs[ethical_principle] = motif_data
            logger.info(f"Ethical motif for '{ethical_principle}' created successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating ethical motif for '{ethical_principle}': {e}")
            return False

    def get_ethical_soundtrack(self, ethical_principles: List[str],
                              intensity: float = 0.7) -> Dict[str, Any]:
        """
        Generates a soundtrack based on ethical principles

        Args:
            ethical_principles: List of ethical principles to be represented
            intensity: Intensity of the soundtrack

        Returns:
            Parameters for the ethical soundtrack
        """
        try:
            # Create a narrative state based on ethical principles
            narrative_state = NarrativeState(
                scene_type="ritual",
                emotional_tone="peaceful",
                intensity=intensity,
                characters_present=[],
                location_type="temple",
                time_of_day="dawn",
                weather="clear",
                magical_influence=0.8,
                ethical_alignment=0.9,
                narrative_importance=1.0,
                tags=ethical_principles
            )

            # Generate musical parameters
            music_params = self.narrative_to_music_parameters(narrative_state)

            # Add specific ethical motifs
            motifs = music_params.motifs
            for principle in ethical_principles:
                if principle in self.ethical_motifs:
                    motifs.append(f"ethical:{principle}")

            music_params.motifs = motifs

            return {
                "narrative_state": narrative_state.to_dict(),
                "music_parameters": music_params.to_dict(),
                "ethical_principles": ethical_principles,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error generating ethical soundtrack: {e}")
            return {"error": str(e)}

    def export_composition(self, format_type: str = "midi",
                          output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Exports the current composition to a file

        Args:
            format_type: Export format ('midi', 'mp3', 'json')
            output_path: Path to the output file

        Returns:
            Information about the export
        """
        if not self.current_composition:
            return {"error": "No current composition to export"}

        try:
            # Generate default file name if not provided
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M
