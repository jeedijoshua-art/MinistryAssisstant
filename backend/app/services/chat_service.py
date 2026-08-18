from typing import Generator
from uuid import UUID
from app.repositories.conversation_repository import ConversationRepository, MessageRepository
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService
from app.services.memory_service import MemoryService
from app.services.bible.bible_service import BibleService
from app.services.bible.reference_parser import ReferenceParser
from app.models.domain import Message

class ChatService:
    def __init__(
        self,
        conversation_repo: ConversationRepository,
        message_repo: MessageRepository,
        gemini_service: GeminiService,
        prompt_service: PromptService,
        memory_service: MemoryService,
        bible_service: BibleService,
        creative_service=None
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.gemini_service = gemini_service
        self.prompt_service = prompt_service
        self.memory_service = memory_service
        self.bible_service = bible_service
        self.creative_service = creative_service

    def stream_conversation(self, conversation_id: UUID, new_message_content: str) -> Generator[str, None, None]:
        import logging
        from app.models.domain import Conversation

        # 1. Get conversation (graceful fallback)
        try:
            conversation = self.conversation_repo.get(conversation_id)
        except Exception as e:
            logging.warning(f"Failed to fetch conversation {conversation_id}: {e}")
            conversation = None

        if not conversation:
            # Create a dummy conversation in memory
            conversation = Conversation(id=conversation_id, church_id=conversation_id, title="Fallback Conversation")

        # 2. Save user message (graceful fallback)
        user_msg = Message(conversation_id=conversation_id, role="user", content=new_message_content)
        try:
            self.message_repo.add(user_msg)
            self.message_repo.session.commit()
        except Exception as e:
            self.message_repo.session.rollback()
            logging.warning(f"Failed to save user message: {e}")

        # 3. Retrieve history (graceful fallback)
        try:
            history = self.message_repo.list_by_conversation(conversation_id)
        except Exception as e:
            logging.warning(f"Failed to fetch history: {e}")
            history = []
            
        # Ensure current message is in history if DB fetch failed to include it
        if not history or history[-1].content != new_message_content:
            history = list(history) + [user_msg]

        messages_dicts = [{"role": m.role, "content": m.content} for m in history]

        # 4. Prepare context (Prompt + Memory)
        try:
            sys_prompt = self.prompt_service.get_system_prompt()
            memory_context = self.memory_service.get_context(conversation)
        except Exception as e:
            logging.warning(f"Failed to load prompts/memory: {e}")
            sys_prompt = "You are a helpful AI Assistant for a church ministry."
            memory_context = ""
        
        # 4.5. Retrieve Bible context
        # We perform a basic search on the latest user message to retrieve relevant verses
        # First try to extract references, then fallback to text search
        bible_context = ""
        try:
            refs = ReferenceParser.extract_all(new_message_content)
            verses = []
            if refs:
                for ref in refs:
                    ref_str = f"{ref.book} {ref.chapter}"
                    if ref.start_verse:
                        ref_str += f":{ref.start_verse}"
                    if ref.end_verse:
                        ref_str += f"-{ref.end_verse}"
                    verses.extend(self.bible_service.resolve_reference(ref_str))
            else:
                # Remove stop words for a better search
                query_words = [w for w in new_message_content.replace('?','').split() if len(w) > 3]
                search_query = " ".join(query_words)
                
                if search_query:
                    verses = self.bible_service.search(search_query, limit=5)
                    
            if verses:
                bible_context = "Relevant Scripture Retrieved by Bible Engine:\n"
                for v in verses:
                    bible_context += f"- {v.chapter.book.name} {v.chapter.chapter_number}:{v.verse_number}: {v.text}\n"
        except Exception as e:
            logging.warning(f"Failed to retrieve Bible context: {e}")

        final_system_instruction = f"{sys_prompt}\n\nContext:\n{memory_context}\n\n{bible_context}"

        tools = [{
            "function_declarations": [
                {
                    "name": "generate_poster",
                    "description": "Use this tool ONLY when the user explicitly requests an image, poster, banner, or wallpaper generation. This tool triggers the Creative Studio to generate the requested media. Do not generate text design concepts. Call this tool immediately instead.",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "theme": {
                                "type": "STRING",
                                "description": "The theme or topic of the poster (e.g. Christmas, Faith)"
                            },
                            "verse": {
                                "type": "STRING",
                                "description": "The Bible verse to include if requested"
                            }
                        },
                        "required": ["theme"]
                    }
                }
            ]
        }]

        # 5. Stream from Gemini and yield tokens, accumulating full response
        full_response = ""
        try:
            stream = self.gemini_service.stream_chat(
                messages=messages_dicts,
                system_instruction=final_system_instruction,
                tools=tools
            )
            for chunk in stream:
                if getattr(chunk, "function_calls", None):
                    import json, asyncio
                    args = chunk.function_calls[0].args
                    theme = args.get("theme", "Church Poster")
                    if self.creative_service:
                        try:
                            project = self.creative_service.create_project(title=theme, media_type="poster")
                            try:
                                loop = asyncio.get_event_loop()
                            except RuntimeError:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                            
                            updated_project = loop.run_until_complete(
                                self.creative_service.generate_project_media(project.id, conversation_id)
                            )
                            
                            image_url = updated_project.editor_state.get("background_image") if updated_project.editor_state else None
                            
                            if not image_url:
                                raise Exception("Failed to generate image URL")
                                
                            response_obj = {
                                "type": "image",
                                "image_url": image_url,
                                "title": updated_project.title,
                                "prompt": updated_project.ai_prompt
                            }
                            json_str = json.dumps(response_obj)
                            full_response += json_str
                            yield json_str
                            
                        except Exception as e:
                            logging.error(f"Image generation failed: {e}")
                            err_obj = {
                                "type": "error",
                                "error_message": f"Image Generation Failed: {str(e)}"
                            }
                            json_str = json.dumps(err_obj)
                            full_response += json_str
                            yield json_str
                    else:
                        yield json.dumps({"type": "error", "error_message": "CreativeService not configured."})
                else:
                    if isinstance(chunk, str):
                        full_response += chunk
                        yield chunk
        finally:
            # 6. Save assistant message after streaming completes
            if full_response:
                assistant_msg = Message(conversation_id=conversation_id, role="assistant", content=full_response)
                try:
                    self.message_repo.add(assistant_msg)
                    self.message_repo.session.commit()
                except Exception as e:
                    self.message_repo.session.rollback()
                    logging.warning(f"Failed to save assistant message: {e}")
