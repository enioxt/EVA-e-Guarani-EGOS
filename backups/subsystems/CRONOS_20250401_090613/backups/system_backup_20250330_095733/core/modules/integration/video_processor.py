#!/usr/bin/env python3
python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Video Processing Module - EVA & GUARANI
---------------------------------------
This module manages video processing using FFmpeg
and integration with external APIs for advanced effects.

Version: 1.0.0
"""

import os
import json
import logging
import subprocess
import time
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Union, List, Tuple
import asyncio
import aiohttp
import shutil

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/video_processor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("video-processor")

class VideoProcessor:
    """Manages video processing using FFmpeg and external APIs."""
    
    def __init__(self, config_path: str = "config/telegram_config.json"):
        """
        Initializes the video processor.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        # Directories for temporary and processed files
        self.temp_dir = Path("temp/videos")
        self.output_dir = Path("data/processed_videos")
        
        # Create directories if they don't exist
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if FFmpeg is installed
        self.ffmpeg_available = self._check_ffmpeg()
        
        # Usage statistics
        self.stats = {
            "processing_count": 0,
            "total_processing_time": 0,
            "last_processing_time": 0,
            "errors": 0,
            "successful_operations": 0
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.
        
        Returns:
            Dict: Loaded configurations
        """
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Configuration file not found: {self.config_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}
    
    def _check_ffmpeg(self) -> bool:
        """
        Checks if FFmpeg is installed on the system.
        
        Returns:
            bool: True if FFmpeg is available, False otherwise
        """
        try:
            subprocess.run(
                ["ffmpeg", "-version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                check=True
            )
            logger.info("FFmpeg found on the system.")
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            logger.warning("FFmpeg not found. Video processing functionalities will be limited.")
            return False
    
    async def process_video(self, video_path: str, operation: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Processes a video with the specified operation.
        
        Args:
            video_path: Path to the video file
            operation: Type of operation (convert, resize, extract_frames, etc)
            params: Additional parameters for the operation
        
        Returns:
            Dict: Operation result with processed file path
        """
        if not self.ffmpeg_available:
            return {
                "success": False,
                "error": "FFmpeg is not available on the system",
                "output_path": None
            }
        
        if not os.path.exists(video_path):
            return {
                "success": False,
                "error": f"Video file not found: {video_path}",
                "output_path": None
            }
        
        if params is None:
            params = {}
        
        start_time = time.time()
        self.stats["processing_count"] += 1
        
        try:
            # Generate unique name for the output file
            output_filename = f"{uuid.uuid4()}_{os.path.basename(video_path)}"
            output_path = str(self.output_dir / output_filename)
            
            # Execute specific operation
            if operation == "convert":
                result = await self._convert_format(video_path, output_path, params)
            elif operation == "resize":
                result = await self._resize_video(video_path, output_path, params)
            elif operation == "extract_frames":
                result = await self._extract_frames(video_path, output_path, params)
            elif operation == "add_watermark":
                result = await self._add_watermark(video_path, output_path, params)
            elif operation == "trim":
                result = await self._trim_video(video_path, output_path, params)
            else:
                result = {
                    "success": False,
                    "error": f"Unsupported operation: {operation}",
                    "output_path": None
                }
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats["last_processing_time"] = processing_time
            self.stats["total_processing_time"] += processing_time
            
            if result["success"]:
                self.stats["successful_operations"] += 1
                # Log success
                logger.info(f"[PROCESSING][{operation}] Successfully completed in {processing_time:.2f}s")
                logger.info(f"[PROCESSING][{operation}] Input: {video_path} | Output: {result['output_path']}")
            else:
                self.stats["errors"] += 1
                # Log error
                logger.error(f"[PROCESSING][{operation}] Failure: {result['error']}")
            
            return result
            
        except Exception as e:
            self.stats["errors"] += 1
            processing_time = time.time() - start_time
            self.stats["last_processing_time"] = processing_time
            self.stats["total_processing_time"] += processing_time
            
            logger.error(f"Error processing video: {e}")
            return {
                "success": False,
                "error": str(e),
                "output_path": None
            }
    
    async def _convert_format(self, input_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a video to another format.
        
        Args:
            input_path: Input video path
            output_path: Base path for the output video
            params: Additional parameters (format, codec, etc)
        
        Returns:
            Dict: Operation result
        """
        target_format = params.get("format", "mp4")
        codec = params.get("codec", "libx264")
        
        # Adjust output file extension
        output_path = f"{os.path.splitext(output_path)[0]}.{target_format}"
        
        try:
            cmd = [
                "ffmpeg", "-i", input_path,
                "-c:v", codec,
                "-preset", "medium",
                "-c:a", "aac",
                "-b:a", "128k",
                "-y", output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output_path": output_path,
                    "format": target_format
                }
            else:
                return {
                    "success": False,
                    "error": f"Error converting video: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception converting video: {str(e)}",
                "output_path": None
            }
    
    async def _resize_video(self, input_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resizes a video.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            params: Additional parameters (width, height, etc)
        
        Returns:
            Dict: Operation result
        """
        width = params.get("width", 640)
        height = params.get("height", 480)
        maintain_aspect_ratio = params.get("maintain_aspect_ratio", True)
        
        try:
            filter_complex = f"scale={width}:{height}"
            if maintain_aspect_ratio:
                filter_complex = f"scale={width}:{height}:force_original_aspect_ratio=decrease"
            
            cmd = [
                "ffmpeg", "-i", input_path,
                "-vf", filter_complex,
                "-c:a", "copy",
                "-y", output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output_path": output_path,
                    "dimensions": f"{width}x{height}"
                }
            else:
                return {
                    "success": False,
                    "error": f"Error resizing video: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception resizing video: {str(e)}",
                "output_path": None
            }
    
    async def _extract_frames(self, input_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts frames from a video.
        
        Args:
            input_path: Input video path
            output_path: Base path for extracted frames
            params: Additional parameters (fps, start_time, duration, etc)
        
        Returns:
            Dict: Operation result
        """
        fps = params.get("fps", 1)
        start_time = params.get("start_time", 0)
        duration = params.get("duration", None)
        
        # Create directory for frames
        frames_dir = f"{os.path.splitext(output_path)[0]}_frames"
        os.makedirs(frames_dir, exist_ok=True)
        
        try:
            cmd = ["ffmpeg", "-i", input_path]
            
            if start_time > 0:
                cmd.extend(["-ss", str(start_time)])
            
            if duration:
                cmd.extend(["-t", str(duration)])
            
            cmd.extend([
                "-vf", f"fps={fps}",
                "-y", f"{frames_dir}/frame_%04d.jpg"
            ])
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # Count how many frames were extracted
                frame_count = len([f for f in os.listdir(frames_dir) if f.startswith("frame_")])
                
                return {
                    "success": True,
                    "output_path": frames_dir,
                    "frame_count": frame_count,
                    "fps": fps
                }
            else:
                return {
                    "success": False,
                    "error": f"Error extracting frames: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception extracting frames: {str(e)}",
                "output_path": None
            }
    
    async def _add_watermark(self, input_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adds a watermark to a video.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            params: Additional parameters (watermark_path, position, etc)
        
        Returns:
            Dict: Operation result
        """
        watermark_path = params.get("watermark_path")
        position = params.get("position", "bottomright")
        opacity = params.get("opacity", 0.7)
        
        if not watermark_path or not os.path.exists(watermark_path):
            return {
                "success": False,
                "error": f"Watermark file not found: {watermark_path}",
                "output_path": None
            }
        
        try:
            # Define watermark position
            position_map = {
                "topleft": "10:10",
                "topright": "W-w-10:10",
                "bottomleft": "10:H-h-10",
                "bottomright": "W-w-10:H-h-10",
                "center": "(W-w)/2:(H-h)/2"
            }
            pos = position_map.get(position, position_map["bottomright"])
            
            cmd = [
                "ffmpeg", "-i", input_path,
                "-i", watermark_path,
                "-filter_complex", f"overlay={pos}:alpha={opacity}",
                "-codec:a", "copy",
                "-y", output_path
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output_path": output_path,
                    "watermark": os.path.basename(watermark_path)
                }
            else:
                return {
                    "success": False,
                    "error": f"Error adding watermark: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception adding watermark: {str(e)}",
                "output_path": None
            }
    
    async def _trim_video(self, input_path: str, output_path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trims a video based on start time and duration.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            params: Additional parameters (start_time, duration, etc)
        
        Returns:
            Dict: Operation result
        """
        start_time = params.get("start_time", 0)
        duration = params.get("duration")
        
        try:
            cmd = ["ffmpeg", "-i", input_path, "-ss", str(start_time)]
            
            if duration:
                cmd.extend(["-t", str(duration)])
            
            cmd.extend([
                "-c:v", "copy",
                "-c:a", "copy",
                "-y", output_path
            ])
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output_path": output_path,
                    "start_time": start_time,
                    "duration": duration
                }
            else:
                return {
                    "success": False,
                    "error": f"Error trimming video: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception trimming video: {str(e)}",
                "output_path": None
            }
    
    async def create_gif_from_video(self, input_path: str, output_path: str | None = None, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """
        Creates a GIF from a video.
        
        Args:
            input_path: Input video path
            output_path: Output GIF path (optional)
            params: Additional parameters (start_time, duration, fps, width, etc)
        
        Returns:
            Dict: Operation result
        """
        if not self.ffmpeg_available:
            return {
                "success": False,
                "error": "FFmpeg is not available on the system",
                "output_path": None
            }
        
        if not os.path.exists(input_path):
            return {
                "success": False,
                "error": f"Video file not found: {input_path}",
                "output_path": None
            }
        
        if params is None:
            params = {}
        
        start_time = params.get("start_time", 0)
        duration = params.get("duration")
        fps = params.get("fps", 10)
        width = params.get("width", 320)
        quality = params.get("quality", 90)
        
        # Generate name for the output file if not provided
        if output_path is None:
            output_filename = f"{uuid.uuid4()}_{os.path.splitext(os.path.basename(input_path))[0]}.gif"
            output_path = str(self.output_dir / output_filename)
        
        try:
            # Build command to create the GIF
            filters = [
                f"fps={fps}",
                f"scale={width}:-1:flags=lanczos"
            ]
            
            filter_complex = ",".join(filters)
            
            cmd = ["ffmpeg", "-i", input_path]
            
            if start_time > 0:
                cmd.extend(["-ss", str(start_time)])
            
            if duration:
                cmd.extend(["-t", str(duration)])
            
            cmd.extend([
                "-vf", filter_complex,
                "-y", output_path
            ])
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return {
                    "success": True,
                    "output_path": output_path,
                    "format": "gif",
                    "fps": fps,
                    "width": width
                }
            else:
                return {
                    "success": False,
                    "error": f"Error creating GIF: {stderr.decode()}",
                    "output_path": None
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception creating GIF: {str(e)}",
                "output_path": None
            }
    
    async def concatenate_videos(self, video_paths: List[str], output_path: str = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Concatenates multiple videos into a single file.
        
        Args:
            video_paths: List of paths to input videos
            output_path: Output video path (optional)
            params: Additional parameters (codec, bitrate, etc)
        
        Returns:
            Dict: Operation result
        """
        if not self.ff