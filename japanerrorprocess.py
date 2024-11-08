import re

countries = ["afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda", "argentina", "armenia", 
            "australia", "austria", "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", 
            "belize", "benin", "bhutan", "bolivia", "bosnia and herzegovina", "botswana", "brazil", "brunei", "bulgaria", 
            "burkina faso", "burundi", "cabo verde", "cambodia", "cameroon", "canada", "central african republic", "chad", 
            "chile", "china", "colombia", "comoros", "congo", "costa rica", "croatia", "cuba", "cyprus", "czech republic", 
            "democratic republic of the congo", "denmark", "djibouti", "dominica", "dominican republic", "ecuador", "egypt", 
            "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji", "finland", "france", 
            "gabon", "gambia", "georgia", "germany", "ghana", "greece", "grenada", "guatemala", "guinea", "guinea-bissau", 
            "guyana", "haiti", "honduras", "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland", "israel", 
            "italy", "ivory coast", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "kuwait", "kyrgyzstan", 
            "laos", "latvia", "lebanon", "lesotho", "liberia", "libya", "liechtenstein", "lithuania", "luxembourg", 
            "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania", "mauritius", 
            "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar", 
            "namibia", "nauru", "nepal", "netherlands", "new zealand", "nicaragua", "niger", "nigeria", "north korea", 
            "north macedonia", "norway", "oman", "pakistan", "palau", "palestine", "panama", "papua new guinea", "paraguay", 
            "peru", "philippines", "poland", "portugal", "qatar", "romania", "russia", "rwanda", "saint kitts and nevis", 
            "saint lucia", "saint vincent and the grenadines", "samoa", "san marino", "sao tome and principe", "saudi arabia", 
            "senegal", "serbia", "seychelles", "sierra leone", "singapore", "slovakia", "slovenia", "solomon islands", 
            "somalia", "south africa", "south korea", "south sudan", "spain", "sri lanka", "sudan", "suriname", "sweden", 
            "switzerland", "syria", "taiwan", "tajikistan", "tanzania", "thailand", "timor-leste", "togo", "tonga", 
            "trinidad and tobago", "tunisia", "turkey", "turkmenistan", "tuvalu", "uganda", "ukraine", "united arab emirates", 
            "united kingdom", "united states", "uruguay", "uzbekistan", "vanuatu", "vatican city", "venezuela", "vietnam", 
            "yemen", "zambia", "zimbabwe"]
nationalities = ["afghan", "albanian", "algerian", "american", "andorran", "angolan", "antiguan", "argentine", "armenian", "australian", "austrian", "azerbaijani", "bahamian", "bahraini", "bangladeshi", "barbadian", "belarusian", "belgian", "belizean", "beninese", "bhutanese", "bolivian", "bosnian", "botswanan", "brazilian", "british", "bruneian", "bulgarian", "burkinabe", "burmese", "burundian", "cambodian", "cameroonian", "canadian", "cape verdean", "central african", "chadian", "chilean", "chinese", "colombian", "comoran", "congolese", "costa rican", "croatian", "cuban", "cypriot", "czech", "danish", "djiboutian", "dominican", "dutch", "east timorese", "ecuadorian", "egyptian", "emirian", "equatorial guinean", "eritrean", "estonian", "ethiopian", "fijian", "filipino", "finnish", "french", "gabonese", "gambian", "georgian", "german", "ghanaian", "greek", "grenadian", "guatemalan", "guinean", "guyanese", "haitian", "honduran", "hungarian", "icelandic", "indian", "indonesian", "iranian", "iraqi", "irish", "israeli", "italian", "ivorian", "jamaican", "japanese", "jordanian", "kazakhstani", "kenyan", "kiribati", "korean", "kuwaiti", "kyrgyz", "laotian", "latvian", "lebanese", "lesothan", "liberian", "libyan", "liechtensteiner", "lithuanian", "luxembourgish", "macedonian", "malagasy", "malawian", "malaysian", "maldivian", "malian", "maltese", "marshallese", "mauritanian", "mauritian", "mexican", "micronesian", "moldovan", "monacan", "mongolian", "montenegrin", "moroccan", "mozambican", "namibian", "nauruan", "nepalese", "new zealander", "nicaraguan", "nigerian", "nigerien", "norwegian", "omani", "pakistani", "palauan", "palestinian", "panamanian", "papua new guinean", "paraguayan", "peruvian", "polish", "portuguese", "qatari", "romanian", "russian", "rwandan", "saint kitts and nevis", "saint lucian", "saint vincent and the grenadines", "samoan", "san marinese", "sao tomean", "saudi", "senegalese", "serbian", "seychellois", "sierra leonean", "singaporean", "slovak", "slovenian", "solomon islander", "somali", "south african", "south sudanese", "spanish", "sri lankan", "sudanese", "surinamese", "swazi", "swedish", "swiss", "syrian", "tajik", "tanzanian", "thai", "togolese", "tongan", "trinidadian and tobagonian", "tunisian", "turkish", "turkmen", "tuvaluan", "ugandan", "ukrainian", "uruguayan", "uzbek", "vanuatuan", "vatican", "venezuelan", "vietnamese", "yemeni", "zambian", "zimbabwean"]


