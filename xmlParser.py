import xml.etree.ElementTree as ET
import collections
import csv

class XMLParser:
    def __init__(self, xml_file_path, csv_directory, n_rows, delim):
        self.xml_file_path = xml_file_path
        self.csv_directory = csv_directory
        self.n_rows = n_rows
        self.delim = delim

        # Maps tag paths to columns in the csv
        self.tag_columns = {}
        self.n_cols = 0

    def parse_record(self, elem):
        # This function gets an element node from ElementTree and parses it into one csv row
        q = collections.deque()
        q.append((elem, ""))
        row = [None] * self.n_cols

        while q:
            node, node_path = q.popleft()
            tag = node_path + node.tag
            if tag not in self.tag_columns:
                self.tag_columns[tag] = self.n_cols
                self.n_cols += 1
                row.append(node.text)

            else:
                row[self.tag_columns[tag]] = node.text

            for attr in node.attrib:
                attr_tag = tag + "@" + attr
                if attr_tag not in self.tag_columns:
                    self.tag_columns[attr_tag] = self.n_cols
                    self.n_cols += 1
                    row.append(node.attrib[attr])
                else:
                    row[self.tag_columns[attr_tag]] = node.attrib[attr]

            for child in node:
                q.append((child, tag + "/"))
        
        return row

    def parse(self):
        with open(self.csv_directory + "variant_rows.csv", 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delim)
            counter = 0
            for event, elem in ET.iterparse(self.xml_file_path):
                row = self.parse_record(elem)
                writer.writerow(row)
                counter += 1
                if counter >= self.n_rows:
                    break

        with open(self.csv_directory + "column_table.csv", 'w+') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delim)
            tagList = sorted(self.tag_columns.items(), key=lambda x:x[1])
            writer.writerow([tup[0] for tup in tagList])


parser = XMLParser("ClinVarVCVRelease_2024-02.xml", "csv/", 10000, ',')
parser.parse()

