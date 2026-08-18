"""Persistence entities. Keep business behaviour in services, not ORM models."""
from __future__ import annotations

from typing import Any, Optional
from uuid import UUID, uuid4
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String, Text, Table, DateTime, func, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base, UUIDTimestampMixin

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

class User(UUIDTimestampMixin, Base):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(160))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    church_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("churches.id", ondelete="SET NULL"), index=True)
    church: Mapped[Optional["Church"]] = relationship(back_populates="users")
    roles: Mapped[list["Role"]] = relationship(secondary=user_roles, back_populates="users")


class Role(UUIDTimestampMixin, Base):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    users: Mapped[list[User]] = relationship(secondary=user_roles, back_populates="roles")
    permissions: Mapped[list["Permission"]] = relationship(secondary=role_permissions, back_populates="roles")


class Permission(UUIDTimestampMixin, Base):
    __tablename__ = "permissions"
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    roles: Mapped[list[Role]] = relationship(secondary=role_permissions, back_populates="permissions")


class AuditLog(UUIDTimestampMixin, Base):
    __tablename__ = "audit_logs"
    user_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(100), index=True)
    resource_type: Mapped[str] = mapped_column(String(100), index=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(255))
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    ip_address: Mapped[Optional[str]] = mapped_column(String(50))
    user: Mapped[Optional[User]] = relationship()



class Church(UUIDTimestampMixin, Base):
    __tablename__ = "churches"
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    primary_theme: Mapped[str] = mapped_column(String(50), default="Dark Blue")
    accent: Mapped[str] = mapped_column(String(50), default="Gold")
    users: Mapped[list[User]] = relationship(back_populates="church")
    pastors: Mapped[list[Pastor]] = relationship(back_populates="church")
    conversations: Mapped[list[Conversation]] = relationship(back_populates="church")


class Pastor(UUIDTimestampMixin, Base):
    __tablename__ = "pastors"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), index=True)
    full_name: Mapped[str] = mapped_column(String(160), index=True)
    email: Mapped[Optional[str]] = mapped_column(String(254), unique=True)
    church: Mapped[Church] = relationship(back_populates="pastors")
    sermons: Mapped[list[Sermon]] = relationship(back_populates="pastor")


class Conversation(UUIDTimestampMixin, Base):
    __tablename__ = "conversations"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255), default="Untitled conversation")
    status: Mapped[str] = mapped_column(String(30), default="active", index=True)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    church: Mapped[Church] = relationship(back_populates="conversations")
    messages: Mapped[list[Message]] = relationship(back_populates="conversation", cascade="all, delete-orphan")


class Message(UUIDTimestampMixin, Base):
    __tablename__ = "messages"
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(String(30), index=True)
    content: Mapped[str] = mapped_column(Text)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    conversation: Mapped[Conversation] = relationship(back_populates="messages")


