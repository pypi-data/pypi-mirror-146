from dataclasses import dataclass
from enum import Enum
from random import choice
from typing import List


def str_type(name: str):
    return type(name, (str,), {})


def int_type(name: str):
    return type(name, (int,), {})


Address = str_type("Address")
BBAN = str_type("BBAN")
CarNumber = str_type("CarNumber")
Country = str_type("Country")
CountryCode = str_type("CountryCode")
CreditCardExpire = str_type("CreditCardExpire")
CreditCardNumber = str_type("CreditCardNumber")
CreditCardProvider = str_type("CreditCardProvider")
CreditCardSecurityCode = str_type("CreditCardSecurityCode")
CompanyName = str_type("CompanyName")
CompanySuffix = str_type("CompanySuffix")
Date = str_type("Date")
Email = str_type("Email")
FileName = str_type("FileName")
FirstName = str_type("FirstName")
PostCode = str_type("PostCode")
StreetAddress = str_type("StreetAddress")
IBAN = str_type("IBAN")
SWIFT11 = str_type("SWIFT11")
SWIFT8 = str_type("SWIFT8")
Ipv4 = str_type("Ipv4")
Ipv6 = str_type("Ipv6")
MacAddress = str_type("MacAddress")
UserAgent = str_type("UserAgent")
URI = str_type("URI")
Username = str_type("UserName")
LastName = str_type("LastName")
MiddleName = str_type("MiddleName")
Paragraph = str_type("Paragraph")
Password = str_type("Password")
Patronymic = str_type("Patronymic")
PhoneNumber = str_type("PhoneNumber")
Job = str_type("Job")
BusinessInn = str_type("BusinessInn")
IndividualsInn = str_type("IndividualInn")
BusinessOgrn = str_type("BusinessOgrn")
IndividualsOgrn = str_type("BusinessOgrn")
Kpp = str_type("Kpp")
TimeStamp = int_type("TimeStamp")


class BaseEnum(Enum):
    @classmethod
    def all(cls):
        return [i.value for i in cls]

    @classmethod
    def random(cls):
        return choice(cls.all())


@dataclass
class NamedData:
    code: str
    text: str
    digital_code: int = None


class NamedEnum(Enum):
    @classmethod
    def all(cls) -> List[NamedData]:
        return [i.value for i in cls]

    @classmethod
    def all_code(cls):
        return [i.value.code for i in cls]

    @classmethod
    def all_text(cls):
        return [i.value.text for i in cls]

    @classmethod
    def random(cls):
        return choice(cls.all())

    @classmethod
    def random_code(cls):
        return choice(cls.all_code())

    @classmethod
    def random_text(cls):
        return choice(cls.all_text())

    @classmethod
    def dict(cls) -> dict:
        d = {}
        for i in cls:
            d[i.value.code] = i.value.text
        return d

    @classmethod
    def text_by_code(cls, code: str) -> str:
        return cls.dict().get(code)

    @classmethod
    def code_by_text(cls, text: str) -> str:
        for k, v in cls.dict().items():
            if v == text:
                return k
        return None

    @property
    def text(self):
        return self.value.text

    @property
    def code(self):
        return self.value.code

    @property
    def digital_code(self):
        return self.value.digital_code
