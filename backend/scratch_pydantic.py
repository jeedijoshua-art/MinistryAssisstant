from pydantic import BaseModel, Field, AliasChoices, ConfigDict
from typing import Dict, Any, Optional

class DummyORM:
    def __init__(self):
        self.metadata = "SQLAlchemy_MetaData"
        self.metadata_ = {"key": "value"}

class MySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    metadata_: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        validation_alias=AliasChoices("metadata_", "metadata"),
        serialization_alias="metadata"
    )

orm_obj = DummyORM()
schema_obj = MySchema.model_validate(orm_obj)
print(schema_obj.model_dump(by_alias=True))

