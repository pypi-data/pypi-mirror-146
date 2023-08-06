from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="BearerToken")


@attr.s(auto_attribs=True)
class BearerToken:
    """ """

    access_token: str
    email: str

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "access_token": access_token,
                "email": email,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        email = d.pop("email")

        bearer_token = cls(
            access_token=access_token,
            email=email,
        )

        return bearer_token
