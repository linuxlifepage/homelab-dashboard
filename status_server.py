from aiohttp import web, ClientSession, ClientTimeout
import asyncio
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = web.RouteTableDef()

@routes.get('/check')
async def check_status(request):
    url = request.query.get('url')
    if not url:
        return web.json_response({'error': 'URL не указан'}, status=400)
    
    try:
        # Проверяем, что URL содержит протокол
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        parsed = urlparse(url)
        if not parsed.netloc:
            return web.json_response({'error': 'Некорректный URL'}, status=400)

        timeout = ClientTimeout(total=5)  # 5 секунд таймаут
        async with ClientSession(timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    return web.json_response({
                        'status': 'online',
                        'code': response.status,
                        'url': url
                    })
            except Exception as e:
                logger.error(f"Ошибка при проверке {url}: {str(e)}")
                return web.json_response({
                    'status': 'offline',
                    'error': str(e),
                    'url': url
                })
    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {str(e)}")
        return web.json_response({'error': str(e)}, status=500)

@routes.get('/')
async def health_check(request):
    return web.Response(text='Status checker is running')

app = web.Application()
app.add_routes(routes)

# Добавляем CORS
async def cors_middleware(app, handler):
    async def middleware(request):
        response = await handler(request)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return middleware

if __name__ == '__main__':
    app.middlewares.append(cors_middleware)
    web.run_app(app, port=5757) 