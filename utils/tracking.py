import csv
import os
import datetime
import re


def save_cover_letter_file(job_title, agency_name, cover_letter):

    directory = "data/cover_letters"

    os.makedirs(directory, exist_ok=True)

    safe_job = re.sub(r'[^a-zA-Z0-9_]', '_', job_title)
    safe_agency = re.sub(r'[^a-zA-Z0-9_]', '_', agency_name)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{safe_job}_{safe_agency}_{timestamp}.txt"

    file_path = os.path.join(directory, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    return file_path


def log_application(job_title, agency, resume_summary, filepath="data/applications_log.csv"):

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    exists = os.path.exists(filepath)

    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:

        writer = csv.writer(csvfile)

        if not exists:
            writer.writerow([
                "Job Title",
                "Agency",
                "ResumeSummary",
                "DateApplied"
            ])

        writer.writerow([
            job_title.strip(),
            agency.strip(),
            resume_summary.strip()[:150],
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])