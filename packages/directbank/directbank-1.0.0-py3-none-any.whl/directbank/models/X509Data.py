from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class X509Data:
    """
    Описание набора данных по сертификату.

    :ivar x509_issuer_name: Имя издателя сертификата электронной подписи
        (значение атрибута"CN").
    :ivar x509_serial_number: Серийный номер сертификата электронной
        подписи
    :ivar x509_certificate: Двоичные данные сертификата электронной
        подписи
    :ivar id: Идентификатор набора данных
    :ivar format_version: Версия формата
    :ivar creation_date: Дата и время формирования
    :ivar user_agent: Наименование и версия программы
    """
    class Meta:
        namespace = "http://directbank.1c.ru/XMLSchema"

    x509_issuer_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "X509IssuerName",
            "type": "Element",
            "required": True,
        }
    )
    x509_serial_number: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "X509SerialNumber",
            "type": "Element",
            "required": True,
            "format": "base16",
        }
    )
    x509_certificate: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "X509Certificate",
            "type": "Element",
            "required": True,
            "format": "base64",
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
