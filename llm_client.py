import asyncio
import asyncio
import json
import os
import sys
import time
import wave
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from google import genai
from google.genai import types

from audio_player.audioPlayer import AudioPlayer
from model_control.vts_expressions import agree_sync as agree
from model_control.vts_expressions import angry_sync as angry
from model_control.vts_expressions import blink_sync as blink
from model_control.vts_expressions import disagree_sync as disagree
from model_control.vts_expressions import laugh_sync as laugh
from model_control.vts_expressions import love_sync as love
from model_control.vts_expressions import sad_sync as sad
from model_control.vts_expressions import shy_sync as shy
from model_control.vts_expressions import smile_sync as smile
from model_control.vts_expressions import wow_sync as wow
from model_control.vts_expressions import yap_sync as yap

# Configuration Constants
DEFAULT_PROVIDER = "google"
DEFAULT_TIMEOUT = 30
DEFAULT_TEMPERATURE = 0.75

# TTS Configuration Constants
DEFAULT_TTS_ENABLED = True
DEFAULT_TTS_VOICE = "Kore"
DEFAULT_TTS_CLEANUP_DAYS = 7
DEFAULT_TTS_AUDIO_FORMAT = "wav"

# Expression functions for function calling
EXPRESSION_TOOLS = [
    smile,
    laugh,
    angry,
    blink,
    wow,
    agree,
    disagree,
    yap,
    shy,
    sad,
    love,
]

# Provider Model Defaults
PROVIDER_MODEL_DEFAULTS = "models/gemini-2.5-flash"


