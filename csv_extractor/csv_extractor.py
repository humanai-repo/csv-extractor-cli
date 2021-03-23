import argparse
import csv


def build_parser():
    parser = argparse.ArgumentParser(
        description='Extract specified columns from a CSV file and split ' +
        'output based on the specified ID column.')
    parser.add_argument('-i', '--input', action='append', required=True,
                        help='input file (or files) to process. Delimited ' +
                        'format. For large files split into chunks, list ' +
                        'the chunks in order. Assumed only the first file ' +
                        'has a header row.')
    parser.add_argument('-c', '--column', action='append', required=True,
                        help='The column (or columns) to extract.')
    parser.add_argument('--id', required=True,
                        help='Column containing a unique identifier to be ' +
                        'differentially private with respect to.')
    parser.add_argument('-n', type=int, required=False,
                        help='Optionally provide the expected number of ' +
                        'output files. This will be validated and ' +
                        'and error thrown if this does not match.')
    parser.add_argument('-p', '--prefix', required=False,
                        help='Output prefix.')
    parser.add_argument('-f', '--format', required=False, choices=['tdcsv'],
                        default='tdcsv',
                        help="File format. tdcsv = tilda delimited csv")
    return parser


class FileSet:
	"""An iterator for a set of files"""

    def __init__(self, files):
        self.file = None
        self.files = files

    def __iter__(self):
        self.filesIter = iter(self.files)
        return self

    def __next__(self):
        try:
            if self.file is None:
                raise StopIteration
            return next(self.file)
        except StopIteration:
            if not self.file is None:
                self.file.close()
            self.file = open(next(self.filesIter), newline='')
            return next(self)


def validateColumns(header, columns, idColumn):
	"""Return the indexes of the columns to extract and the ID columns,
	raise an exception if any do not exist."""

    try:
        columnIndexes = [header.index(c) for c in columns]
        idIndex = header.index(idColumn)
        return columnIndexes, idIndex
    except ValueError:
        raise Exception("Column or ID not found in header")


def buildOutputColumn(row, columnIndexes):
    return [row[ci] for ci in columnIndexes]


def getOutputFile(outputFiles, i, prefix, columns):
	# TODO: Keep a reference to the open files and close them.
    if not i in outputFiles:
        filename = "%s-%s.csv" % (prefix, len(outputFiles))
        outputFiles[i] = csv.writer(open(filename, 'w'))
        outputFiles[i].writerow(columns)
    return outputFiles[i]


def main():
    # Initialise vars
    parser = build_parser()
    parsed = parser.parse_args()
    # TODO: When more formats added support here and switch on the format arg.
    reader = csv.reader(FileSet(parsed.input), quotechar='~')
    prefix = parsed.prefix
    columnIndexes, idIndex, header = None, None, None
    columns = parsed.column
    idColumn = parsed.id
    outputFiles = {}

    # Main loop
    for row in reader:
        if header is None:
            header = row
            columnIndexes, idIndex = validateColumns(header, columns, idColumn)
        else:
            i = row[idIndex]
            outputRow = buildOutputColumn(row, columnIndexes)
            # Get File
            outputFile = getOutputFile(outputFiles, i, prefix, columns)
            # Write row
            outputFile.writerow(outputRow)

    if parsed.n and parsed.n != len(outputFiles):
        raise Exception("Number of output files not as expected")


if __name__ == "__main__":
    main()
