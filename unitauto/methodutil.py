# encoding=utf-8
# MIT License
#
# Copyright (c) 2023 TommyLemon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import asyncio
import builtins
import json
import re
import time
import inspect
from typing import Type

null = None
false = False
true = True

KEY_OK = 'ok'
KEY_CODE = 'code'
KEY_MSG = 'msg'
KEY_THROW = 'throw'
KEY_TRACE = 'trace'

CODE_SUCCESS = 200
CODE_SERVER_ERROR = 500
MSG_SUCCESS = 'success'
LANGUAGE = 'Python'

KEY_LANGUAGE = "language"
KEY_REUSE = "reuse"
KEY_UI = "ui"
KEY_TIME = "time"
KEY_TIMEOUT = "timeout"
KEY_PACKAGE = "package"
KEY_THIS = "this"
KEY_CLASS = "class"
KEY_CONSTRUCTOR = "constructor"
KEY_KEY = 'key'
KEY_TYPE = "type"
KEY_AT_TYPE = "@type"
KEY_VALUE = "value"
KEY_WARN = "warn"
KEY_STATIC = "static"
KEY_ASYNC = "async"
KEY_NAME = "name"
KEY_METHOD = "method"
KEY_MOCK = "mock"
KEY_QUERY = "query"
KEY_RETURN = "return"
KEY_TIME_DETAIL = "time:start|duration|end"
KEY_CLASS_ARGS = "classArgs"
KEY_METHOD_ARGS = "methodArgs"
KEY_CALLBACK = "callback"
KEY_GLOBAL = "global"

KEY_CALL_LIST = "call()[]"
KEY_CALL_MAP = "call(){}"
KEY_PACKAGE_TOTAL = "packageTotal"
KEY_CLASS_TOTAL = "classTotal"
KEY_METHOD_TOTAL = "methodTotal"
KEY_PACKAGE_LIST = "packageList"
KEY_CLASS_LIST = "classList"
KEY_METHOD_LIST = "methodList"

MILLIS_TIME = 1000000

PATTERN_ALPHABET = re.compile('^[A-Za-z]+$')
PATTERN_NUMBER = re.compile('^[0-9]+$')
PATTERN_NAME = re.compile('^[A-Za-z0-9_]+$')

PRIMITIVE_CLASS_MAP = {
    None: any,
    'None': any,
    'any': any,
    'bool': bool,
    'False': bool,
    'True': bool,
    'int': int,
    'float': float,
    'str': str
}

CLASS_MAP = dict(PRIMITIVE_CLASS_MAP, **{
    'object': object,
    'list': list,
    'tuple': tuple,
    'range': range,
    'slice': slice,
    'set': set,
    'reversed': reversed,
    'dict': dict,
    'map': map,
    'bytes': bytes,
    'bytearray': bytearray,
    'frozenset': frozenset,
    'enumerate': enumerate,
    'filter': filter,
    'complex': complex,
    'Exception': Exception,
    'BaseException': BaseException,
    'OSError': OSError,
    'IOError': IOError,
    'BlockingIOError': BlockingIOError,
    'EnvironmentError': EnvironmentError,
    'ConnectionError': ConnectionError,
    'BrokenPipeError': BrokenPipeError,
    'BufferError': BufferError,
    'EOFError': EOFError,
    'SyntaxError': SyntaxError,
    'FileExistsError': FileExistsError,
    'FileNotFoundError': FileNotFoundError,
    'Warning': Warning,
    'BytesWarning': BytesWarning,
    'ChildProcessError': ChildProcessError,
    'property': property,
    'classmethod': classmethod,
    'staticmethod': staticmethod,
    'super': super,
    'type': type,
    'zip': zip,
})


class InterfaceProxy:
    pass


def get_instance(self, typ: Type, value: any, class_args: list = null, reuse: bool = false):
    return


def on_complete(data: any, method: callable, proxy: InterfaceProxy, *extras: any):
    pass


def on_callback(data: any, method: callable, proxy: InterfaceProxy, *extras: any):
    pass


class Listener:
    complete: callable = callable(on_complete)
    callback: callable = callable(on_callback)
    getinstance: callable = callable(get_instance)


listener = Listener()


