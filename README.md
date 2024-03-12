# Data analysis
- Document here the project: filmsyl
- Description: Project Description
- Data Source:
- Type of analysis:

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
#sudo apt-get install virtualenv python-pip python-dev
#deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
```
```bash
pyenv virtualenv films-you-like
pyenv local films-you-like
pyenv versions
make install_requirements
```

Unittest test:
```bash
make clean install test
```

Check for filmsyl in github.com/freudenfranz. If your project is not set please add it:

Create a new project on [github.com/freundenfranz/filmsyl](https://github.com/freudenfranz/filmsyl)
Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "filmsyl"
git remote add origin git@github.com:freudenfranz/filmsyl.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
filmsyl-run
```

# Install

Go to `https://github.com/{group}/filmsyl` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
#sudo apt-get install virtualenv python-pip python-dev
#deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
pyenv virtualenv films-you-like
pyenv local films-you-like
pyenv versions
```

Clone the project and install it:

```bash
cd ~/code/<username>
git clone git@github.com:freudenfranz/filmsyl.git
cd filmsyl
git checkout dev
make install_requirements
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
filmsyl-run
```

# Getting Started

- change the environment variables in the filmsyl and filmsyl-frontend folders

# API

## Routes

base_url = ''
```
/cluster
/get-recommendation
/upload-netflix-history
```

## Docker
in case you want to test locally, change the image in Docker file and run
```docker run -e PORT=8000 -p 8000:8000 --env-file your/path/to/.env $GAR_IMAGE:dev```

for building the production environment:
```docker build -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/filmsyl/$GAR_IMAGE:prod .```
.. and on a M1/M2 proecessor
```docker build --platform linux/amd64 -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/filmsyl/$GAR_IMAGE:prod .```

to test the environment:
```docker run -e PORT=8000 -p 8000:8000 --env-file .env $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/filmsyl/$GAR_IMAGE:prod```

to push the environment:
``` docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/filmsyl/$GAR_IMAGE:prod```



### example answer cinemas.py
{'show_times': {'Cinema 6': {'cinema': {'cinema_id': 10636, 'cinema_name': 'Cinema 6'}, 'films': [{'film_id': 7772, 'imdb_id': 82971, 'imdb_title_id': 'tt0082971', 'film_name': 'Raiders of the Lost Ark', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'Contains moderate violence and mild language'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/7772/GBR_007772h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/7772/007772h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 7772, 'film_name': 'Raiders of the Lost Ark', 'times': [{'start_time': '10:00', 'end_time': '12:14'}, {'start_time': '10:40', 'end_time': '12:54'}, {'start_time': '11:20', 'end_time': '13:34'}, {'start_time': '12:00', 'end_time': '14:14'}, {'start_time': '12:40', 'end_time': '14:54'}, {'start_time': '13:30', 'end_time': '15:44'}, {'start_time': '14:00', 'end_time': '16:14'}, {'start_time': '14:10', 'end_time': '16:24'}, {'start_time': '14:50', 'end_time': '17:04'}, {'start_time': '15:10', 'end_time': '17:24'}, {'start_time': '15:30', 'end_time': '17:44'}, {'start_time': '16:20', 'end_time': '18:34'}, {'start_time': '16:45', 'end_time': '18:59'}, {'start_time': '17:00', 'end_time': '19:14'}, {'start_time': '17:40', 'end_time': '19:54'}, {'start_time': '17:50', 'end_time': '20:04'}, {'start_time': '18:20', 'end_time': '20:34'}, {'start_time': '18:45', 'end_time': '20:59'}, {'start_time': '19:10', 'end_time': '21:24'}, {'start_time': '19:45', 'end_time': '21:59'}, {'start_time': '19:50', 'end_time': '22:04'}, {'start_time': '20:30', 'end_time': '22:44'}, {'start_time': '21:10', 'end_time': '23:24'}, {'start_time': '22:00', 'end_time': '00:14'}, {'start_time': '22:50', 'end_time': '01:04'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 184126, 'imdb_id': 3659388, 'imdb_title_id': 'tt3659388', 'film_name': 'The Martian', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '12A ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/12a.png', 'age_advisory': 'infrequent strong language, injury detail'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/184126/GBR_184126h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/184126/184126h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 184126, 'film_name': 'The Martian', 'times': [{'start_time': '10:10', 'end_time': '12:16'}, {'start_time': '11:00', 'end_time': '13:06'}, {'start_time': '11:50', 'end_time': '13:56'}, {'start_time': '12:40', 'end_time': '14:46'}, {'start_time': '13:15', 'end_time': '15:21'}, {'start_time': '13:30', 'end_time': '15:36'}, {'start_time': '14:20', 'end_time': '16:26'}, {'start_time': '15:10', 'end_time': '17:16'}, {'start_time': '16:00', 'end_time': '18:06'}, {'start_time': '16:50', 'end_time': '18:56'}, {'start_time': '17:40', 'end_time': '19:46'}, {'start_time': '18:30', 'end_time': '20:36'}, {'start_time': '20:10', 'end_time': '22:16'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 59906, 'imdb_id': 469494, 'imdb_title_id': 'tt0469494', 'film_name': 'There Will Be Blood', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'Contains strong violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/59906/059906h1.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/59906/059906h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 59906, 'film_name': 'There Will Be Blood', 'times': [{'start_time': '10:40', 'end_time': '13:08'}, {'start_time': '12:00', 'end_time': '14:28'}, {'start_time': '13:40', 'end_time': '16:08'}, {'start_time': '15:00', 'end_time': '17:28'}, {'start_time': '16:40', 'end_time': '19:08'}, {'start_time': '18:00', 'end_time': '20:28'}, {'start_time': '19:40', 'end_time': '22:08'}, {'start_time': '21:00', 'end_time': '23:28'}, {'start_time': '22:40', 'end_time': '01:08'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 3427, 'imdb_id': 116367, 'imdb_title_id': 'tt0116367', 'film_name': 'From Dusk Till Dawn', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '18 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/18.png', 'age_advisory': ''}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/3427/GBR_003427h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/3427/003427h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 3427, 'film_name': 'From Dusk Till Dawn', 'times': [{'start_time': '12:00', 'end_time': '14:24'}, {'start_time': '14:50', 'end_time': '17:14'}, {'start_time': '17:40', 'end_time': '20:04'}, {'start_time': '19:00', 'end_time': '21:24'}, {'start_time': '20:30', 'end_time': '22:54'}, {'start_time': '22:00', 'end_time': '00:24'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 1685, 'imdb_id': 109045, 'imdb_title_id': 'tt0109045', 'film_name': 'The Adventures of Priscilla, Queen of the Desert', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'Contains strong language, sex references and threat'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/1685/GBR_001685h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/1685/001685h2.jpg', 'width': 300, 'height': 197}}}}, 'showings': {'Standard': {'film_id': 1685, 'film_name': 'The Adventures of Priscilla, Queen of the Desert', 'times': [{'start_time': '14:20', 'end_time': '16:20'}, {'start_time': '16:40', 'end_time': '18:40'}, {'start_time': '19:00', 'end_time': '21:00'}, {'start_time': '21:20', 'end_time': '23:20'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 25, 'imdb_id': 111282, 'imdb_title_id': 'tt0111282', 'film_name': 'Stargate', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'Contains mild language and fantasy violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/25/000025h1.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 25, 'film_name': 'Stargate', 'times': [{'start_time': '21:00', 'end_time': '23:18'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 8675, 'imdb_id': 56172, 'imdb_title_id': 'tt0056172', 'film_name': 'Lawrence Of Arabia - 70mm', 'other_titles': {'EN': 'Lawrence Of Arabia'}, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'mild violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/8675/GBR_008675h0.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 8675, 'film_name': 'Lawrence Of Arabia - 70mm', 'times': [{'start_time': '10:20', 'end_time': '12:10'}]}}, 'show_dates': [{'date': '2024-03-09'}, {'date': '2024-03-10'}]}, {'film_id': 62407, 'imdb_id': 460791, 'imdb_title_id': 'tt0460791', 'film_name': 'The Fall', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'Contains strong violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/62407/062407h1.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/62407/062407h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 62407, 'film_name': 'The Fall', 'times': [{'start_time': '13:20', 'end_time': '15:34'}]}}, 'show_dates': [{'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}], 'status': {'count': 8, 'state': 'OK', 'method': 'cinemaShowTimes', 'message': None, 'request_method': 'GET', 'version': 'LEWA_XXv200', 'territory': 'XX', 'device_datetime_sent': '2024-03-08T15:23:23.150320Z', 'device_datetime_used': '2024-03-08 15:23:23'}}, 'Cinema 7': {'cinema': {'cinema_id': 42963, 'cinema_name': 'Cinema 7'}, 'films': [{'film_id': 7772, 'imdb_id': 82971, 'imdb_title_id': 'tt0082971', 'film_name': 'Raiders of the Lost Ark', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'Contains moderate violence and mild language'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/7772/GBR_007772h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/7772/007772h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 7772, 'film_name': 'Raiders of the Lost Ark', 'times': [{'start_time': '10:30', 'end_time': '12:44'}, {'start_time': '11:00', 'end_time': '13:14'}, {'start_time': '11:30', 'end_time': '13:44'}, {'start_time': '13:00', 'end_time': '15:14'}, {'start_time': '13:30', 'end_time': '15:44'}, {'start_time': '14:00', 'end_time': '16:14'}, {'start_time': '15:30', 'end_time': '17:44'}, {'start_time': '16:00', 'end_time': '18:14'}, {'start_time': '16:30', 'end_time': '18:44'}, {'start_time': '18:00', 'end_time': '20:14'}, {'start_time': '18:30', 'end_time': '20:44'}, {'start_time': '19:00', 'end_time': '21:14'}, {'start_time': '20:30', 'end_time': '22:44'}, {'start_time': '21:00', 'end_time': '23:14'}, {'start_time': '21:30', 'end_time': '23:44'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 184126, 'imdb_id': 3659388, 'imdb_title_id': 'tt3659388', 'film_name': 'The Martian', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '12A ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/12a.png', 'age_advisory': 'infrequent strong language, injury detail'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/184126/GBR_184126h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/184126/184126h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 184126, 'film_name': 'The Martian', 'times': [{'start_time': '11:00', 'end_time': '13:06'}, {'start_time': '11:40', 'end_time': '13:46'}, {'start_time': '12:40', 'end_time': '14:46'}, {'start_time': '13:20', 'end_time': '15:26'}, {'start_time': '14:30', 'end_time': '16:36'}, {'start_time': '15:00', 'end_time': '17:06'}, {'start_time': '15:40', 'end_time': '17:46'}, {'start_time': '17:00', 'end_time': '19:06'}, {'start_time': '18:00', 'end_time': '20:06'}, {'start_time': '20:20', 'end_time': '22:26'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 59906, 'imdb_id': 469494, 'imdb_title_id': 'tt0469494', 'film_name': 'There Will Be Blood', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'Contains strong violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/59906/059906h1.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/59906/059906h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 59906, 'film_name': 'There Will Be Blood', 'times': [{'start_time': '12:40', 'end_time': '15:08'}, {'start_time': '15:30', 'end_time': '17:58'}, {'start_time': '17:20', 'end_time': '19:48'}, {'start_time': '18:20', 'end_time': '20:48'}, {'start_time': '20:10', 'end_time': '22:38'}, {'start_time': '21:10', 'end_time': '23:38'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 3427, 'imdb_id': 116367, 'imdb_title_id': 'tt0116367', 'film_name': 'From Dusk Till Dawn', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '18 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/18.png', 'age_advisory': ''}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/3427/GBR_003427h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/3427/003427h2.jpg', 'width': 300, 'height': 200}}}}, 'showings': {'Standard': {'film_id': 3427, 'film_name': 'From Dusk Till Dawn', 'times': [{'start_time': '11:50', 'end_time': '14:14'}, {'start_time': '12:50', 'end_time': '15:14'}, {'start_time': '15:30', 'end_time': '17:54'}, {'start_time': '18:10', 'end_time': '20:34'}, {'start_time': '18:40', 'end_time': '21:04'}, {'start_time': '20:00', 'end_time': '22:24'}, {'start_time': '20:50', 'end_time': '23:14'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 1685, 'imdb_id': 109045, 'imdb_title_id': 'tt0109045', 'film_name': 'The Adventures of Priscilla, Queen of the Desert', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'Contains strong language, sex references and threat'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/1685/GBR_001685h0.jpg', 'width': 200, 'height': 300}}}, 'still': {'1': {'image_orientation': 'landscape', 'medium': {'film_image': 'https://image.movieglu.com/1685/001685h2.jpg', 'width': 300, 'height': 197}}}}, 'showings': {'Standard': {'film_id': 1685, 'film_name': 'The Adventures of Priscilla, Queen of the Desert', 'times': [{'start_time': '12:10', 'end_time': '14:10'}, {'start_time': '14:30', 'end_time': '16:30'}, {'start_time': '16:50', 'end_time': '18:50'}, {'start_time': '19:10', 'end_time': '21:10'}, {'start_time': '21:40', 'end_time': '23:40'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 25, 'imdb_id': 111282, 'imdb_title_id': 'tt0111282', 'film_name': 'Stargate', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'Contains mild language and fantasy violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/25/000025h1.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 25, 'film_name': 'Stargate', 'times': [{'start_time': '21:20', 'end_time': '23:38'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 6650, 'imdb_id': 116209, 'imdb_title_id': 'tt0116209', 'film_name': 'The English Patient', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': ''}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/6650/006650h1.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 6650, 'film_name': 'The English Patient', 'times': [{'start_time': '12:20', 'end_time': '14:41'}, {'start_time': '15:10', 'end_time': '17:31'}, {'start_time': '17:50', 'end_time': '20:11'}, {'start_time': '20:30', 'end_time': '22:51'}]}}, 'show_dates': [{'date': '2024-03-08'}, {'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}, {'film_id': 8675, 'imdb_id': 56172, 'imdb_title_id': 'tt0056172', 'film_name': 'Lawrence Of Arabia - 70mm', 'other_titles': {'EN': 'Lawrence Of Arabia'}, 'version_type': 'Standard', 'age_rating': [{'rating': 'PG ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/pg.png', 'age_advisory': 'mild violence'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'UK', 'medium': {'film_image': 'https://image.movieglu.com/8675/GBR_008675h0.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 8675, 'film_name': 'Lawrence Of Arabia - 70mm', 'times': [{'start_time': '10:40', 'end_time': '12:30'}]}}, 'show_dates': [{'date': '2024-03-09'}, {'date': '2024-03-10'}]}, {'film_id': 21448, 'imdb_id': 120188, 'imdb_title_id': 'tt0120188', 'film_name': 'Three Kings', 'other_titles': None, 'version_type': 'Standard', 'age_rating': [{'rating': '15 ', 'age_rating_image': 'https://assets.movieglu.com/age_rating_logos/xx/15.png', 'age_advisory': 'for graphic war violence and very strong language'}], 'images': {'poster': {'1': {'image_orientation': 'portrait', 'region': 'global', 'medium': {'film_image': 'https://image.movieglu.com/21448/021448h1.jpg', 'width': 200, 'height': 300}}}}, 'showings': {'Standard': {'film_id': 21448, 'film_name': 'Three Kings', 'times': [{'start_time': '12:00', 'end_time': '14:40'}]}}, 'show_dates': [{'date': '2024-03-09'}, {'date': '2024-03-10'}, {'date': '2024-03-11'}, {'date': '2024-03-12'}, {'date': '2024-03-13'}, {'date': '2024-03-14'}]}], 'status': {'count': 9, 'state': 'OK', 'method': 'cinemaShowTimes', 'message': None, 'request_method': 'GET', 'version': 'LEWA_XXv200', 'territory': 'XX', 'device_datetime_sent': '2024-03-08T15:23:23.150320Z', 'device_datetime_used': '2024-03-08 15:23:23'}}}, 'cinemas_info': [{'name': 'Cinema 6', 'cinema_id': 10636, 'lat': -22.680721, 'lng': 14.519094, 'distance': 57.55892076987}, {'name': 'Cinema 7', 'cinema_id': 42963, 'lat': -22.669146, 'lng': 15.028214, 'distance': 80.352112347501}]}
