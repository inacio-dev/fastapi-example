import json
import asyncio
from functools import wraps
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..cache import redis_client
from .logger import async_info, async_error, async_warning


def custom_cache(expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request or not isinstance(request, Request):
                await async_warning(f"Request válido não encontrado para {func.__name__}. Cache desativado.")
                return await func(*args, **kwargs)

            # Gerar uma chave base única para a rota
            base_key = f"cache:{request.url.path}"

            # Gerar chaves separadas para cada parâmetro
            param_keys = []
            for key, value in request.query_params.items():
                param_keys.append(f"{key}:{value}")

            # Combinar a chave base com as chaves de parâmetros
            cache_key = f"{base_key}:{':'.join(sorted(param_keys))}"

            try:
                # Verificar se o resultado está no cache de forma assíncrona
                cached_result = await asyncio.to_thread(redis_client.get, cache_key)
                if cached_result:
                    await async_info(f"Cache hit para {cache_key}")
                    return json.loads(cached_result)

                await async_info(f"Cache miss para {cache_key}")

                # Se não estiver no cache, executar a função
                result = await func(*args, **kwargs)

                # Serializar o resultado antes de armazenar no cache
                serialized_result = jsonable_encoder(result)

                # Armazenar o resultado serializado no cache de forma assíncrona
                await asyncio.to_thread(redis_client.setex, cache_key, expire, json.dumps(serialized_result))
                await async_info(f"Resultado armazenado no cache para {cache_key}")

                return result

            except json.JSONDecodeError:
                await async_error(f"Erro ao decodificar JSON do cache para {cache_key}")
                return await func(*args, **kwargs)
            except Exception as e:
                await async_error(f"Erro no cache para {cache_key}: {str(e)}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator
