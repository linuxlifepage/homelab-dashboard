## Dashboard for homelab services

1. Поддерживает смену тем по кнопке в топбаре
2. Сохранение и загрузка конфигурации в json (кнопки рядом с лого)
3. Смена размеров сетки сервисов
4. Добавление категорий
5. NeonMode фича


## Как запустить?

```
docker build . -t homelab-dashboard:latest --no-cache
```

Старт контейнера

```
docker run -d -p 8888:80 --name homelab-dashboard homelab-dashboard:latest
```