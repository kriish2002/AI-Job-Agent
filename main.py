import re
import time

from app.menu import Menu

from agents.search_agent import SearchAgent
from agents.apply_agent import ApplyAgent

from utils.csv_writer import CSVWriter
from utils.resume_reader import ResumeReader
from utils.resume_matcher import ResumeMatcher
from utils.cover_letter_generator import CoverLetterGenerator
from utils.notification_tracker import NotificationTracker

from ai.gemini_analyzer import analyze_job
from notifications.telegram_notifier import send_telegram_message


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

        print(
            f"❌ Score Parse Error: {error}"
        )

    return 0


def create_job_description(job):

    description = getattr(
        job,
        "description",
        ""
    )

    job_description = f"""
Company: {getattr(job, 'company', 'Unknown')}

Role: {getattr(job, 'title', 'Unknown')}

Location: {getattr(job, 'location', 'Unknown')}

Salary: {getattr(job, 'salary', 'Not Mentioned')}

Job Description:

{description}
"""

    return job_description


def main():

    while True:

        menu = Menu()

        choice = menu.show()

        # ==========================================
        # OPTION 1 - SEARCH JOBS
        # ==========================================

        if choice == "1":

            print(
                "\n🔍 Searching Jobs...\n"
            )

            search_agent = SearchAgent()

            jobs = search_agent.search()

            print(
                f"\n✅ Total Jobs Found : {len(jobs)}\n"
            )

            if len(jobs) == 0:

                print(
                    "❌ No Jobs Found\n"
                )

                continue

            writer = CSVWriter()

            writer.save(jobs)

            for job in jobs[:10]:

                print("=" * 60)

                print(
                    f"🎯 Match    : "
                    f"{getattr(job, 'match_score', 0)}%"
                )

                print(
                    f"🏢 Company  : {job.company}"
                )

                print(
                    f"💼 Role     : {job.title}"
                )

                print(
                    f"📍 Location : {job.location}"
                )

                print(
                    f"💰 Salary   : {job.salary}"
                )

                print(
                    f"🌍 Source   : {job.source}"
                )

                print(
                    f"🔗 Link     : {job.apply_url}"
                )

            print("=" * 60)

        # ==========================================
        # OPTION 2 - RESUME MATCH
        # ==========================================

        elif choice == "2":

            print(
                "\n📄 Loading Resume...\n"
            )

            resume_reader = ResumeReader()

            resume_text = resume_reader.read(
                "resume.pdf"
            )

            if not resume_text:

                print(
                    "❌ Resume could not be loaded"
                )

                continue

            print(
                "\n✅ Resume Successfully Loaded"
            )

            print(
                "\n🔍 Searching Jobs...\n"
            )

            search_agent = SearchAgent()

            jobs = search_agent.search()

            if len(jobs) == 0:

                print(
                    "\n❌ No Jobs Found"
                )

                continue

            resume_matcher = ResumeMatcher()

            print(
                "\n🤖 RESUME MATCH RESULTS\n"
            )

            for job in jobs[:10]:

                result = resume_matcher.match(
                    resume_text,
                    job
                )

                print("=" * 60)

                print(
                    f"🎯 Resume Match : "
                    f"{result.get('score', 0)}%"
                )

                print(
                    f"🏢 Company      : "
                    f"{job.company}"
                )

                print(
                    f"💼 Role         : "
                    f"{job.title}"
                )

                matched_skills = result.get(
                    "matched_skills",
                    []
                )

                missing_skills = result.get(
                    "missing_skills",
                    []
                )

                print(
                    "✅ Matched Skills: "
                    + ", ".join(matched_skills)
                )

                print(
                    "❌ Missing Skills: "
                    + ", ".join(missing_skills)
                )

                print(
                    f"🔗 Apply        : "
                    f"{job.apply_url}"
                )

            print("=" * 60)

        # ==========================================
        # OPTION 3 - AI COVER LETTER
        # ==========================================

        elif choice == "3":

            print(
                "\n🤖 Starting AI Cover Letter Generator..."
            )

            resume_reader = ResumeReader()

            resume_text = resume_reader.read(
                "resume.pdf"
            )

            if not resume_text:

                print(
                    "\n❌ Resume could not be loaded"
                )

                continue

            search_agent = SearchAgent()

            jobs = search_agent.search()

            if len(jobs) == 0:

                print(
                    "\n❌ No Jobs Found"
                )

                continue

            print(
                "\n📋 SELECT JOB\n"
            )

            for index, job in enumerate(
                jobs[:10],
                start=1
            ):

                print(
                    f"{index}. "
                    f"{job.company} - "
                    f"{job.title}"
                )

            try:

                job_choice = int(
                    input(
                        "\n👉 Select Job Number: "
                    )
                )

                if (
                    job_choice < 1
                    or job_choice > min(
                        10,
                        len(jobs)
                    )
                ):

                    print(
                        "\n❌ Invalid Job Number"
                    )

                    continue

            except ValueError:

                print(
                    "\n❌ Please enter a number"
                )

                continue

            selected_job = jobs[
                job_choice - 1
            ]

            resume_matcher = ResumeMatcher()

            match_result = resume_matcher.match(
                resume_text,
                selected_job
            )

            generator = CoverLetterGenerator()

            cover_letter = generator.generate(
                resume_text,
                selected_job,
                match_result
            )

            if not cover_letter:

                print(
                    "\n❌ Cover Letter Generation Failed"
                )

                continue

            print(
                "\n📝 GENERATED COVER LETTER"
            )

            print("=" * 60)

            print(cover_letter)

            print("=" * 60)

            generator.save(
                cover_letter
            )

        # ==========================================
        # OPTION 4 - SAFE APPLY JOBS
        # ==========================================

        elif choice == "4":

            print(
                "\n🤖 Starting Safe Apply Agent..."
            )

            search_agent = SearchAgent()

            jobs = search_agent.search()

            if len(jobs) == 0:

                print(
                    "\n❌ No Matched Jobs Found"
                )

                continue

            apply_agent = ApplyAgent()

            apply_agent.apply(
                jobs
            )

        # ==========================================
        # OPTION 5 - AI TELEGRAM JOB REPORT
        # ==========================================

        elif choice == "5":

            print(
                "\n🤖 Starting AI Telegram Job Report...\n"
            )

            search_agent = SearchAgent()

            notification_tracker = NotificationTracker()

            jobs = search_agent.search()

            if len(jobs) == 0:

                print(
                    "\n❌ No Jobs Found"
                )

                continue

            print(
                f"\n🔍 Checking "
                f"{min(10, len(jobs))} Jobs...\n"
            )

            matched_jobs = 0

            duplicate_jobs = 0

            analyzed_jobs = 0

            for index, job in enumerate(
                jobs[:10],
                start=1
            ):

                print(
                    f"🔍 Checking Job {index}/"
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

                # ==================================
                # DUPLICATE CHECK
                # ==================================

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

                    print("-" * 60)

                    continue

                # ==================================
                # GEMINI AI ANALYSIS
                # ==================================

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

                    print("-" * 60)

                    time.sleep(2)

                    continue

                match_score = get_ai_match_score(
                    ai_result
                )

                print(
                    f"🎯 AI Match Score: {match_score}%"
                )

                # ==================================
                # MATCHED JOB
                # ==================================

                if match_score >= 70:

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
                            "💾 Job Saved in Duplicate Tracker"
                        )

                    else:

                        print(
                            "❌ Telegram Failed"
                        )

                        print(
                            "⚠️ Job NOT Marked as Notified"
                        )

                else:

                    print(
                        "⏭️ Job Skipped - Low Match"
                    )

                print("-" * 60)

                time.sleep(2)

            # ======================================
            # SUMMARY
            # ======================================

            summary_message = f"""
🤖 AI JOB SEARCH COMPLETED

🔍 Jobs Checked: {min(10, len(jobs))}

🤖 New Jobs Analyzed: {analyzed_jobs}

🚫 Duplicate Jobs Skipped: {duplicate_jobs}

🎯 New Matched Jobs: {matched_jobs}

📲 Matching Criteria: 70% or Above

🚀 AI Job Agent Completed
"""

            send_telegram_message(
                summary_message
            )

            print(
                "\n✅ AI Telegram Job Report Completed"
            )

            print(
                f"🤖 Jobs Analyzed: {analyzed_jobs}"
            )

            print(
                f"🚫 Duplicates Skipped: {duplicate_jobs}"
            )

            print(
                f"🎯 New Matched Jobs: {matched_jobs}"
            )

        # ==========================================
        # OPTION 6 - EXIT
        # ==========================================

        elif choice == "6":

            print(
                "\n👋 Goodbye!"
            )

            break

        # ==========================================
        # INVALID OPTION
        # ==========================================

        else:

            print(
                "\n❌ Invalid Choice"
            )


if __name__ == "__main__":

    main()