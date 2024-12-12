import json
import asyncio
from functools import wraps
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from ..cache import redis_client
from .logger import async_info, async_error, async_warning


async def remove_cache_item(key: str):
    try:
        result = await asyncio.to_thread(redis_client.delete, key)
        if result:
            await async_info(f"Item removido do cache: {key}")
        else:
            await async_info(f"Item não encontrado no cache: {key}")
    except Exception as e:
        await async_error(f"Erro ao remover item do cache {key}: {str(e)}")


async def remove_related_cache(path: str):
    try:
        pattern = f"cache:{path}*"
        keys = await asyncio.to_thread(redis_client.keys, pattern)
        if keys:
            await asyncio.to_thread(redis_client.delete, *keys)
            await async_info(f"Cache removido para o padrão: {pattern}")
    except Exception as e:
        await async_error(f"Erro ao remover cache para {path}: {str(e)}")


def custom_cache(expire: int = 60):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            if not request or not isinstance(request, Request):
                await async_warning(f"Request válido não encontrado para {func.__name__}. Cache desativado.")
                return await func(*args, **kwargs)

            # Para métodos de modificação, remover o cache relacionado e executar a função
            if request.method in ["POST", "PATCH", "PUT", "DELETE"]:
                await remove_related_cache(request.url.path)
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
