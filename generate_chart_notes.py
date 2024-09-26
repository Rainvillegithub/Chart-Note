import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AIRTABLE_PERSONAL_ACCESS_TOKEN = os.getenv('AIRTABLE_PERSONAL_ACCESS_TOKEN')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')
AIRTABLE_API_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

HEADERS = {
    'Authorization': f'Bearer {AIRTABLE_PERSONAL_ACCESS_TOKEN}',
    'Content-Type': 'application/json'
}

def fetch_latest_record():
    """
    Fetch the most recent record based on the Timestamp field.
    """
    # Sort records by Timestamp in descending order and limit to 1
    params = {
        'maxRecords': 1,
        'sort[0][field]': 'Timestamp',   # Assuming there's a 'Timestamp' field
        'sort[0][direction]': 'desc'
    }

    response = requests.get(AIRTABLE_API_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        raise Exception(f"Error fetching records: {response.text}")

    records = response.json().get('records', [])
    if records:
        return records[0]  # Return the single latest record
    else:
        return None

def format_chart_note(record):
    """
    Format a single Airtable record into a chart note.
    """
    fields = record.get('fields', {})
    
    chart_note = f"""
    Patient Information
    - Name: {fields.get('Patient_First', '')} {fields.get('Last_Name', '')}
    - Chart Number: {fields.get('Chart_Number', '')}
    - Provider: {fields.get('Provider', '')}
    - Timestamp: {fields.get('Timestamp', '')}

    Chief Complaint
    - {fields.get('Chief_Complaint_PROBLEM', '')}

    Diagnoses
    1. Primary Diagnosis: {fields.get('1st_DX', '')}
        - {fields.get('1_DX_Comment', '')}
    """

    # Handle optional second diagnosis
    second_dx = fields.get('2nd_DX_if_Applicable', '')
    if second_dx:
        chart_note += f"""
    2. Secondary Diagnosis: {second_dx}
        - {fields.get('2_DX_Comment', '')}
    """

    chart_note += f"""
    Etiology Analysis
    - {fields.get('Etiology_ANALYZE', '')}

    Treatment Offered
    - {fields.get('TREATMENT_Offered', '')}

    Patient Consent
    - {fields.get('What_the_Patient_CONSENTed_To', '')}

    Treatment Plan
    - Short Term (Today to 3 months): {fields.get('Patient_Treatment_ST_Todat_3mo', '')}
    - Medium Term (3 months to 1 year): {fields.get('Patient_Treatment_MT_3mo-1year', '')}
    - Long Term (Over 1 year): {fields.get('Patient_Treatment_LT_over_1year', '')}

    Prognosis and Patient Expectations
    - {fields.get('Prognosis_To_Patient_Expectations', '')}

    Education Provided
    - {fields.get('Education', '')}

    ---
    """
    return chart_note.strip()

def main():
    try:
        record = fetch_latest_record()
        if not record:
            print("No records found.")
            return

        chart_note = format_chart_note(record)
        # Output the chart note to the console
        print(f"--- Chart Note for Record ID: {record.get('id')} ---\n")
        print(chart_note)
        print("\n--- End of Chart Note ---")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()





