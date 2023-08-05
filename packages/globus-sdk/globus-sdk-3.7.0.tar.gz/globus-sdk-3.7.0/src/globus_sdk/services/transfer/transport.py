"""
Custom Transport class for the TransferClient that overrides
default_check_transient_error
"""
from globus_sdk.transport import RequestsTransport, RetryCheckResult, RetryContext


class TransferRequestsTransport(RequestsTransport):
    def default_check_transient_error(self, ctx: RetryContext) -> RetryCheckResult:
        """
        check for transient error status codes which could be resolved by
        retrying the request. Does not retry ExternalErrors as those are
        unlikely to actually be transient.
        """
        if ctx.response is not None and (
            ctx.response.status_code in self.TRANSIENT_ERROR_STATUS_CODES
        ):
            try:
                code = ctx.response.json()["code"]
            except (ValueError, KeyError):
                code = ""
            if "ExternalError" not in code:
                return RetryCheckResult.do_retry

        return RetryCheckResult.no_decision
