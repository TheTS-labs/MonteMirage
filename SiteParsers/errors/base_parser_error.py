from typing import Self


class BaseParserError(Exception):
    def __init__(self: Self, message: str) -> Self:
        """Exception is raised for any parser errors.

        Args:
            message: Error message
        """
        self.message = message
        super().__init__(self.message)
