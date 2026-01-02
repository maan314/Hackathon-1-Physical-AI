from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
import asyncio
import re

from src.models.translation import TranslationRequest, TranslationRequestCreate, TranslationPair, SupportedLanguage
from src.database.database import get_db


class TranslationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.supported_languages = {
            "en": SupportedLanguage(language_code="en", language_name="English", is_enabled=True, supports_formatting=True),
            "ur": SupportedLanguage(language_code="ur", language_name="Urdu", is_enabled=True, supports_formatting=True),
        }

    async def request_translation(self, translation_data: TranslationRequestCreate, user_id: Optional[str] = None) -> TranslationRequest:
        # Check if translation already exists and is cached
        existing_translation = await self.get_cached_translation(
            translation_data.content_id,
            translation_data.source_language,
            translation_data.target_language
        )

        if existing_translation:
            return TranslationRequest(
                id=str(hash(f"cached_{translation_data.content_id}"))[:12],
                content_id=translation_data.content_id,
                source_language=translation_data.source_language,
                target_language=translation_data.target_language,
                content_type=translation_data.content_type,
                preserve_formatting=translation_data.preserve_formatting,
                user_id=user_id,
                status="completed",
                translated_content=existing_translation.translated_content,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                completed_at=datetime.utcnow()
            )

        # Create new translation request
        db_request = TranslationRequest(
            id=str(hash(f"trans_{translation_data.content_id}_{datetime.utcnow()}"))[:12],
            content_id=translation_data.content_id,
            source_language=translation_data.source_language,
            target_language=translation_data.target_language,
            content_type=translation_data.content_type,
            preserve_formatting=translation_data.preserve_formatting,
            user_id=user_id,
            status="pending",
            translated_content=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            completed_at=None
        )

        self.db.add(db_request)
        await self.db.commit()
        await self.db.refresh(db_request)

        # Process translation in background
        asyncio.create_task(self._process_translation_request(db_request.id))

        return db_request

    async def _process_translation_request(self, request_id: str):
        """Process translation request in background"""
        # Get the request
        result = await self.db.execute(
            select(TranslationRequest).where(TranslationRequest.id == request_id)
        )
        request = result.scalars().first()

        if not request:
            return

        # Update status to in progress
        request.status = "in_progress"
        request.updated_at = datetime.utcnow()
        self.db.add(request)
        await self.db.commit()

        # Simulate translation process (in real implementation, this would call an AI translation service)
        # For now, we'll implement a simple mock translation
        translated_content = await self._translate_content(
            request.content_id,  # This would be the actual content in a real implementation
            request.source_language,
            request.target_language,
            request.preserve_formatting
        )

        # Update request with translated content
        request.translated_content = translated_content
        request.status = "completed"
        request.completed_at = datetime.utcnow()
        request.updated_at = datetime.utcnow()
        self.db.add(request)
        await self.db.commit()

    async def _translate_content(self, content_id: str, source_lang: str, target_lang: str, preserve_formatting: bool) -> str:
        """
        Translate content from source to target language
        In a real implementation, this would use an AI translation service like OpenAI
        """
        # This is a mock implementation - in reality, this would call an AI service
        # For demonstration purposes, we'll return a placeholder translation
        if target_lang == "ur":
            # Simple mock translation to Urdu
            mock_urdu_content = f"({target_lang.upper()} TRANSLATION) This is the translated content for {content_id}. The original content has been translated from {source_lang} to {target_lang}."

            if preserve_formatting:
                # In a real implementation, we would preserve code blocks, equations, etc.
                # For now, we'll just add a note about preserving formatting
                mock_urdu_content += "\n\n(Formatting preserved: Code blocks, equations, and special formatting maintained)"

            return mock_urdu_content
        else:
            # For other languages, return a simple translated placeholder
            return f"({target_lang.upper()} TRANSLATION) Translated content for {content_id} from {source_lang} to {target_lang}"

    async def get_translation_request(self, request_id: str) -> Optional[TranslationRequest]:
        result = await self.db.execute(
            select(TranslationRequest).where(TranslationRequest.id == request_id)
        )
        request = result.scalars().first()
        return request

    async def get_cached_translation(self, content_id: str, source_lang: str, target_lang: str) -> Optional[TranslationPair]:
        """Check if translation is already cached"""
        # In a real implementation, this would query a translation cache/table
        # For now, we'll return None to indicate no cached translation
        return None

    async def translate_content(self, content: str, source_lang: str, target_lang: str, preserve_formatting: bool = True) -> str:
        """
        Translate content directly (not as a request)
        """
        if target_lang == "ur":
            # Mock translation to Urdu
            translated = f"({target_lang.upper()} TRANSLATION)\n\n{content}"

            if preserve_formatting:
                # Preserve code blocks and equations by identifying and protecting them
                translated = self._preserve_formatting(translated)

            return translated
        else:
            return f"({target_lang.upper()} TRANSLATION) {content}"

    def _preserve_formatting(self, content: str) -> str:
        """
        Preserve code blocks, equations, and other special formatting during translation
        """
        # This is a simplified implementation
        # In a real system, this would use more sophisticated parsing

        # Protect code blocks (```...```)
        code_blocks = []
        def replace_code(match):
            code_blocks.append(match.group(0))
            return f"{{CODE_BLOCK_{len(code_blocks)-1}}}"

        content = re.sub(r'```[\s\S]*?```', replace_code, content)

        # Protect inline code (`...`)
        inline_code = []
        def replace_inline_code(match):
            inline_code.append(match.group(0))
            return f"{{INLINE_CODE_{len(inline_code)-1}}}"

        content = re.sub(r'`[^`]+`', replace_inline_code, content)

        # Protect equations ($...$ or $$...$$)
        equations = []
        def replace_equation(match):
            equations.append(match.group(0))
            return f"{{EQUATION_{len(equations)-1}}}"

        content = re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$', replace_equation, content)

        # In a real implementation, the translation would happen here
        # For now, we'll just return the content with placeholders

        # Restore code blocks
        for i, code_block in enumerate(code_blocks):
            content = content.replace(f"{{CODE_BLOCK_{i}}}", code_block)

        # Restore inline code
        for i, code in enumerate(inline_code):
            content = content.replace(f"{{INLINE_CODE_{i}}}", code)

        # Restore equations
        for i, eq in enumerate(equations):
            content = content.replace(f"{{EQUATION_{i}}}", eq)

        return content

    async def get_supported_languages(self) -> List[SupportedLanguage]:
        return list(self.supported_languages.values())

    async def get_translation_pair(self, content_id: str, source_lang: str, target_lang: str) -> Optional[TranslationPair]:
        """Get a specific translation pair"""
        # In a real implementation, this would query the database for stored translations
        # For now, return None
        return None