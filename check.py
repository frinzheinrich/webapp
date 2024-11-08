#crosscheck
from datetime import datetime

def parse_date(date_string):
    # Try parsing the date in different formats
    for fmt in ("%d %b %Y", "%m/%d/%y", "%Y/%m/%d"):
        try:
            # Parse the date and then format it as a string
            dt = datetime.strptime(date_string, fmt)
            return dt.strftime("%Y-%m-%d")  # Format the output as YYYY-MM-DD
        except ValueError:
            continue
    return None

def jcompare_dict_values(iddict, formdict):
    mismatches = []

    if 'Given and middle names (as shown in passport)_a' in formdict:
        if iddict.get('FIRST_NAME').lower() != formdict.get('Given and middle names (as shown in passport)_a')[0].lower():
            mismatches.append(f"First Name Mismatch: '{iddict.get('FIRST_NAME')}' vs '{formdict.get('Given and middle names (as shown in passport)_a')[0]}'")
    else:
        mismatches.append("Given Name not detected in the VAF")

    if 'Surname (as shown in passport)_a' in formdict:
        if iddict.get('LAST_NAME').lower() != formdict.get('Surname (as shown in passport)_a')[0].lower():
            mismatches.append(f"Last Name Mismatch: '{iddict.get('LAST_NAME')}' vs '{formdict.get('Surname (as shown in passport)_a')[0]}'")
    else:
        mismatches.append("Last Name not detected in the VAF")

    if 'Date of birth_a' in formdict:
        if parse_date(iddict.get('DATE_OF_BIRTH')) != parse_date(formdict.get('Date of birth_a')[0]):
            mismatches.append(f"Date of Birth Mismatch: '{iddict.get('DATE_OF_BIRTH')}' vs '{formdict.get('Date of birth_a')[0]}'")
    else:
        mismatches.append("Date of Birth not detected in the VAF")

    if 'Date of issue_a' in formdict:
        if parse_date(iddict.get('DATE_OF_ISSUE')) != parse_date(formdict.get('Date of issue_a')[0]):
            mismatches.append(f"Date of Issue Mismatch: '{iddict.get('DATE_OF_ISSUE')}' vs '{formdict.get('Date of issue_a')[0]}'")
    else: 
        mismatches.append(f"Date of Issue is not detected in VAF")

    if 'Date of expiry_a' in formdict:
        if parse_date(iddict.get('EXPIRATION_DATE')) != parse_date(formdict.get('Date of expiry_a')[0]):
            mismatches.append(f"Date of Expiry Mismatch: '{iddict.get('EXPIRATION_DATE')}' vs '{formdict.get('Date of expiry_a')[0]}'")
    else: 
        mismatches.append(f"Date of Expiry is not detected in VAF")

    if 'Passport No._a' in formdict:
        if iddict.get('DOCUMENT_NUMBER') != formdict.get('Passport No._a')[0]:
            mismatches.append(f"Passport No. Mismatch: '{iddict.get('DOCUMENT_NUMBER')}' vs '{formdict.get('Passport No._a')[0]}'")
    else:
        mismatches.append(f"Passport No. is not detected in VAF")

    # Return appropriate message
    nomis =['ID matches information in the application form']
    if mismatches:
        return mismatches
    else:
        return nomis
    

def kcompare_dict_values(iddict, formdict):
    mismatches = []

    if 'OF Given Names_a' in formdict:
        if iddict.get('FIRST_NAME').lower() != formdict.get('OF Given Names_a')[0].lower():
            mismatches.append(f"First Name Mismatch: '{iddict.get('FIRST_NAME')}' vs '{formdict.get('OF Given Names_a')[0]}'")
    else:
        mismatches.append(f"Given Name is not detected in VAF")

    if 'NO Family Name_a' in formdict:
        if iddict.get('LAST_NAME').lower() != formdict.get('NO Family Name_a')[0].lower():
            mismatches.append(f"Last Name Mismatch: '{iddict.get('LAST_NAME')}' vs '{formdict.get('NO Family Name_a')[0]}'")
    else:
        mismatches.append(f"Last Name is not detected in VAF")
        
    if '1.4 Date of Birth (yyyy/mm/dd)_a' in formdict:    
        if parse_date(iddict.get('DATE_OF_BIRTH')) != parse_date(formdict.get('1.4 Date of Birth (yyyy/mm/dd)_a')[0]):
            mismatches.append(f"Date of Birth Mismatch: '{iddict.get('DATE_OF_BIRTH')}' vs '{formdict.get('1.4 Date of Birth (yyyy/mm/dd)_a')[0]}'")
    else:
        mismatches.append(f"Date of Birth is not detected in VAF")

    if '3.5 Date of Issue_b' in formdict:
        if parse_date(iddict.get('DATE_OF_ISSUE')) != parse_date(formdict.get('3.5 Date of Issue_b')[0]):
            mismatches.append(f"Date of Issue Mismatch: '{iddict.get('DATE_OF_ISSUE')}' vs '{formdict.get('3.5 Date of Issue_b')[0]}'")
    else: 
        mismatches.append(f"Date of Issue is not detected in VAF")

    if '3.6 Date Of Expiry_b' in formdict:
        if parse_date(iddict.get('EXPIRATION_DATE')) != parse_date(formdict.get('3.6 Date Of Expiry_b')[0]):
            mismatches.append(f"Date of Expiry Mismatch: '{iddict.get('EXPIRATION_DATE')}' vs '{formdict.get('3.6 Date Of Expiry_b')[0]}'")
    else: 
        mismatches.append(f"Date of Expiry is not detected in VAF")

    if '3.2 Passport No._b' in formdict:
        if iddict.get('DOCUMENT_NUMBER') != formdict.get('3.2 Passport No._b')[0]:
            mismatches.append(f"Passport No. Mismatch: '{iddict.get('DOCUMENT_NUMBER')}' vs '{formdict.get('3.2 Passport No._b')[0]}'")
    else:
        mismatches.append(f"Passport No. is not detected in VAF")
    
    # Return appropriate message
    nomis =['ID matches information in the application form']
    if mismatches:
        return mismatches
    else:
        return nomis