class LLMClient:
    """Abstract LLM client providing unified interface for multiple AI providers."""

    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client."""
        self._provider = provider or os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).lower()
        self._model = model or os.getenv(
            "LLM_MODEL",
            PROVIDER_MODEL_DEFAULTS,
        )
        self._timeout = int(os.getenv("LLM_TIMEOUT", DEFAULT_TIMEOUT))
        self._temperature = float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE))

        # TTS Configuration
        self._tts_enabled = (
            os.getenv("TTS_ENABLED", str(DEFAULT_TTS_ENABLED)).lower() == "true"
        )
        self._tts_voice = os.getenv("TTS_VOICE", DEFAULT_TTS_VOICE)
        self._tts_cleanup_days = int(
            os.getenv("TTS_CLEANUP_DAYS", DEFAULT_TTS_CLEANUP_DAYS)
        )
        self._tts_audio_format = os.getenv("TTS_AUDIO_FORMAT", DEFAULT_TTS_AUDIO_FORMAT)

        # Google API configuration
        self._google_api_key = os.getenv("GOOGLE_API_KEY")

        self._last_response_time: Optional[float] = None
        self._client: Optional[genai.Client] = None
        self._project_root = os.path.dirname(os.path.abspath(__file__))

        self._setup_audio_player()
        self._validate_and_setup()

    def _setup_audio_player(self):
        """Initialize the audio player and register control tools."""
        self.audio_player = AudioPlayer()
        self.audio_player_task = None  # Will be started in start_audio_player()

        # Define wrapper functions for LLM tools
        def play_music(song_name: str = "__ALL__"):
            """
            Play music or audio files.


            Args:
                song_name: The name of the song to play. Use "__ALL__" to play all songs in queue.
                           Available songs: {self.audio_player.api.get_audio_list()}
            """
            print(f"🎵 LLM requested to play music: {song_name}")
            if song_name == "__ALL__":
                self.audio_player.api.play_all()
            else:
                self.audio_player.api.play_audio(song_name)

        def stop_music():
            """Stop currently playing music."""
            print("🛑 LLM requested to stop music")
            self.audio_player.api.stop_playing()

        # Add to available tools
        global EXPRESSION_TOOLS
        EXPRESSION_TOOLS.append(play_music)
        EXPRESSION_TOOLS.append(stop_music)

    async def start_audio_player(self):
        """Start the audio player background task. Must be called from async context."""
        if self.audio_player_task is None:
            self.audio_player_task = asyncio.create_task(self.audio_player.run())
            print("🔊 Audio player started")
        return self.audio_player_task

    async def stop_audio_player(self):
        """Stop the audio player background task."""
        if self.audio_player_task:
            self.audio_player.stop()
            await self.audio_player_task
            self.audio_player_task = None
            print("🔇 Audio player stopped")


    def _load_prompt(self, prompt_name: str) -> str:
        """Load prompt content from prompts/ folder."""
        prompt_path = os.path.join(self._project_root, "prompts", f"{prompt_name}.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    def _validate_and_setup(self) -> None:
        """Validate configuration and set up google-generativeai client."""
        if not self._validate_provider_config():
            raise ValueError(self._get_provider_validation_error())

        self._validate_tts_config()
        self._setup_provider_environment()
        self._client = self._create_client()

    def _validate_tts_config(self) -> None:
        """Validate TTS configuration parameters."""
        # Validate cleanup days
        if self._tts_cleanup_days < 0:
            raise ValueError(
                f"TTS_CLEANUP_DAYS must be non-negative, got: {self._tts_cleanup_days}"
            )

        # Validate audio format
        if self._tts_audio_format not in ["wav"]:
            raise ValueError(
                f"TTS_AUDIO_FORMAT must be 'wav', got: {self._tts_audio_format}"
            )

        # Create audio directory if TTS is enabled
        if self._tts_enabled:
            audio_dir = os.path.join(self._project_root, "audio")
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir, exist_ok=True)

    def _validate_provider_config(self) -> bool:
        """Validate that the provider has all required configuration."""
        # Only support Google provider with google-generativeai
        if self._provider != "google":
            return False
        # API key is only required if TTS is enabled or if we'll be using LLM functions
        return bool(self._google_api_key)

    def _get_provider_validation_error(self) -> str:
        """Get descriptive error message for provider configuration issues."""
        if self._provider != "google":
            return f"Unsupported provider: {self._provider}. This version only supports 'google' provider."
        return "Google/Gemini provider requires GOOGLE_API_KEY environment variable. Get your API key from https://makersuite.google.com/app/apikey"

    def _setup_provider_environment(self) -> None:
        """Set up provider-specific environment variables."""
        # Set up Google API key if provided
        if self._google_api_key:
            os.environ["GOOGLE_API_KEY"] = self._google_api_key

    def _create_client(self) -> genai.Client:
        """Create and return configured google-generativeai client."""
        return genai.Client(api_key=self._google_api_key)

    def _get_model_string(self) -> str:
        """Get model string for google-generativeai."""
        return self._model

    def call_llm(
        self, user_prompt: str, system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send prompts to the LLM with function calling and return unified response.

        Returns:
            Dict containing:
            - text_response: The LLM's conversational response
            - expression_called: Name of expression function called (if any)
            - intermediate_messages: Full conversation history with function calls
        """
        if not self._client:
            raise RuntimeError("Client not initialized")

        start_time = time.time()
        try:
            # load system prompt from prompt/ folder if not provided
            if not system_prompt:
                system_prompt = self._load_prompt("system")

            # Combine system and user prompts
            combined_prompt = f"{system_prompt}\n\nUser: {user_prompt}"

            # First call to get potential function calls
            response = self._client.models.generate_content(
                model=self._get_model_string(),
                contents=combined_prompt,
                config=types.GenerateContentConfig(
                    tools=EXPRESSION_TOOLS,  # Add expression functions as tools
                    temperature=self._temperature,
                    max_output_tokens=300,  # Increased for conversational responses
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True  # Disable automatic calling so we can capture and execute manually
                    ),
                ),
            )

            self._last_response_time = time.time() - start_time

            # Check if there are function calls to process
            function_calls = []
            if hasattr(response, "function_calls") and response.function_calls:
                function_calls.extend(response.function_calls)
            elif hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if (
                    hasattr(candidate, "content")
                    and candidate.content
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            function_calls.append(part.function_call)

            # If we have function calls, execute them and continue conversation
            if function_calls:
                # Execute the first function call
                function_call = function_calls[0]
                function_name = None
                if hasattr(function_call, "name"):
                    function_name = function_call.name
                elif hasattr(function_call, "function_call") and hasattr(
                    function_call.function_call, "name"
                ):
                    function_name = function_call.function_call.name

                # Execute the function
                if function_name:
                    self._execute_function_call(function_call)

                # Create function response and continue conversation
                try:
                    if not function_name:
                        raise ValueError(
                            "Could not extract function name from function call"
                        )

                    function_response = types.Part.from_function_response(
                        name=function_name,
                        response={
                            "result": f"Expression {function_name} executed successfully"
                        },
                    )

                    # Continue conversation with function response
                    if not (hasattr(response, "candidates") and response.candidates):
                        raise ValueError("No candidates in response")

                    final_response = self._client.models.generate_content(
                        model=self._get_model_string(),
                        contents=[
                            types.Content(
                                role="user",
                                parts=[types.Part.from_text(text=combined_prompt)],
                            ),
                            response.candidates[0].content,  # The function call request
                            types.Content(
                                role="tool", parts=[function_response]
                            ),  # Our function response
                        ],
                        config=types.GenerateContentConfig(
                            tools=EXPRESSION_TOOLS,
                            temperature=self._temperature,
                            max_output_tokens=300,
                        ),
                    )

                    # Parse the final response
                    final_text_response = final_response.text or ""

                    # Generate TTS audio if enabled
                    audio_file = (
                        self.generate_tts_audio(final_text_response)
                        if self._tts_enabled
                        else None
                    )

                    result = {
                        "text_response": final_text_response,
                        "expression_called": function_name,
                        "audio_file": audio_file,
                        "intermediate_messages": [
                            {
                                "role": "assistant",
                                "function_calls": [{"name": function_name, "args": {}}],
                            }
                        ],
                    }

                except Exception as e:
                    print(
                        f"Warning: Could not continue conversation after function call: {e}"
                    )
                    # Fallback to just the function call result
                    fallback_text = f"*{function_name} expression*"
                    audio_file = (
                        self.generate_tts_audio(fallback_text)
                        if self._tts_enabled
                        else None
                    )

                    result = {
                        "text_response": fallback_text,  # Simple fallback
                        "expression_called": function_name,
                        "audio_file": audio_file,
                        "intermediate_messages": [],
                    }
            else:
                # No function calls, just return the text response
                text_response = response.text or ""
                audio_file = (
                    self.generate_tts_audio(text_response)
                    if self._tts_enabled
                    else None
                )

                result = {
                    "text_response": text_response,
                    "expression_called": None,
                    "audio_file": audio_file,
                    "intermediate_messages": [],
                }

            return result

        except Exception as e:
            self._last_response_time = time.time() - start_time
            raise Exception(f"LLM request failed: {e}")

    def _parse_unified_response(self, response) -> Dict[str, Any]:
        """Parse google-generativeai response for both text and expression function calls."""
        result = {
            "text_response": "",
            "expression_called": None,
            "audio_file": None,
            "intermediate_messages": [],
        }

        try:
            # Get text response
            result["text_response"] = response.text or ""

            # Check for function calls in multiple locations
            function_calls = []

            # Check response.function_calls (for automatic function calling)
            if hasattr(response, "function_calls") and response.function_calls:
                function_calls.extend(response.function_calls)

            # Check response.candidates[0].content.parts for function calls
            if hasattr(response, "candidates") and response.candidates:
                candidate = response.candidates[0]
                if (
                    hasattr(candidate, "content")
                    and candidate.content
                    and hasattr(candidate.content, "parts")
                    and candidate.content.parts
                ):
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call"):
                            function_calls.append(part.function_call)

            # Process function calls
            if function_calls:
                # Get the first function call
                function_call = function_calls[0]
                if hasattr(function_call, "name"):
                    result["expression_called"] = function_call.name
                elif hasattr(function_call, "function_call") and hasattr(
                    function_call.function_call, "name"
                ):
                    result["expression_called"] = function_call.function_call.name

                # Execute the function
                self._execute_function_call(function_call)

                # Store function calls info in intermediate messages
                result["intermediate_messages"] = [
                    {
                        "role": "assistant",
                        "function_calls": [
                            {
                                "name": getattr(
                                    fc,
                                    "name",
                                    getattr(fc, "function_call", {}).get(
                                        "name", "unknown"
                                    ),
                                ),
                                "args": getattr(
                                    fc,
                                    "args",
                                    getattr(fc, "function_call", {}).get("args", {}),
                                ),
                            }
                            for fc in function_calls
                        ],
                    }
                ]

        except Exception as e:
            print(f"Warning: Could not parse function calling response: {e}")
            # Fallback to basic text response
            result["text_response"] = (
                str(response.text)
                if hasattr(response, "text") and response.text
                else "Error processing response"
            )

        # Generate TTS audio for the text response
        if self._tts_enabled and result["text_response"]:
            result["audio_file"] = self.generate_tts_audio(result["text_response"])

        return result

    def _execute_function_call(self, function_call) -> None:
        """Execute the called function."""
        try:
            # Extract function name from different possible structures
            function_name = None
            if hasattr(function_call, "name"):
                function_name = function_call.name
            elif hasattr(function_call, "function_call") and hasattr(
                function_call.function_call, "name"
            ):
                function_name = function_call.function_call.name

            if not function_name:
                print(
                    f"Warning: Could not extract function name from function call: {function_call}"
                )
                return

            # Find and call the function from EXPRESSION_TOOLS
            for tool_func in EXPRESSION_TOOLS:
                if tool_func.__name__ == function_name:
                    # Execute the synchronous wrapper function directly
                    print(f"Executing expression function: {function_name}")
                    tool_func()
                    print(f"Successfully executed: {function_name}")
                    break
            else:
                print(
                    f"Warning: Function '{function_name}' not found in EXPRESSION_TOOLS"
                )
        except Exception as e:
            print(f"Warning: Could not execute function call: {e}")
            import traceback

            traceback.print_exc()

    @property
    def provider(self) -> str:
        """Get current provider name."""
        return self._provider

    @property
    def model(self) -> str:
        """Get current model name."""
        return self._model

    @property
    def last_response_time(self) -> Optional[float]:
        """Get last response time in seconds."""
        return self._last_response_time

    def is_performance_acceptable(self) -> bool:
        """Check if last response met performance requirements (<500ms)."""
        if self._last_response_time is None:
            return True
        return self._last_response_time < 0.5

    def generate_tts_audio(
        self, text: str, voice: Optional[str] = None
    ) -> Optional[str]:
        """Generate TTS audio from text and save to file.

        Args:
            text: Text to convert to speech
            voice: Voice name to use (defaults to configured voice)

        Returns:
            File path to generated audio file, or None if TTS disabled or failed
        """
        if not self._tts_enabled:
            return None

        if not self._client:
            print("Warning: TTS client not initialized")
            return None

        if not text or not text.strip():
            print("Warning: Empty text provided for TTS generation")
            return None

        try:
            voice_name = voice or self._tts_voice

            # Generate TTS audio using Gemini TTS API
            response = self._client.models.generate_content(
                model="gemini-2.5-flash-preview-tts",
                contents=f"Say naturally: {text}",
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name,
                            )
                        )
                    ),
                ),
            )

            # Extract audio data
            if not (response.candidates and response.candidates[0].content.parts):
                print("Warning: No audio data in TTS response")
                return None

            audio_data = response.candidates[0].content.parts[0].inline_data.data
            if not audio_data:
                print("Warning: Empty audio data in TTS response")
                return None

            # Generate filename and save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"response_{timestamp}.{self._tts_audio_format}"
            audio_dir = self._ensure_audio_directory()
            file_path = os.path.join(audio_dir, filename)

            # Save as WAV file
            self._save_wav_file(file_path, audio_data)

            # Optionally run cleanup
            if self._tts_cleanup_days > 0:
                self.cleanup_old_audio_files()

            print(f"TTS audio generated: {file_path}")
            return file_path

        except Exception as e:
            print(f"Warning: TTS generation failed: {e}")
            return None

    def _save_wav_file(
        self,
        file_path: str,
        audio_data: bytes,
        channels: int = 1,
        rate: int = 24000,
        sample_width: int = 2,
    ) -> None:
        """Save audio data as WAV file."""
        with wave.open(file_path, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(audio_data)

    @staticmethod
    def cleanup_audio_files_static(
        cleanup_days: int = 7, project_root: Optional[str] = None
    ) -> int:
        """Static method to clean up old audio files without initializing full client.

        Args:
            cleanup_days: Files older than this many days will be removed
            project_root: Project root directory (auto-detected if None)

        Returns:
            Number of files cleaned up
        """
        if cleanup_days <= 0:
            return 0

        if project_root is None:
            project_root = os.path.dirname(os.path.abspath(__file__))

        audio_dir = os.path.join(project_root, "audio")
        if not os.path.exists(audio_dir):
            return 0

        cutoff_date = datetime.now() - timedelta(days=cleanup_days)
        cleanup_count = 0

        try:
            for filename in os.listdir(audio_dir):
                if not filename.endswith(".wav"):
                    continue

                file_path = os.path.join(audio_dir, filename)
                if not os.path.isfile(file_path):
                    continue

                # Check file modification time
                file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_mtime < cutoff_date:
                    os.remove(file_path)
                    cleanup_count += 1

        except Exception as e:
            print(f"Warning: Audio cleanup failed: {e}")

        if cleanup_count > 0:
            print(f"Cleaned up {cleanup_count} old audio files")

        return cleanup_count

    def cleanup_old_audio_files(self) -> int:
        """Remove audio files older than configured cleanup days.

        Returns:
            Number of files cleaned up
        """
        return self.cleanup_audio_files_static(
            self._tts_cleanup_days, self._project_root
        )

    def _ensure_audio_directory(self) -> str:
        """Ensure audio directory exists and return path."""
        audio_dir = os.path.join(self._project_root, "audio")
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir, exist_ok=True)
        return audio_dir

    @property
    def tts_enabled(self) -> bool:
        """Get TTS enabled status."""
        return self._tts_enabled

    @property
    def tts_voice(self) -> str:
        """Get configured TTS voice."""
        return self._tts_voice
