#!/usr/bin/python
#

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import *
from jsonschema import validate, ValidationError
import urllib, json, os, sys

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'equail@redhat.com'}

DOCUMENTATION = '''
---
module: json_validator

version_added: "2.9"

short_description: Validates JSON document against schema

description:
    - Uses jsonschema package to validate a document against its schema. 
      Will look for the "$schema" definition in the root of the document.

options:
    json:
        description:
            - The JSON document to be validated
        required: true
        default: null
    schema:
        description:
            - A JSON schema document.
        required: false
        default: null

author:
    - "equail@redhat.com"
'''
EXAMPLES = '''
    - name: Validate the application manifest 
      json_validator:
        json: manifest
'''

RETURN = '''
'''  # NOQA



def main():
    # The AnsibleModule provides lots of common code for handling returns, parses your arguments for you, and allows you to check inputs
    module = AnsibleModule(
        argument_spec=dict(
        json=dict(required=True, type='raw'),
        schema=dict(required=False)
        ),
        supports_check_mode=True
    )

    # in check mode we take no action
    # since this module actually never changes system state we'll just return False
    if module.check_mode:
        module.exit_json(changed=False)



    _json = module.params['json']
    _schema = module.params['schema']

    if _schema is None:
        if _json['$schema'] is not None:
            response = urllib.urlopen(_json['$schema'])
            _schema = json.loads(response.read())
    else:
        _schema = json.loads(_schema)

    if _schema is None:
        module.fail_json(msg="Schema is not supplied and cannot be loaded from $schema url in document")

    try:
        validate(_json, _schema)
    except ValidationError as ve:
        module.fail_json(msg=str(ve))
    except:
        module.fail_json(msg="Unknown Schema Validation Failed")            
    else:
        module.exit_json(changed=True, msg="Schema Validation Succeeded")

if __name__ == '__main__':
    main()
