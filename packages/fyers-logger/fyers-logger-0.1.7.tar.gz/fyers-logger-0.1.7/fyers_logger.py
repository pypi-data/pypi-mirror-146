import traceback
from typing import Any, Dict, Union
from aws_lambda_powertools import Logger
from threading import local


class CustomLocal(local):
    def __init__(self) -> None:
        self.val = ""


logger_var_fyId = CustomLocal()
logger_var_requestId = CustomLocal()


class FyersLogger(Logger):
    def __init__(
        self, service: str, level: str, stack_level: int = 4, **kwargs
    ) -> None:
        """Create FyersLogger object

        Args:
            service (str): Service name. This should be the same across the code wherever the logger is initialized
            level (str): Logger level. Possible values are [INFO, DEBUG, CRITICAL, WARNING]

        Kwargs:
            stack_level (int): Stack level. This decides how many levels the stack should go up to get the line number
                            to be printed in the logging statement
        """
        super().__init__(
            service=service,
            level=level,
            location="[%(funcName)s:%(lineno)s] %(module)s",
            **kwargs
        )
        self.__stacklevel = stack_level

    def set_fyId(self, fyId: str) -> None:
        """Sets FyId for a particular request. This function needs to be called only once for each request

        Args:
            fyId (str): Fyers ID
        """
        logger_var_fyId.val = fyId

    def set_requestId(self, requestId: str) -> None:
        """Sets RequestId for a particular request. This function needs to be called only once for each request

        Args:
            requestId (str): Request ID [This should be unique for each request]
        """
        logger_var_requestId.val = requestId

    def clear_data(self) -> None:
        """Clears data for this thread so that the data is not propagated in the next request."""
        logger_var_fyId.val = ""
        logger_var_requestId.val = ""

    def __populate_request_data(self, stack_level, **kwargs) -> Dict[str, Any]:
        """Adds additional log data to log statement

        Returns:
            Dict[str, Any]: all the keyword arguments along with extra data
        """
        kwargs["stacklevel"] = stack_level
        if "extra" not in kwargs:
            kwargs["extra"] = {}

        kwargs["extra"]["fyId"] = logger_var_fyId.val
        kwargs["extra"]["requestId"] = logger_var_requestId.val
        if "message" in kwargs["extra"]:
            kwargs["extra"]["passed_message"] = kwargs["extra"].pop("message")
        return kwargs

    def error(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs error statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(stacklevel, **kwargs)
                super().error(msg, *args, **kwargs)
                break
            except:
                stacklevel -= 1

    def info(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs info statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(stacklevel, **kwargs)
                super().info(msg, *args, **kwargs)
                break
            except:
                stacklevel -= 1

    def debug(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs debug statement

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(stacklevel, **kwargs)
                super().debug(msg, *args, **kwargs)
                break
            except:
                stacklevel -= 1

    def exception(self, msg: Union[str, Dict[Any, Any]], *args, **kwargs) -> None:
        """Logs exception statement. Should be called only from exception block

        Args:
            msg (Union[str, Dict[Any, Any]]): Can be str or dict object

        Kwargs:
            extra (Dict[Any, Any]): Adds this data to the log statement
        """
        stacklevel = self.__stacklevel
        while stacklevel > 0:
            try:
                kwargs = self.__populate_request_data(stacklevel, **kwargs)
                super().exception(msg, *args, **kwargs)
                break
            except:
                stacklevel -= 1
