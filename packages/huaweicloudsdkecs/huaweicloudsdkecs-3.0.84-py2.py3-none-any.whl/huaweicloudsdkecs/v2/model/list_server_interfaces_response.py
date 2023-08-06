# coding: utf-8

import re
import six


from huaweicloudsdkcore.sdk_response import SdkResponse
from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class ListServerInterfacesResponse(SdkResponse):


    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'attachable_quantity': 'InterfaceAttachableQuantity',
        'interface_attachments': 'list[InterfaceAttachment]'
    }

    attribute_map = {
        'attachable_quantity': 'attachableQuantity',
        'interface_attachments': 'interfaceAttachments'
    }

    def __init__(self, attachable_quantity=None, interface_attachments=None):
        """ListServerInterfacesResponse - a model defined in huaweicloud sdk"""
        
        super(ListServerInterfacesResponse, self).__init__()

        self._attachable_quantity = None
        self._interface_attachments = None
        self.discriminator = None

        if attachable_quantity is not None:
            self.attachable_quantity = attachable_quantity
        if interface_attachments is not None:
            self.interface_attachments = interface_attachments

    @property
    def attachable_quantity(self):
        """Gets the attachable_quantity of this ListServerInterfacesResponse.


        :return: The attachable_quantity of this ListServerInterfacesResponse.
        :rtype: InterfaceAttachableQuantity
        """
        return self._attachable_quantity

    @attachable_quantity.setter
    def attachable_quantity(self, attachable_quantity):
        """Sets the attachable_quantity of this ListServerInterfacesResponse.


        :param attachable_quantity: The attachable_quantity of this ListServerInterfacesResponse.
        :type: InterfaceAttachableQuantity
        """
        self._attachable_quantity = attachable_quantity

    @property
    def interface_attachments(self):
        """Gets the interface_attachments of this ListServerInterfacesResponse.

        云服务器网卡信息列表

        :return: The interface_attachments of this ListServerInterfacesResponse.
        :rtype: list[InterfaceAttachment]
        """
        return self._interface_attachments

    @interface_attachments.setter
    def interface_attachments(self, interface_attachments):
        """Sets the interface_attachments of this ListServerInterfacesResponse.

        云服务器网卡信息列表

        :param interface_attachments: The interface_attachments of this ListServerInterfacesResponse.
        :type: list[InterfaceAttachment]
        """
        self._interface_attachments = interface_attachments

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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ListServerInterfacesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
