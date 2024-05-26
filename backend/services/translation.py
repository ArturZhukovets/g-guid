from abc import ABC, abstractmethod

import aiohttp
import pycountry

from core.config import settings


class LanguageToLocaleConverter:

    @staticmethod
    def convert(language: str) -> str:
        language_obj = pycountry.languages.get(name=language)
        if language_obj and language_obj.alpha_2:
            return language_obj.alpha_2
        raise ValueError("Specified language does not exist")


class Translator(ABC):

    @abstractmethod
    def translate_text(self, text: str, src_lang: str, tgt_lang: str):
        pass

    @abstractmethod
    def translate_file(self, file_path: str, src_lang: str, tgt_lang: str):
        pass


class TranslatorLingvanex(Translator):

    def __init__(self) -> None:
        self.url = settings.LINGVANEX_API_URL
        self._token = settings.LINGVANEX_API_KEY

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}"
        }

    async def translate_text(self, text: str, src_lang: str, tgt_lang: str):
        src_lang_locale = LanguageToLocaleConverter.convert(src_lang)
        tgt_lang_locale = LanguageToLocaleConverter.convert(tgt_lang)
        payload = {
            "from": src_lang_locale,
            "to": tgt_lang_locale,
            "platform": "api",
            "data": text,
        }
        headers = self._get_headers()
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data['result']

    def translate_file(self, file_path: str, src_lang: str, tgt_lang: str):
        pass

