from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    ParticipantType,
    ResultStatusType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class StatusDocNotice:
    """
    Извещение о состоянии электронного документа.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar ext_id: ID исходного электронного документа, по которому
        возвращается состояния
    :ivar result: Состояние электронного документа
    :ivar ext_idstatus_request: ID запроса о состоянии электронного
        документа, если был такой
    :ivar id: Идентификатор извещения
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
    ext_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExtID",
            "type": "Element",
            "required": True,
        }
    )
    result: Optional[ResultStatusType] = field(
        default=None,
        metadata={
            "name": "Result",
            "type": "Element",
            "required": True,
        }
    )
    ext_idstatus_request: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExtIDStatusRequest",
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
