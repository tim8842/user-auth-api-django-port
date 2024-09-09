from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer, ProfileSerializer, UpdateProfileSerializer
from .models import Profile
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RegisterSerializer, UserSerializer

swg_tmp = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer {JWT token}", type=openapi.TYPE_STRING)
        ]
    )

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: openapi.Response(
                'Bad Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                    }
                )
            )
        },
        operation_description="""
    Регистрация нового пользователя.

    Данный эндпоинт позволяет создать нового пользователя в системе. 
    После успешной регистрации возвращает токен для дальнейшей аутентификации.

    Параметры:
    - `email`: Адрес электронной почты (обязательный).
    - `name`: Имя (обязательное).
    - `password`: Пароль пользователя (обязательный).

    Пример запроса:
    ```
    POST /api/register/
    {
        "email": "user@example.com",
        "name": "dmitry",
        "password": "strongpassword123"
    }
    ```
    """,
        examples={
            "application/json": {
                "email": "user@example.com",
                "name": "dmitry",
                "password": "strongpassword123"
            }
        }
        
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class LoginView(generics.GenericAPIView):
    """
    Вход пользователя в систему.

    Этот эндпоинт позволяет пользователям аутентифицироваться в системе. 
    Он принимает email и пароль, и возвращает токен для дальнейшей аутентификации.

    Параметры запроса:
    - `email`: Адрес электронной почты пользователя (обязательный).
    - `password`: Пароль пользователя (обязательный).

    Пример запроса:
    ```
    POST /api/login/
    {
        "email": "user@example.com",
        "password": "strongpassword123"
    }
    ```

    Пример ответа:
    ```
    {
        "token": "jwt_access_token_here",
        "refresh": "jwt_refresh_token_here"
    }
    ```

    Коды ответов:
    - 200: Успешный вход, возвращен токен.
    - 400: Ошибка валидации данных (неверный email или пароль).
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)
    
class ChangePasswordView(generics.UpdateAPIView):
    """
    Смена пароля пользователя.

    Этот эндпоинт позволяет аутентифицированным пользователям изменить свой текущий пароль.

    Параметры запроса:
    - `old_password`: Текущий пароль пользователя (обязательный).
    - `new_password`: Новый пароль пользователя (обязательный).

    Пример запроса:
    ```
    PUT /api/change-password/
    {
        "old_password": "oldpassword123",
        "new_password": "newpassword456",
    }
    ```

    Коды ответов:
    - 200: Пароль успешно изменен.
    - 400: Ошибка валидации (например, старый пароль неверен или пароли не совпадают).
    - 401: Пользователь не авторизован.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user
    
    
    @swg_tmp
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    @swg_tmp
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
        
    

class ProfileDetailView(generics.RetrieveAPIView):
    """
    Получение профиля пользователя.

    Этот эндпоинт позволяет аутентифицированным пользователям получить информацию о своем профиле.

    Пример запроса:
    ```
    GET /api/profile/
    ```

    Пример ответа:
    ```
    {
        "bio": "Hello, I'm a developer!",
        "phone_number": "+1234567890",
        "profile_picture": "http://example.com/profile-pic.jpg",
        "location": "New York",
        "created_at": "2023-09-01T12:34:56Z",
        "updated_at": "2023-09-01T12:34:56Z"
    }
    ```

    Коды ответов:
    - 200: Успешно получен профиль пользователя.
    - 401: Пользователь не авторизован.
    - 404: Профиль не найден.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        profile, created = Profile.objects.get_or_create(user=user)
        return profile
    
    @swg_tmp
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class UpdateProfileView(generics.UpdateAPIView):
    """
    Обновление профиля пользователя.

    Этот эндпоинт позволяет аутентифицированным пользователям обновлять данные своего профиля.

    Параметры запроса:
    - `bio`: Описание пользователя (необязательное).
    - `phone_number`: Номер телефона пользователя (необязательное).
    - `profile_picture`: Ссылка на аватар пользователя (необязательное).
    - `location`: Местоположение пользователя (необязательное).

    Пример запроса:
    ```
    PUT /api/profile/update/
    {
        "bio": "New bio",
        "phone_number": "+987654321",
        "profile_picture": "http://example.com/new-pic.jpg",
        "location": "San Francisco"
    }
    ```

    Коды ответов:
    - 200: Профиль успешно обновлен.
    - 400: Ошибка валидации данных.
    - 401: Пользователь не авторизован.
    """
    
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    @swg_tmp
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    @swg_tmp
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)