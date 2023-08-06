from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from ExchCommon import ErrorType
from Packet import Packet

__NAMESPACE__ = "http://directbank.1c.ru/XMLSchema"


@dataclass
class GetPacketListResponseType:
    """
    :ivar packet_id: Идентификатор транспортного контейнера (GUID), по
        которому его можно получить клиенту
    :ivar time_stamp_last_packet: Метка времени, на которую вернули всю
        актуальную информацию
    """
    packet_id: List[str] = field(
        default_factory=list,
        metadata={
            "name": "PacketID",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    time_stamp_last_packet: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "TimeStampLastPacket",
            "type": "Attribute",
        }
    )


@dataclass
class GetSettingsResponseType:
    """
    :ivar data: Настройки обмена с банком
    :ivar id: Идентификатор настроек
    :ivar format_version: Версия формата
    :ivar creation_date: Дата и время формирования
    :ivar user_agent: Наименование и версия программы
    """
    data: Optional["GetSettingsResponseType.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
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
        :ivar value:
        :ivar dockind: Код вида электронного документа, как он задан в
            описаниии к стандарту
        """
        value: Optional[bytes] = field(
            default=None,
            metadata={
                "required": True,
                "format": "base64",
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


@dataclass
class LogonCertResponseType:
    """
    :ivar encrypted_sid: Зашифрованный Идентификатор сессии
    """
    encrypted_sid: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "EncryptedSID",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
            "format": "base64",
        }
    )


@dataclass
class LogonResponseType:
    """
    :ivar sid: Идентификатор сессии
    :ivar extra_auth: Дополнительная аутентификация. Указывается, если
        требуется доп. аутентфикация
    """
    sid: Optional[str] = field(
        default=None,
        metadata={
            "name": "SID",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )
    extra_auth: Optional["LogonResponseType.ExtraAuth"] = field(
        default=None,
        metadata={
            "name": "ExtraAuth",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )

    @dataclass
    class ExtraAuth:
        """
        :ivar otp: Параметры доп.аутентификации, которые будут
            направляны клиенту
        """
        otp: Optional["LogonResponseType.ExtraAuth.Otp"] = field(
            default=None,
            metadata={
                "name": "OTP",
                "type": "Element",
                "namespace": "http://directbank.1c.ru/XMLSchema",
            }
        )

        @dataclass
        class Otp:
            """
            :ivar phone_mask: Маска телефона или номер  клиента
            :ivar code: Короткий код сессии, который будет показан при
                вводе OTP
            """
            phone_mask: Optional[str] = field(
                default=None,
                metadata={
                    "name": "phoneMask",
                    "type": "Attribute",
                    "max_length": 12,
                }
            )
            code: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "max_length": 10,
                }
            )


@dataclass
class SendPacketResponseType:
    """
    :ivar id: Идентификатор транспортного контейнера (GUID), который был
        ему назначен на стороне банка
    """
    id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ID",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
            "required": True,
        }
    )


@dataclass
class SuccessResultType:
    """
    :ivar send_packet_response: Отправка транспортного контейнера в банк
    :ivar get_packet_list_response: Список ID транспортных контейнеров,
        готовых к передачи клиенту
    :ivar get_packet_response: Транспортный контейнер с данными
        электронных документов для получения клиентом
    :ivar logon_response: Аутентификация по логину + ОТР (опционально)
    :ivar logon_cert_response: Аутентификация по сертификату
    :ivar get_settings_response: Получение настроек обмена в
        автоматическом режиме
    """
    send_packet_response: Optional[SendPacketResponseType] = field(
        default=None,
        metadata={
            "name": "SendPacketResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    get_packet_list_response: Optional[GetPacketListResponseType] = field(
        default=None,
        metadata={
            "name": "GetPacketListResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    get_packet_response: Optional[Packet] = field(
        default=None,
        metadata={
            "name": "GetPacketResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    logon_response: Optional[LogonResponseType] = field(
        default=None,
        metadata={
            "name": "LogonResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    logon_cert_response: Optional[LogonCertResponseType] = field(
        default=None,
        metadata={
            "name": "LogonCertResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )
    get_settings_response: Optional[GetSettingsResponseType] = field(
        default=None,
        metadata={
            "name": "GetSettingsResponse",
            "type": "Element",
            "namespace": "http://directbank.1c.ru/XMLSchema",
        }
    )


@dataclass
class ResultBank:
    """
    :ivar success: Успешный ответ банка
    :ivar error: Ответ банка в случае возникновения ошибки
    :ivar format_version: Версия формата
    :ivar user_agent: Наименование и версия программы
    """

    class Meta:
        namespace = "http://directbank.1c.ru/XMLSchema"

    success: Optional[SuccessResultType] = field(
        default=None,
        metadata={
            "name": "Success",
            "type": "Element",
        }
    )
    error: Optional[ErrorType] = field(
        default=None,
        metadata={
            "name": "Error",
            "type": "Element",
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
    user_agent: Optional[str] = field(
        default=None,
        metadata={
            "name": "userAgent",
            "type": "Attribute",
            "max_length": 100,
        }
    )
