from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ExchCommon import (
    ParticipantType,
    SignatureType,
)

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class Letter:
    """
    Письмо.

    :ivar sender: Отправитель
    :ivar recipient: Получатель
    :ivar data: Данные письма
    :ivar id:
    :ivar format_version:
    :ivar creation_date:
    :ivar user_agent:
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
    data: Optional["Letter.Data"] = field(
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
        :ivar doc_num: Номер документа
        :ivar doc_date: Дата составления
        :ivar letter_type_code: Код типа письма
        :ivar theme: Тема письма
        :ivar text: Текст письма
        :ivar attachment: Вложение
        :ivar linked_doc: Объект обсуждения. Например, платежное
            поручение или требование.
        :ivar linked_id: ID изначального письма
        :ivar correspondence_id: ID переписки
        """
        doc_num: Optional[str] = field(
            default=None,
            metadata={
                "name": "DocNum",
                "type": "Element",
                "required": True,
            }
        )
        doc_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "DocDate",
                "type": "Element",
                "required": True,
            }
        )
        letter_type_code: Optional[str] = field(
            default=None,
            metadata={
                "name": "LetterTypeCode",
                "type": "Element",
                "max_length": 2,
            }
        )
        theme: Optional[str] = field(
            default=None,
            metadata={
                "name": "Theme",
                "type": "Element",
                "max_length": 100,
            }
        )
        text: Optional[str] = field(
            default=None,
            metadata={
                "name": "Text",
                "type": "Element",
                "required": True,
            }
        )
        attachment: List["Letter.Data.Attachment"] = field(
            default_factory=list,
            metadata={
                "name": "Attachment",
                "type": "Element",
            }
        )
        linked_doc: Optional["Letter.Data.LinkedDoc"] = field(
            default=None,
            metadata={
                "name": "LinkedDoc",
                "type": "Element",
            }
        )
        linked_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "linkedID",
                "type": "Attribute",
            }
        )
        correspondence_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "correspondenceID",
                "type": "Attribute",
            }
        )

        @dataclass
        class Attachment:
            """
            :ivar binary_file: Двоичные данные файла
            :ivar signature: Данные электронных подписей
            """
            binary_file: Optional["Letter.Data.Attachment.BinaryFile"] = field(
                default=None,
                metadata={
                    "name": "BinaryFile",
                    "type": "Element",
                    "required": True,
                }
            )
            signature: List[SignatureType] = field(
                default_factory=list,
                metadata={
                    "name": "Signature",
                    "type": "Element",
                }
            )

            @dataclass
            class BinaryFile:
                """
                :ivar value:
                :ivar id: Уникальный идентификатор вложения
                :ivar name: Полное имя файла с расширением
                :ivar extension: Расширение имени файла
                :ivar size: Размер файла в байтах
                :ivar crc: Контрольная сумма файла (алгоритм CRC32)
                :ivar creation_date: Дата создания
                """
                value: Optional[bytes] = field(
                    default=None,
                    metadata={
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
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                        "min_length": 1,
                        "max_length": 256,
                    }
                )
                extension: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                        "max_length": 10,
                    }
                )
                size: Optional[int] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )
                crc: Optional[int] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
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

        @dataclass
        class LinkedDoc:
            """
            :ivar id: Идентификатор документа
            :ivar dockind: Код вида электронного документа, как он задан
                в описаниии к стандарту
            """
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
