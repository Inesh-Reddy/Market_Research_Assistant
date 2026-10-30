class AppError(Exception):
    def __init__(self, message: str, code: str = "app_error"):
        super().__init__(message); self.message=message; self.code=code
class ConfigError(AppError):
    def __init__(self, message: str): super().__init__(message, "config_error")
class ToolError(AppError):
    def __init__(self, message: str): super().__init__(message, "tool_error")
class ProviderUnavailableError(AppError):
    def __init__(self, message: str): super().__init__(message, "provider_unavailable")
