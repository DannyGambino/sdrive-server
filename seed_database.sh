rm db.sqlite3
rm -rf ./sdrive-server/migrations

python3 manage.py migrate
python3 manage.py makemigrations sdriveapi
python3 manage.py migrate sdriveapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata advisors
python3 manage.py loaddata technicians
python3 manage.py loaddata service_tickets