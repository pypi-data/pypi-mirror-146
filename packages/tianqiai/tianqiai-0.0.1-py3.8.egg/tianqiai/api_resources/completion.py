import time

from tianqiai import util
# from tianqiai.api_resources.abstract import DeletableAPIResource, ListableAPIResource
from tianqiai.api_resources.abstract.engine_api_resource import EngineAPIResource
from tianqiai.error import InvalidRequestError, TryAgain


class Completion(EngineAPIResource):
    engine_required = False
    OBJECT_NAME = "completion"

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new completion for the provided prompt and parameters.

        See https://beta.tianqiai.com/docs/api-reference/completions/create for a list
        of valid parameters.
        """
        start = time.time()
        timeout = kwargs.pop("timeout", None)
        if kwargs.get("model", None) is None and kwargs.get("engine", None) is None:
            raise InvalidRequestError(
                "Must provide an 'engine' or 'model' parameter to create a Completion.",
                param="engine",
            )

        while True:
            try:
                return super().create(*args, **kwargs)
            except TryAgain as e:
                if timeout is not None and time.time() > start + timeout:
                    raise

                util.log_info("Waiting for model to warm up", error=e)
