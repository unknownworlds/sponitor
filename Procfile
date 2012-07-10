web: sh -c 'newrelic-admin run-program python Sponitor/manage.py collectstatic --noinput && python Sponitor/manage.py run_gunicorn -b 0.0.0.0:$PORT -w 3'
