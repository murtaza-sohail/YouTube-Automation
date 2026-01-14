# pipeline/config.py
"""Configuration module for the YouTube Motivational Content Engine.
Store API keys and adjustable parameters. Users should set environment variables
or edit this file with their own keys before running the pipeline.
"""
import os

# API Keys – set via environment variables
CHATGPT_API_KEY = os.getenv("CHATGPT_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Pipeline parameters
IMAGE_DURATION_SECONDS = 3  # 3 seconds per image as requested
VIDEO_RESOLUTION = "1920x1080"
BACKGROUND_MUSIC_PATH = "assets/background.mp3"
BEAT_DROP_TIMESTAMP = 120
