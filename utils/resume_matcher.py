import re


class ResumeMatcher:

    SKILLS = [
        "azure",
        "aws",
        "gcp",
        "terraform",
        "ansible",
        "kubernetes",
        "docker",
        "helm",
        "jenkins",
        "linux",
        "github actions",
        "azure devops",
        "ci/cd",
        "prometheus",
        "grafana",
        "sonarqube",
        "trivy",
        "tfsec",
        "tflint",
        "python",
        "bash",
        "powershell",
        "git",
        "vmware",
        "vcenter",
        "vsphere",
        "openshift",
        "argocd",
        "gitlab",
        "datadog",
        "splunk",
        "elk",
        "new relic",
        "cloudformation",
        "pulumi",
        "networking",
        "tcp/ip",
        "dns",
        "nginx",
        "apache",
        "postgresql",
        "mysql",
        "redis",
        "rabbitmq",
        "kafka"
    ]

    TARGET_ROLES = [
        "devops",
        "cloud",
        "platform",
        "site reliability",
        "sre",
        "infrastructure",
        "devsecops"
    ]

    def match(self, resume_text, job):

        resume_text = resume_text.lower()

        job_title = job.title.lower()

        job_text = (
            job.title + " " + job.description
        ).lower()

        required_skills = []
        matched_skills = []
        missing_skills = []

        # -------------------------
        # SKILL MATCH - 60 POINTS
        # -------------------------

        for skill in self.SKILLS:

            if skill in job_text:

                required_skills.append(skill)

                if skill in resume_text:
                    matched_skills.append(skill)

                else:
                    missing_skills.append(skill)

        if required_skills:

            skill_score = (
                len(matched_skills)
                / len(required_skills)
            ) * 60

        else:

            skill_score = 0

        # -------------------------
        # ROLE MATCH - 20 POINTS
        # -------------------------

        role_score = 0

        for role in self.TARGET_ROLES:

            if role in job_title:

                if role in resume_text:
                    role_score = 20

                else:
                    role_score = 10

                break

        # -------------------------
        # EXPERIENCE - 15 POINTS
        # -------------------------

        experience_score = 0

        resume_experience = re.findall(
            r"(\d+)\+?\s*(?:years|year|yrs|yr)",
            resume_text
        )

        job_experience = re.findall(
            r"(\d+)\+?\s*(?:years|year|yrs|yr)",
            job_text
        )

        if resume_experience:

            resume_years = max(
                int(year)
                for year in resume_experience
            )

        else:

            resume_years = 0

        if job_experience:

            job_years = min(
                int(year)
                for year in job_experience
            )

            if resume_years >= job_years:
                experience_score = 15

            elif job_years - resume_years == 1:
                experience_score = 8

            else:
                experience_score = 0

        else:

            experience_score = 10

        # -------------------------
        # LOCATION - 5 POINTS
        # -------------------------

        location_score = 0

        location = job.location.lower()

        good_locations = [
            "india",
            "worldwide",
            "anywhere",
            "global",
            "remote"
        ]

        for good_location in good_locations:

            if good_location in location:
                location_score = 5
                break

        # -------------------------
        # FINAL SCORE
        # -------------------------

        final_score = int(
            skill_score
            + role_score
            + experience_score
            + location_score
        )

        final_score = min(final_score, 100)

        return {
            "score": final_score,
            "skill_score": int(skill_score),
            "role_score": role_score,
            "experience_score": experience_score,
            "location_score": location_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }