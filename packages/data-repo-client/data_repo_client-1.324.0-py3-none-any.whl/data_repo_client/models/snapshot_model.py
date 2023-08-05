# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from data_repo_client.configuration import Configuration


class SnapshotModel(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'id': 'str',
        'name': 'str',
        'description': 'str',
        'created_date': 'str',
        'consent_code': 'str',
        'source': 'list[SnapshotSourceModel]',
        'tables': 'list[TableModel]',
        'relationships': 'list[RelationshipModel]',
        'profile_id': 'str',
        'data_project': 'str',
        'access_information': 'AccessInfoModel',
        'creation_information': 'SnapshotRequestContentsModel'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'created_date': 'createdDate',
        'consent_code': 'consentCode',
        'source': 'source',
        'tables': 'tables',
        'relationships': 'relationships',
        'profile_id': 'profileId',
        'data_project': 'dataProject',
        'access_information': 'accessInformation',
        'creation_information': 'creationInformation'
    }

    def __init__(self, id=None, name=None, description=None, created_date=None, consent_code=None, source=None, tables=None, relationships=None, profile_id=None, data_project=None, access_information=None, creation_information=None, local_vars_configuration=None):  # noqa: E501
        """SnapshotModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._description = None
        self._created_date = None
        self._consent_code = None
        self._source = None
        self._tables = None
        self._relationships = None
        self._profile_id = None
        self._data_project = None
        self._access_information = None
        self._creation_information = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if created_date is not None:
            self.created_date = created_date
        if consent_code is not None:
            self.consent_code = consent_code
        if source is not None:
            self.source = source
        if tables is not None:
            self.tables = tables
        if relationships is not None:
            self.relationships = relationships
        if profile_id is not None:
            self.profile_id = profile_id
        if data_project is not None:
            self.data_project = data_project
        if access_information is not None:
            self.access_information = access_information
        if creation_information is not None:
            self.creation_information = creation_information

    @property
    def id(self):
        """Gets the id of this SnapshotModel.  # noqa: E501

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :return: The id of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SnapshotModel.

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :param id: The id of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this SnapshotModel.  # noqa: E501

        Dataset and snapshot names follow this pattern. It is the same as ObjectNameProperty, but has a greater maxLength.   # noqa: E501

        :return: The name of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SnapshotModel.

        Dataset and snapshot names follow this pattern. It is the same as ObjectNameProperty, but has a greater maxLength.   # noqa: E501

        :param name: The name of this SnapshotModel.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 511):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `511`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and not re.search(r'^[a-zA-Z0-9][_a-zA-Z0-9]*$', name)):  # noqa: E501
            raise ValueError(r"Invalid value for `name`, must be a follow pattern or equal to `/^[a-zA-Z0-9][_a-zA-Z0-9]*$/`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this SnapshotModel.  # noqa: E501

        Description of the snapshot  # noqa: E501

        :return: The description of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SnapshotModel.

        Description of the snapshot  # noqa: E501

        :param description: The description of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def created_date(self):
        """Gets the created_date of this SnapshotModel.  # noqa: E501

        Date the snapshot was created  # noqa: E501

        :return: The created_date of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this SnapshotModel.

        Date the snapshot was created  # noqa: E501

        :param created_date: The created_date of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._created_date = created_date

    @property
    def consent_code(self):
        """Gets the consent_code of this SnapshotModel.  # noqa: E501

        Consent code together with PHS Id that will determine user access  # noqa: E501

        :return: The consent_code of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._consent_code

    @consent_code.setter
    def consent_code(self, consent_code):
        """Sets the consent_code of this SnapshotModel.

        Consent code together with PHS Id that will determine user access  # noqa: E501

        :param consent_code: The consent_code of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._consent_code = consent_code

    @property
    def source(self):
        """Gets the source of this SnapshotModel.  # noqa: E501


        :return: The source of this SnapshotModel.  # noqa: E501
        :rtype: list[SnapshotSourceModel]
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this SnapshotModel.


        :param source: The source of this SnapshotModel.  # noqa: E501
        :type: list[SnapshotSourceModel]
        """

        self._source = source

    @property
    def tables(self):
        """Gets the tables of this SnapshotModel.  # noqa: E501


        :return: The tables of this SnapshotModel.  # noqa: E501
        :rtype: list[TableModel]
        """
        return self._tables

    @tables.setter
    def tables(self, tables):
        """Sets the tables of this SnapshotModel.


        :param tables: The tables of this SnapshotModel.  # noqa: E501
        :type: list[TableModel]
        """

        self._tables = tables

    @property
    def relationships(self):
        """Gets the relationships of this SnapshotModel.  # noqa: E501


        :return: The relationships of this SnapshotModel.  # noqa: E501
        :rtype: list[RelationshipModel]
        """
        return self._relationships

    @relationships.setter
    def relationships(self, relationships):
        """Sets the relationships of this SnapshotModel.


        :param relationships: The relationships of this SnapshotModel.  # noqa: E501
        :type: list[RelationshipModel]
        """

        self._relationships = relationships

    @property
    def profile_id(self):
        """Gets the profile_id of this SnapshotModel.  # noqa: E501

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :return: The profile_id of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._profile_id

    @profile_id.setter
    def profile_id(self, profile_id):
        """Sets the profile_id of this SnapshotModel.

        Unique identifier for a dataset, snapshot, etc.   # noqa: E501

        :param profile_id: The profile_id of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._profile_id = profile_id

    @property
    def data_project(self):
        """Gets the data_project of this SnapshotModel.  # noqa: E501

        Project id of the snapshot data project  # noqa: E501

        :return: The data_project of this SnapshotModel.  # noqa: E501
        :rtype: str
        """
        return self._data_project

    @data_project.setter
    def data_project(self, data_project):
        """Sets the data_project of this SnapshotModel.

        Project id of the snapshot data project  # noqa: E501

        :param data_project: The data_project of this SnapshotModel.  # noqa: E501
        :type: str
        """

        self._data_project = data_project

    @property
    def access_information(self):
        """Gets the access_information of this SnapshotModel.  # noqa: E501


        :return: The access_information of this SnapshotModel.  # noqa: E501
        :rtype: AccessInfoModel
        """
        return self._access_information

    @access_information.setter
    def access_information(self, access_information):
        """Sets the access_information of this SnapshotModel.


        :param access_information: The access_information of this SnapshotModel.  # noqa: E501
        :type: AccessInfoModel
        """

        self._access_information = access_information

    @property
    def creation_information(self):
        """Gets the creation_information of this SnapshotModel.  # noqa: E501


        :return: The creation_information of this SnapshotModel.  # noqa: E501
        :rtype: SnapshotRequestContentsModel
        """
        return self._creation_information

    @creation_information.setter
    def creation_information(self, creation_information):
        """Sets the creation_information of this SnapshotModel.


        :param creation_information: The creation_information of this SnapshotModel.  # noqa: E501
        :type: SnapshotRequestContentsModel
        """

        self._creation_information = creation_information

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SnapshotModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SnapshotModel):
            return True

        return self.to_dict() != other.to_dict()