class Sermon(UUIDTimestampMixin, Base):
    __tablename__ = "sermons"
    pastor_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("pastors.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    theme: Mapped[Optional[str]] = mapped_column(String(255))
    main_verse: Mapped[Optional[str]] = mapped_column(String(255))
    bible_version: Mapped[str] = mapped_column(String(50), default="KJV")
    audience: Mapped[Optional[str]] = mapped_column(String(255))
    occasion: Mapped[Optional[str]] = mapped_column(String(255))
    estimated_duration: Mapped[Optional[int]] = mapped_column(Integer) # in minutes
    date_preached: Mapped[Optional[str]] = mapped_column(String(50))
    content: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="draft", index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    pastor: Mapped[Optional[Pastor]] = relationship(back_populates="sermons")
    sections: Mapped[list[SermonSection]] = relationship(back_populates="sermon", cascade="all, delete-orphan", order_by="SermonSection.order_index")
    history: Mapped[list[SermonHistory]] = relationship(back_populates="sermon", cascade="all, delete-orphan", order_by="SermonHistory.created_at.desc()")
    tags: Mapped[list[SermonTag]] = relationship(secondary="sermon_tags_link", back_populates="sermons")
    references: Mapped[list[SermonReference]] = relationship(back_populates="sermon", cascade="all, delete-orphan")
    creative_projects: Mapped[list["CreativeProject"]] = relationship(back_populates="sermon")
    communication_projects: Mapped[list["CommunicationProject"]] = relationship(back_populates="sermon")


class SermonSection(UUIDTimestampMixin, Base):
    __tablename__ = "sermon_sections"
    sermon_id: Mapped[UUID] = mapped_column(ForeignKey("sermons.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    sermon: Mapped[Sermon] = relationship(back_populates="sections")


class SermonHistory(UUIDTimestampMixin, Base):
    __tablename__ = "sermon_history"
    sermon_id: Mapped[UUID] = mapped_column(ForeignKey("sermons.id", ondelete="CASCADE"), index=True)
    content_snapshot: Mapped[str] = mapped_column(Text)
    version_note: Mapped[Optional[str]] = mapped_column(String(255))
    sermon: Mapped[Sermon] = relationship(back_populates="history")


class SermonTemplate(UUIDTimestampMixin, Base):
    __tablename__ = "sermon_templates"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    structure: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)


class SermonTag(UUIDTimestampMixin, Base):
    __tablename__ = "sermon_tags"
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    sermons: Mapped[list[Sermon]] = relationship(secondary="sermon_tags_link", back_populates="tags")


class SermonTagsLink(Base):
    __tablename__ = "sermon_tags_link"
    sermon_id: Mapped[UUID] = mapped_column(ForeignKey("sermons.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("sermon_tags.id", ondelete="CASCADE"), primary_key=True)


class SermonReference(UUIDTimestampMixin, Base):
    __tablename__ = "sermon_references"
    sermon_id: Mapped[UUID] = mapped_column(ForeignKey("sermons.id", ondelete="CASCADE"), index=True)
    verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)
    reference_string: Mapped[str] = mapped_column(String(255))
    sermon: Mapped[Sermon] = relationship(back_populates="references")


class Prayer(UUIDTimestampMixin, Base):
    __tablename__ = "prayers"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(String(100), index=True) # e.g., Healing, Family
    bible_verse: Mapped[Optional[str]] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    closing: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), default="draft")

class Devotional(UUIDTimestampMixin, Base):
    __tablename__ = "devotionals"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(255))
    main_verse: Mapped[str] = mapped_column(String(255))
    reflection: Mapped[str] = mapped_column(Text)
    life_application: Mapped[Optional[str]] = mapped_column(Text)
    prayer: Mapped[Optional[str]] = mapped_column(Text)
    challenge: Mapped[Optional[str]] = mapped_column(Text)
    reading_time: Mapped[Optional[int]] = mapped_column(Integer) # in minutes
    status: Mapped[str] = mapped_column(String(50), default="draft")

class BibleCharacter(UUIDTimestampMixin, Base):
    __tablename__ = "bible_characters"
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    biography: Mapped[Optional[str]] = mapped_column(Text)
    timeline: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=dict)
    family: Mapped[Optional[dict[str, Any]]] = mapped_column(JSONB, default=dict)
    important_events: Mapped[Optional[list[str]]] = mapped_column(JSONB, default=list)
    lessons: Mapped[Optional[list[str]]] = mapped_column(JSONB, default=list)


class BibleVersion(UUIDTimestampMixin, Base):
    __tablename__ = "bible_versions"
    code: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    language: Mapped[str] = mapped_column(String(64), default="English", index=True)


class VerseHistory(UUIDTimestampMixin, Base):
    __tablename__ = "verse_history"
    bible_version_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("bible_versions.id", ondelete="SET NULL"), index=True)
    reference: Mapped[str] = mapped_column(String(120), index=True)
    content: Mapped[Optional[str]] = mapped_column(Text)
    bible_version: Mapped[Optional[BibleVersion]] = relationship()



class Preferences(UUIDTimestampMixin, Base):
    __tablename__ = "preferences"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), unique=True, index=True)
    settings: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    church: Mapped[Church] = relationship()


class ChurchProfile(UUIDTimestampMixin, Base):
    __tablename__ = "church_profiles"
    church_name: Mapped[str] = mapped_column(String, nullable=False, default="My Church")
    pastor_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    brand_colors: Mapped[Optional[str]] = mapped_column(String, nullable=True)


class PromptHistory(UUIDTimestampMixin, Base):
    __tablename__ = "prompt_history"
    module: Mapped[str] = mapped_column(String(80), index=True)
    prompt: Mapped[str] = mapped_column(Text)
    response_summary: Mapped[Optional[str]] = mapped_column(Text)


class AIUsage(UUIDTimestampMixin, Base):
    __tablename__ = "ai_usage"
    module: Mapped[str] = mapped_column(String(80), index=True)
    provider: Mapped[str] = mapped_column(String(80), default="gemini", index=True)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)


