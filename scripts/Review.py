import subprocess
import os
import smtplib
from dotenv import load_dotenv
from google import genai
from email.mime.text import MIMEText

# Load environment variables
load_dotenv()

# Initialize Gemini model
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def send_email(body):
    sender_email = "desdeepak42@gmail.com"
    receiver_email = "desdeepak42@gmail.com"
    msg = MIMEText(body, "html")
    msg["Subject"] = "Code Review Feedback"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, os.getenv("PYTHON_APP"))
        server.sendmail(sender_email, receiver_email, msg.as_string())


def main():
    try:
        # Get latest commit changes
        diff = subprocess.check_output(
            ["git", "show", "--format=", "HEAD"],
            text=True
        )

        if not diff.strip():
            print("No code changes found.")
            return

        prompt = """You are a Senior Python Software Engineer and Code Reviewer.

                        Review the following Git diff.

                        Return ONLY valid HTML.

                        Requirements:

                        - The email must use the FULL WIDTH of the email body.
                        - Do NOT create a centered container, card, or fixed-width box.
                        - Use a white background.
                        - Use Arial, Helvetica, sans-serif font.
                        - Keep the design clean, simple, and professional.
                        - Add enough spacing between sections.
                        - Separate each section using a horizontal line (<hr>).
                        - Do NOT use Markdown.
                        - Do NOT wrap the HTML inside ```.

                        Use these colors:

                        - Main Title: #2563EB (Blue)
                        - Summary Heading: #2563EB
                        - Strengths Heading: #16A34A
                        - Bugs Found Heading: #DC2626
                        - Security Issues Heading: #B91C1C
                        - Performance Improvements Heading: #F59E0B
                        - Code Quality Heading: #4F46E5
                        - Suggestions Heading: #7C3AED

                        Formatting Rules:

                        1. Add this title at the top:

                        <h1>Python Code Review</h1>

                        2. Create these sections in order:

                        Summary

                        Strengths

                        Bugs Found

                        Security Issues

                        Performance Improvements

                        Code Quality

                        Suggestions

                        Overall Rating

                        3. Use ONLY these emojis:

                        ✅ for Strengths

                        ❌ for Bugs Found

                        ❌ for Security Issues

                        Do not use any other emojis.

                        4. Overall Rating:

                        Display the rating inside a colored badge.

                        Rating >= 9
                        Green

                        Rating 7–8.9
                        Orange

                        Rating below 7
                        Red

                        Example:

                        <div style="display:inline-block;padding:8px 18px;border-radius:6px;background:#ffe5e5;color:#b91c1c;font-weight:bold;">
                        6.5 / 10
                        </div>

                        5. If a code snippet is required, place it inside:

                        <pre style="background:#f4f4f4;padding:10px;border-left:4px solid #2563EB;overflow:auto;">
                        ...
                        </pre>

                        6. Use unordered lists wherever appropriate.

                        7. Keep the language concise and professional.

                        8. Do not mention things that are not present in the Git diff.

                        Git Diff:

                        {diff}"""

        response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )
        send_email(response.text)

        print("✅ Code review email sent successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()