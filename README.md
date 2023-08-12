# MafiAStarLite

MafiAStarLite is a software to display UltraStar-Karaoke songs from a DB in a webbrowser.

The current version supports displaying of songs, as well as their album covers and a search function.

The frontend is written in Vue.js and can be found at https://github.com/8fuhst/MafiAStarLite-frontend.

# Install
Clone the repository:
  `git clone https://github.com/8fuhst/MafiAStarLite`

Install pipenv for dependencies and activate pipenv:
  `pipenv install`
  `pipenv shell`

Enter required data into .env.dev file:
  `DJANGO_DEBUG=True
  DJANGO_SECRET_KEY=mysecretkey
  SONG_PATH=...
  DATABASE_URL=postgres://user:password@localhost/MafiAStarLite`

Initialize DB:
  `python3 manage.py migrate`

Update DB:
  `python3 manage.py updatedb`

Run testserver:
  `python3 manage.py runserver`

# Production
Use .env file instead of .env.dev, set DJANGO_DEBUG to False, change secret key!
