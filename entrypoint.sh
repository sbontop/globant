#!/bin/bash
# Production
/usr/local/bin/gunicorn poke_berry_api.wsgi:application \
--bind "0.0.0.0:$PORT" \
--env DJANGO_SETTINGS_MODULE=poke_berry_api.settings \
--timeout $TIMEOUT \
--reload

# Local
# /usr/local/bin/gunicorn poke_berry_api.wsgi:application \
# --bind "0.0.0.0:$PORT" \
# --env DJANGO_SETTINGS_MODULE=poke_berry_api.settings.local \
# --timeout $TIMEOUT \
# --reload
