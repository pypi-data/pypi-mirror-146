from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import (
    BankPartyType,
    CustomerPartyType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


class DataEncoding(Enum):
    UTF_8 = "UTF-8"


@dataclass
class Settings:
    """
    Настройки обмена клиента с банком.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar data: Параметры обмена
    :ivar id: Идентификатор набора данных
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
    data: Optional["Settings.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "required": True,
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
        :ivar customer_id: Уникальный идентификатор организации в банке
        :ivar bank_server_address: Адрес ресурса банка
        :ivar format_version: Актуальная версия формата обмена данными
        :ivar encoding: Кодировка файлов обмена
        :ivar compress: Признак сжатия электронных документов при обмене
        :ivar logon: Способ аутентификации на ресурсе банка
        :ivar crypto_parameters: Настройки криптографии
        :ivar document: Настройки по видам электронных документов,
            которыми возможен обмен с банком
        :ivar receipt_statement: Параметры получения выписки в
            автоматическом режиме
        :ivar letters: Свойства писем
        """
        customer_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "CustomerID",
                "type": "Element",
                "required": True,
                "min_length": 1,
                "max_length": 50,
            }
        )
        bank_server_address: Optional[str] = field(
            default=None,
            metadata={
                "name": "BankServerAddress",
                "type": "Element",
                "required": True,
                "min_length": 1,
            }
        )
        format_version: Optional[str] = field(
            default=None,
            metadata={
                "name": "FormatVersion",
                "type": "Element",
                "required": True,
                "max_length": 12,
            }
        )
        encoding: DataEncoding = field(
            default=DataEncoding.UTF_8,
            metadata={
                "name": "Encoding",
                "type": "Element",
                "required": True,
            }
        )
        compress: Optional[bool] = field(
            default=None,
            metadata={
                "name": "Compress",
                "type": "Element",
            }
        )
        logon: Optional["Settings.Data.Logon"] = field(
            default=None,
            metadata={
                "name": "Logon",
                "type": "Element",
                "required": True,
            }
        )
        crypto_parameters: Optional["Settings.Data.CryptoParameters"] = field(
            default=None,
            metadata={
                "name": "CryptoParameters",
                "type": "Element",
            }
        )
        document: List["Settings.Data.Document"] = field(
            default_factory=list,
            metadata={
                "name": "Document",
                "type": "Element",
                "min_occurs": 1,
            }
        )
        receipt_statement: Optional["Settings.Data.ReceiptStatement"] = field(
            default=None,
            metadata={
                "name": "ReceiptStatement",
                "type": "Element",
            }
        )
        letters: Optional["Settings.Data.Letters"] = field(
            default=None,
            metadata={
                "name": "Letters",
                "type": "Element",
            }
        )

        @dataclass
        class Logon:
            """
            :ivar login: По логину и паролю
            :ivar certificate: По сертификату электронной подписи
            """
            login: Optional["Settings.Data.Logon.Login"] = field(
                default=None,
                metadata={
                    "name": "Login",
                    "type": "Element",
                }
            )
            certificate: Optional["Settings.Data.Logon.Certificate"] = field(
                default=None,
                metadata={
                    "name": "Certificate",
                    "type": "Element",
                }
            )

            @dataclass
            class Login:
                """
                :ivar user: Логин пользователя
                """
                user: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "User",
                        "type": "Element",
                        "required": True,
                        "max_length": 50,
                    }
                )

            @dataclass
            class Certificate:
                """
                :ivar encrypting_algorithm: Алгоритм шифрования,
                    например, GOST 28147-89
                """
                encrypting_algorithm: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "EncryptingAlgorithm",
                        "type": "Element",
                        "required": True,
                        "max_length": 50,
                    }
                )

        @dataclass
        class CryptoParameters:
            """
            :ivar cspname: Имя CSP (cryptographic service provider)
            :ivar csptype: Тип CSP (cryptographic service provider)
            :ivar sign_algorithm: Алгоритм подписи, например, GOST R
                34.10-2001
            :ivar hash_algorithm: Алгоритм хэширования, например, GOST R
                34.11-94
            :ivar encrypted: Применение шифрования данных на прикладном
                уровне
            :ivar bank_trusted_root_certificate: Доверенный корневой
                сертификат УЦ банка
            :ivar bank_certificate: Сертификат электронной подписи банка
            :ivar customer_signature: Карточка электронных подписей
                клиента
            :ivar urladdin_info: Адрес-ссылка, откуда надо будет
                загружаться файл описания внешн.модуля, если он
                используется в обмене
            """
            cspname: Optional[str] = field(
                default=None,
                metadata={
                    "name": "CSPName",
                    "type": "Element",
                    "required": True,
                    "max_length": 256,
                }
            )
            csptype: Optional[int] = field(
                default=None,
                metadata={
                    "name": "CSPType",
                    "type": "Element",
                    "required": True,
                }
            )
            sign_algorithm: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SignAlgorithm",
                    "type": "Element",
                    "required": True,
                    "max_length": 50,
                }
            )
            hash_algorithm: Optional[str] = field(
                default=None,
                metadata={
                    "name": "HashAlgorithm",
                    "type": "Element",
                    "required": True,
                    "max_length": 50,
                }
            )
            encrypted: Optional["Settings.Data.CryptoParameters.Encrypted"] = field(
                default=None,
                metadata={
                    "name": "Encrypted",
                    "type": "Element",
                }
            )
            bank_trusted_root_certificate: Optional[bytes] = field(
                default=None,
                metadata={
                    "name": "BankTrustedRootCertificate",
                    "type": "Element",
                    "format": "base64",
                }
            )
            bank_certificate: Optional[bytes] = field(
                default=None,
                metadata={
                    "name": "BankCertificate",
                    "type": "Element",
                    "format": "base64",
                }
            )
            customer_signature: Optional["Settings.Data.CryptoParameters.CustomerSignature"] = field(
                default=None,
                metadata={
                    "name": "CustomerSignature",
                    "type": "Element",
                    "required": True,
                }
            )
            urladdin_info: Optional[str] = field(
                default=None,
                metadata={
                    "name": "URLAddinInfo",
                    "type": "Element",
                }
            )

            @dataclass
            class CustomerSignature:
                """
                :ivar group_signatures: Группа электронных подписей
                """
                group_signatures: List["Settings.Data.CryptoParameters.CustomerSignature.GroupSignatures"] = field(
                    default_factory=list,
                    metadata={
                        "name": "GroupSignatures",
                        "type": "Element",
                        "min_occurs": 1,
                    }
                )

                @dataclass
                class GroupSignatures:
                    """
                    :ivar certificate: Сертификаты электронных подписей
                        сотрудников клиента
                    :ivar number_group: Номер группы электронных
                        подписей
                    """
                    certificate: List[bytes] = field(
                        default_factory=list,
                        metadata={
                            "name": "Certificate",
                            "type": "Element",
                            "min_occurs": 1,
                            "max_occurs": 9,
                            "format": "base64",
                        }
                    )
                    number_group: Optional[int] = field(
                        default=None,
                        metadata={
                            "name": "numberGroup",
                            "type": "Attribute",
                            "required": True,
                        }
                    )

            @dataclass
            class Encrypted:
                """
                :ivar encrypt_algorithm: Алгоритм шифрования, например,
                    GOST 28147-89
                """
                encrypt_algorithm: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "EncryptAlgorithm",
                        "type": "Element",
                        "required": True,
                        "max_length": 50,
                    }
                )

        @dataclass
        class Document:
            """
            :ivar signed: Применение электронной подписи для данного
                вида электронного документа
            :ivar doc_kind: Код вида электронного документа, как он
                задан в описании к стандарту
            """
            signed: Optional["Settings.Data.Document.Signed"] = field(
                default=None,
                metadata={
                    "name": "Signed",
                    "type": "Element",
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
            class Signed:
                """
                :ivar rule_signatures: Правило, задающее наличие
                    электронных подписей для данного вида электронного
                    документа
                """
                rule_signatures: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "RuleSignatures",
                        "type": "Element",
                        "required": True,
                    }
                )

        @dataclass
        class ReceiptStatement:
            """
            :ivar login: Логин, по которому можно получать только
                выписку банка
            :ivar instructions: Инструкция по получению пароля для
                вышеуказанного логина
            """
            login: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Login",
                    "type": "Element",
                    "required": True,
                    "max_length": 50,
                }
            )
            instructions: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Instructions",
                    "type": "Element",
                    "required": True,
                }
            )

        @dataclass
        class Letters:
            """
            :ivar attachments_limit: Максимальный суммартный объем
                присоединенных файлов (в байтах)
            :ivar letter_type: Возможные типы писем
            """
            attachments_limit: Optional[int] = field(
                default=None,
                metadata={
                    "name": "AttachmentsLimit",
                    "type": "Element",
                    "required": True,
                }
            )
            letter_type: List["Settings.Data.Letters.LetterType"] = field(
                default_factory=list,
                metadata={
                    "name": "LetterType",
                    "type": "Element",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class LetterType:
                """
                :ivar code: Код типа письма
                :ivar name: Наименование письма
                """
                code: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Code",
                        "type": "Element",
                        "required": True,
                        "max_length": 2,
                    }
                )
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "Name",
                        "type": "Element",
                        "required": True,
                        "max_length": 150,
                    }
                )
