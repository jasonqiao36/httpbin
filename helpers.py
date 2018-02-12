import base64
import json
from flask import request

ASCII_ART = """
    -=[ teapot ]=-

       _...._
     .'  _ _ `.
    | ."` ^ `". _,
    \_;`"---"`|//
      |       ;/
      \_     _/
        `\"\"\"`
"""


def convert_to_normal_dict(obj):
    """
    将ImmutableMultiDict转化为普通dict
    :param obj:
    :return:
    """
    ret = dict()
    for k, v in obj.to_dict(flat=False).items():
        if len(v) == 1:
            ret[k] = v[0]
        else:
            ret[k] = v
    return ret


def gen_base64(filename):
    with open(filename, 'rb') as f:
        return base64.b64encode(f.read())


def json_safe(string, content_type='application/octet-stream'):
    try:
        string = string.decode('utf8')
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b''.join([
            b'data:',
            content_type.encode('utf8'),
            b':base64;',
            base64.b64encode(string)
        ]).decode('utf8')


def get_files():
    files = dict()

    for k, v in request.files.items():

        content_type = request.files[k].content_type or 'application/octet-stream'
        val = json_safe(v.read(), content_type)
        if files.get(k):
            if not isinstance(files[k], list):
                files[k] = [files[k]]
            else:
                files[k].append(val)
        else:
            files[k] = val
    return files


if __name__ == '__main__':
    # from werkzeug.datastructures import ImmutableMultiDict
    #
    # obj = ImmutableMultiDict(dict(name=['tom', 'jason'], age=30))
    # print(convert_to_normal_dict(obj))

    print(gen_base64('device.xlsx'))
