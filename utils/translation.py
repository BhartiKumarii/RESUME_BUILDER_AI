# utils/translation.py
import google.generativeai as genai
import json
import os
from config import Config
from functools import lru_cache

class AITranslator:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
        
        # Enhanced language code mapping with better Indian language support
        self.language_codes = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu', 
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            'or': 'Odia',
            'as': 'Assamese'
        }
        
        # Common phrases for blue-collar context
        self.common_phrases = {
            'en': {
                'profession': 'Profession',
                'experience': 'Experience',
                'skills': 'Skills',
                'verification': 'Verification',
                'resume': 'Resume',
                'jobs': 'Jobs',
                'download': 'Download',
                'generate': 'Generate',
                'mobile': 'Mobile Number',
                'otp': 'OTP',
                'verify': 'Verify',
                'continue': 'Continue',
                'save': 'Save',
                'choose_language': 'Choose Your Language',
                'select_profession': 'Select Your Profession',
                'complete_profile': 'Complete Your Profile',
                'id_verification': 'ID Verification',
                'create_resume': 'Create Your Resume',
                'job_recommendations': 'Job Recommendations'
            }
        }
        
        # Cache for translations
        self.translation_cache = self.load_cache()

    def load_cache(self):
        """Load translation cache from file"""
        cache_file = 'instance/translation_cache.json'
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_cache(self):
        """Save translation cache to file"""
        cache_file = 'instance/translation_cache.json'
        os.makedirs('instance', exist_ok=True)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.translation_cache, f, ensure_ascii=False, indent=2)
        except:
            pass

    def translate_text(self, text, target_language, source_language='en'):
        """Translate text using Google Generative AI with context awareness"""
        
        if target_language == source_language:
            return text
            
        if not text or not text.strip():
            return text
            
        # Check cache first
        cache_key = f"{source_language}_{target_language}_{text}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]
        
        # If no API key, return original text
        if not self.api_key or not self.model:
            return text
        
        try:
            target_lang_name = self.language_codes.get(target_language, target_language)
            source_lang_name = self.language_codes.get(source_language, source_language)
            
            prompt = f"""
            Translate the following text from {source_lang_name} to {target_lang_name}.
            
            CONTEXT: This is for a blue-collar resume building application in India. 
            The translation should be natural, professional, and appropriate for workers in skilled trades.
            Use common, easily understandable terms that blue-collar workers would recognize.
            
            IMPORTANT: Return ONLY the translated text without any additional text, explanations, or notes.
            Do not add any prefixes, suffixes, or formatting marks.
            
            Text to translate: "{text}"
            
            Translated text:
            """
            
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            # Clean up the response - remove quotes if present
            if translated_text.startswith('"') and translated_text.endswith('"'):
                translated_text = translated_text[1:-1]
            elif translated_text.startswith("'") and translated_text.endswith("'"):
                translated_text = translated_text[1:-1]
            
            # Remove any explanatory text that might have been added
            if ':' in translated_text:
                translated_text = translated_text.split(':', 1)[-1].strip()
            
            # Cache the translation
            self.translation_cache[cache_key] = translated_text
            self.save_cache()
            
            return translated_text
            
        except Exception as e:
            print(f"Translation error for '{text}': {e}")
            return text

    def translate_dict(self, data_dict, target_language, source_language='en'):
        """Translate all string values in a dictionary"""
        if target_language == source_language:
            return data_dict
            
        translated_dict = {}
        for key, value in data_dict.items():
            if isinstance(value, str):
                translated_dict[key] = self.translate_text(value, target_language, source_language)
            elif isinstance(value, dict):
                translated_dict[key] = self.translate_dict(value, target_language, source_language)
            elif isinstance(value, list):
                translated_dict[key] = [self.translate_text(item, target_language, source_language) 
                                      if isinstance(item, str) else item for item in value]
            else:
                translated_dict[key] = value
        return translated_dict

    def batch_translate(self, texts, target_language, source_language='en'):
        """Translate multiple texts at once"""
        if target_language == source_language:
            return texts
            
        return [self.translate_text(text, target_language, source_language) for text in texts]

    def get_common_phrase(self, phrase_key, language='en'):
        """Get common translated phrases"""
        if language == 'en':
            return self.common_phrases['en'].get(phrase_key, phrase_key)
        
        # Translate if not English
        english_phrase = self.common_phrases['en'].get(phrase_key, phrase_key)
        return self.translate_text(english_phrase, language)

# Global translator instance
translator = AITranslator()