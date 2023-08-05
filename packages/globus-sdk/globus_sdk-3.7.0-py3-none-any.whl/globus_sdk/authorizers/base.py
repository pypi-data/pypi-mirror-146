import abc
from typing import Optional


class GlobusAuthorizer(metaclass=abc.ABCMeta):
    """
    A ``GlobusAuthorizer`` is a very simple object which generates valid
    Authorization headers.
    It may also have handling for responses that indicate that it has provided
    an invalid Authorization header.
    """

    @abc.abstractmethod
    def get_authorization_header(self) -> Optional[str]:
        """
        Get the value for the ``Authorization`` header from this authorizer.
        If this method returns ``None``, then no ``Authorization`` header should be
        used.
        """

    def handle_missing_authorization(self) -> bool:
        """
        This operation should be called if a request is made with an
        Authorization header generated by this object which returns a 401
        (HTTP Unauthorized).
        If the ``GlobusAuthorizer`` thinks that it can take some action to
        remedy this, it should update its state and return ``True``.
        If the Authorizer cannot do anything in the event of a 401, this *may*
        update state, but importantly returns ``False``.

        By default, this always returns ``False`` and takes no other action.
        """
        return False


class StaticGlobusAuthorizer(GlobusAuthorizer):
    """A static authorizer has some static string as its header val which it always
    returns as the authz header."""

    header_val: str

    def get_authorization_header(self) -> str:
        return self.header_val


class NullAuthorizer(GlobusAuthorizer):
    """
    This Authorizer implements No Authentication -- as in, it ensures that
    there is no Authorization header.
    """

    def get_authorization_header(self) -> None:
        return None