def list_method(req) -> dict:
    start_time = time.time_ns()
    try:
        if is_str(req):
            req = parse_json(req)

        mock = req.get(KEY_MOCK)
        assert mock in [null, true, false], KEY_MOCK + ' must must in [true, false]!'

        query = req.get(KEY_QUERY)
        assert query in [null, 0, 1, 2], KEY_QUERY + ' must must in [0, 1, 2]! 0-Data, 1-Total count, 2-Both above'

        package = req.get(KEY_PACKAGE)
        assert is_str(package), KEY_PACKAGE + ' must be str!'

        clazz = req.get(KEY_CLASS)
        assert is_str(clazz), KEY_CLASS + ' must be str!'

        method = req.get(KEY_METHOD)
        assert is_str(method), KEY_METHOD + ' must be str!'

        types = req.get('types')
        assert is_list(types), 'types must be list!'

        is_all_pkg = is_empty(package)
        is_all_cls = is_empty(clazz)
        is_all_mtd = is_empty(method)

        fl = split(clazz, '$')

        module_list = []
        if is_all_pkg:
            root_module = __import__('')
        else:
            mn = package if is_empty(fl) else package + '.' + fl[0]
            root_module = __import__(mn, fromlist=['__init__'] if is_empty(fl) else fl[0])

            module_list.append(root_module)
            try:
                mdl_dict = root_module.__dict__
                vs = mdl_dict.values()
                for v in vs:
                    if type(v).__name__ == 'module' and str(v).endswith("/__init__.py'>"):  # if isinstance(v, module):
                        module_list.append(v)
                        pass
            except Exception as e:
                print(e)

        pkg_list = []

        for module_item in module_list:
            cl = []
            pkg = module_item.__name__
            pkg_str = str(module_item)
            is_file = pkg_str.endswith(".py'>") and not pkg_str.endswith("/__init__.py'>")
            if is_file:
                ns = split(pkg, '.')  # 不存在这个函数 ind = pkg.lastindex('.')
                pkg = pkg[:-1-len(ns[-1])]

            if is_empty(pkg):
                continue

            mdl_list = dir(module_item)
            l = size(mdl_list)

            cls_list = []
            if l > 1 and not is_all_cls:
                try:
                    cls = module_item
                    i = -1
                    for n in fl:
                        i += 1
                        if i <= 0:
                            continue
                        cls = getattr(cls, n)
                    cl = [cls]
                except Exception as e:
                    print(e)
            else:
                for mdl in mdl_list:
                    pn = str(mdl)
                    if is_empty(pn) or pn.startswith('_') or pn.endswith('_'):
                        continue
                    try:
                        cls = getattr(module_item, pn)

                        ct = type(cls).__name__
                        s = str(cls)
                        if ct == 'function':
                            mtd = parse_method(cls) if is_all_mtd or cls.__name__ == method else null
                            if is_empty(mtd):
                                continue

                            cls_list.append({
                                KEY_CLASS: cls.__name__,
                                KEY_METHOD_LIST: [mtd]
                            })
                        if ct == 'class' or ct == 'type':
                            cl.append(cls)
                        elif ct == 'module':
                            if is_file or (s.endswith(".py'>") and not s.endswith("/__init__.py'>")):
                                cl.append(cls)
                            # elif not (cls in module_list):
                            #     module_list.append(cls)
                    except Exception as e:
                        print(e)

            for cls in cl:
                cn = cls.__name__

                cs = str(cls).strip()  # 一样 cs = cls.__str__()
                ind = index(cs, "'")
                if ind >= 0:
                    cs = cs[ind + 1:]

                ind = index(cs, "'")
                if ind >= 0:
                    cs = cs[:ind]

                if not cs.startswith(pkg + '.'):
                    continue

                cs = cs[len(pkg + '.'):]
                if is_empty(cs):
                    continue

                if true:
                    ml = []
                    if callable(cls) and type(cls).__name__ == 'function':
                        if is_all_mtd or cn == method:
                            ml = [cls]
                        else:
                            continue
                    elif not is_all_mtd:
                        try:
                            func = getattr(cls, method)
                            if callable(func) and type(func).__name__ == 'function':
                                ml = [func]
                        except Exception as e:
                            print(e)
                    else:
                        ns = dir(cls)
                        if not_empty(ns):
                            for n in ns:
                                if is_empty(n) or n.startswith('_') or n.endswith('_'):
                                    continue

                                try:
                                    func = getattr(cls, n)
                                    if callable(func):
                                        ft = type(func).__name__
                                        if ft == 'function':
                                            ml.append(func)
                                        elif ft in ('type', 'class') and str(func) == ("<class '" + cn + "." + func.__name__ + "'>"):
                                            cl.append(func)
                                except Exception as e:
                                    print(e)
                        # cls.__class__.methods

                    mtd_list = []
                    for mtd in ml:
                        m = parse_method(mtd)
                        if not_empty(m):
                            mtd_list.append(m)

                    # 不存在这个函数 ind = cn.lastindex('.')
                    # <module 'unitauto.test.testutil' from 'unitauto/test/testutil.py'>
                    # if cs.startswith("class <'"):
                    #     cs = cs[len("class <'"):]
                    # if cs.endswith("'>"):
                    #     cs = cs[:-len("'>")]

                    if is_empty(mtd_list):
                        continue

                    cls_list.append({
                        # KEY_CLASS: cn if ind < 0 else cn[ind+1:],
                        KEY_CLASS: cs.replace('.', '$'),
                        KEY_METHOD_LIST: mtd_list
                    })

            if is_empty(cls_list):
                continue

            pkg_list.append({
                KEY_PACKAGE: pkg,
                KEY_CLASS_LIST: cls_list
            })

        time_detail = get_time_detail(start_time)
        return {
            KEY_LANGUAGE: LANGUAGE,
            KEY_OK: true,
            KEY_CODE: CODE_SUCCESS,
            KEY_MSG: MSG_SUCCESS,
            KEY_PACKAGE_LIST: pkg_list,
            KEY_TIME_DETAIL: time_detail
        }
    except Exception as e:
        return {
            KEY_LANGUAGE: LANGUAGE,
            KEY_OK: false,
            KEY_CODE: CODE_SERVER_ERROR,
            KEY_MSG: str(e),
            KEY_TIME_DETAIL: get_time_detail(start_time),
            KEY_THROW: e.__class__.__name__,
            # KEY_TRACE: e.__traceback__.__str__
        }


