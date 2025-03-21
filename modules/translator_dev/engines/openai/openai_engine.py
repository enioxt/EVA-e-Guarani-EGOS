from dataclasses import dataclass
import os
import json
import time
import re
from typing import Optional, List, Dict, Any, Tuple
import logging
try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Optional imports for format-specific handlers
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Import term manager
try:
    from modules.translator_dev.core.term_manager import TermManager
    TERM_MANAGER_AVAILABLE = True
except ImportError:
    TERM_MANAGER_AVAILABLE = False

# Setup logging
logger = logging.getLogger("openai_engine")

@dataclass
class OpenAIConfig:
    api_key: Optional[str] = None
    model: str = "gpt-4o"
    max_tokens: int = 4096
    temperature: float = 0.3
    retries: int = 3
    retry_delay: float = 2.0
    timeout: float = 60.0
    preserve_formatting: bool = True
    system_prompt: str = "You are a translator that translates Portuguese to English. Maintain the format and structure of the original text."

class OpenAITranslator:
    def __init__(self, config: Optional[OpenAIConfig] = None):
        """Initialize the OpenAI translator
        
        Args:
            config: OpenAIConfig with settings for the OpenAI API
        """
        self.config = config or OpenAIConfig()
        self._client = None
        
        # Initialize term manager if available
        self.term_manager = None
        if TERM_MANAGER_AVAILABLE:
            try:
                self.term_manager = TermManager()
                logger.info("Term manager initialized for technical terminology handling")
            except Exception as e:
                logger.warning(f"Failed to initialize term manager: {str(e)}")
        
        if not OPENAI_AVAILABLE:
            logger.warning("OpenAI package not available. Install with 'pip install openai'")
        
        if not self.config.api_key:
            # Try to get API key from environment
            self.config.api_key = os.environ.get("OPENAI_API_KEY")
            
        if not self.config.api_key:
            logger.warning("No OpenAI API key provided. Set OPENAI_API_KEY environment variable or provide in config")
    
    @property
    def client(self):
        """Get or create OpenAI client"""
        if not self._client and OPENAI_AVAILABLE and self.config.api_key:
            self._client = OpenAI(api_key=self.config.api_key, timeout=self.config.timeout)
        return self._client
    
    def _create_translation_prompt(self, text: str) -> List[Dict[str, str]]:
        """Create a prompt for translation
        
        Args:
            text: Text to translate from Portuguese to English
            
        Returns:
            List of message dictionaries for the API
        """
        messages = [
            {"role": "system", "content": self.config.system_prompt},
            {"role": "user", "content": f"Translate the following Portuguese text to English:\n\n{text}"}
        ]
        
        return messages
    
    def translate(self, text: str) -> str:
        """Translate a text from Portuguese to English
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return text
            
        if not self.client:
            logger.error("OpenAI client not available. Check API key and installation.")
            return text
        
        # Apply term management if available
        preprocessed_text = text
        placeholder_map = {}
        
        if self.term_manager:
            try:
                # Replace technical terms with placeholders
                preprocessed_text, placeholder_map = self.term_manager.preprocess_text(text, "pt")
                logger.debug(f"Preprocessed text with {len(placeholder_map)} technical terms")
            except Exception as e:
                logger.warning(f"Term preprocessing failed: {str(e)}")
                preprocessed_text = text
            
        # Prepare the translation prompt
        messages = self._create_translation_prompt(preprocessed_text)
        
        # Retry logic for API calls
        for attempt in range(self.config.retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=messages,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                if response.choices and len(response.choices) > 0:
                    translated_text = response.choices[0].message.content.strip()
                    
                    # Restore technical terms if we used placeholders
                    if self.term_manager and placeholder_map:
                        try:
                            translated_text = self.term_manager.postprocess_text(translated_text, placeholder_map)
                            # Apply additional terminology correction
                            translated_text = self.term_manager.apply_terminology(translated_text, "pt", "en")
                        except Exception as e:
                            logger.warning(f"Term postprocessing failed: {str(e)}")
                    
                    return translated_text
                else:
                    logger.warning("Empty response from OpenAI API")
                    
            except Exception as e:
                logger.warning(f"Error calling OpenAI API (attempt {attempt+1}/{self.config.retries}): {str(e)}")
                if attempt < self.config.retries - 1:
                    time.sleep(self.config.retry_delay)
                else:
                    logger.error(f"Failed to translate after {self.config.retries} attempts")
                    return text
        
        return text
    
    def translate_batch(self, texts: List[str], batch_size: int = 1) -> List[str]:
        """Translate a batch of texts
        
        Args:
            texts: List of texts to translate
            batch_size: Number of texts to translate in a single API call (1 by default for simplicity)
            
        Returns:
            List of translated texts
        """
        if not texts:
            return []
            
        results = []
        
        # Simple implementation: translate one by one
        # TODO: Implement true batching with a single API call for multiple texts
        for text in texts:
            translated = self.translate(text)
            results.append(translated)
            
        return results
    
    def translate_file_content(self, content: str, file_type: str = "") -> str:
        """Translate file content with special handling based on file type
        
        Args:
            content: File content to translate
            file_type: Type of file (e.g., "py", "md", "html")
            
        Returns:
            Translated file content
        """
        if not content or not content.strip():
            return content
            
        # Store original prompt to restore later
        original_prompt = self.config.system_prompt
        
        try:
            # Select specialized handler based on file type
            if file_type in ["py", "js", "java", "c", "cpp", "h", "cs", "go", "rb"]:
                return self._translate_code(content, file_type)
            elif file_type in ["md", "markdown"]:
                return self._translate_markdown(content)
            elif file_type in ["html", "htm", "xml"]:
                return self._translate_html(content)
            elif file_type in ["json"]:
                return self._translate_json(content)
            elif file_type in ["yaml", "yml"]:
                return self._translate_yaml(content)
            else:
                # Default handler for other file types
                self.config.system_prompt = """
                You are a translator that translates Portuguese to English.
                Maintain the format and structure of the original text.
                Preserve any technical terms, code, or special formatting.
                """
                return self.translate(content)
        finally:
            # Restore original prompt
            self.config.system_prompt = original_prompt

    def _translate_code(self, content: str, file_type: str) -> str:
        """Specialized handler for code files
        
        Args:
            content: Code content to translate
            file_type: Type of code file (e.g., "py", "js")
            
        Returns:
            Translated code with comments and strings translated
        """
        self.config.system_prompt = """
        You are a specialized code translator. Translate code comments and strings from Portuguese to English.
        DO NOT modify any code logic, variables, function names, or programming syntax.
        Preserve all indentation, formatting, and structure exactly.
        Only translate text within comments (// /* */ ''', #, etc.) and string literals.
        """
        return self.translate(content)
        
    def _translate_markdown(self, content: str) -> str:
        """Specialized handler for Markdown files with preservation of formatting
        
        Args:
            content: Markdown content to translate
            
        Returns:
            Translated markdown with preserved formatting elements
        """
        # Define patterns for elements to protect
        code_block_pattern = r'```[\s\S]*?```'
        inline_code_pattern = r'`[^`]+`'
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
        
        # Find and store elements to protect
        code_blocks = re.findall(code_block_pattern, content)
        inline_codes = re.findall(inline_code_pattern, content)
        links = [(m.group(1), m.group(2)) for m in re.finditer(link_pattern, content)]
        images = [(m.group(1), m.group(2)) for m in re.finditer(image_pattern, content)]
        
        # Replace elements with placeholders
        placeholder_map = {}
        
        # Replace code blocks
        for i, block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            content = content.replace(block, placeholder)
            placeholder_map[placeholder] = block
        
        # Replace inline code
        for i, code in enumerate(inline_codes):
            placeholder = f"__INLINE_CODE_{i}__"
            content = content.replace(code, placeholder)
            placeholder_map[placeholder] = code
        
        # Replace links
        for i, (text, url) in enumerate(links):
            original = f"[{text}]({url})"
            placeholder = f"__LINK_{i}__"
            content = content.replace(original, placeholder)
            placeholder_map[placeholder] = original
        
        # Replace images
        for i, (alt, url) in enumerate(images):
            original = f"![{alt}]({url})"
            placeholder = f"__IMAGE_{i}__"
            content = content.replace(original, placeholder)
            placeholder_map[placeholder] = original
        
        # Set a specialized prompt for markdown
        self.config.system_prompt = """
        You are a specialized document translator that translates Portuguese to English.
        Maintain all markdown formatting like headings (#), lists (-, *, 1.), bold (**), italic (*), blockquotes (>), etc.
        Do not translate placeholders like __CODE_BLOCK_0__, __LINK_1__, etc. - leave these exactly as they are.
        Preserve all formatting, spacing, and document structure.
        """
        
        # Translate content
        translated = self.translate(content)
        
        # Restore protected elements
        for placeholder, original in placeholder_map.items():
            translated = translated.replace(placeholder, original)
        
        return translated
    
    def _translate_html(self, content: str) -> str:
        """Specialized handler for HTML files with tag preservation
        
        Args:
            content: HTML content to translate
            
        Returns:
            Translated HTML with preserved tags and structure
        """
        if BS4_AVAILABLE:
            try:
                # Parse HTML with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Find all text nodes that are not in scripts or styles
                text_nodes = []
                placeholders = {}
                
                def collect_text_nodes(element):
                    # Skip script and style elements
                    if element.name in ['script', 'style']:
                        return
                    
                    # Process text nodes - check if string exists and is not None
                    if element.string is not None and element.string.strip():
                        placeholder = f"__TEXT_{len(text_nodes)}__"
                        text_nodes.append(element.string)
                        placeholders[placeholder] = element.string
                        element.string.replace_with(placeholder)
                    
                    # Process children
                    for child in element.children:
                        if hasattr(child, 'name'):
                            collect_text_nodes(child)
                
                # Collect text nodes
                collect_text_nodes(soup)
                
                # Translate all text nodes at once
                if text_nodes:
                    self.config.system_prompt = """
                    You are a translator that translates text from Portuguese to English.
                    Translate each line independently.
                    Maintain any formatting or special characters.
                    """
                    
                    translated_texts = self.translate_batch(text_nodes)
                    
                    # Update placeholders with translations
                    html_content = str(soup)
                    for i, placeholder in enumerate(placeholders.keys()):
                        html_content = html_content.replace(placeholder, translated_texts[i])
                    
                    return html_content
                
                return content
            
            except Exception as e:
                logger.warning(f"Error processing HTML with BeautifulSoup: {str(e)}. Falling back to prompt-based translation.")
        
        # Fallback to prompt-based translation
        self.config.system_prompt = """
        You are a specialized HTML translator. Translate from Portuguese to English while preserving:
        1. All HTML/XML tags and attributes - do not modify ANY tags
        2. All JavaScript and CSS code
        3. Only translate text content between tags
        4. Preserve all whitespace, indentation, and formatting
        """
        return self.translate(content)
    
    def _translate_json(self, content: str) -> str:
        """Specialized handler for JSON files to translate only string values
        
        Args:
            content: JSON content to translate
            
        Returns:
            Translated JSON with preserved structure
        """
        try:
            # Parse JSON
            data = json.loads(content)
            
            # Function to recursively translate string values
            def translate_values(obj):
                if isinstance(obj, dict):
                    return {k: translate_values(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [translate_values(item) for item in obj]
                elif isinstance(obj, str) and obj.strip():
                    # Only translate non-empty strings
                    return self.translate(obj)
                else:
                    return obj
            
            # Translate all string values
            translated_data = translate_values(data)
            
            # Convert back to JSON with the same formatting
            return json.dumps(translated_data, indent=4, ensure_ascii=False)
            
        except Exception as e:
            logger.warning(f"Error processing JSON: {str(e)}. Falling back to prompt-based translation.")
            
            # Fallback to prompt-based translation
            self.config.system_prompt = """
            You are a specialized JSON translator. Translate from Portuguese to English while preserving:
            1. All JSON structure and syntax
            2. Only translate string values, not keys
            3. Preserve all numbers, booleans, and null values exactly
            4. Maintain all quoting, brackets, commas and formatting
            """
            return self.translate(content)
    
    def _translate_yaml(self, content: str) -> str:
        """Specialized handler for YAML files to translate only string values
        
        Args:
            content: YAML content to translate
            
        Returns:
            Translated YAML with preserved structure
        """
        if YAML_AVAILABLE:
            try:
                # Parse YAML
                data = yaml.safe_load(content)
                
                # Function to recursively translate string values (same as JSON)
                def translate_values(obj):
                    if isinstance(obj, dict):
                        return {k: translate_values(v) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [translate_values(item) for item in obj]
                    elif isinstance(obj, str) and obj.strip():
                        # Only translate non-empty strings
                        return self.translate(obj)
                    else:
                        return obj
                
                # Translate all string values
                translated_data = translate_values(data)
                
                # Convert back to YAML with the same formatting
                return yaml.dump(translated_data, allow_unicode=True)
                
            except Exception as e:
                logger.warning(f"Error processing YAML: {str(e)}. Falling back to prompt-based translation.")
        
        # Fallback to prompt-based translation
        self.config.system_prompt = """
        You are a specialized YAML translator. Translate from Portuguese to English while preserving:
        1. All YAML structure and syntax
        2. Only translate string values, not keys
        3. Preserve all numbers, booleans, and null values exactly
        4. Maintain all indentation, dashes, colons and formatting
        """
        return self.translate(content) 