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

# API

## Routes

base_url = ''
```
/cluster
/get-recommendation
/upload-netflix-history
```
