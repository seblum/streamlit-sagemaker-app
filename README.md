# Streamlit Sagemaker App

This is a simple Streamlit web application that allows you to list and display information about Amazon SageMaker endpoints. Amazon SageMaker is a fully managed machine learning service that enables you to build, train, and deploy machine learning models at scale.

### How to Use

To use this app, you need to provide your AWS access key and secret key. You will need to set up your credentials using environment variables. Make sure the AWS IAM role has sufficient permissions to list SageMaker endpoints.

```
export AWS_REGION="YOUR-AWS-REGION"
export AWS_ACCESS_KEY_ID="YOUR-SECRET-ACCESS-KEY"
export AWS_SECRET_ACCESS_KEY="YOUR-ACCESS-KEY-ID"
export AWS_ROLE_NAME="YOUR-ROLE-NAME"
```

Run the script either locally using the following command.

```
poetry run streamlit run app/main.py --server.baseUrlPath=/sagemaker
```

Or build the container image and run it within docker.

```
docker build -f Dockerfile -t=streamlitsagemaker:latest .

docker run -it -e AWS_REGION="YOUR-AWS-REGION" \
-e AWS_ACCESS_KEY_ID="YOUR-ACCESS-KEY-ID" \
-e AWS_SECRET_ACCESS_KEY="YOUR-SECRET-ACCESS-KEY" \
-e AWS_ROLE_NAME="YOUR-ROLE-NAME"" \
-p 8501:8501 \
streamlitsagemaker:latest
```