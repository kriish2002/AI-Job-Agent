import csv
import os
from datetime import datetime


class ApplicationTracker:

    FILE_PATH = "database/applied_jobs.csv"

    def __init__(self):

        os.makedirs(
            "database",
            exist_ok=True
        )

        self._create_file()

    def _create_file(self):

        if os.path.exists(self.FILE_PATH):
            return

        with open(
            self.FILE_PATH,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Company",
                "Role",
                "Location",
                "Source",
                "Apply URL",
                "Status",
                "Applied Date"
            ])

    def is_applied(self, job):

        if not os.path.exists(self.FILE_PATH):
            return False

        with open(
            self.FILE_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["Apply URL"] == job.apply_url:
                    return True

        return False

    def save_application(
        self,
        job,
        status="Applied"
    ):

        if self.is_applied(job):

            print(
                "\n⚠️ Job already exists in tracker"
            )

            return False

        with open(
            self.FILE_PATH,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                job.company,
                job.title,
                job.location,
                job.source,
                job.apply_url,
                status,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ])

        print(
            "\n💾 Application Saved"
        )

        return True