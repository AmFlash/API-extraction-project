#This is the code to read various test data cases and convert them into a single CSV file


import logging
import os.path

#Now we have imported some more important libraries
#The shutil library in Python provides a set of high-level file operations that make it easy to work with files and directories. It offers functions for copying, moving, renaming, and deleting files, as well as for creating and manipulating directories.
#The zipfile library in Python provides functionalities to work with ZIP archives. It allows you to create, extract, modify, and manage ZIP files.

import shutil
import zipfile

from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_renditions_element_type import \
    ExtractRenditionsElementType
from adobe.pdfservices.operation.pdfops.options.extractpdf.table_structure_type import TableStructureType
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

try:
    # Get base path.
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Initial setup, create credentials instance.
    credentials = Credentials.service_account_credentials_builder() \
        .from_file(base_path + "/pdfservices-api-credentials.json") \
        .build()

    # Create an ExecutionContext using credentials.
    execution_context = ExecutionContext.create(credentials)

    # Create a temporary directory to store extracted files.
    temp_dir = os.path.join(base_path, "output", "temp")
    os.makedirs(temp_dir, exist_ok=True)

    for i in range(100):
        output = "output" + str(i)

        # Create a new operation instance for each iteration.
        extract_pdf_operation = ExtractPDFOperation.create_new()

        # Set operation input from a source file.
        source = FileRef.create_from_local_file(base_path + "/TestDataSet/" + output + ".pdf")
        extract_pdf_operation.set_input(source)

