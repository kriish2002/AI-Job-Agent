import os
import pandas as pd


class CSVWriter:

    def save(self, jobs):

        data = []

        for job in jobs:

            data.append({
                "Match Score": f"{job.score}%",
                "Company": job.company,
                "Role": job.title,
                "Location": job.location,
                "Salary": job.salary,
                "Source": job.source,
                "Link": job.apply_url
            })

        df = pd.DataFrame(data)

        os.makedirs(
            "database",
            exist_ok=True
        )

        file_path = "database/jobs.csv"

        df.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        print(
            f"\n💾 Jobs Saved : {file_path}"
        )