from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class BankPartyType:
    """
    :ivar bic: БИК банка
    :ivar name: Название банка
    """
    bic: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "length": 9,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 160,
        }
    )


@dataclass
class BankType:
    """
    Реквизиты банка.

    :ivar bic: БИК банка
    :ivar name: Название банка
    :ivar city: Город (неселенный пункт) банка
    :ivar corresp_acc: Коррсчет банка
    """
    bic: Optional[str] = field(
        default=None,
        metadata={
            "name": "BIC",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "length": 9,
            "pattern": r"[0-9]{9}",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 160,
        }
    )
    city: Optional[str] = field(
        default=None,
        metadata={
            "name": "City",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 30,
        }
    )
    corresp_acc: Optional[str] = field(
        default=None,
        metadata={
            "name": "CorrespAcc",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 20,
        }
    )


@dataclass
class BudgetPaymentInfoType:
    """Реквизиты бюджетного документа.

    См.правила заполнения платежных поручений, утвержденные приказом
    Минфина России от 12 ноября 2013 года № 107н.

    :ivar drawer_status: Статус составителя  (поле 101).
    :ivar cbc: Код бюджетной классификации (КБК) в соответствии с
        классификацией доходов бюджетов РФ (поле 104).
    :ivar oktmo: Значение кода ОКТМО муниципального образования или 0
        (ноль) (поле 105).
    :ivar reason: Основание налогового платежа или 0 (ноль) (поле 106).
    :ivar tax_period: Налоговый период или 0 (ноль) / код таможенного
        органа (поле 107).
    :ivar doc_no: Номер налогового документа (поле 108).
    :ivar doc_date: Дата налогового документа или 0 (ноль) (поле 109).
    :ivar pay_type: Код выплат (поле 110).
    """
    drawer_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "DrawerStatus",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 2,
        }
    )
    cbc: Optional[str] = field(
        default=None,
        metadata={
            "name": "CBC",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 20,
        }
    )
    oktmo: Optional[str] = field(
        default=None,
        metadata={
            "name": "OKTMO",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 11,
        }
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "Reason",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 2,
        }
    )
    tax_period: Optional[str] = field(
        default=None,
        metadata={
            "name": "TaxPeriod",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 10,
        }
    )
    doc_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 15,
        }
    )
    doc_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 10,
        }
    )
    pay_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "PayType",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 2,
        }
    )


@dataclass
class CustomerPartyType:
    """
    :ivar id: Идентификатор клиента, как он задан на стороне банка
    :ivar name: Наименование клиента
    :ivar inn: ИНН клиента
    :ivar kpp: КПП клиента
    """
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "max_length": 160,
        }
    )
    inn: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "min_length": 10,
            "max_length": 12,
        }
    )
    kpp: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "length": 9,
        }
    )


@dataclass
class DigestType:
    """
    :ivar data: Данные дайджеста в base64
    """
    data: Optional["DigestType.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )

    @dataclass
    class Data:
        """
        :ivar value:
        :ivar algorithm_version: Версия алгоритма формирования дайджеста
        """
        value: Optional[bytes] = field(
            default=None,
            metadata={
                "required": True,
                "format": "base64",
            }
        )
        algorithm_version: Optional[str] = field(
            default=None,
            metadata={
                "name": "algorithmVersion",
                "type": "Attribute",
                "required": True,
                "max_length": 12,
            }
        )


@dataclass
class ErrorType:
    """
    :ivar code: Код ошибки, как он задан в описании к стандарту
    :ivar description: Описание ошибки, как оно задано в описании к
        стандарту
    :ivar more_info: Подробное пояснение к ошибке для пользователя
    """
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "length": 4,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "max_length": 255,
        }
    )
    more_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "MoreInfo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class SignatureType:
    """
    Электронная подпись.

    :ivar signed_data: Электронная подпись
    :ivar x509_issuer_name: Имя издателя сертификата открытого ключа ЭП
        (значение атрибута "CN").
    :ivar x509_serial_number: Серийный номер сертификата открытого ключа
        ЭП
    """
    signed_data: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "SignedData",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "format": "base64",
        }
    )
    x509_issuer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "x509IssuerName",
            "type": "Attribute",
            "required": True,
        }
    )
    x509_serial_number: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "x509SerialNumber",
            "type": "Attribute",
            "required": True,
            "format": "base16",
        }
    )


class StatementKindType(Enum):
    """
    Тип выписки банка.

    :cvar VALUE_0: Окончательная выписка
    :cvar VALUE_1: Промежуточная выписка
    :cvar VALUE_2: Текущий остаток на счете
    """
    VALUE_0 = "0"
    VALUE_1 = "1"
    VALUE_2 = "2"


