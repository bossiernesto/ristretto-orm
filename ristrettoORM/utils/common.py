import types
import sys
from ristrettoORMExceptions import RistrettoORMException, DAOEngineException


# Type checking
def isObjOfType(obj, _type):
    return type(obj) in ([_type] + _type.__subclasses__())


def unbind(f):
    self = getattr(f, '__self__', None)
    if self is not None and not isinstance(self, types.ModuleType) \
        and not isinstance(self, type):
        if hasattr(f, '__func__'):
            return f.__func__
        return getattr(type(f.__self__), f.__name__)
    raise TypeError('not a bound method')


def bind(f, obj):
    obj.__dict__[f.__name__] = types.MethodType(f, obj)


def rebind(f, obj):
    bind(unbind(f), obj)


def wrap_ristrettorm_exception(message):
    """
    Function that wraps an existing Exception in stackTrace with a RistrettoORMException

    :param message: Description of the message that the developer wants to show when the wrap Exception is raised
    :type message: str
    """
    wrap_exception(RistrettoORMException, message)


def wrap_dao_exception(message):
    """
    Function that wraps an existing Exception in stackTrace with a DAOEngineException

    :param message: Description of the message that the developer wants to show when the wrap Exception is raised
    :type message: str
    """
    wrap_exception(DAOEngineException, message)


def wrap_exception(exceptionClass, message):
    """
    Function that given an Exception class, wraps an existing exception in the stack trace with the given one.

    :param exceptionClass: Exception class that will wrap the current raised exception
    :param message: Description of the message that the developer wants to show when the wrap Exception is raised
    :type message: str
    """
    trace = sys.exc_info()[2]
    raise (exceptionClass, message, None, trace)


def inherit(cls, *supercls):
    for superclass in supercls:
        if cls.__name__ == superclass.__name__:
            raise TypeError("Class name collision trying to inherit class {0} to {1}"
            .format(superclass.__name__, cls.__name__))
    return type(cls.__name__, supercls + (object,), dict(cls.__dict__))


def add_mixin(cls, mixin, force=False):
    for name, value in mixin.__dict__.items():
        if name.startswith("_"):
            continue
        if not force and hasattr(cls, name):
            raise TypeError("name collision ({})".format(name))
        setattr(cls, name, value)
    try:
        mixin.register(cls)
    except AttributeError:
        pass


def mixin_classes(*mixins, force=False):
    """A class decorator factory that adds mixins using add_mixin.

    """

    def decorator(cls):
        for mixin in mixins:
            add_mixin(cls, mixin, force)
        return cls

    return decorator