def parse_method(func) -> dict:
    signature = null if func is None else inspect.signature(func)
    if signature is None:
        return {}

    return_annotation = signature.return_annotation
    rt = null
    if return_annotation is not None:
        try:
            rt = return_annotation.__name__
        except Exception as e:
            rt = str(return_annotation)

    if rt in ('_empty', 'POSITIONAL_OR_KEYWORD'):
        rt = null

    types = []
    for param in signature.parameters.values():
        a = null if param is None else param.annotation
        n = null
        if a is not None:
            try:
                n = a.__name__
            except Exception as e:
                n = str(a)

        types.append('any' if is_empty(n) or n in ('_empty', 'POSITIONAL_OR_KEYWORD') else n)

    names = [param.name for param in signature.parameters.values()]
    static = is_empty(names) or names[0] != 'self'
    name = func.__name__
    return {
        KEY_STATIC: static,
        'returnType': rt,
        'genericReturnType': rt,
        KEY_METHOD: name,
        KEY_NAME: name,
        'parameterTypeList': types if static else types[1:],
        'genericParameterTypeList': types if static else types[1:],
        'parameterNameList': names if static else names[1:],
        'parameterDefaultValueList': null
    }


def wrap_result(func, method_args, ma_types, ma_values, result, start_time):
    time_detail = get_time_detail(start_time)

    signature = inspect.signature(func)
    return_annotation = null if signature is None else signature.return_annotation
    rt = null
    if return_annotation is not None:
        try:
            rt = return_annotation.__name__
            if rt in ('_empty', 'POSITIONAL_OR_KEYWORD'):
                rt = type(result).__name__
        except Exception as e:
            print(e)
            rt = type(result).__name__  # str(return_annotation)

    mal = size(method_args)
    mas = [null] * mal
    if mal > 0:  # bug 要及时发现 and size(ma_values) == mal:
        i = -1
        for v in ma_values:
            i += 1

            if callable(v):
                mas[i] = method_args[i]
                continue

            t = ma_types[i]

            mas[i] = {
                KEY_TYPE: t.__name__ if t is not None else type(v),
                KEY_VALUE: v
            }

    return {
        KEY_LANGUAGE: LANGUAGE,
        KEY_OK: true,
        KEY_CODE: CODE_SUCCESS,
        KEY_MSG: MSG_SUCCESS,
        KEY_TYPE: rt,
        KEY_RETURN: result,
        KEY_METHOD_ARGS: mas,
        KEY_TIME_DETAIL: time_detail
    }


