import gspread
from oauth2client.service_account import ServiceAccountCredentials


# AUTH
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "db/credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1koTckEkFB0E1lSbmgLL5kvT3b-O4tB6n2V0yLnV2cig"
).sheet1


# ✅ CLEAR + HEADER
def clear_sheet():
    sheet.clear()
    sheet.append_row([
        "Company Name",
        "Website",
        "Tech Stack",
        "Hiring Detected (Y/N)",
        "QA Signals (Y/N)",
        "Product Type",
        "Pain Point",
        "Personalization Line",
        "Lead Score",
        "Status",
        "Follow-up Date",
        "Notes"
    ])


# ✅ SAVE DATA
def save_bulk_to_sheet(results):
    rows = []

    for r in results:
        try:
            row = [
                r.get("Company Name", ""),
                r.get("Website", ""),
                r.get("Tech Stack", ""),
                r.get("Hiring Detected", ""),
                r.get("QA Signals", ""),
                r.get("Product Type", ""),
                r.get("Pain Point", ""),
                r.get("Personalization Line", ""),
                r.get("Lead Score", ""),

                # extra columns
                "Not Contacted",
                "",
                ""
            ]
            rows.append(row)

        except Exception as e:
            print("ROW ERROR:", e)

    print("ROWS TO INSERT:", len(rows))  # 🔥 DEBUG

    if rows:
        sheet.append_rows(rows)
        print("SHEET UPDATED")
    else:
        print("NO DATA TO INSERT")