"""
Chatbot Response Generator for AstroGuy AI
Generates responses based on user queries
"""

import random
import re
from typing import Dict, Optional, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.chatbot_knowledge import CHATBOT_KNOWLEDGE, KEYWORD_MAPPINGS
from data.horoscope_data import HOROSCOPE_DATA


class AstroChatbot:
    """AI Chatbot for Vedic Astrology queries"""
    
    def __init__(self):
        self.knowledge = CHATBOT_KNOWLEDGE
        self.keywords = KEYWORD_MAPPINGS
    
    def generate_response(self, message: str, user_chart: Optional[Dict] = None, 
                         language: str = "en") -> str:
        """Generate a response based on user message"""
        message_lower = message.lower().strip()
        
        # Check for greetings
        if self._contains_any(message_lower, self.keywords["greetings"]):
            return self._get_random_response("greetings", language)
        
        # Check for Rasi queries
        if self._contains_any(message_lower, self.keywords["rasi_keywords"]):
            return self._handle_rasi_query(message_lower, user_chart, language)
        
        # Check for Nakshatra queries
        if self._contains_any(message_lower, self.keywords["nakshatra_keywords"]):
            return self._handle_nakshatra_query(message_lower, user_chart, language)
        
        # Check for Planet queries
        planet_response = self._handle_planet_query(message_lower, language)
        if planet_response:
            return planet_response
        
        # Check for Career queries
        if self._contains_any(message_lower, self.keywords["career_keywords"]):
            return self._handle_career_query(user_chart, language)
        
        # Check for Love/Relationship queries
        if self._contains_any(message_lower, self.keywords["love_keywords"]):
            return self._handle_love_query(user_chart, language)
        
        # Check for Health queries
        if self._contains_any(message_lower, self.keywords["health_keywords"]):
            return self._handle_health_query(user_chart, language)
        
        # Check for Finance queries
        if self._contains_any(message_lower, self.keywords["finance_keywords"]):
            return self._handle_finance_query(user_chart, language)
        
        # Check for Remedy queries
        if self._contains_any(message_lower, self.keywords["remedy_keywords"]):
            return self.knowledge["remedies"]["general"][language]
        
        # Check for Dosha queries
        if self._contains_any(message_lower, self.keywords["dosha_keywords"]):
            return self._handle_dosha_query(message_lower, language)
        
        # Check for Compatibility queries
        if self._contains_any(message_lower, self.keywords["compatibility_keywords"]):
            return self._handle_compatibility_query(language)
        
        # Check for Birth Chart queries
        if self._contains_any(message_lower, self.keywords["birthchart_keywords"]):
            return self._handle_birthchart_query(user_chart, language)
        
        # Default response
        return self._get_random_response("default_responses", language)
    
    def _contains_any(self, message: str, keywords: List[str]) -> bool:
        """Check if message contains any of the keywords"""
        return any(keyword in message for keyword in keywords)
    
    def _get_random_response(self, category: str, language: str) -> str:
        """Get a random response from a category"""
        responses = self.knowledge[category][language]
        return random.choice(responses)
    
    def _handle_rasi_query(self, message: str, user_chart: Optional[Dict], 
                          language: str) -> str:
        """Handle Rasi-related queries"""
        rasi_keys = list(self.knowledge["rasi_info"].keys())
        
        # Check if specific Rasi is mentioned
        for rasi in rasi_keys:
            if rasi.lower() in message:
                return self.knowledge["rasi_info"][rasi][language]
        
        # If user has chart, return their Rasi info
        if user_chart:
            rasi_name = user_chart["rasi"]["english_name"]
            return self.knowledge["rasi_info"].get(rasi_name, {}).get(language, "")
        
        # Ask for birth details
        if language == "ta":
            return "உங்கள் ராசியை அறிய, தயவுசெய்து உங்கள் பிறந்த தேதி மற்றும் நேரத்தை உள்ளிடவும்."
        return "Please enter your birth date and time to know your Rasi."
    
    def _handle_nakshatra_query(self, message: str, user_chart: Optional[Dict], 
                               language: str) -> str:
        """Handle Nakshatra-related queries"""
        nak_keys = list(self.knowledge["nakshatra_info"].keys())
        
        # Check if specific Nakshatra is mentioned
        for nak in nak_keys:
            if nak.lower() in message:
                return self.knowledge["nakshatra_info"][nak][language]
        
        # If user has chart, return their Nakshatra info
        if user_chart:
            nak_name = user_chart["nakshatra"]["name"]
            return self.knowledge["nakshatra_info"].get(nak_name, {}).get(language, "")
        
        # Ask for birth details
        if language == "ta":
            return "உங்கள் நட்சத்திரத்தை அறிய, தயவுசெய்து உங்கள் பிறந்த தேதி மற்றும் நேரத்தை உள்ளிடவும்."
        return "Please enter your birth date and time to know your Nakshatra."
    
    def _handle_planet_query(self, message: str, language: str) -> Optional[str]:
        """Handle Planet-related queries"""
        planet_map = self.keywords["planet_keywords"]
        
        for keyword, planet in planet_map.items():
            if keyword in message:
                return self.knowledge["planet_info"][planet][language]
        
        return None
    
    def _handle_career_query(self, user_chart: Optional[Dict], language: str) -> str:
        """Handle Career-related queries"""
        if user_chart:
            rasi_name = user_chart["rasi"]["english_name"]
            rasi_data = HOROSCOPE_DATA.get(rasi_name, {})
            if rasi_data:
                return rasi_data.get(language, {}).get("career", 
                    self.knowledge["remedies"]["career"][language])
        return self.knowledge["remedies"]["career"][language]
    
    def _handle_love_query(self, user_chart: Optional[Dict], language: str) -> str:
        """Handle Love/Relationship queries"""
        if user_chart:
            rasi_name = user_chart["rasi"]["english_name"]
            rasi_data = HOROSCOPE_DATA.get(rasi_name, {})
            if rasi_data:
                return rasi_data.get(language, {}).get("love",
                    self.knowledge["remedies"]["love"][language])
        return self.knowledge["remedies"]["love"][language]
    
    def _handle_health_query(self, user_chart: Optional[Dict], language: str) -> str:
        """Handle Health-related queries"""
        if user_chart:
            rasi_name = user_chart["rasi"]["english_name"]
            rasi_data = HOROSCOPE_DATA.get(rasi_name, {})
            if rasi_data:
                return rasi_data.get(language, {}).get("health",
                    self.knowledge["remedies"]["health"][language])
        return self.knowledge["remedies"]["health"][language]
    
    def _handle_finance_query(self, user_chart: Optional[Dict], language: str) -> str:
        """Handle Finance-related queries"""
        if user_chart:
            rasi_name = user_chart["rasi"]["english_name"]
            rasi_data = HOROSCOPE_DATA.get(rasi_name, {})
            if rasi_data:
                return rasi_data.get(language, {}).get("finance",
                    self.knowledge["remedies"]["finance"][language])
        return self.knowledge["remedies"]["finance"][language]
    
    def _handle_dosha_query(self, message: str, language: str) -> str:
        """Handle Dosha-related queries"""
        if "manglik" in message or "மாங்கலிக" in message:
            return self.knowledge["doshas"]["manglik"][language]
        elif "nadi" in message or "நாடி" in message:
            return self.knowledge["doshas"]["nadi"][language]
        elif "bhakoot" in message or "பாகூட்" in message:
            return self.knowledge["doshas"]["bhakoot"][language]
        
        if language == "ta":
            return "முக்கிய தோஷங்கள்: மாங்கலிக தோஷம் (செவ்வாய்), நாடி தோஷம், பாகூட் தோஷம். எந்த தோஷத்தைப் பற்றி அறிய விரும்புகிறீர்கள்?"
        return "Major doshas: Manglik Dosha (Mars), Nadi Dosha, Bhakoot Dosha. Which dosha would you like to know about?"
    
    def _handle_compatibility_query(self, language: str) -> str:
        """Handle Compatibility queries"""
        if language == "ta":
            return "அஷ்டகூட பொருத்தம் 8 அம்சங்களை அடிப்படையாகக் கொண்டது: வர்ணம், வசியம், தாரா, யோனி, கிரக மைத்திரி, கணம், பாகூட், நாடி. பொருத்தம் பார் பக்கத்தில் உங்கள் விவரங்களை உள்ளிடவும்."
        return "Ashtakoota matching is based on 8 aspects: Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, and Nadi. Please enter your details in the Match section."
    
    def _handle_birthchart_query(self, user_chart: Optional[Dict], language: str) -> str:
        """Handle Birth Chart queries"""
        if user_chart:
            if language == "ta":
                return f"உங்கள் ஜாதகம்: ராசி - {user_chart['rasi']['tamil_name']}, நட்சத்திரம் - {user_chart['nakshatra']['tamil_name']} (பாதம் {user_chart['nakshatra']['pada']}), லக்னம் - {user_chart['lagna']['name']}. விரிவான ஜாதகத்தை Birth Chart பக்கத்தில் காணலாம்."
            return f"Your birth chart: Rasi - {user_chart['rasi']['english_name']}, Nakshatra - {user_chart['nakshatra']['name']} (Pada {user_chart['nakshatra']['pada']}), Lagna - {user_chart['lagna']['name']}. See detailed chart in Birth Chart section."
        
        if language == "ta":
            return "உங்கள் ஜாதகத்தைப் பார்க்க, தயவுசெய்து முதல் பக்கத்தில் உங்கள் பிறந்த தேதி மற்றும் நேரத்தை உள்ளிடவும்."
        return "To see your birth chart, please enter your birth date and time on the home page."


# Create singleton instance
chatbot = AstroChatbot()


def get_chatbot_response(message: str, user_chart: Optional[Dict] = None, 
                        language: str = "en") -> str:
    """Convenience function to get chatbot response"""
    return chatbot.generate_response(message, user_chart, language)
