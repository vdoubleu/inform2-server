# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from inform_server.models.base_model_ import Model
from inform_server import util


class Opinion(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, id: int=None, user: str=None, value: int=None):  # noqa: E501
        """Opinion - a model defined in Swagger

        :param id: The id of this Opinion.  # noqa: E501
        :type id: int
        :param user: The user of this Opinion.  # noqa: E501
        :type user: str
        :param value: The value of this Opinion.  # noqa: E501
        :type value: int
        """
        self.swagger_types = {
            'id': int,
            'user': str,
            'value': int
        }

        self.attribute_map = {
            'id': 'id',
            'user': 'user',
            'value': 'value'
        }
        self._id = id
        self._user = user
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Opinion':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Opinion of this Opinion.  # noqa: E501
        :rtype: Opinion
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        """Gets the id of this Opinion.

        article id  # noqa: E501

        :return: The id of this Opinion.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Opinion.

        article id  # noqa: E501

        :param id: The id of this Opinion.
        :type id: int
        """

        self._id = id

    @property
    def user(self) -> str:
        """Gets the user of this Opinion.

        name of user who gave the opinion  # noqa: E501

        :return: The user of this Opinion.
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user: str):
        """Sets the user of this Opinion.

        name of user who gave the opinion  # noqa: E501

        :param user: The user of this Opinion.
        :type user: str
        """

        self._user = user

    @property
    def value(self) -> int:
        """Gets the value of this Opinion.

        the users opinion, 1 for positive, 0 for no opinion, -1 for negative  # noqa: E501

        :return: The value of this Opinion.
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value: int):
        """Sets the value of this Opinion.

        the users opinion, 1 for positive, 0 for no opinion, -1 for negative  # noqa: E501

        :param value: The value of this Opinion.
        :type value: int
        """

        self._value = value