# By a few changes in the code,the file has been converted into csv format instead of xlsx.


        # Build ExtractPDF options and set them into the operation.
        extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
            .with_elements_to_extract([ExtractElementType.TEXT, ExtractElementType.TABLES]) \
            .with_element_to_extract_renditions(ExtractRenditionsElementType.TABLES) \
            .with_table_structure_format(TableStructureType.CSV) \
            .build()
        extract_pdf_operation.set_options(extract_pdf_options)

        # Execute the operation.
        result: FileRef = extract_pdf_operation.execute(execution_context)
        
        # Save the result to the temporary directory.
        temp_file_path = os.path.join(temp_dir, f"result_{i}.zip")
        result.save_as(temp_file_path)

    # Create a final ZIP file and add all the extracted files.
    final_zip_path = os.path.join(base_path, "outputcsv", "ExtractTextTableInfoFromPDF.zip")
    with zipfile.ZipFile(final_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as final_zip:
        for i in range(100):
            temp_file_path = os.path.join(temp_dir, f"result_{i}.zip")
            final_zip.write(temp_file_path, arcname=f"result_{i}.zip")

    # # Remove the temporary directory.
    #shutil.rmtree(temp_dir)

except (ServiceApiException, ServiceUsageException, SdkException):
    logging.exception("Exception encountered while executing operation")
    
# The code till here has extracted the required info and save it into a zip file named ExtractTextTableInfoFromPDF

# Now the code below unzips all the files inside the folder ExtractTextTableInfoFromPDF

from zipfile import ZipFile
# Get the base path.
base_path ="/Users/vibha/Desktop/kli/"
# Loop to extract multiple zip files
for i in range(100):
    output = str(i)
    zip_file_path = os.path.join(base_path+ "outputcsv/ExtractTextTableInfoFromPDF/"+ "result_" + output + ".zip")
    destination_path = os.path.join(base_path, "unzippedfiles/output"+output)
    
    with ZipFile(zip_file_path, 'r') as zip_object:
        # Extracting files from the zip to a specific location.
        zip_object.extractall(path=destination_path)

    print("Extraction completed for", zip_file_path)

print("Extraction completed for all zip files.")


# Now we have imported some more required libraries.
# The re module in Python provides support for regular expressions, allowing you to perform pattern matching and manipulation on strings. Regular expressions are powerful tools for searching, extracting, and manipulating text data.
import re
# The csv module in Python provides functionalities to work with Comma-Separated Values (CSV) files. It allows you to read from and write to CSV files using a simple and straightforward API.
import csv
import pandas as pd
#The json library in Python provides functionalities to work with JavaScript Object Notation (JSON) data. It allows you to serialize Python objects into JSON format and deserialize JSON data into Python objects.
import json
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
def remove_numbers(input_string):
    # Iterate over each character and keep non-digit characters
    result = ''.join(char for char in input_string if not char.isdigit())
    return result
df_list = []
for x in range(2,100):
   
# Opening JSON file

    json_file_path = os.path.join(base_path, "unzippedfiles/output"+str(x)+"/structuredData.json")
    f = open(json_file_path)
    # Initialize variables
    Bussiness__Name = ""
    Bussiness__StreetAddress = ""
    Bussiness__Country = ""
    Bussiness__Zipcode = ""
    Invoice__Number = ""
    Bussiness__Description = ""
    Customer__Name = ""
    Customer__Email = ""
    Customer__Name = ""
    Customer__PhoneNumber = ""
    Customer_Address_line1 = ""
    Customer_Address_line2 = ""
    Roman =""
    dosa = ""
    Invoice__IssueDate="12-05-23"
    Invoice__Description = ""
    Invoice__DueDate=""
    Invoice__Tax="10"
    count = 0
    taxidx=0
        # Load JSON data as a dictionary
    data = json.load(f)

        # Create a list of dictionaries for DataFrame creation
    entries = []
    fptr = open(base_path+"/textFiles/structure"+str(x)+".txt", "w")
        # Iterate through the JSON elements
    shift_idx = 0
    type2_idx=0

    for idx, i in enumerate(data['elements']):
            
        if 'Text' in i.keys():
            value = i['Text']
            fptr.write(value+"\n")
            print(idx,value)
            if idx == 0:
                Bussiness__Name = value
            elif idx == 1:
                Bussiness__StreetAddress = value
                Bussiness__City=Bussiness__StreetAddress.split(',')[1]
            elif idx == 2:
                Bussiness__Country = value
            elif idx == 3:
                Bussiness__Zipcode = value
            elif idx == 4:
                Invoice__Number = value
                Invoice__Number = Invoice__Number.split(' ')[1]
                if len(value.split())==2:
                    shift_idx=2
                else:
                    type2_idx=1
            elif idx == 6 + shift_idx:
                    Bussiness__Description = value
            elif idx == 7+ shift_idx:
                    Roman= value
            elif idx == 8+ shift_idx:
                    Customer__Name = value
            elif idx == 9+ shift_idx:
                    Customer__Email = value
            elif idx == 10+ shift_idx+type2_idx:
                    Customer__PhoneNumber = value
            elif idx == 11+ shift_idx+type2_idx:
                    Customer_Address_line1= value
            elif idx == 12+ shift_idx+type2_idx:
                    Customer_Address_line2 = value
            elif idx == 14+ shift_idx+type2_idx:
                    Invoice__Description= value
            # elif idx == 15 + shift_idx:
            #   Invoice__Description+= value
            elif idx == 18:
                    Invoice__DueDate = value.split()[-1]
            else:
                continue
    fptr.close()
            #     taxidx=idx+1
        # else :print("text not found")
    with open(base_path+"/textFiles/structure"+str(x)+".txt", "r") as file:
        content = file.read()

#pointer
#The code opens a file specified by the path 
    fptr = open(base_path+"/textFiles/structure"+str(x)+".txt", "r")  

    phone_pattern = r'(\d{3}-\d{3}-\d{4})'
    # Matches a phone number in the format xxx-xxx-xxxx.
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{1,}\b'
    # Matches an email address.
    duedate_pattern = r'Due date:'
    # Matches the string "Due date:".
    invoice_pattern = r'DETAILS(.*?)PAYMENT'
    # Matches the substring between the strings "DETAILS" and "PAYMENT".
    tax_pattern = r'Tax % '
    # Matches the string "Tax % ".
    # Code performs pattern matching using regular expressions on the content variable . It searches for matches using the re.search() function, and the matches are stored in respective variables 
    phone_match = re.search(phone_pattern, content, re.DOTALL)
    email_match = re.search(email_pattern, content, re.MULTILINE)
    duedate_match = re.search(duedate_pattern, content, re.MULTILINE)
    invoice_match = re.search(invoice_pattern, content, re.DOTALL)
    tax_match = re.search(tax_pattern, content, re.DOTALL)
    print(tax_match)
    print(invoice_match)
    print(email_match)
    print(phone_match)
    print(duedate_match)
    if tax_match:
        index = content.find(tax_match.group(0))
        fptr.seek((index+len(tax_match.group(0))+1))
        lines_after_index = fptr.readlines()[:1]
        Invoice__Tax = lines_after_index[0].strip()
        # print(Invoice__Tax)
        # The code finds the index of the matched text within content, seeks to that index in the file (fptr), reads the line following the matched text, and assigns the stripped line to the variable Invoice__Tax.
    if invoice_match:
        extracted_text = invoice_match.group(1)
        # print('this',extracted_text)
        Invoice__Description = extracted_text.strip()
        # The code extracts the matched text (between "DETAILS" and "PAYMENT") and assigns the stripped text to the variable Invoice__Description.


    if phone_match:
        phone_number = phone_match.group(1)
        Customer__PhoneNumber = phone_number.strip()
        # print(phone_number)
        index = content.find(phone_number)
    
        fptr.seek((index+len(phone_number)+2))
        lines_after_index = fptr.readlines()[:2]
        Customer_Address_line1 = lines_after_index[0].strip()
        Customer_Address_line2 = lines_after_index[1].strip()
        # print(lines_after_index)
        fptr.seek(0)
        # The code extracts the matched phone number, assigns it to the variable phone_number, finds its index in content, seeks to that index in the file, reads the next two lines, and assigns the stripped lines to Customer_Address_line1 and Customer_Address_line2 variables.
    if duedate_match:
        duedate = duedate_match.group(0)
        # print(duedate)
        index = content.find(duedate)
        fptr.seek((index+len(duedate)+2))
        lines_after_index = fptr.readlines()[:1]
        Invoice__DueDate = lines_after_index[0].strip()
        fptr.seek(0)
        # The code extracts the matched text ("Due date:") and assigns it to the variable duedate. It finds the index of the matched text in content, seeks to that index in the file, reads the next line, and assigns the stripped line to the variable Invoice__DueDate.
    if email_match:
        email = email_match.group(0)
        # print(email)
        Customer__Email = email.strip()
        
        
        name = email.split('@')[0]
        
        name = name.replace('.', ' ').title()
        name = name.replace('_', ' ').title()
        name = remove_numbers(name)
        # name = re.sub(r'[_\.]', ' ', name).title()
        # name=remove_numbers(name)
        # name = name.replace('.','_', ' ').title()
        Customer__Name = name.strip()
        # The code extracts the matched email address and assigns it to the variable email. It assigns the stripped email address to Customer__Email. It also processes the email address to extract the customer's name by splitting the email at '@', replacing dots ('.') and underscores ('_') with spaces, converting the name to title case, and removing numbers. The resulting name is assigned to the variable Customer__Name.
        
    print(Invoice__Tax)
    print(Customer_Address_line1)
    print(Customer_Address_line2)
    print(Invoice__DueDate)
    print(Customer__Email)
    print(Customer__Name)
    print(Customer__PhoneNumber)
        
    if len(Invoice__Tax)==0:Invoice__Tax="10"
           

    entry = {
            'Business__City': Bussiness__City,
            'Business__country': Bussiness__Country,
            'Business__Description':Bussiness__Description,
            'Business__Name': Bussiness__Name,
            'Business__StreetAddress': Bussiness__StreetAddress,
            'Bussiness__Zipcode': Bussiness__Zipcode,
            'Customer_Address_line1': Customer_Address_line1,
            'Customer_Address_line2': Customer_Address_line2,
            'Customer__Email' : Customer__Email,
            'Customer__Name': Customer__Name,
            'Customer__PhoneNumber': Customer__PhoneNumber,
            #'Invoice__BillDetails__Name': Invoice__BillDetails__Name,
            #'Invoice__BillDetails__Quantity': Invoice__BillDetails__Quantity,
            #'Invoice__BillDetails__Rate':Invoice__BillDetails__Rate,
            'Invoice__Description' :Invoice__Description,
            'Invoice__DueDate' : Invoice__DueDate,
            'Invoice__IssueDate': Invoice__IssueDate,
            'Invoice__Number' : Invoice__Number,
            'Invoice__Tax':Invoice__Tax,
        }

    entries.append(entry)

  

    

    filepartnu=0
    for m in range(0,7,2):
    # A loop is executed for the range (0, 7, 2), which means it will iterate over the values 0, 2, 4, and 6. The loop variable m takes these values.
        filename = "/Users/vibha/Desktop/kli/unzippedfiles/output"+str(x)+"/tables/fileoutpart"+str(m)+".csv"
    # Inside the loop, a filename is constructed using the value of x and m. The file is read using pd.read_csv() function, and the resulting DataFrame is stored in the variable dfa.
        dfa= pd.read_csv(filename)
    
        row_count = len(dfa)
        columns_count=len(dfa.columns)
        if row_count>1 and columns_count==4: 
              filepartnu=str(m)
              break
    
    filename = "/Users/vibha/Desktop/kli/unzippedfiles/output"+str(x)+"/tables/fileoutpart"+filepartnu+".csv"
    
    dfa= pd.read_csv(filename)
    row_count = len(dfa)
    c=row_count

    dfa.columns = ['Invoice__BillDetails__Name', 'Invoice__BillDetails__Quantity', 'Invoice__BillDetails__Rate',""]
    #The column names of dfa are updated 

    df1 = pd.concat([pd.DataFrame([entry])]*(row_count), ignore_index=True)
    #A new DataFrame df1 is created by concatenating the single-row DataFrame [entry] (repeated row_count times) for each row in dfa. The resulting DataFrame has the same number of rows as dfa.

    df1['Invoice__BillDetails__Name'] = dfa['Invoice__BillDetails__Name'].iloc[0:c].reset_index(drop=True)
    df1['Invoice__BillDetails__Quantity'] = dfa['Invoice__BillDetails__Quantity'].iloc[0:c].reset_index(drop=True)
    df1['Invoice__BillDetails__Rate'] = dfa['Invoice__BillDetails__Rate'].iloc[0:c].reset_index(drop=True)

    print(df1)
    df_list.append(df1)
    #df1 is appended to the df_list.

final_df = pd.concat(df_list, ignore_index=True)
# Convert DataFrame to CSV file
final_df.to_csv('/Users/vibha/Desktop/kli/finalcsv/final.csv', index=False)