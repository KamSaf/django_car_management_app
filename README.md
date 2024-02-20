Django web application created to make it easier to keep records of car operating expenses. 

How to run:

1. Create virtual environment and activate it:

        virtualenv venv
        cd venv/bin
        source activate

2. Install dependencies by running:

        pip install -r requirements.txt

3. Go to /car_management_app/settings.py and provide your PostgreSQL database connection credentials:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': '< YOUR DATABASE NAME >',
                'USER': '< YOUR DATABASE USER NAME >',
                'PASSWORD': '< YOUR DATABASE PASSWORD >',
                'HOST': '< YOUR DATABASE HOST ADDRESS >',
                'PORT': '< YOUR DATABASE PORT >'
            }
        }

4. Go to the main project directory and run migration commands:

        python manage.py migrate

3. Run application with command when in main project directory:

        python manage.py migrate

