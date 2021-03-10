FROM python:3.6
COPY dist/csv-extractor-cli-*.tar.gz ./csv-extractor-cli.tar.gz
WORKDIR ./
RUN pip install csv-extractor-cli.tar.gz
CMD bash