FROM makeplane/plane-aio-community:v1.4.2
# Same programs as upstream, but logging to stdout so Railway shows them
# (upstream writes everything to files under /app/logs), plus the admin setup.
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY railway_setup.py /app/backend/plane/db/management/commands/railway_setup.py
