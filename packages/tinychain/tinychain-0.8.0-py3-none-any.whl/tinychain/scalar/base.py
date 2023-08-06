from ..interface import Equality
from ..state import State
from ..util import form_of, to_json, uri


class Scalar(State, Equality):
    """
    An immutable :class:`State` which always resides entirely in the host's memory.

    Do not subclass :class:`Scalar` directly. Use :class:`Value` instead.
    """

    __uri__ = uri(State) + "/scalar"

    def __json__(self):
        return to_json(form_of(self))

    def eq(self, other):
        from .number import Bool
        return self._get("eq", other, Bool)

    def ne(self, other):
        from .number import Bool
        return self._get("ne", other, Bool)
