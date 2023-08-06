##############################################################################
#
# Copyright (c) 2006 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from z3c.schema.email.interfaces import IRFC822MailAddress
from z3c.schema.email.interfaces import NotValidRFC822MailAdress
from z3c.schema.email.field import isValidMailAddress
from z3c.schema.email.field import RFC822MailAddress


__all__ = [
    'IRFC822MailAddress',
    'NotValidRFC822MailAdress',
    'isValidMailAddress',
    'RFC822MailAddress',
]
