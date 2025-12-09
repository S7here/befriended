import re
import pdfplumber

def extract_allotment_data(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    text = text.upper()
    print("RAW TEXT:", text)  # DEBUG

    data = {}

    # 1. Counselling ID
    m = re.search(r"COLLEGE ALLOTTED\s*\n\s*(\d{4})-", text)
    if m:
        data["counselling_id"] = int(m.group(1))

    # 2. Application Number
    m = re.search(r"APPLICATION NO\.\s*(\d+)", text)
    if m:
        data["application_no"] = m.group(1)

    # 3. Admission Number
    m = re.search(r"ADMISSION NO\.\s*([\w/]+)", text)
    if m:
        data["admission_no"] = m.group(1)

    # 4. Department
    m = re.search(r"BRANCH ALLOTTED\s+([A-Z]+)-([A-Za-z ]+)", text)
    if m:
        data["branch_code"] = m.group(1)
        data["department"] = m.group(2).strip()

    return data
