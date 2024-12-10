Docker demo for testing a stock trading strategy
Intended to be executed on a cloud container platform such as AWS Batch


To use the notebook in coderpad
pip install numpy==1.23.5 boto3 backtesting yfinance bokeh==2.4.3

To use with docker
docker build -t backtest .

To Run locally pass in environment variables to docker run

eval "$(aws configure export-credentials --format env)"

docker run  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
            -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
            -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
            -e TICKER=GOOG \
            -e BUCKET=<yourS3bucket> \
             backtest



