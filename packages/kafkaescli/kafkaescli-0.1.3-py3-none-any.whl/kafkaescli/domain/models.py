""" App Models
"""
import base64
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, fields
from pydantic.types import UUID4

from kafkaescli.domain.constants import DEFAULT_BOOTSTRAP_SERVERS
from kafkaescli.domain.types import JSONSerializable


class Model(BaseModel):
    """Models"""

    class Config:
        use_enum_values = True
        extra = "ignore"


class DataModel(Model):
    uuid: UUID4 = fields.Field(default_factory=uuid4)


class Config(Model):
    bootstrap_servers: str = DEFAULT_BOOTSTRAP_SERVERS
    middleware_classes: List[str] = fields.Field(default_factory=list)


class ConfigProfile(Model):
    name: str
    config: Config


class ConfigFile(Model):
    version: int = 1
    default_profile: Optional[str] = None
    profiles: List[ConfigProfile] = fields.Field(default_factory=list)


class PayloadMetadata(Model):
    topic: str
    partition: int
    offset: int
    timestamp: int

    class Config:
        extra = "allow"


class Payload(Model):
    metadata: PayloadMetadata
    message: JSONSerializable
    key: Optional[JSONSerializable] = fields.Field(default=None)

    class Config:
        json_encoders = {
            bytes: lambda x: base64.b64encode(x).decode("utf-8"),
        }


class ConsumerPayload(Payload):
    """Consumer Payload"""


class ProducerPayload(Payload):
    """Producer Payload"""
