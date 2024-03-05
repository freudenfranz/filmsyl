# Install

Go to `https://github.com/{group}/filmsyl` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
#sudo apt-get install virtualenv python-pip python-dev
#deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
pyenv virtualenv films-you-like-api
pyenv local films-you-like-api
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

# API

## Routes

base_url = ''
```
/get-clusters
/get-recommendation
/upload-netflix-history
```