def invoke_method(req: any, callback: callable = null) -> dict:
    start_time = time.time_ns()
    try:
        assert is_none(callback) or callable(callback)

        if is_str(req):
            req = parse_json(req)

        static = req.get(KEY_STATIC)
        assert is_bool(static), (KEY_STATIC + ' must be bool!')

        is_async = req.get(KEY_ASYNC)
        assert is_bool(is_async), (KEY_ASYNC + ' must be bool!')

        package = req.get(KEY_PACKAGE)
        assert is_str(package), (KEY_PACKAGE + ' must be str!')

        clazz = req.get(KEY_CLASS)
        assert is_str(clazz), (KEY_CLASS + ' must be str!')

        method = req.get(KEY_METHOD)
        assert is_str(method), (KEY_METHOD + ' must be str!')
        assert not_empty(method), (KEY_CLASS + ' method be empty!')

        class_args = req.get(KEY_CLASS_ARGS)
        assert is_list(class_args), (KEY_CLASS_ARGS + ' must be list!')

        method_args = req.get(KEY_METHOD_ARGS)
        assert is_list(method_args), (KEY_METHOD_ARGS + ' must be list!')

        constructor = req.get(KEY_CONSTRUCTOR)
        assert is_str(constructor), (KEY_CONSTRUCTOR + ' must be str!')

        this = req.get(KEY_THIS)
        assert is_dict(this), (KEY_THIS + ' must be dict!')

        instance = None
        if this is not None:
            assert not static, KEY_STATIC + ' cannot appear together with ' + KEY_THIS + '!'
            assert class_args is None, KEY_THIS + ' cannot appear together with ' + KEY_CLASS_ARGS + '!'
            assert constructor is None, KEY_THIS + ' cannot appear together with ' + KEY_CONSTRUCTOR + '!'

            this_keys = [null]
            this_types = [null]
            this_values = [null]
            this_kwargs = {}
            init_args([this], this_keys, this_types, this_values, this_kwargs)
            instance = this_values[0]

        if class_args is not None:
            assert not static, KEY_CLASS_ARGS + ' cannot appear together with ' + KEY_STATIC + '!'
            assert this is None, KEY_CLASS_ARGS + ' cannot appear together with ' + KEY_THIS + '!'

        mal = size(method_args)
        ma_keys = [null] * mal
        ma_types = [null] * mal
        ma_values = [null] * mal
        m_kwargs = {}

        final_result = {}
        def final_callback(*args, **kwargs):
            if not_none(callback):  # callable(callback):
                callback(wrap_result(func, method_args, ma_types, ma_values, final_result.get(KEY_VALUE), start_time))

        is_wait = init_args(method_args, ma_keys, ma_types, ma_values, m_kwargs, true, final_callback)

        fl = split(clazz, '$')
        l = size(fl)

        mn = package if l <= 0 else package + '.' + fl[0]
        module = __import__(mn, fromlist=['__init__'] if l <= 0 else fl[0])

        cls: any = null
        if l > 1:
            i = -1
            for n in fl:
                i += 1
                if i <= 0:
                    continue
                cls = getattr(module, n)

        if cls is None:
            func = getattr(module, method)
        elif static:
            func = getattr(cls, method)
        else:
            constructor_func = None if constructor is None else getattr(module, constructor)

            if instance is None:
                cal = size(class_args)
                ca_keys = [null] * cal
                ca_types = [null] * cal
                ca_values = [null] * cal
                c_kwargs = {}
                init_args(class_args, ca_keys, ca_types, ca_values, c_kwargs)
                instance = cls(*ca_values, **c_kwargs) if constructor_func is None else constructor_func(*ca_values, **c_kwargs)

            func = getattr(instance, method)

        ksl = size(m_kwargs)
        start_time = time.time_ns()

        result = asyncio.run(func(*ma_values[:mal-ksl], **m_kwargs)) if is_async \
            else func(*ma_values[:mal-ksl], **m_kwargs)  # asyncio.run 只允许调 async 函数 is_async != false

        final_result[KEY_VALUE] = result
        return wrap_result(func, method_args, ma_types, ma_values, result, start_time)
    except Exception as e:
        return {
            KEY_LANGUAGE: LANGUAGE,
            KEY_OK: false,
            KEY_CODE: CODE_SERVER_ERROR,
            KEY_MSG: str(e),
            KEY_TIME_DETAIL: get_time_detail(start_time),
            KEY_THROW: e.__class__.__name__,
            # KEY_TRACE: e.__traceback__.__str__()
        }


