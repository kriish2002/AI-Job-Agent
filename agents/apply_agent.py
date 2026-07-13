import webbrowser

from utils.application_tracker import ApplicationTracker
from utils.resume_reader import ResumeReader
from utils.resume_matcher import ResumeMatcher

from agents.eligibility_agent import EligibilityAgent


class ApplyAgent:

    def __init__(self):

        self.tracker = ApplicationTracker()

        self.resume_reader = ResumeReader()

        self.resume_matcher = ResumeMatcher()

        self.eligibility_agent = EligibilityAgent()

    def apply(self, jobs):

        if not jobs:

            print("\n❌ No Jobs Available")

            return

        print("\n📄 Loading Resume...")

        resume_text = self.resume_reader.read()

        if not resume_text:

            print(
                "\n❌ Resume could not be loaded"
            )

            return

        print(
            "\n🤖 Calculating Resume Match Scores..."
        )

        scored_jobs = []

        for job in jobs:

            if self.tracker.is_applied(job):

                continue

            match_result = self.resume_matcher.match(
                resume_text,
                job
            )

            score = match_result.get(
                "score",
                0
            )

            scored_jobs.append({
                "job": job,
                "score": score
            })

        scored_jobs.sort(
            key=lambda item: item["score"],
            reverse=True
        )

        print(
            "\n🧠 AI Checking Job Eligibility...\n"
        )

        eligible_jobs = []

        for item in scored_jobs[:10]:

            job = item["job"]

            score = item["score"]

            print(
                f"🔍 Checking : "
                f"{job.company} - {job.title}"
            )

            result = self.eligibility_agent.check(
                resume_text,
                job
            )

            if result["eligible"]:

                print(
                    f"✅ ELIGIBLE : "
                    f"{result['reason']}"
                )

                eligible_jobs.append({
                    "job": job,
                    "score": score,
                    "reason": result["reason"]
                })

            else:

                print(
                    f"❌ REJECTED : "
                    f"{result['reason']}"
                )

        if not eligible_jobs:

            print(
                "\n❌ No Eligible Jobs Found"
            )

            return

        print("\n🤖 SAFE APPLY MODE\n")

        for index, item in enumerate(
            eligible_jobs,
            start=1
        ):

            job = item["job"]

            score = item["score"]

            reason = item["reason"]

            print("=" * 60)

            print(
                f"Job #{index}"
            )

            print(
                f"🏢 Company : {job.company}"
            )

            print(
                f"💼 Role    : {job.title}"
            )

            print(
                f"📍 Location: {job.location}"
            )

            print(
                f"🎯 Match   : {score}%"
            )

            print(
                f"🧠 AI Check: {reason}"
            )

            print(
                f"🌍 Source  : {job.source}"
            )

            print(
                f"🔗 Link    : {job.apply_url}"
            )

            choice = input(
                "\n👉 Open this job? (y/n/q): "
            ).strip().lower()

            if choice == "q":

                print(
                    "\n🛑 Apply Mode Stopped"
                )

                break

            if choice != "y":

                print(
                    "\n⏭️ Job Skipped"
                )

                continue

            print(
                "\n🌐 Opening Application..."
            )

            webbrowser.open(
                job.apply_url
            )

            status = input(
                "\n👉 Did you apply successfully? (y/n): "
            ).strip().lower()

            if status == "y":

                self.tracker.save_application(
                    job,
                    status="Applied"
                )

            else:

                save_status = input(
                    "\n👉 Save as skipped? (y/n): "
                ).strip().lower()

                if save_status == "y":

                    self.tracker.save_application(
                        job,
                        status="Skipped"
                    )

        print(
            "\n✅ Safe Apply Session Completed"
        )