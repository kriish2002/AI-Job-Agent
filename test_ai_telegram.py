from ai.gemini_analyzer import analyze_job
from notifications.telegram_notifier import send_telegram_message


test_job = """
We are hiring an Azure DevOps Engineer.

Experience Required: 1-3 years

Required Skills:
Azure
Terraform
Azure DevOps
Docker
Kubernetes
Linux
CI/CD Pipelines

The engineer will manage cloud infrastructure,
automate deployments and maintain CI/CD pipelines.
"""


print("🔍 Analyzing Job with Gemini AI...")

result = analyze_job(test_job)

print("\n🤖 AI RESULT\n")
print(result)

telegram_message = f"""
🚀 NEW JOB ANALYSIS

{result}
"""

print("\n📲 Sending result to Telegram...")

send_telegram_message(telegram_message)