def init_args(
    method_args: list, ma_keys: list, ma_types: list, ma_values: list,
    ma_kwargs: dict, keep_kwargs_in_types_and_values: bool = false, callback: callable = null
):
    is_wait = false
    mal = size(method_args)
    if mal > 0:
        i = -1
        for arg in method_args:
            i += 1
            value = null
            is_fun = false

            if is_str(arg) and (arg.__contains__(':') or arg.__contains__('=')):
                ind = index(arg, ':')
                eq_ind = index(arg, '=')
                key = (arg[:eq_ind] if ind < 0 else arg[ind+1:eq_ind]) if eq_ind >= 0 else null
                typ = arg[:ind] if ind >= 0 else null
                # ma_types.append(arg[:ind] if ind >= 0 else 'str')
                value = arg[eq_ind+1:] if eq_ind >= 0 else (arg[ind+1:] if ind >= 0 else arg)
                # ma_values.append(arg[ind + 1:] if ind >= 0 else arg)
            else:
                id = is_dict(arg)
                key = arg.get(KEY_KEY) if id else null
                typ = arg.get(KEY_TYPE) if id else null
                # ma_types.append(arg.get(KEY_TYPE) if id else type(arg))
                value = arg.get(KEY_VALUE) if id else arg
                # ma_values.append(arg.get(KEY_VALUE) if id else arg)

                start = index(typ, '(')
                end = last_index(typ, ')')
                if start >= 0 and end > start:  # 命名函数 或 lambda 匿名函数
                    assert is_dict(value, true), '{"type": "def(arg0,arg1...)", "value": value} 中 value 类型错误，' \
                        '必须为 dict！且格式必须为 {"type": returnType, "return": returnValue, "callback": bool}'
                    cb = value.get(KEY_CALLBACK)
                    assert is_bool(cb, false), '{"type": "def(arg0,arg1...)", "value": {"callback": bool}} 中' \
                        ' value/callback 类型错误，必须为 true 或 false ！'

                    is_fun = true
                    is_wait = is_wait or cb

                    fun = typ[:start] if start > 0 else null
                    # assert is_none(fun) or is_name(fun), '{"type": "fun(arg0,arg1...)"} 必须是函数名，或者关键词 def '
                    assert fun == 'def', '{"type": "fun(arg0,arg1...)"} 必须是函数名，或者关键词 def '

                    aks = split(typ[start+1:end])
                    akl = size(aks)
                    fa_types = [null] * akl
                    fa_keys = [null] * akl
                    for j in range(akl):
                        ak = aks[j]
                        ak_ind = index(ak, ':')
                        fa_types[j] = null if ak_ind < 0 else ak[:ak_ind]
                        fa_keys[j] = ak if ak_ind < 0 else ak[ak_ind+1:]

                    rtn_type = value.get(KEY_TYPE)
                    rtn_val = value.get(KEY_RETURN)

                    raw_val: dict = value
                    def cb_fun(*args, **kwargs):
                        mas: list = []
                        if not_empty(args):
                            for a in args:
                                mas.append({
                                    KEY_TYPE: type(a).__name__,
                                    KEY_VALUE: a
                                })

                        if not_empty(kwargs):
                            for k in kwargs:
                                v = kwargs[k]
                                mas.append({
                                    KEY_KEY: k,
                                    KEY_TYPE: type(v).__name__,
                                    KEY_VALUE: v
                                })

                        call_list: list = raw_val.get(KEY_CALL_LIST) or []
                        call_list.append({
                            KEY_TIME: round(time.time_ns()/MILLIS_TIME),
                            KEY_METHOD_ARGS: mas
                        })
                        raw_val[KEY_CALL_LIST] = call_list

                        if cb:
                            callback(*args, **kwargs)
                        return cast(rtn_val, get_class(rtn_type, rtn_val))

                    value = cb_fun  # eval('lambda ' + ', '.join(fa_keys) + ': ' + str(rtn_val))

            clazz = type(value) if is_fun else get_class(typ, value)
            value = cast(value, clazz) if not is_fun else value

            ma_keys[i] = key
            if is_none(key):
                if is_empty(ma_kwargs):
                    ma_types[i] = clazz
                    ma_values[i] = value
                    continue
                raise Exception('所有已经有 key 的参数，必须后面也跟着有 key，对应调用 fun(key=value, key2=value2...) ！')

            assert key not in ma_kwargs, '调函数传参，所有 key 不允许重名！必须有唯一的不同名称！'
            ma_kwargs[key] = value

            if keep_kwargs_in_types_and_values:
                ma_types[i] = clazz
                ma_values[i] = value
            else:
                del ma_types[-1]
                del ma_values[-1]

    return is_wait


