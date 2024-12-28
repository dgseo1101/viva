from core.application.dtos.base import BaseRequest, BaseResponse

class ResponseTokenDto(BaseResponse):
    access_token: str
    refresh_token: str

class RefreshTokenRequestDto(BaseRequest):
    token: str

class AccessTokenResponseDto(BaseResponse):
    token: str