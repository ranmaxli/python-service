#!/usr/bin/env python
import os
import re
import argparse
from bottle import template

def get_handler(handler_name):
    if not handler_name[0].isupper():
        raise Exception("handler name [%s] must be HumpForm" % handler_name)
    filename = ""
    for idx, char in enumerate(handler_name):
        if char.isupper():
            if idx == 0:
                filename += char.lower()
            else:
                filename += "_" + char.lower()
        else:
            filename += char
    if not filename.endswith("_handler"):
        filename += "_handler"
        handler_name += "Handler"
    filename += ".py"
    return filename, handler_name

def format_method(method):
    methods = ["head", "get", "post", "delete", "patch", "put", "options"]
    if method.lower() not in methods:
        raise Exception("unknown method [%s]" % method)
    return method.lower()

def register_handler(url_path, fn, handler_name):
    if not url_path.startswith("/"):
        url_path = "/" + url_path
    register_file = "../src/handler_mapping.py"
    if not os.path.exists(register_file):
        raise Exception("file [%s] not exists" % register_file)
    cont = open(register_file).read()
    m = re.search("handler_mapping\s*=\s*(\[\s*(.*)\s*\])", cont, re.S)
    if not m:
        raise Exception("can not find handler_mapping")
    class_path = "handlers.%s.%s" % (fn[:-len(".py")], handler_name)
    new_str = append_handler_string(m.group(2), f"(\"{url_path}\", \"{class_path}\")")
    cont = cont[:m.start(1)] + f"[\n{new_str}\n]" + cont[m.end(1):]
    with open(register_file, "w") as f:
        f.write(cont)

def append_handler_string(org_str, new_str):
    start_char = "("
    end_char = ")"
    items = []
    count = 0
    item = ""
    for char in org_str:
        if char == start_char:
            count += 1
            item += char
        elif char == end_char:
            count -= 1
            item += char
            if count == 0:
                items.append(item)
                item = ""
        else:
            if count > 0:
                item += char
    items.append(new_str)
    return ",\n".join(["    " + item for item in items])

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("handler_name", type=str, help="handler class name")
    parser.add_argument("path", type=str, help="http path")
    parser.add_argument("-m", "--method", type=str, help="http method, default is post", default="post")

    args = parser.parse_args()
    fn, cls = get_handler(args.handler_name)
    method = format_method(args.method)
    handler_folder = "../src/handlers"

    if not os.path.exists(handler_folder):
        os.mkdir(handler_folder)
    handler_path = os.path.join(handler_folder, fn)
    if os.path.exists(handler_path):
        print("file [%s] has exists" % handler_path)
        exit(0)
    with open(handler_path, "w") as f:
        f.write(template(open("handler.py.tpl").read(), handler_name=cls, method=method))
    register_handler(args.path, fn, cls)
    print("add handler success")
