# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install --upgrade pip
	@pip install -r requirements.txt


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


# ----------------------------------
#     PACKAGE AND UPLOAD TO GOOGLE CLOUD
# ----------------------------------

build_deploy_dev:
	@docker build --platform linux/amd64 -t \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:dev .
	@docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:dev \
				--quiet
	@gcloud run deploy films-you-like-dev --image \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:dev \
				--memory ${GAR_MEMORY} --region ${GCP_REGION} \
				--env-vars-file .env.yaml

build_deploy_prod:
	@docker build --platform linux/amd64 -t \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod .
	@docker push ${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod \
				--quiet
	@gcloud run deploy films-you-like --image \
				${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/filmsyl/${GAR_IMAGE}:prod \
				--memory ${GAR_MEMORY} --region ${GCP_REGION} \
				--env-vars-file .env.yaml

# ----------------------------------
#     API
# ----------------------------------
run_api:
	uvicorn filmsyl.api.fast:app --reload
