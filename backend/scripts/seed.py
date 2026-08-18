import logging
from sqlalchemy.orm import Session
from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.models.domain import Church, Preferences, BrandProfile, Role, Permission, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_database(db: Session) -> None:
    logger.info("Starting database seeding...")

    # Seed Roles
    admin_role = db.query(Role).filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role(name="admin", description="Administrator with full access")
        db.add(admin_role)

    user_role = db.query(Role).filter_by(name="user").first()
    if not user_role:
        user_role = Role(name="user", description="Standard user")
        db.add(user_role)
        
    db.commit()

    # Seed Default Church
    church = db.query(Church).filter_by(name="ZION PRAYER TOWER").first()
    if not church:
        logger.info("Creating default church...")
        church = Church(
            name="ZION PRAYER TOWER",
            primary_theme="Dark Blue",
            accent="Gold"
        )
        db.add(church)
        db.commit()
        db.refresh(church)
    
    # Seed Preferences for Default Church
    prefs = db.query(Preferences).filter_by(church_id=church.id).first()
    if not prefs:
        logger.info("Creating default preferences...")
        prefs = Preferences(
            church_id=church.id,
            settings={"allow_registration": False, "default_language": "en"}
        )
        db.add(prefs)
        
    # Seed Brand Profile for Default Church
    brand = db.query(BrandProfile).filter_by(church_id=church.id).first()
    if not brand:
        logger.info("Creating default brand profile...")
        brand = BrandProfile(
            church_id=church.id,
            primary_color="#0f172a",
            secondary_color="#3b82f6",
            accent_color="#eab308",
            heading_font="Inter",
            body_font="Inter",
            church_motto="A place of prayer for all nations"
        )
        db.add(brand)
        
    db.commit()
    logger.info("Database seeding completed successfully.")


def main():
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
