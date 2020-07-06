# Key

dd74decc-8825-4a49-b9bc-e4608249d612

# Local Development

conda activate entroprise-api
conda env export --file environment.yml --name entroprise-api

gcloud auth application-default login

#dev    
uvicorn main:app --reload

#prod
gunicorn main:app -c gunicorn_config.py