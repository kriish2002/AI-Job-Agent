import re


class JobScorer:

    SKILLS = {
        "devops": 15,
        "azure": 10,
        "terraform": 10,
        "kubernetes": 8,
        "docker": 8,
        "ci/cd": 8,
        "jenkins": 5,
        "linux": 5,
        "github actions": 5,
        "azure devops": 10
    }

    TARGET_ROLES = {
        "devops engineer": 30,
        "azure devops": 30,
        "cloud engineer": 30,
        "platform engineer": 25,
        "site reliability": 25,
        "sre engineer": 25,
        "infrastructure engineer": 20,
        "devsecops": 30
    }

    GOOD_LEVELS = [
        "junior",
        "associate",
        "entry level",
        "entry-level"
    ]

    REJECT_LEVELS = [
        "senior",
        "sr.",
        "sr ",
        "principal",
        "staff",
        "lead",
        "manager",
        "director",
        "architect",
        "head of",
        "vp "
    ]

    GOOD_LOCATIONS = [
        "india",
        "worldwide",
        "anywhere",
        "global",
        "remote"
    ]

    def calculate_score(self, job):

        score = 0

        title = job.title.lower().strip()
        description = job.description.lower()
        location = job.location.lower()

        full_text = f"{title} {description}"

        # Hard reject senior roles

        for level in self.REJECT_LEVELS:

            if level in title:
                job.score = 0
                return job

        # Target role score

        role_matched = False

        for role, points in self.TARGET_ROLES.items():

            if role in title:
                score += points
                role_matched = True
                break

        # Reject unrelated roles

        if not role_matched:
            job.score = 0
            return job

        # Skill score

        for skill, points in self.SKILLS.items():

            if skill in full_text:
                score += points

        # Junior bonus

        for level in self.GOOD_LEVELS:

            if level in title:
                score += 15
                break

        # Location bonus

        for good_location in self.GOOD_LOCATIONS:

            if good_location in location:
                score += 10
                break

        # Experience check

        experience_matches = re.findall(
            r"(\d+)\+?\s*(?:years|year|yrs|yr)",
            description
        )

        if experience_matches:

            experience_numbers = [
                int(number)
                for number in experience_matches
            ]

            minimum_experience = min(experience_numbers)

            if minimum_experience <= 2:
                score += 15

            elif minimum_experience == 3:
                score += 10

            elif minimum_experience >= 5:
                job.score = 0
                return job

        score = max(0, min(score, 100))

        job.score = score

        return job