@dataclass
class StatusType:
    """
    :ivar code: Код статуса, как он задан в описанию к стандарту
    :ivar name: Наименование статуса на стороне банка
    :ivar more_info: Дополнительная информация к статусу
    """
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "length": 2,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 25,
        }
    )
    more_info: Optional[str] = field(
        default=None,
        metadata={
            "name": "MoreInfo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class CustomerDetailsType:
    """
    Реквизиты налогоплательщика.

    :ivar name: Наименование налогоплательщика
    :ivar inn: Идентификационный номера налогоплательщика (ИНН)
    :ivar kpp: Для платежей в бюджет - указывать обязательно
    :ivar account: Расчетный счет клиента в его банке, независимо от
        того, прямые расчеты у этого банка или нет. Номер счета может не
        указываться в следующих случаях: в распоряжении, если
        получателем средств является кредитная организация, филиал
        кредитной организации, в том числе в целях выдачи наличных
        денежных средств получателю средств - физическому лицу без
        открытия банковского счета; в платежном поручении на общую сумму
        с реестром, в котором указаны получатели средств, обслуживаемые
        одним банком, составляемом плательщиком; в платежном поручении
        на общую сумму с реестром, в котором указаны плательщики,
        обслуживаемые одним банком, и получатели средств, обслуживаемые
        другим банком, составляемом банком плательщика
    :ivar bank: Реквизиты банка
    """
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    inn: Optional[str] = field(
        default=None,
        metadata={
            "name": "INN",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    kpp: Optional[str] = field(
        default=None,
        metadata={
            "name": "KPP",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 9,
        }
    )
    account: Optional[str] = field(
        default=None,
        metadata={
            "name": "Account",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 20,
        }
    )
    bank: Optional[BankType] = field(
        default=None,
        metadata={
            "name": "Bank",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )


@dataclass
class MemOrderApp:
    """
    Данные мемориального ордера.

    :ivar doc_no: Номер документа (поле 3).
    :ivar doc_date: Дата составления (поле 4).
    :ivar spare_field5: Свободное поле (поле 5)
    :ivar author: Составитель (поле 6).
    :ivar account_name_debit: Наименование счета по дебету (поле 7)
    :ivar account_debit: Счет по дебету (поле 8)
    :ivar sum: Сумма документа (поле 9).
    :ivar spare_field9a: Свободное поле (поле 9a)
    :ivar account_name_credit: Наименование счета по кредиту (поле 10)
    :ivar account_credit: Счет по кредиту (поле 11)
    :ivar partial_transition_kind: Шифр документа (поле 13).
    :ivar spare_field14: Свободное поле (поле 14)
    :ivar spare_field15: Свободное поле (поле 15)
    :ivar transition_content: Содержание операции (поле 16).
    :ivar spare_field20: Свободное поле (поле 20)
    """
    doc_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    doc_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DocDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    spare_field5: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpareField5",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    author: Optional["MemOrderApp.Author"] = field(
        default=None,
        metadata={
            "name": "Author",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    account_name_debit: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNameDebit",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    account_debit: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountDebit",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 20,
        }
    )
    sum: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 2,
        }
    )
    spare_field9a: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpareField9a",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    account_name_credit: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountNameCredit",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    account_credit: Optional[str] = field(
        default=None,
        metadata={
            "name": "AccountCredit",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 20,
        }
    )
    partial_transition_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartialTransitionKind",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 2,
        }
    )
    spare_field14: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpareField14",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    spare_field15: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpareField15",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    transition_content: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransitionContent",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    spare_field20: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpareField20",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )

    @dataclass
    class Author(BankType):
        """
        :ivar branch: Отделение банка
        """
        branch: Optional[str] = field(
            default=None,
            metadata={
                "name": "Branch",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )


@dataclass
class OtherCustomerDetailsType:
    """
    Реквизиты прочих налогоплательщиков.

    :ivar name: Наименование налогоплательщика
    :ivar inn: Идентификационный номера налогоплательщика (ИНН)
    :ivar kpp: Для платежей в бюджет - указывать обязательно
    :ivar account: Расчетный счет клиента в его банке, независимо от
        того, прямые расчеты у этого банка или нет
    :ivar bank: Реквизиты банка
    """
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    inn: Optional[str] = field(
        default=None,
        metadata={
            "name": "INN",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    kpp: Optional[str] = field(
        default=None,
        metadata={
            "name": "KPP",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 9,
        }
    )
    account: Optional[str] = field(
        default=None,
        metadata={
            "name": "Account",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "min_length": 1,
            "max_length": 20,
        }
    )
    bank: Optional[BankType] = field(
        default=None,
        metadata={
            "name": "Bank",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class ParticipantType:
    """
    Одна из сторон, принимающая участие в обмене электронными документами
    (Участник)

    :ivar customer: Клиент
    :ivar bank: Банк
    """
    customer: Optional[CustomerPartyType] = field(
        default=None,
        metadata={
            "name": "Customer",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    bank: Optional[BankPartyType] = field(
        default=None,
        metadata={
            "name": "Bank",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class ResultStatusType:
    """
    :ivar error: Ответ в случае возникновения ошибки
    :ivar status: Успешный ответ
    """
    error: Optional[ErrorType] = field(
        default=None,
        metadata={
            "name": "Error",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    status: Optional[StatusType] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class OtherPaymentDataType:
    """
    Реквизиты иных банковских документов.

    :ivar doc_no: Номер документа
    :ivar doc_date: Дата составления
    :ivar sum: Сумма документа
    :ivar payer: Плательщик
    :ivar payee: Получатель
    :ivar transition_kind: Вид операции
    :ivar code: Уникальный идентификатор платежа
    :ivar purpose: Назначение
    """
    doc_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    doc_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DocDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    sum: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 2,
        }
    )
    payer: Optional[OtherCustomerDetailsType] = field(
        default=None,
        metadata={
            "name": "Payer",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    payee: Optional[OtherCustomerDetailsType] = field(
        default=None,
        metadata={
            "name": "Payee",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    transition_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransitionKind",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 2,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 25,
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class PaymentDataType:
    """
    Данные платежного документа.

    :ivar doc_no: Номер документа (поле 3).
    :ivar doc_date: Дата составления (поле 4).
    :ivar sum: Сумма документа (поле 7).
    :ivar payer: Плательщик (поля 8, 9, 10, 11, 12, 60, 102).
    :ivar payee: Получатель (поля 13, 14, 15, 16, 17, 61, 103).
    :ivar payment_kind: Вид платежа (поле 5). Указывается "срочно",
        "телеграфом",  "почтой",   иное значение в порядке,
        установленном  банком.
    :ivar transition_kind: Вид операции (поле 18). Указывается условное
        цифровое обозначение документа, согласно установленного ЦБР
        перечня условных обозначений (шифров) документов, проводимых по
        счетам в кредитных организациях.
    :ivar priority: Очередность платежа (поле 21).
    :ivar code: Уникальный идентификатор платежа (поле 22). С 31 марта
        2014 года согласно Указанию N 3025-У ЦБР.
    :ivar income_type_code: Код вида дохода (поле 20) согласно Указанию
        5286-У ЦБРФ
    :ivar purpose: Назначение платежа (поле 24).
    """
    doc_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    doc_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DocDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    sum: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "Sum",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "total_digits": 18,
            "fraction_digits": 2,
        }
    )
    payer: Optional[CustomerDetailsType] = field(
        default=None,
        metadata={
            "name": "Payer",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    payee: Optional[CustomerDetailsType] = field(
        default=None,
        metadata={
            "name": "Payee",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    payment_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentKind",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 15,
        }
    )
    transition_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransitionKind",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 2,
        }
    )
    priority: Optional[str] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 1,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 25,
        }
    )
    income_type_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "IncomeTypeCode",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 1,
        }
    )
    purpose: Optional[str] = field(
        default=None,
        metadata={
            "name": "Purpose",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "max_length": 210,
        }
    )


@dataclass
class BankOrderApp(PaymentDataType):
    """
    Данные банковского ордера.
    """


@dataclass
class CashContributionType(OtherPaymentDataType):
    """
    Данные объявления на взнос наличными.

    :ivar person: От кого
    :ivar symbol: Указываются цифрами символы, предусмотренные
        отчетностью по форме 0409202, в соответствии с Указанием Банка
        России N 2332-У
    :ivar source: Указываются источники поступления наличных денег в
        соответствии с содержанием символов отчетности по форме 0409202
        и содержанием операции
    """
    person: Optional["CashContributionType.Person"] = field(
        default=None,
        metadata={
            "name": "Person",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    symbol: Optional[str] = field(
        default=None,
        metadata={
            "name": "Symbol",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 10,
        }
    )
    source: Optional[str] = field(
        default=None,
        metadata={
            "name": "Source",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 255,
        }
    )

    @dataclass
    class Person:
        """
        :ivar full_name: ФИО вносителя
        :ivar identity_document: Документ, удостоверяющий личность
        """
        full_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "FullName",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )
        identity_document: Optional[str] = field(
            default=None,
            metadata={
                "name": "IdentityDocument",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )


@dataclass
class CheckType(OtherPaymentDataType):
    """
    Данные денежного чека.

    :ivar person: Кому
    :ivar data_printing: Данные бумажной формы чека
    :ivar details: Направления и суммы выдачи
    """
    person: Optional["CheckType.Person"] = field(
        default=None,
        metadata={
            "name": "Person",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    data_printing: Optional["CheckType.DataPrinting"] = field(
        default=None,
        metadata={
            "name": "DataPrinting",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    details: List["CheckType.Details"] = field(
        default_factory=list,
        metadata={
            "name": "Details",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )

    @dataclass
    class Person:
        """
        :ivar full_name: ФИО получателя
        :ivar identity_document: Документ, удостоверяющий личность
        """
        full_name: Optional[str] = field(
            default=None,
            metadata={
                "name": "FullName",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )
        identity_document: Optional[str] = field(
            default=None,
            metadata={
                "name": "IdentityDocument",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )

    @dataclass
    class DataPrinting:
        """
        :ivar check_series: Серия чека
        :ivar check_number: Номер чека
        """
        check_series: Optional[str] = field(
            default=None,
            metadata={
                "name": "CheckSeries",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )
        check_number: Optional[str] = field(
            default=None,
            metadata={
                "name": "CheckNumber",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )

    @dataclass
    class Details:
        """
        :ivar symbol: Указываются цифрами символы, предусмотренные
            отчетностью по форме 0409202, в соответствии с Указанием
            Банка России N 2332-У
        :ivar purpose: Указываются направления (цели) выдачи наличных
            денег в соответствии с содержанием символов отчетности по
            форме 0409202 и содержанием операции
        :ivar sum: Сумма расходов
        """
        symbol: Optional[str] = field(
            default=None,
            metadata={
                "name": "Symbol",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "required": True,
                "max_length": 10,
            }
        )
        purpose: Optional[str] = field(
            default=None,
            metadata={
                "name": "Purpose",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "max_length": 255,
            }
        )
        sum: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "Sum",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
                "required": True,
                "total_digits": 18,
                "fraction_digits": 2,
            }
        )


@dataclass
class CollectionOrderApp(PaymentDataType):
    """
    Данные инкассового поручения.

    :ivar budget_payment_info: Реквизиты бюджетного документа.
        См.правила заполнения платежных поручений, утвержденные приказом
        Минфина России от 12 ноября 2013 года № 107н.
    """
    budget_payment_info: Optional[BudgetPaymentInfoType] = field(
        default=None,
        metadata={
            "name": "BudgetPaymentInfo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class PayDocRuApp(PaymentDataType):
    """
    Данные платежного поручения.

    :ivar budget_payment_info: Реквизиты бюджетного документа.
        См.правила заполнения платежных поручений, утвержденные приказом
        Минфина России от 12 ноября 2013 года № 107н.
    """
    budget_payment_info: Optional[BudgetPaymentInfoType] = field(
        default=None,
        metadata={
            "name": "BudgetPaymentInfo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class PayRequestApp(PaymentDataType):
    """
    Данные платежного требования.

    :ivar payment_condition: Условие оплаты (поле 35): 1 - заранее
        данный акцепт плательщика; 2 - требуется получение акцепта
        плательщика.
    :ivar accept_term: Срок для акцепта (поле 36): количество дней.
    :ivar doc_dispatch_date: Дата отсылки (вручения) плательщику
        предусмотренных договором документов (поле 37).
    """
    payment_condition: Optional[str] = field(
        default=None,
        metadata={
            "name": "PaymentCondition",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "length": 1,
        }
    )
    accept_term: Optional[int] = field(
        default=None,
        metadata={
            "name": "AcceptTerm",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    doc_dispatch_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocDispatchDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class PaymentOrderApp(PaymentDataType):
    """
    Данные платежного ордера.

    :ivar transition_content: Содержание операции (поле 70).
    :ivar partial_payment_no: Номер частичного платежа (поле 38).
    :ivar partial_transition_kind: Шифр платежного документа (поле 39).
    :ivar sum_residual_payment: Сумма остатка платежа (поле 42).
    :ivar partial_doc_no: Номер платежного документа (поле 40).
    :ivar partial_doc_date: Дата платежного документа (поле 41).
    :ivar budget_payment_info: Реквизиты бюджетного документа.
        См.правила заполнения платежных поручений, утвержденные приказом
        Минфина России от 12 ноября 2013 года № 107н.
    """
    transition_content: Optional[str] = field(
        default=None,
        metadata={
            "name": "TransitionContent",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 16,
        }
    )
    partial_payment_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartialPaymentNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 3,
        }
    )
    partial_transition_kind: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartialTransitionKind",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "length": 2,
        }
    )
    sum_residual_payment: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "SumResidualPayment",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "total_digits": 18,
            "fraction_digits": 2,
        }
    )
    partial_doc_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartialDocNo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "max_length": 6,
        }
    )
    partial_doc_date: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartialDocDate",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    budget_payment_info: Optional[BudgetPaymentInfoType] = field(
        default=None,
        metadata={
            "name": "BudgetPaymentInfo",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
