web: sh -c 'python Sponitor/manage.py collectstatic --noinput && newrelic-admin run-program python Sponitor/manage.py run_gunicorn -b 0.0.0.0:$PORT -w 3'
cron: python Sponitor/stats/util/precomputeCache.py
