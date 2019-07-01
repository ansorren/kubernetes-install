#!/usr/bin/python

from ansible.module_utils.basic import *

import os
import struct
import time
import base64

def ceph_key(params):
    dest = params['dest']
    state = params['state']
    force = params['force']

    file_exist = os.path.isfile(dest)

    if state == 'absent':
        if file_exist:
            os.unlink(dest)
            return True, {"msg": "Deleted", "params": params}
        return False, {"msg": "NotFound", "params": params}

    if file_exist and not force:
        return False, {"msg": "Exist", "params": params}

    with open(dest, 'w') as key_file:
        key = os.urandom(16)
        header = struct.pack(
            '<hiih',
            1,                 # le16 type: CEPH_CRYPTO_AES
            int(time.time()),  # le32 created: seconds
            0,                 # le32 created: nanoseconds,
            len(key),          # le16: len(key)
        )
        key_file.write(base64.b64encode(header + key).decode('ascii'))

    return True, {"msg": "Written", "params": params}

def main():
    module_args = {
        "dest": {
            "type": "str",
            "required": True
        },
        "state": {
            "type": "str",
            "required": True,
            "choices": ["present", "absent"]
        },
        "force": {
            "type": "bool",
            "required": False,
            "default": False
        },
    }
    module = AnsibleModule(argument_spec=module_args)
    changed, result = ceph_key(module.params)
    module.exit_json(changed=changed, meta=result)

if __name__ == '__main__':
    main()
