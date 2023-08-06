# -*- coding: utf-8 -*-
"""
    pip_services_common.errors.UnknownException
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Unknown error type
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from typing import Optional

from .ApplicationException import ApplicationException
from .ErrorCategory import ErrorCategory


class UnknownException(ApplicationException):
    """
    Unknown or unexpected errors
    """

    def __init__(self, correlation_id: Optional[str] = None, code: str = None, message: str = None):
        """
        Creates an error instance and assigns its values.

        :param correlation_id: (optional) a unique transaction id to trace execution through call chain.

        :param code: (optional) a unique error code. Default: "UNKNOWN"

        :param message: (optional) a human-readable description of the error.
        """
        super(UnknownException, self).__init__(ErrorCategory.Unknown, correlation_id, code, message)
        self.status = 500
