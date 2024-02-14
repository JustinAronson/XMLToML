import csv
import pandas as pd

class CSVNormalizer:
    def __init__(self, csv_path, delim):
        self.column_table_path = csv_path + "column_table.csv"
        self.variant_rows_path = csv_path + "variant_rows.csv"
        self.delim = delim

        with open(self.column_table_path) as headersFP:
            column_header_reader = csv.reader(headersFP, delimiter=self.delim)
            column_header_list = next(column_header_reader)
            self.number_of_columns = len(column_header_list)
        
    def normalize_row_length(self):
        # Normalize the row length of the csv file so we can process it with pandas
        with open(self.column_table_path, 'a') as column_table:
            writer = csv.writer(column_table, delimiter=self.delim)
            with open(self.variant_rows_path, 'r') as variant_rows:
                csv_reader = csv.reader(variant_rows, delimiter=self.delim)
                for csvRow in csv_reader:
                    csvRow.extend([None] * (self.number_of_columns - len(csvRow)))
                    writer.writerow(csvRow)

    def remove_empty_columns(self):
        # Remove empty columns from the csv file
        df = pd.read_csv(self.column_table_path, delimiter=self.delim)
        df.dropna(axis=1, how='all', inplace=True)
        df.to_csv(self.column_table_path, sep=self.delim, index=False)

normalizer = CSVNormalizer("csv/", ',')
normalizer.normalize_row_length()
normalizer.remove_empty_columns()