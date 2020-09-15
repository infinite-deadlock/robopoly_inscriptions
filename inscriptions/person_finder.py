#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Based on the work of GregLeBarbar, MIT License, https://github.com/epfl-si/epfl-ldap, consulted 18/04/2020
# MIT License
# Copyright (c) 2017 Ecole Polytechnique Federale de Lausanne, Switzerland
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import ldap3

LDAP_SERVER_BASE = 'ldap.epfl.ch'
LDAP_SERVER_REGIO = 'c=ch'
LDAP_SERVER_CONNECTION_TIMEOUT = 2  # in sec

def get_LDAP_connection():
    """
    Return a LDAP connection
    """
    server = ldap3.Server('ldap://' + LDAP_SERVER_BASE, connect_timeout=LDAP_SERVER_CONNECTION_TIMEOUT)
    connection = ldap3.Connection(server)
    connection.open()

    return connection

def LDAP_search(pattern_search, attribute):
    """
    Do a LDAP search
    """
    connection = get_LDAP_connection()

    connection.search(search_base=LDAP_SERVER_REGIO, search_filter=pattern_search, attributes=[attribute])
    # attributes=['*'] to show everything

    return connection.response

def get_attribute(sciper, attribute):
    try:
        response = LDAP_search('(uniqueIdentifier={})'.format(sciper), attribute)
        return response[-1]['attributes'][attribute][0]
    except ldap3.core.exceptions.LDAPSocketOpenError:
        print("LDAP EPFL SERVER UNREACHABLE ! USE VPN !")
    except:
        print("Impossible to get attribute{} for sciper {}".format(attribute, sciper))
    return ''


def LDAP_get_infos(sciper):
    """
    Return informations of this user
    """
    mail = get_attribute(sciper, 'mail')
    first_name = get_attribute(sciper, 'givenName')
    name = get_attribute(sciper, 'sn')
    title = get_attribute(sciper, 'personalTitle')
    section = get_attribute(sciper, 'ou')

    return [title, first_name, name, mail, section]

if __name__ == "__main__":
    print(LDAP_get_infos(273553))
