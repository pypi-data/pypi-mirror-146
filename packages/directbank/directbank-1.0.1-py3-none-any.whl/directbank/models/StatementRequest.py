from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    BankPartyType,
    BankType,
    CustomerPartyType,
    DigestType,
    StatementKindType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class StatementRequest:
    """
    Запрос выписки банка.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar data: Данные запроса
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
    data: Optional["StatementRequest.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "required": True,
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

    @dataclass
    class Data:
        """
        :ivar statement_type: Тип выписки
        :ivar date_from: Начало периода формирования выписки
        :ivar date_to: Конец периода формирования выписки
        :ivar account: Номер счета, по которому производится запрос
        :ivar bank: Банк, в котором открыт счет
        """
        statement_type: Optional[StatementKindType] = field(
            default=None,
            metadata={
                "name": "StatementType",
                "type": "Element",
                "required": True,
            }
        )
        date_from: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "DateFrom",
                "type": "Element",
                "required": True,
            }
        )
        date_to: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "DateTo",
                "type": "Element",
                "required": True,
            }
        )
        account: Optional[str] = field(
            default=None,
            metadata={
                "name": "Account",
                "type": "Element",
                "required": True,
                "min_length": 1,
                "max_length": 20,
            }
        )
        bank: Optional[BankType] = field(
            default=None,
            metadata={
                "name": "Bank",
                "type": "Element",
                "required": True,
            }
        )
