import re
import time
from datetime import datetime

from agents.search_agent import SearchAgent
from utils.notification_tracker import NotificationTracker
from ai.gemini_analyzer import analyze_job
from notifications.telegram_notifier import send_telegram_message


CHECK_INTERVAL = 3600
MATCH_SCORE_LIMIT = 70


def get_ai_match_score(ai_result):

    try:
        match = re.search(
            r"MATCH_SCORE:\s*(\d+)",
            ai_result,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

    except Exception as error:
        print(f"❌ Score Parse Error: {error}")

    return 0


def create_job_description(job):

    description = getattr(
        job,
        "description",
        ""
    )

    return f"""
Company: {getattr(job, 'company', 'Unknown')}

Role: {getattr(job, 'title', 'Unknown')}

Location: {getattr(job, 'location', 'Unknown')}

Salary: {getattr(job, 'salary', 'Not Mentioned')}

Job Description:

{description}
"""


def run_job_search():

    print("\n" + "=" * 60)

    print(
        f"🤖 AUTOMATIC JOB SEARCH STARTED"
        f" - {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
    )

    print("=" * 60)

    try:

        search_agent = SearchAgent()

        notification_tracker = NotificationTracker()

        jobs = search_agent.search()

        if len(jobs) == 0:

            print("❌ No Jobs Found")

            return

        matched_jobs = 0
        duplicate_jobs = 0
        analyzed_jobs = 0

        for index, job in enumerate(
            jobs[:10],
            start=1
        ):

            print(
                f"\n🔍 Checking Job {index}/"
                f"{min(10, len(jobs))}"
            )

            print(
                f"🏢 {job.company} - {job.title}"
            )

            job_url = getattr(
                job,
                "apply_url",
                ""
            )

            if notification_tracker.is_notified(
                job_url
            ):

                duplicate_jobs += 1

                print(
                    "🚫 Already Sent to Telegram"
                )

                print(
                    "⏭️ Skipping Duplicate Job"
                )

                continue

            print(
                "🤖 Analyzing with Gemini AI..."
            )

            analyzed_jobs += 1

            job_description = create_job_description(
                job
            )

            ai_result = analyze_job(
                job_description
            )

            if ai_result.startswith("❌"):

                print(ai_result)

                time.sleep(2)

                continue

            match_score = get_ai_match_score(
                ai_result
            )

            print(
                f"🎯 AI Match Score: {match_score}%"
            )

            if match_score >= MATCH_SCORE_LIMIT:

                telegram_message = f"""
🚀 NEW MATCHED JOB

🏢 Company: {job.company}

💼 Role: {job.title}

📍 Location: {job.location}

💰 Salary: {job.salary}

🎯 AI Match Score: {match_score}%

🤖 AI ANALYSIS:

{ai_result}

🔗 APPLY HERE:

{job_url}
"""

                notification_sent = (
                    send_telegram_message(
                        telegram_message
                    )
                )

                if notification_sent:

                    notification_tracker.mark_notified(
                        job_url
                    )

                    matched_jobs += 1

                    print(
                        "📲 Job Sent to Telegram"
                    )

                    print(
                        "💾 Saved in Duplicate Tracker"
                    )

            else:

                print(
                    "⏭️ Job Skipped - Low Match"
                )

            time.sleep(2)

        print("\n" + "=" * 60)

        print("✅ AUTOMATIC JOB SEARCH COMPLETED")

        print(
            f"🤖 Jobs Analyzed: {analyzed_jobs}"
        )

        print(
            f"🚫 Duplicates Skipped: {duplicate_jobs}"
        )

        print(
            f"🎯 New Matched Jobs: {matched_jobs}"
        )

        print("=" * 60)

    except Exception as error:

        print(
            f"❌ Scheduler Error: {error}"
        )


def main():

    print("\n🤖 AI JOB AGENT SCHEDULER STARTED")

    print("⏰ Job Search Interval: 1 Hour")

    print(
        "⚠️ Keep this terminal running\n"
    )

    while True:

        run_job_search()

        print(
            "\n😴 Bot Sleeping for 1 Hour..."
        )

        print(
            "⏰ Next job search will run automatically."
        )

        time.sleep(
            CHECK_INTERVAL
        )


if __name__ == "__main__":

    main()