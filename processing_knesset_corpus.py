import os
import re
from docx import Document

class ProtocolFile:
    def init(self, knesset_num, protocol, file_num):
        self.knesset_num = knesset_num
        self.protocol = protocol
        self.file_num = file_num

def extract_info_from_filename(filename):
    try:

        pattern = re.compile(r'(\d+)_pt[vm]_(\d+)\.docx')
        match = pattern.match(filename)

        if match:
            parsed_list = filename.split("_")

            knesset_number = int(parsed_list[0])
            protocol = parsed_list[1].replace("pt", "")
            file_num = int(parsed_list[2].split(".")[0])
            return int(knesset_number), protocol, int(file_num)
        else:
            return -1

    except Exception as e:
        raise ValueError(f"Error extracting information from filename: {str(e)}")

def process_docx_files(directory="."):
    protocol_files_list = []

    for filename in os.listdir(directory):
        if filename.endswith(".docx"):
            try:

                result = extract_info_from_filename(filename)
                if result == -1:
                    continue

                if result:
                    knesset_number, protocol, file_num = result
                    if protocol == 'v':
                        protocol = 'committee'
                    else:
                        protocol = 'plenary'
                    protocol_file = ProtocolFile(knesset_number, protocol, file_num)
                    protocol_files_list.append(protocol_file)

                    # doc_path = os.path.join(directory, filename)
                    # document = Document(doc_path)


            except ValueError as ve:
                print(f"Error processing file '{filename}': {str(ve)}")

    return protocol_files_list

if name == "main":
    result_list = process_docx_files()
    for protocol_file in result_list:
        print(f"Knesset Number: {protocol_file.knesset_num}, Protocol: {protocol_file.protocol}, File Number: {protocol_file.file_num}")