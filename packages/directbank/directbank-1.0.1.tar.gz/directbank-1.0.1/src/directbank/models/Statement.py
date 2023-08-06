from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ExchCommon import (
    BankOrderApp,
    BankPartyType,
    BankType,
    CashContributionType,
    CheckType,
    CollectionOrderApp,
    CustomerPartyType,
    MemOrderApp,
    OtherPaymentDataType,
    PayDocRuApp,
    PayRequestApp,
    PaymentOrderApp,
    StatementKindType,
    StatusType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


class OperationInfoDc(Enum):
    """
    :cvar VALUE_1: Операция по дебету
    :cvar VALUE_2: Операция по кредиту
    """
    VALUE_1 = "1"
    VALUE_2 = "2"


@dataclass
class Statement:
    """
    Выписка банка по лицевому счету.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar data: Данные выписки по лиц.счету
    :ivar ext_idstatement_request: ID исходного запроса на выписку, если
        такой был
    :ivar id: Идентификатор выписки
    :ivar format_version: Версия формата
    :ivar creation_date: Дата и время формирования
    :ivar user_agent: Наименование и версия программы
    """

    class Meta:
        namespace = "http://directbank.1c.ru/XMLSchema"

    sender: Optional[BankPartyType] = field(
        default=None,
        metadata={
            "name": "Sender",
            "type": "Element",
            "required": True,
        }
    )
    recipient: Optional[CustomerPartyType] = field(
        default=None,
        metadata={
            "name": "Recipient",
            "type": "Element",
            "required": True,
        }
    )
    data: Optional["Statement.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "required": True,
        }
    )
    ext_idstatement_request: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExtIDStatementRequest",
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
        :ivar date_from: Начало периода выписки
        :ivar date_to: Конец периода выписки
        :ivar account: Номер лиц.счета
        :ivar bank: Банк, в котором открыт счет
        :ivar opening_balance: Остаток на счете на начало периода
        :ivar total_debits: Общая сумма документов по дебету счета
        :ivar total_credits: Общая сумма документов по кредиту счета
        :ivar closing_balance: Остаток на счете на конец периода
        :ivar operation_info: Информация об одной операции по лицевому
            счету в выписке
        :ivar stamp: Данные штампа банка по выписке в целом
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
        opening_balance: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "OpeningBalance",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
            }
        )
        total_debits: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "TotalDebits",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
            }
        )
        total_credits: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "TotalCredits",
                "type": "Element",
                "total_digits": 18,
                "fraction_digits": 2,
            }
        )
        closing_balance: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "ClosingBalance",
                "type": "Element",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            }
        )
        operation_info: List["Statement.Data.OperationInfo"] = field(
            default_factory=list,
            metadata={
                "name": "OperationInfo",
                "type": "Element",
            }
        )
        stamp: Optional["Statement.Data.Stamp"] = field(
            default=None,
            metadata={
                "name": "Stamp",
                "type": "Element",
            }
        )

        @dataclass
        class OperationInfo:
            """
            :ivar pay_doc: Данные платежного документа
            :ivar dc: Признак дебета/кредита: 1 - дебет, 2 - кредит
            :ivar date: Дата проводки документа по лиц.счету
            :ivar ext_id: ID исходного платежного документа плательщика
            :ivar stamp: Данные штампа банка по каждому платежному
                документу
            """
            pay_doc: Optional["Statement.Data.OperationInfo.PayDoc"] = field(
                default=None,
                metadata={
                    "name": "PayDoc",
                    "type": "Element",
                    "required": True,
                }
            )
            dc: Optional[OperationInfoDc] = field(
                default=None,
                metadata={
                    "name": "DC",
                    "type": "Element",
                    "required": True,
                    "length": 1,
                }
            )
            date: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "name": "Date",
                    "type": "Element",
                    "required": True,
                }
            )
            ext_id: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ExtID",
                    "type": "Element",
                }
            )
            stamp: Optional["Statement.Data.OperationInfo.Stamp"] = field(
                default=None,
                metadata={
                    "name": "Stamp",
                    "type": "Element",
                }
            )

            @dataclass
            class PayDoc:
                """
                :ivar pay_doc_ru: Данные платежного поручения
                :ivar pay_request: Данные платежного требования
                :ivar collection_order: Данные инкассового поручения
                :ivar payment_order: Данные платежного ордера
                :ivar bank_order: Данные банковского ордера
                :ivar mem_order: Данные мемориального ордера
                :ivar inner_doc: Данные внутр.банковского документа
                :ivar cash_contribution: Данные объявления на взнос
                    наличными
                :ivar check: Данные денежного чека
                :ivar id: ID платежного документа в банке
                :ivar doc_kind: Код вида электронного документа, как он
                    задан в описании к стандарту
                """
                pay_doc_ru: Optional[PayDocRuApp] = field(
                    default=None,
                    metadata={
                        "name": "PayDocRu",
                        "type": "Element",
                    }
                )
                pay_request: Optional[PayRequestApp] = field(
                    default=None,
                    metadata={
                        "name": "PayRequest",
                        "type": "Element",
                    }
                )
                collection_order: Optional[CollectionOrderApp] = field(
                    default=None,
                    metadata={
                        "name": "CollectionOrder",
                        "type": "Element",
                    }
                )
                payment_order: Optional[PaymentOrderApp] = field(
                    default=None,
                    metadata={
                        "name": "PaymentOrder",
                        "type": "Element",
                    }
                )
                bank_order: Optional[BankOrderApp] = field(
                    default=None,
                    metadata={
                        "name": "BankOrder",
                        "type": "Element",
                    }
                )
                mem_order: Optional[MemOrderApp] = field(
                    default=None,
                    metadata={
                        "name": "MemOrder",
                        "type": "Element",
                    }
                )
                inner_doc: Optional["Statement.Data.OperationInfo.PayDoc.InnerDoc"] = field(
                    default=None,
                    metadata={
                        "name": "InnerDoc",
                        "type": "Element",
                    }
                )
                cash_contribution: Optional[CashContributionType] = field(
                    default=None,
                    metadata={
                        "name": "CashContribution",
                        "type": "Element",
                    }
                )
                check: Optional[CheckType] = field(
                    default=None,
                    metadata={
                        "name": "Check",
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
                doc_kind: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "docKind",
                        "type": "Attribute",
                        "required": True,
                        "length": 2,
                    }
                )

                @dataclass
                class InnerDoc(OtherPaymentDataType):
                    """
                    :ivar inner_doc_kind: Название типа
                        внутр.банковского документа
                    """
                    inner_doc_kind: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "InnerDocKind",
                            "type": "Element",
                            "required": True,
                            "max_length": 255,
                        }
                    )

            @dataclass
            class Stamp(BankType):
                """
                :ivar branch: Отделение банка
                :ivar status: Статус платежного документа в банке
                """
                branch: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Branch",
                        "type": "Element",
                        "max_length": 255,
                    }
                )
                status: Optional[StatusType] = field(
                    default=None,
                    metadata={
                        "name": "Status",
                        "type": "Element",
                        "required": True,
                    }
                )

        @dataclass
        class Stamp(BankType):
            """
            :ivar branch: Отделение банка
            """
            branch: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Branch",
                    "type": "Element",
                    "max_length": 255,
                }
            )
