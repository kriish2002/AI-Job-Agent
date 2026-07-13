import csv
import os


class NotificationTracker:

    def __init__(self):
        self.file_path = "database/notified_jobs.csv"

        self._prepare_file()

    def _prepare_file(self):

        os.makedirs(
            os.path.dirname(self.file_path),
            exist_ok=True
        )

        if (
            not os.path.exists(self.file_path)
            or os.path.getsize(self.file_path) == 0
        ):

            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "job_url"
                ])

            return

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            first_line = file.readline().strip()

        if first_line != "job_url":

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                old_urls = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]

            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "job_url"
                ])

                for job_url in old_urls:

                    writer.writerow([
                        job_url
                    ])

    def is_notified(self, job_url):

        if not job_url:
            return False

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for row in reader:

                    saved_url = row.get(
                        "job_url",
                        ""
                    ).strip()

                    if saved_url == job_url.strip():
                        return True

        except Exception as error:

            print(
                f"❌ Notification Tracker Error: {error}"
            )

        return False

    def mark_notified(self, job_url):

        if not job_url:
            return

        if self.is_notified(job_url):
            return

        try:

            with open(
                self.file_path,
                "a",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    job_url.strip()
                ])

        except Exception as error:

            print(
                f"❌ Notification Save Error: {error}"
            )