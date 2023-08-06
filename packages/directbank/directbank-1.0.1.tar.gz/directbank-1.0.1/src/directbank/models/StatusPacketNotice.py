from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    ParticipantType,
    ResultStatusType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class StatusPacketNotice:
    """
    Извещение о состоянии транспортного контейнера.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar idresult_success_response: ID, который сервис вернул в ответ
        после получения транспортного контейнера
    :ivar result: Состояние транспортного контейнера
    :ivar ext_idpacket: ID исходного транспортного контейнера, по
        которому возвращается состояния
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
    idresult_success_response: Optional[str] = field(
        default=None,
        metadata={
            "name": "IDResultSuccessResponse",
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
    ext_idpacket: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExtIDPacket",
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
