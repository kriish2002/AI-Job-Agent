class JobFilter:

    TARGET_ROLES = [
        "devops",
        "cloud engineer",
        "cloud infrastructure",
        "azure engineer",
        "azure devops",
        "site reliability",
        "sre engineer",
        "platform engineer",
        "infrastructure engineer",
        "systems engineer",
        "cloud operations",
        "devsecops"
    ]

    def filter_jobs(self, jobs):

        filtered_jobs = []

        for job in jobs:

            title = job.title.lower().strip()

            for role in self.TARGET_ROLES:

                if role in title:

                    filtered_jobs.append(job)
                    break

        print(
            f"🎯 Profile Matched Jobs : {len(filtered_jobs)}"
        )

        return filtered_jobs