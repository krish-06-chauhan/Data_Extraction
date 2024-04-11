import pdfplumber
import re
import pandas as pd

def extract_contacts(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})\b'
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    return emails, phones

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            all_text += page_text + "\n"
    return all_text

def process_resumes(pdf_files):
    data = []
    for pdf_file in pdf_files:
        text = extract_text_from_pdf(pdf_file)
        emails, phones = extract_contacts(text)
        data.append({
            "PDF File": pdf_file,
            "Email IDs": emails,
            "Phone Numbers": phones,
            "Text": text
        })
    return data

pdf_files = ["resume1.pdf", "resume2.pdf", "resume3.pdf"]  

resume_data = process_resumes(pdf_files)

df = pd.DataFrame(resume_data)

output_file = "Output_File_Path"
df.to_excel(output_file, index=False)

print(f"Data extracted from resumes has been saved to {output_file}")
