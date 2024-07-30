FROM debian:bullseye AS base

# Install normal dependencies
RUN apt-get update
RUN apt-get -y --no-install-recommends install uwsgi uwsgi-plugin-python3 python3 python3-pip python3-setuptools pipenv nginx wkhtmltopdf
RUN pip3 install wheel

# Add project code to container
ADD backend /app/backend

# Setup backend
RUN cd /app/backend && pipenv install --system --deploy --ignore-pipfile

FROM node:18 AS frontend

# Build frontend
ADD frontend /app/frontend
WORKDIR /app/frontend
ENV VITE_HOSTNAME=https://karaoke.mafiasi.de/api/
RUN npm install
RUN npm run build

FROM base AS final
COPY --from=frontend /app/frontend/dist /app/static
RUN mkdir /app/backend/logs
ADD docker/run /usr/local/bin/run
ADD docker/uwsgi-mafiastar.ini /etc/uwsgi/mafiastar.ini
ADD docker/nginx.conf /etc/nginx/sites-enabled/default

RUN usermod -u 2009 -g 33 -d /app/backend www-data
RUN chown -R www-data:www-data /app/backend

CMD /usr/local/bin/run