def cast(value, clazz):
    if value is not None and not isinstance(value, clazz):
        s = ''
        try:
            s = value if is_str(value) else json.dumps(value)
            if PRIMITIVE_CLASS_MAP.__contains__(clazz.__name__):
                value = eval(clazz.__name__ + '(' + s + ')')
            else:
                value = json.loads(s, cls=clazz)  # FIXME 目前仅支持继承 JSONDecoder 且重写了 decode 方法的类
        except Exception as e:
            print(e)
            if is_str(value):
                value = json.loads(value)

            if not isinstance(value, clazz):
                if is_list(value):
                    value = clazz(*value)
                elif is_dict(value):
                    value = clazz(**value)  # FIXME 目前仅支持继承 __init__ 传完整参数且顺序一致的类
                else:
                    pass

    return value


def get_class(typ: str, value: any = None) -> Type:
    fl = split(typ, '$')
    if is_empty(fl):
        return type(value)

    path = typ
    clazz = CLASS_MAP.get(path)
    if clazz is None:
        fl = split(path, '$')
        pkg = fl[0]

        pl = split(pkg, '.')
        end = size(pl) - 1
        cn = null if end < 0 else pl[end]
        # pkg = pkg[:-len(cn)]

        l = size(fl)
        mn = fl[0]  # pkg if is_empty(fl) else pkg + '.' + cn
        module = __import__(mn, fromlist=cn)
        if l <= 1:
            clazz = getattr(module, cn)
        else:
            j = -1
            for n in fl:
                j += 1
                if j <= 0:
                    continue
                clazz = getattr(module, n)

        CLASS_MAP[path] = clazz

    return clazz


def split(s: str, seperator: str = ',') -> list:
    if s is None:
        return null
    if is_contain(s, seperator):
        return s.split(seperator)
    return [s]


def is_contain(s: str, seperator: str = ',') -> bool:
    return false if is_empty(s) else seperator in s  # s.__contains__(seperator)


def is_bool(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, bool)


def is_int(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, int)


def is_float(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, float)


def is_str(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, str)


def is_list(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, list)


def is_dict(obj, strict: bool = false) -> bool:
    return (not strict) if obj is None else isinstance(obj, dict)


def not_none(obj):
    return not is_none(obj)


def is_none(obj):
    return obj is None


def not_empty(obj) -> bool:
    return not is_empty(obj)


def is_empty(obj) -> bool:
    if obj is None:
        return true
    if is_int(obj) or is_float(obj):
        return obj <= 0

    return size(obj) <= 0


def is_name(s: str) -> bool:
    m = null if is_empty(s) else PATTERN_NUMBER.match(s[:1])
    return is_none(m) and not_none(PATTERN_NAME.match(s))


def size(obj) -> int:
    if obj is None:
        return 0

    if is_bool(obj) or is_int(obj) or is_float(obj):
        raise Exception('obj cannot be any one of [bool, int, float]!')

    return len(obj)


def index(s: str, sub: str) -> int:
    try:
        return s.index(sub)
    except Exception:
        return -1


def last_index(s: str, sub: str) -> int:
    ws = split(s, sub)
    if size(ws) <= 1:
        return -1
    return size(s) - size(ws[-1]) - 1


def get_time_detail(start_time: int, end_time: int = 0):
    if end_time is None or end_time <= 0:
        end_time = time.time_ns()
    duration = end_time - start_time
    return str(round(start_time/MILLIS_TIME)) + '|' + str(round(duration/MILLIS_TIME)) + '|' + str(round(end_time/MILLIS_TIME))


def parse_json(s: str):
    return json.loads(s)


def to_json_str(obj, indent: int = 2) -> str:
    return json.dumps(obj, ensure_ascii=false, indent=indent)

