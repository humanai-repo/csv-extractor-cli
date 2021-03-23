# CSV Extractor CLI
A simple command line tool to extract specific columns from a CSV file and
split the output files by user.

The purpose of the Extractor is to pre-process datafiles so that the minimum
data is passed to an unsafe processor.

## Example Usage

```bash
csv_extractor -h
usage: csv_extractor [-h] -i INPUT -c COLUMN --id ID [-n N] [-p PREFIX]
                     [-f {tdcsv}]

Extract specified columns from a CSV file and split output based on the
specified ID column.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file (or files) to process. Delimited format.
                        For large files split into chunks, list the chunks in
                        order.
  -c COLUMN, --column COLUMN
                        The column (or columns) to extract.
  --id ID               Column containing a unique identifier to be
                        differentially private with respect to.
  -n N                  Optionally provide the expected number of output
                        files. This will be validated and and error thrown if
                        this does not match.
  -p PREFIX, --prefix PREFIX
                        Output prefix.
  -f {tdcsv}, --format {tdcsv}
                        File format. tdcsv = tilda delimited csv
```

```bash
csv_extractor -i Paragraphs.txt.chunk1 -i Paragraphs.txt.chunk2 -c PlainText --id WorkID -p data/paragraphs
```

To run from Docker, launch the docker image in interactive mode with the
directory containing input data mounted in the container.
```bash
docker run -it -v $ABSOLUTE_PATH_INPUT_DIR:$CONTAINER_INPUT --name csv-extractor csv-extractor
```

Then run the commands as above.

## Build
To build a local python package (tested on Mac OS 10.2).

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
# Virtual env bundled with MacOS is faulty.
pip install --upgrade virtualenv
pip install --upgrade build
python3 -m build
# This will output a Tar file in dist/csv-extractor-*.tar.gz
deactivate
```

To wrap the local python package in into a Docker image run
```bash
docker build --tag csv-extractor .
```

To push to docker hub
```bash
# List runing docker image to get the Image ID
docker images

docker tag $IMAGE_ID $DOCKERHUB_USERNAME/csv-extractor:latest

docker login --username=$DOCKERHUB_USERNAME

docker push $DOCKERHUB_USERNAME/csv-extractor
```

## Install
Install from a local tar file.

```bash
# Optionally install in local virtual env.
source venv/bin/activate
pip install dist/csv-extractor-cli-*.tar.gz
# Reload the virtual environment to make the tool available.
deactivate; source venv/bin/activate
```