Index("ix_messages_conversation_created", Message.conversation_id, Message.created_at)
Index("ix_prompt_history_module_created", PromptHistory.module, PromptHistory.created_at)
Index("ix_ai_usage_provider_created", AIUsage.provider, AIUsage.created_at)

# Bible Engine Models
class BibleTranslation(UUIDTimestampMixin, Base):
    __tablename__ = "bible_translations"
    code: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    language: Mapped[str] = mapped_column(String(64), default="English")
    books: Mapped[list["BibleBook"]] = relationship(back_populates="translation", cascade="all, delete-orphan")

class BibleBook(UUIDTimestampMixin, Base):
    __tablename__ = "bible_books"
    translation_id: Mapped[UUID] = mapped_column(ForeignKey("bible_translations.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    abbreviation: Mapped[str] = mapped_column(String(20))
    testament: Mapped[str] = mapped_column(String(20))
    book_number: Mapped[int] = mapped_column(Integer)
    translation: Mapped["BibleTranslation"] = relationship(back_populates="books")
    chapters: Mapped[list["BibleChapter"]] = relationship(back_populates="book", cascade="all, delete-orphan")
    summary: Mapped[Optional["BookSummary"]] = relationship(back_populates="book", uselist=False)

class BibleChapter(UUIDTimestampMixin, Base):
    __tablename__ = "bible_chapters"
    book_id: Mapped[UUID] = mapped_column(ForeignKey("bible_books.id", ondelete="CASCADE"), index=True)
    chapter_number: Mapped[int] = mapped_column(Integer, index=True)
    book: Mapped["BibleBook"] = relationship(back_populates="chapters")
    verses: Mapped[list["BibleVerse"]] = relationship(back_populates="chapter", cascade="all, delete-orphan")
    summary: Mapped[Optional["ChapterSummary"]] = relationship(back_populates="chapter", uselist=False)

class BibleVerse(UUIDTimestampMixin, Base):
    __tablename__ = "bible_verses"
    chapter_id: Mapped[UUID] = mapped_column(ForeignKey("bible_chapters.id", ondelete="CASCADE"), index=True)
    verse_number: Mapped[int] = mapped_column(Integer, index=True)
    text: Mapped[str] = mapped_column(Text)
    chapter: Mapped["BibleChapter"] = relationship(back_populates="verses")
    notes: Mapped[list["VerseNotes"]] = relationship(back_populates="verse", cascade="all, delete-orphan")
    references_out: Mapped[list["CrossReference"]] = relationship(
        "CrossReference",
        foreign_keys="[CrossReference.from_verse_id]",
        back_populates="from_verse",
        cascade="all, delete-orphan"
    )

class CrossReference(UUIDTimestampMixin, Base):
    __tablename__ = "cross_references"
    from_verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)
    to_verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)
    reference_type: Mapped[str] = mapped_column(String(50), default="related")
    from_verse: Mapped["BibleVerse"] = relationship("BibleVerse", foreign_keys=[from_verse_id], back_populates="references_out")
    to_verse: Mapped["BibleVerse"] = relationship("BibleVerse", foreign_keys=[to_verse_id])

class BibleTopic(UUIDTimestampMixin, Base):
    __tablename__ = "bible_topics"
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)

class TopicVerse(UUIDTimestampMixin, Base):
    __tablename__ = "topic_verses"
    topic_id: Mapped[UUID] = mapped_column(ForeignKey("bible_topics.id", ondelete="CASCADE"), index=True)
    verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)

class CharacterReference(UUIDTimestampMixin, Base):
    __tablename__ = "character_references"
    character_id: Mapped[UUID] = mapped_column(ForeignKey("bible_characters.id", ondelete="CASCADE"), index=True)
    verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)

class BookSummary(UUIDTimestampMixin, Base):
    __tablename__ = "book_summaries"
    book_id: Mapped[UUID] = mapped_column(ForeignKey("bible_books.id", ondelete="CASCADE"), unique=True, index=True)
    summary: Mapped[str] = mapped_column(Text)
    book: Mapped["BibleBook"] = relationship(back_populates="summary")

class ChapterSummary(UUIDTimestampMixin, Base):
    __tablename__ = "chapter_summaries"
    chapter_id: Mapped[UUID] = mapped_column(ForeignKey("bible_chapters.id", ondelete="CASCADE"), unique=True, index=True)
    summary: Mapped[str] = mapped_column(Text)
    chapter: Mapped["BibleChapter"] = relationship(back_populates="summary")

