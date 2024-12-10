
# latest Ubuntu version
FROM conda/miniconda3

ADD environment.yml /tmp/

RUN conda env create -f /tmp/environment.yml

ADD backtest.py /tmp/

ENV BUCKET=hosman-backtest
ENV TICKER=AAPL

CMD ["bash", "-c", "source activate backtest && python /tmp/backtest.py"]