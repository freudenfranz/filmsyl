# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install --upgrade pip
	@pip install -r requirements.txt

# cd #./filmsyl-api
# @pyenv virtualenv films-you-like-api
# @pyenv local films-you-like-api
# @pip install -r requirements.txt
# cd ..

#check_code:
#	@flake8 scripts/* filmsyl/*.py

#black:
#	@black scripts/* filmsyl/*.py

#test:
#	@coverage run -m pytest tests/*.py
#	@coverage report -m --omit="${VIRTUAL_ENV}/lib/python*"

#ftest:
#	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr filmsyl-*.dist-info
	@rm -fr filmsyl.egg-info

install:
	@pip install . -U

all: clean install #test black check_code

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#     PACKAGE AND UPLOAD TO GOOGLE CLOUD
# ----------------------------------
build_deploy:
	@docker build --platform linux/amd64 -t \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod .
	@docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod \
				--quiet
	@gcloud run deploy --image \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod \
				--memory ${GAR_MEMORY} --region ${GCP_REGION} \
				--env-vars-file .env.yaml


# ----------------------------------
#     API
# ----------------------------------
run_api:
	uvicorn filmsyl.api.fast:app --reload

