# Architecture decision record: foundation

The API follows dependency direction: HTTP routers depend on services; services depend on repository interfaces/implementations; repositories own SQLAlchemy access. ORM entities remain persistence-focused. Configuration enters through Pydantic settings and environment variables only.

Each domain table has a UUID identity and auditable timestamps. PostgreSQL is the production database, with Alembic as its schema lifecycle owner. The initial migration creates the schema and seeds the ministry identity.

Future AI providers must be introduced behind a service boundary, never directly in a router or ORM model.
