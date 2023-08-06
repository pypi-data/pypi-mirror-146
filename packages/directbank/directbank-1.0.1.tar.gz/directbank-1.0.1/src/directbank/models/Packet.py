from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    ParticipantType,
    SignatureType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


class ContentType(Enum):
    APPLICATION_XML = "application/xml"
    APPLICATION_OCTET_STREAM = "application/octet-stream"
    TEXT_PLAIN = "text/plain"
    TEXT_XML = "text/xml"


@dataclass
class DocumentType:
    """
    :ivar data: Данные электронного документа
    :ivar signature: Данные электронных подписей
    :ivar id: Идентификатор электронного документа
    :ivar dockind: Код вида электронного документа, как он задан в
        описаниии к стандарту
    :ivar format_version: Версия формата
    :ivar test_only: Тестовый документ
    :ivar compressed: Документ сжат
    :ivar encrypted: Документ зашифрован
    :ivar sign_response: Требуется Ответная Подпись
    :ivar notify_required: Требуется Извещение О Получении
    :ivar ext_id: ID исходного документа, если такой был
    """
    data: Optional["DocumentType.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    signature: List[SignatureType] = field(
        default_factory=list,
        metadata={
            "name": "Signature",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    dockind: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 2,
        }
    )
    format_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "formatVersion",
            "type": "Attribute",
            "required": True,
            "max_length": 12,
        }
    )
    test_only: Optional[bool] = field(
        default=None,
        metadata={
            "name": "testOnly",
            "type": "Attribute",
        }
    )
    compressed: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    encrypted: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    sign_response: Optional[bool] = field(
        default=None,
        metadata={
            "name": "signResponse",
            "type": "Attribute",
        }
    )
    notify_required: Optional[bool] = field(
        default=None,
        metadata={
            "name": "notifyRequired",
            "type": "Attribute",
        }
    )
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "extID",
            "type": "Attribute",
        }
    )

    @dataclass
    class Data:
        """
        :ivar value:
        :ivar file_name: Имя файла
        :ivar content_type: Тип контента передаваемого файла
        """
        value: Optional[bytes] = field(
            default=None,
            metadata={
                "required": True,
                "format": "base64",
            }
        )
        file_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "fileName",
                "type": "Attribute",
            }
        )
        content_type: Optional[ContentType] = field(
            default=None,
            metadata={
                "name": "contentType",
                "type": "Attribute",
            }
        )


@dataclass
class Packet:
    """
    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar document: Электронный документ
    :ivar sender_footprint:
    :ivar id: Идентификатор транспортного контейнера
    :ivar format_version: Версия формата
    :ivar creation_date: Дата и время формирования
    :ivar user_agent: Наименование и версия программы
    """

    class Meta:
        namespace = "http://directbank.1c.ru/XMLSchema"

    sender: Optional[ParticipantType] = field(
        default=None,
        metadata={
            "name": "Sender",
            "type": "Element",
            "required": True,
        }
    )
    recipient: Optional[ParticipantType] = field(
        default=None,
        metadata={
            "name": "Recipient",
            "type": "Element",
            "required": True,
        }
    )
    document: List[DocumentType] = field(
        default_factory=list,
        metadata={
            "name": "Document",
            "type": "Element",
            "min_occurs": 1,
        }
    )
    sender_footprint: Optional["Packet.SenderFootprint"] = field(
        default=None,
        metadata={
            "name": "SenderFootprint",
            "type": "Element",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    format_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "formatVersion",
            "type": "Attribute",
            "required": True,
            "max_length": 12,
        }
    )
    creation_date: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "creationDate",
            "type": "Attribute",
            "required": True,
        }
    )
    user_agent: Optional[str] = field(
        default=None,
        metadata={
            "name": "userAgent",
            "type": "Attribute",
            "max_length": 100,
        }
    )

    @dataclass
    class SenderFootprint:
        ip: List[str] = field(
            default_factory=list,
            metadata={
                "name": "IP",
                "type": "Element",
                "max_length": 39,
            }
        )
        mac: List[str] = field(
            default_factory=list,
            metadata={
                "name": "MAC",
                "type": "Element",
                "max_length": 17,
            }
        )