class VerseNotes(UUIDTimestampMixin, Base):
    __tablename__ = "verse_notes"
    verse_id: Mapped[UUID] = mapped_column(ForeignKey("bible_verses.id", ondelete="CASCADE"), index=True)
    note: Mapped[str] = mapped_column(Text)
    verse: Mapped["BibleVerse"] = relationship(back_populates="notes")

class BrandProfile(UUIDTimestampMixin, Base):
    __tablename__ = "brand_profiles"
    church_id: Mapped[UUID] = mapped_column(ForeignKey("churches.id", ondelete="CASCADE"), index=True, unique=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(512))
    primary_color: Mapped[str] = mapped_column(String(50), default="#0f172a")
    secondary_color: Mapped[str] = mapped_column(String(50), default="#3b82f6")
    accent_color: Mapped[str] = mapped_column(String(50), default="#eab308")
    heading_font: Mapped[str] = mapped_column(String(100), default="Inter")
    body_font: Mapped[str] = mapped_column(String(100), default="Inter")
    address: Mapped[Optional[str]] = mapped_column(Text)
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(254))
    website: Mapped[Optional[str]] = mapped_column(String(255))
    social_handles: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    church_motto: Mapped[Optional[str]] = mapped_column(String(255))


class AssetFolder(UUIDTimestampMixin, Base):
    __tablename__ = "asset_folders"
    name: Mapped[str] = mapped_column(String(255))
    assets: Mapped[list["CreativeAsset"]] = relationship(back_populates="folder")


class AssetTag(UUIDTimestampMixin, Base):
    __tablename__ = "asset_tags"
    name: Mapped[str] = mapped_column(String(100), unique=True)


class AssetTagsLink(Base):
    __tablename__ = "asset_tags_link"
    asset_id: Mapped[UUID] = mapped_column(ForeignKey("creative_assets.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[UUID] = mapped_column(ForeignKey("asset_tags.id", ondelete="CASCADE"), primary_key=True)


class CreativeProject(UUIDTimestampMixin, Base):
    __tablename__ = "creative_projects"
    sermon_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("sermons.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    media_type: Mapped[str] = mapped_column(String(50), index=True)
    target_dimensions: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    editor_state: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    ai_prompt: Mapped[Optional[str]] = mapped_column(Text)
    sermon: Mapped[Optional[Sermon]] = relationship(back_populates="creative_projects")
    assets: Mapped[list["CreativeAsset"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class CreativeAsset(UUIDTimestampMixin, Base):
    __tablename__ = "creative_assets"
    project_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("creative_projects.id", ondelete="SET NULL"), index=True)
    folder_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("asset_folders.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(255), index=True)
    asset_type: Mapped[str] = mapped_column(String(50), index=True)
    url: Mapped[str] = mapped_column(String(512))
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict)
    project: Mapped[Optional[CreativeProject]] = relationship(back_populates="assets")
    folder: Mapped[Optional[AssetFolder]] = relationship(back_populates="assets")
    tags: Mapped[list[AssetTag]] = relationship(secondary="asset_tags_link")


class CommunicationProject(UUIDTimestampMixin, Base):
    __tablename__ = "communication_projects"
    sermon_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("sermons.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    campaign_type: Mapped[str] = mapped_column(String(100), index=True) # e.g. Sunday Service Announcement
    status: Mapped[str] = mapped_column(String(50), default="draft")
    sermon: Mapped[Optional[Sermon]] = relationship(back_populates="communication_projects")
    assets: Mapped[list["CommunicationAsset"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class CommunicationAsset(UUIDTimestampMixin, Base):
    __tablename__ = "communication_assets"
    project_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("communication_projects.id", ondelete="SET NULL"), index=True)
    platform: Mapped[str] = mapped_column(String(100), index=True) # e.g. Instagram, Newsletter
    content_length: Mapped[str] = mapped_column(String(50), default="Medium") # Short, Medium, Long
    content: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    project: Mapped[Optional[CommunicationProject]] = relationship(back_populates="assets")


class GeneratedImage(UUIDTimestampMixin, Base):
    __tablename__ = "generated_images"
    prompt: Mapped[str] = mapped_column(Text)
    provider: Mapped[str] = mapped_column(String(50))
    provider_model: Mapped[Optional[str]] = mapped_column(String(100))
    cloudinary_url: Mapped[Optional[str]] = mapped_column(String(512))
    generation_status: Mapped[str] = mapped_column(String(50))
    conversation_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("conversations.id", ondelete="SET NULL"), index=True)
    tool_name: Mapped[Optional[str]] = mapped_column(String(100))


