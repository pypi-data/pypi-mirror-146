from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    BankPartyType,
    CustomerPartyType,
    DigestType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class CancelationRequest:
    """
    Запрос об отзыве электронного документа.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar ext_id: ID исходного электронного документа, который требуется
        отозвать
    :ivar reason: Причина, основание отзыва электронного документа
    :ivar digest: Дайджест запроса
    :ivar id: Идентификатор запроса
    :ivar format_version: Версия формата
    :ivar creation_date: Дата и время формирования
    :ivar user_agent: Наименование и версия программы
    """

    class Meta:
        namespace = "http://directbank.1c.ru/XMLSchema"

    sender: Optional[CustomerPartyType] = field(
        default=None,
        metadata={
            "name": "Sender",
            "type": "Element",
            "required": True,
        }
    )
    recipient: Optional[BankPartyType] = field(
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
    reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Element",
        }
    )
    digest: Optional[DigestType] = field(
        default=None,
        metadata={
            "name": "Digest",
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
