from itertools import chain
import sys
import logging
import random
import functools
import time
from time import perf_counter
import inspect

zus = ["Zakład", "Ubezpieczeń", "Społecznych"]

def acronym(input):
    return "".join([x[0] for x in input])

print(acronym(zus))

_3 = [1, 1, 19, 2, 3, 4, 4, 5, 1]

def median(input):
    l = len(input)
    return sorted(input)[l // 2] \
                if l % 2 != 0 \
                else sum(sorted(input)[l // 2 - 1:l // 2 + 1]) / 2

print(median(_3))

def pierwiastek(x, eps):
    def aux(y, x, eps):
        return y if y >= 0 and abs(y ** 2 - x) < eps else aux((y+x/y) * 0.5, x, eps)
    return aux(x/2,x,eps)

print(pierwiastek(3, 0.1))

def make_alpha_dict(input):
    return {k:[x for x in input.split(" ") if k in x] for k in set(list(input.replace(" ", "")))}

print(make_alpha_dict("ona i on"))

def flatten(l):
    return list(chain.from_iterable([flatten(x) if type(x) is list else [x] for x in l]))

print(flatten([1, [], [[4, 5], 6]]))

# also list.count() or filter()

def forall(pred, iterable):
    for it in iterable:
        if not pred(it):
            return False
    return True

def exists(pred, iterable):
    for it in iterable:
        if pred(it):
            return True
    return False

def atleast(n, pred, iterable):
    for it in iterable:
        if pred(it):
            n -= 1
            if n == 0:
                return True
    return False

def atmost(n, pred, iterable):
    for it in iterable:
        if pred(it):
            n -= 1
            if n < 0:
                return False
    return True

print(atmost(2, lambda x: x == 2, [1,2,3,2,6]))

class PasswordGenerator():
    def __init__(self, length, charset = "".join([chr(x) for x in range(48,91)]), count = 3) -> None:
        self.length = length
        self.charset = charset
        self.count = count

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == 0:
            raise StopIteration
        self.count -= 1
        return "".join([random.choice(self.charset) for _ in range(self.length)])

for i in PasswordGenerator(5):
    print(i)

def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)

seq = lambda x: 1 * (2 ** (x-1)) # a1 * q^(n-1); a1=1, q=2

def make_generator(f):
    def aux():
        i = 1
        while True:
            yield f(i)
            i += 1
    return aux()

gen_fib = make_generator(fib)

gen_seq = make_generator(seq)

for _ in range(10):
    print(next(gen_fib))

for _ in range(10):
    print(next(gen_seq))

@functools.cache
def make_generator_mem(f):
    def infinity():
        i = 1
        while True:
            yield i
            i += 1
    for i in infinity():
        yield f(i)


gen_fib_mem = make_generator_mem(fib)

for _ in range(10):
    print(next(gen_fib_mem))

def log(arg):
    if arg.lower() == "info":
        logging.basicConfig(encoding='utf-8', level=logging.INFO)
    elif arg.lower() == "warning":
        logging.basicConfig(encoding='utf-8', level=logging.WARNING)
    elif arg.lower() == "error":
        logging.basicConfig(encoding='utf-8', level=logging.ERROR)
    elif arg.lower() == "critical":
        logging.basicConfig(encoding='utf-8', level=logging.CRITICAL)
    else:
        logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    console_handler_err = logging.StreamHandler(sys.stderr)
    console_handler_cri = logging.StreamHandler(sys.stderr)
    console_handler_debug = logging.StreamHandler(sys.stdout)
    console_handler_info = logging.StreamHandler(sys.stdout)
    console_handler_warning = logging.StreamHandler(sys.stdout)

    console_handler_err.setLevel(logging.ERROR)
    console_handler_cri.setLevel(logging.CRITICAL)
    console_handler_debug.setLevel(logging.DEBUG)
    console_handler_info.setLevel(logging.INFO)
    console_handler_warning.setLevel(logging.WARNING)

    # formatter = logging.Formatter('%(levelname)s: %(message)s')
    formatter = logging.Formatter('%(message)s')

    console_handler_err.setFormatter(formatter)
    console_handler_cri.setFormatter(formatter)
    console_handler_debug.setFormatter(formatter)
    console_handler_info.setFormatter(formatter)
    console_handler_warning.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(console_handler_err)
    logger.addHandler(console_handler_cri)
    logger.addHandler(console_handler_info)
    logger.addHandler(console_handler_warning)
    logger.addHandler(console_handler_debug)

    def wrapper(obj):

        if inspect.isfunction(obj):

            def inner_wrapper_func(*args, **kwargs):
                start_time = perf_counter()

                t = time.localtime()
                curr_t = time.strftime("%D %H:%M:%S", t)

                result = obj(*args, **kwargs)

                finish_time = perf_counter()

                duration = round(finish_time - start_time, 5)

                func_name = obj.__name__

                arg_names = obj.__code__.co_varnames

                log_input = f"called: {curr_t}, duration: {duration}, name: {func_name}, args: {arg_names} - {args,kwargs}, result: {result}"

                if arg.lower() == "info":
                    logging.info(log_input)
                elif arg.lower() == "warning":
                    logging.warning(log_input)
                elif arg.lower() == "error":
                    logging.error(log_input)
                elif arg.lower() == "critical":
                    logging.critical(log_input)
                else:
                    logging.debug(log_input)

                return obj(*args, **kwargs)

            return inner_wrapper_func

        else:

            def wrapper_for_inner_inner_class(self, *args, **kwargs):
                def inner_wrapper_class():
                    log_input = "Class initialized"
                    if arg.lower() == "info":
                        logging.info(log_input)
                    elif arg.lower() == "warning":
                        logging.warning(log_input)
                    elif arg.lower() == "error":
                        logging.error(log_input)
                    elif arg.lower() == "critical":
                        logging.critical(log_input)
                    else:
                        logging.debug(log_input)

                    return obj.__init__(self, *args, **kwargs)
                return inner_wrapper_class()

            obj.__new__ = wrapper_for_inner_inner_class

            return obj

    return wrapper

@log("info")
def fib_log(n):
    return 4 ** n

@log("info")
class A():
    def __init__(self):
        print("Hello")

a = A()
b = A()

print(fib_log(40))
