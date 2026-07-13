from utils.gemini_client import GeminiClient


def main():

    print("\n🤖 Testing Gemini Connection...\n")

    try:

        gemini = GeminiClient()

        response = gemini.generate(
            "Reply only with: AI Job Agent Connected Successfully"
        )

        print("✅ Gemini Response:\n")

        print(response)

    except Exception as e:

        print("❌ Gemini Error:")
        print(e)


if __name__ == "__main__":
    main()