def japanep(data_dict, sig):
    errors = []

    if 'Surname (as shown in passport)_a' in data_dict:
        name_info = data_dict['Surname (as shown in passport)_a']
        name = str(name_info[0])  # Assuming the value is in a list
        confidence = name_info[1]  # Confidence score

        error_message = ""
        if not name.replace(' ', '').isalpha():
            error_message += "Surname should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Surname Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Surname not detected in the form")

    if 'Given and middle names (as shown in passport)_a' in data_dict:
        name_info = data_dict['Given and middle names (as shown in passport)_a']
        name = str(name_info[0])  # Assuming the value is in a list
        confidence = name_info[1]  # Confidence score

        error_message = ""
        if not name.replace(' ', '').isalpha():
            error_message += "Given and middle names should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Given and middle names Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Given Names not detected in the form")

    if 'Date of birth_a' in data_dict:
        dob_info = data_dict['Date of birth_a']
        birthdate = str(dob_info[0])
        confidence = dob_info[1]
        error_message = ""
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', birthdate):
            error_message += "Date of birth should be in DD/MM/YYYY format. "
        else:
            day, month, year = map(int, birthdate.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2024): 
                error_message += "Invalid date of birth."
        if confidence < 85:
            error_message += "Date of birth Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Date of Birth not detected in the form")

    if '(Country)_a' in data_dict:
        country_info = data_dict['(Country)_a']
        country = str(country_info[0])  # Assuming the value is in a list
        confidence = country_info[1]  # Confidence score

        error_message = ""
        if country.rstrip().lower() not in countries:
            error_message += "Invalid Country on Place of birth. "
        if confidence < 85:
            error_message += "Country of Birth Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Country of birth not detected in the form")

    if 'Nationality or citizenship_a' in data_dict:
        nationality_info = data_dict['Nationality or citizenship_a']
        nationality = str(nationality_info[0])  # Assuming the value is in a list
        confidence = nationality_info[1]  # Confidence score

        error_message = ""
        if nationality.rstrip().lower() not in countries:
            error_message += "Invalid Country on Nationality. "
        if confidence < 85:
            error_message += "Country of Nationality Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Country of Nationality not detected in the form")

    # Check if both 'Male_a' and 'Female_a' keys are present in the data_dict
    if 'Male_a' in data_dict and 'Female_a' in data_dict:
        # Ensure that exactly one of 'Male' or 'Female' is selected (i.e., marked with 'X')
        if not ((data_dict['Male_a'][0] == 'X' and data_dict['Female_a'][0] == '') or 
                (data_dict['Male_a'][0] == '' and data_dict['Female_a'][0] == 'X')):
            errors.append("Exactly one of 'Male' or 'Female' must be selected")
    else:
        errors.append("Gender Selection not detected in the form")


    status_keys = ['Married_a', 'Single_a', 'Widowed_a', 'Divorced_a']
    # Check if all civil status keys are present in the data_dict
    if all(key in data_dict for key in status_keys):
        # Check if exactly one status is selected (i.e., marked with 'X')
        if sum(data_dict[key][0] == 'X' for key in status_keys) != 1:
            errors.append("Exactly one of 'Single', 'Married', 'Widowed', or 'Divorced' must be selected")
    else:
        errors.append("Civil Status not detected in the form")


    if 'ID No. issued to you by your government_a' in data_dict:
        id_number_info = data_dict['ID No. issued to you by your government_a']
        id_number = str(id_number_info[0])  # Assuming the value is in a list
        confidence = id_number_info[1]

        error_message = ""
        try:
            int(id_number)  # Check if id_number is an integer
        except ValueError:
            # If conversion fails, check for 'N/A' or 'NA'
            if id_number.upper() in ['N/A', 'NA']:
                pass  # ID number is valid as 'N/A' or 'NA'
            else:
                error_message += "ID number must be an integer, 'N/A', or 'NA'"
        if confidence < 85:
            error_message += "ID Number Confidence Level below 85%."

        if error_message: 
            errors.append(error_message.strip())
    else:
        errors.append("ID number not detected in the form")

    passport_keys = ['Diplomatic_a', 'Official_a', 'Ordinary_a', 'Other_a']

    # Check if all passport keys are present in the data_dict
    if all(key in data_dict for key in passport_keys):
        # Check if exactly one of the options is selected (i.e., marked with 'X')
        if sum(data_dict[key][0] == 'X' for key in passport_keys) != 1:
            errors.append("Exactly one Passport Type must be selected")
    else:
        errors.append("Passport type not detected in the form")


    if 'Date of issue_a' in data_dict:
        issue_info = data_dict['Date of issue_a']
        date_of_issue = str(issue_info[0])  # Assuming the value is in a list
        confidence_issue = issue_info[1]
        error_message = ""

        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_of_issue):
            errors.append("Date of issue should be in DD/MM/YYYY format")
        else:
            # Validate if it's a real date
            day, month, year = map(int, date_of_issue.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2024):
                error_message += "Invalid date of issue"
        if confidence_issue < 85:
            error_message += "Date of issue Confidence Level below 85%. "

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Date of issue not detected in the form")

    if 'Date of expiry_a' in data_dict:
        expiry_info = data_dict['Date of expiry_a']
        date_of_expiry = str(expiry_info[0])  # Assuming the value is in a list
        confidence_expiry = expiry_info[1]
        error_message = ""

        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date_of_expiry):
            errors.append("Date of expiry should be in DD/MM/YYYY format")
        else:
            # Validate if it's a real date
            day, month, year = map(int, date_of_expiry.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2040):
                error_message += "Invalid date of expiry"
        if confidence_expiry < 85:
            error_message += "Date of expiry Confidence Level below 85%. "

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Date of expiry not detected in the form")

    if 'Place of issue_a' in data_dict:
        place_info = data_dict['Place of issue_a']
        place = str(place_info[0])  # Assuming the value is in a list
        confidence = place_info[1]  # Confidence score

        error_message = ""
        if not place.replace(' ', '').isalpha():
            error_message += "Place of issue should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Place of issue Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Place of issue not detected in the form")

    if 'Issuing authority_a' in data_dict:
        authority_info = data_dict['Issuing authority_a']
        authority = str(authority_info[0])  # Assuming the value is in a list
        confidence = authority_info[1]  # Confidence score

        error_message = ""
        if not authority.replace(' ', '').isalpha():
            error_message += "Issuing authority should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Issuing authority Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Issuing authority not detected in the form")

    if 'Certificate of Eligibility No._a' in data_dict:
        eligibility_info = data_dict['Certificate of Eligibility No._a']
        eligibility_number = str(eligibility_info[0])  # Assuming the value is in a list
        confidence = eligibility_info[1]  # Confidence score

        error_message = ""
        try:
            int(eligibility_number)
        except ValueError:
            if eligibility_number.upper() == 'N/A' or eligibility_number.upper() == 'NA':
                # Certificate number is 'N/A' or 'NA'
                pass
            else:
                error_message += "Certificate of Eligibility No. must be an integer, 'N/A', or 'NA'. "
        if confidence < 85:
            error_message += "Certificate of Eligibility No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Certificate of Eligibility not detected in the form")

    if 'Passport No._a' in data_dict:
        passport_info = data_dict['Passport No._a']
        passport_number = str(passport_info[0])  # Assuming the value is in a list
        confidence = passport_info[1]  # Confidence score

        error_message = ""
        if len(passport_number) != 9 or not all(char.isalnum() for char in passport_number):
            error_message += "Passport number must be 9 characters long and contain only letters and numbers. "
        if confidence < 85:
            error_message += "Passport number Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Passport Number not detected in the form")

    if 'Date of arrival in Japan_a' in data_dict:
        date_info = data_dict['Date of arrival in Japan_a']
        date = str(date_info[0])  # Assuming the value is in a list
        confidence = date_info[1]  # Confidence score

        error_message = ""
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            error_message += "Date of arrival should be in DD/MM/YYYY format. "
        else:
            # Validate if it's a real date
            day, month, year = map(int, date.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2040): 
                error_message += "Invalid date of arrival. "

        if confidence < 85:
            error_message += "Date of arrival Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Date of arrival not detected in the form")

    if 'Intended length of stay in Japan_a' in data_dict:
        length_info = data_dict['Intended length of stay in Japan_a']
        length = str(length_info[0])  # Assuming the value is in a list
        confidence = length_info[1]  # Confidence score

        error_message = ""
        if not length.replace(' ', '').isalpha():
            error_message += "Length of stay should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Length of stay Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Length of stay not detected in the form")

    if 'Port of entry into Japan_a' in data_dict:
        port_info = data_dict['Port of entry into Japan_a']
        port = str(port_info[0])  # Assuming the value is in a list
        confidence = port_info[1]  # Confidence score

        error_message = ""
        if not port.replace(' ', '').isalpha():
            error_message += "Port of entry should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Port of entry Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Port of entry not detected in the form")

    if 'Name of ship or airline_a' in data_dict:
        airline_info = data_dict['Name of ship or airline_a']
        airline_name = str(airline_info[0])  # Assuming the value is in a list
        confidence = airline_info[1]  # Confidence score

        error_message = ""
        if not airline_name.replace(' ', '').isalpha():
            error_message += "Ship/Airline should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Name of ship or airline Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Name of ship/airline not detected in the form")

    if 'Name_a' in data_dict:
        name_info = data_dict['Name_a']
        name = str(name_info[0])  # Assuming the value is in a list
        confidence = name_info[1]  # Confidence score

        error_message = ""
        if not name.replace(' ', '').isalpha():
            error_message += "Name should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Name Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Name 1 not detected in the form")

    if 'Name2_a' in data_dict:
        name2_info = data_dict['Name2_a']
        name2 = str(name2_info[0])  # Assuming the value is in a list
        confidence = name2_info[1]  # Confidence score

        error_message = ""
        if not name2.replace(' ', '').isalpha():
            error_message += "Name 2 should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Name 2 Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Name 2 not detected in the form")

    if 'Address_a' in data_dict:
        address_info = data_dict['Address_a']
        address = str(address_info[0])  # Assuming the value is in a list
        confidence = address_info[1]  # Confidence score

        error_message = ""
        if not address.replace(' ', '').isalpha():
            error_message += "Address should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Address Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the addresses not detected in the form")

    if 'Address2_a' in data_dict:
        address2_info = data_dict['Address2_a']
        address2 = str(address2_info[0])  # Assuming the value is in a list
        confidence = address2_info[1]  # Confidence score

        error_message = ""
        if not address2.replace(' ', '').isalpha():
            error_message += "Address 2 should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Address 2 Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the addresses not detected in the form")

    if 'Address3_a' in data_dict:
        address3_info = data_dict['Address3_a']
        address3 = str(address3_info[0])  # Assuming the value is in a list
        confidence = address3_info[1]  # Confidence score

        error_message = ""
        if not address3.replace(' ', '').isalpha():
            error_message += "Address 3 should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Address 3 Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the addresses not detected in the form")

    if 'Tel._a' in data_dict:
        tel_info = data_dict['Tel._a']
        telno = str(tel_info[0])  # Assuming the value is in a list
        confidence = tel_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Tel. must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Tel No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the Tel No. not detected in the form")

    if 'Tel.2_a' in data_dict:
        tel2_info = data_dict['Tel.2_a']
        telno = str(tel2_info[0])  # Assuming the value is in a list
        confidence = tel2_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Tel. 2 must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Tel No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the Tel No. not detected in the form")

    if 'Tel.3_a' in data_dict:
        tel3_info = data_dict['Tel.3_a']
        telno = str(tel3_info[0])  # Assuming the value is in a list
        confidence = tel3_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Tel. 3 must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Tel No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("One of the Tel No. not detected in the form")

    if 'Mobile No._a' in data_dict:
        mobile_info = data_dict['Mobile No._a']
        telno = str(mobile_info[0])  # Assuming the value is in a list
        confidence = mobile_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Mobile No. must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Mobile No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Mobile No. not detected in the form")

    if 'E-Mail_a' in data_dict:
        email_info = data_dict['E-Mail_a']
        email = str(email_info[0])  # Assuming the value is in a list
        confidence = email_info[1]  # Confidence score

        error_message = ""
        if '@' not in email or email.count('@') != 1:
            error_message += "Invalid email address. "
        if confidence < 85:
            error_message += "Email Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("E-Mail not detected in the form")

    if 'Current profession or occupation and position_a' in data_dict:
        profession_info = data_dict['Current profession or occupation and position_a']
        profession = str(profession_info[0])  # Assuming the value is in a list
        confidence = profession_info[1]  # Confidence score

        error_message = ""
        if not profession.replace(' ', '').isalpha():
            error_message += "Profession should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Profession Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Profession not detected in the form")

    if 'Date of application_b' in data_dict:
        date_info = data_dict['Date of application_b']
        date = str(date_info[0])  # Assuming the value is in a list
        confidence = date_info[1]  # Confidence score

        error_message = ""
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', date):
            error_message += "Date of application should be in DD/MM/YYYY format. "
        else:
            # Validate if it's a real date
            day, month, year = map(int, date.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2040):
                error_message += "Invalid date of application. "
        if confidence < 85:
            error_message += "Date of Application Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Date of Application not detected in the form")

    if 'Name_b' in data_dict:
        name_info = data_dict['Name_b']
        name = str(name_info[0])  # Assuming the value is in a list
        confidence = name_info[1]  # Confidence score

        error_message = ""
        if not name.replace(' ', '').isalpha():
            error_message += "Guarantor Name should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Guarantor Name Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Guarantor Name not detected in the form")

    if 'Name2_b' in data_dict:
        name2_info = data_dict['Name2_b']
        name = str(name2_info[0])  # Assuming the value is in a list
        confidence = name2_info[1]  # Confidence score

        error_message = ""
        if not name.replace(' ', '').isalpha():
            error_message += "Inviter Name should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Inviter Name Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Inviter name not detected in the form")

    if 'Tel._b' in data_dict:
        tel_info = data_dict['Tel._b']
        telno = str(tel_info[0])  # Assuming the value is in a list
        confidence = tel_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Guarantor Tel No. must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Guarantor Tel No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Guarantor Tel No. not detected in the form")

    if 'Tel.2_b' in data_dict:
        tel2_info = data_dict['Tel.2_b']
        telno = str(tel2_info[0])  # Assuming the value is in a list
        confidence = tel2_info[1]  # Confidence score

        error_message = ""
        if telno.lower() not in ['n/a', 'na']:
            try:
                int(telno)
            except ValueError:
                error_message += "Inviter Tel No. must be an integer or 'N/A' or 'NA'. "
        if confidence < 85:
            error_message += "Inviter Tel No. Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Inviter Tel No. not detected in the form")

    if 'Address_b' in data_dict:
        address_info = data_dict['Address_b']
        address = str(address_info[0])  # Assuming the value is in a list
        confidence = address_info[1]  # Confidence score

        error_message = ""
        if not address.replace(' ', '').isalpha():
            error_message += "Guarantor Address should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Guarantor Address Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Guarantor Address not detected in the form")

    if 'Address2_b' in data_dict:
        address2_info = data_dict['Address2_b']
        address = str(address2_info[0])  # Assuming the value is in a list
        confidence = address2_info[1]  # Confidence score

        error_message = ""
        if not address.replace(' ', '').isalpha():
            error_message += "Inviter Address should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Inviter Address Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Inviter Address not detected in the form")

    if 'Date of birth_b' in data_dict:
        birthdate_info = data_dict['Date of birth_b']
        birthdate = str(birthdate_info[0])  # Assuming the value is in a list
        confidence = birthdate_info[1]  # Confidence score

        error_message = ""
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', birthdate):
            error_message += "Guarantor Date of birth should be in DD/MM/YYYY format. "
        else:
            # Validate if it's a real date
            day, month, year = map(int, birthdate.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2024):
                error_message += "Invalid Guarantor date of birth."
        if confidence < 85:
            error_message += "Guarantor Date of Birth Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Guarantor Date of Birth not detected in the form")

    if 'Date of birth2_b' in data_dict:
        birthdate2_info = data_dict['Date of birth2_b']
        birthdate = str(birthdate2_info[0])  # Assuming the value is in a list
        confidence = birthdate2_info[1]  # Confidence score

        error_message = ""
        if not re.match(r'^\d{2}/\d{2}/\d{4}$', birthdate):
            error_message += "Inviter Date of birth should be in DD/MM/YYYY format. "
        else:
            # Validate if it's a real date
            day, month, year = map(int, birthdate.split('/'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2024):
                error_message += "Invalid Inviter date of birth. "
        if confidence < 85:
            error_message += "Inviter Date of Birth Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Inviter Date of Birth not detected in the form")

    # Checking Relationship to Applicant
    if 'Relationship to applicant_b' in data_dict:
        relationship_info = data_dict['Relationship to applicant_b']
        relationship = str(relationship_info[0])  # Assuming the value is in a list
        confidence = relationship_info[1]  # Confidence score

        error_message = ""
        if not relationship.replace(' ', '').isalpha():
            error_message += "Relationship to Guarantor should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Relationship to Guarantor Confidence Level below 85%."

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Relationship to Guarantor not detected in the form")

    # Checking Relationship to Applicant 2
    if 'Relationship to applicant2_b' in data_dict:
        relationship2_info = data_dict['Relationship to applicant2_b']
        relationship = str(relationship2_info[0])  # Assuming the value is in a list
        confidence = relationship2_info[1]  # Confidence score

        error_message = ""
        if not relationship.replace(' ', '').isalpha():
            error_message += "Relationship to Inviter should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Relationship to Inviter Confidence level below 85%. "

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Relationship to Inviter not detected in the form")

    # Checking Guarantor's Profession
    if 'Profession or occupation and position_b' in data_dict:
        profession_info = data_dict['Profession or occupation and position_b']
        profession = str(profession_info[0])  # Assuming the value is in a list
        confidence = profession_info[1]  # Confidence score

        error_message = ""
        if not profession.replace(' ', '').isalpha():
            error_message += "Guarantor's Profession should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Guarantor's Profession Confidence Level below 85%. "

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Guarantor's Profession not detected in the form")

    # Checking Inviter's Profession
    if 'Profession or occupation and position2_b' in data_dict:
        profession2_info = data_dict['Profession or occupation and position2_b']
        profession = str(profession2_info[0])  # Assuming the value is in a list
        confidence = profession2_info[1]  # Confidence score

        error_message = ""
        if not profession.replace(' ', '').isalpha():
            error_message += "Inviter's Profession should contain only letters and spaces. "
        if confidence < 85:
            error_message += "Inviter's Profession Confidence Level below 85%. "

        if error_message:
            errors.append(error_message.strip())
    else:
        errors.append("Inviter's Profession not detected in the form")

    # Checking Guarantor's Nationality
    if 'Nationality and immigration status_b' in data_dict:
        nationality_info = data_dict['Nationality and immigration status_b']
        nationality = str(nationality_info[0])  # Assuming the value is in a list
        confidence = nationality_info[1]  # Confidence score

        if nationality.rstrip().lower() not in nationalities:
            errors.append("Invalid Guarantor's Nationality.")
        if confidence < 85:
            errors.append("Guarantor's Nationality Confidence Level below 85%.")
    else:
        errors.append("Guarantor's Nationality not detected in the form")

    # Checking Inviter's Nationality
    if 'Nationality and immigration status2_b' in data_dict:
        nationality2_info = data_dict['Nationality and immigration status2_b']
        nationality = str(nationality2_info[0])  # Assuming the value is in a list
        confidence = nationality2_info[1]  # Confidence score

        if nationality.rstrip().lower() not in nationalities:
            errors.append("Invalid Inviter's Nationality")
        if confidence < 85:
            errors.append("Inviter's Nationality COnfidence Level below 85%.")
    else:
        errors.append("Inviter's Nationality not detected in the form")


    # Define a list of the Male/Female key pairs to check, along with custom error messages
    gender_keys = [
        ('Male_b', 'Female_b', "Guarantor's gender not detected in the form", "Exactly one of 'Male' or 'Female' in page 2 must be selected"),
        ('Male2_b', 'Female2_b', "Inviter's gender not detected in the form", "Exactly one of 'Male' or 'Female' in page 2 must be selected")
    ]

    for male_key, female_key, not_detected_msg, selection_error_msg in gender_keys:
        if male_key in data_dict and female_key in data_dict:
            male_value = data_dict.get(male_key, [''])[0]
            female_value = data_dict.get(female_key, [''])[0]

            # Check if exactly one is selected
            if not ((male_value == 'X' and female_value == '') or (male_value == '' and female_value == 'X')):
                errors.append(selection_error_msg)
        else:
            errors.append(not_detected_msg)


    # Define a list of the Yes/No key pairs to check
    yes_no_keys = [
        ('Yes_b', 'No_b'),
        ('Yes2_b', 'No2_b'),
        ('Yes3_b', 'No3_b'),
        ('Yes4_b', 'No4_b'),
        ('Yes5_b', 'No5_b'),
        ('Yes6_b', 'No6_b')
    ]

    for yes_key, no_key in yes_no_keys:
        if yes_key in data_dict and no_key in data_dict:
            yes_value = data_dict.get(yes_key, [''])[0]
            no_value = data_dict.get(no_key, [''])[0]

            # Check if exactly one is selected
            if not ((yes_value == 'X' and no_value == '') or (yes_value == '' and no_value == 'X')):
                errors.append(f"Exactly one of '{yes_key}' or '{no_key}' must be selected")
        else:
            errors.append(f"One of the checklists ({yes_key} or {no_key}) not detected in the form")


    if any(data_dict.get(key, [None])[0] == 'X' for key in ['Yes_b', 'Yes2_b', 'Yes3_b', 'Yes4_b', 'Yes5_b', 'Yes6_b']):
        if not data_dict.get('If you answered "Yes" to any of the above questions, please provide relevant details._b', [None])[0]:
            errors.append("Optional field cannot be empty if at least one Yes is selected")

    if 'Signature' in sig:
        sign = sig['Signature']
        if not sign == 'Detected':
            errors.append("No signature is detected in the form")
    else:
        errors.append("Signature not detected in the form")

    validform = ['Form is complete and valid']

    if errors:
        return errors
    else:
        return validform


