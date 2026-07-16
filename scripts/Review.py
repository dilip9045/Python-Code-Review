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
    sender_email = "dilip.sisodiya_cs23@gla.ac.in"
    receiver_email = "dilip.sisodiya_cs23@gla.ac.in"

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

        prompt = f"""
                    You are a senior Python software engineer.

                    Review the following Git diff.

                    Return ONLY valid HTML.

                    The HTML must include:

                    <h1>Python Code Review</h1>

                    <h2>Summary</h2>

                    <h2>Strengths</h2>

                    <h2>Bugs Found</h2>

                    <h2>Security Issues</h2>

                    <h2>Performance Improvements</h2>

                    <h2>Code Quality</h2>

                    <h2>Suggestions</h2>

                    <h2>Overall Rating (/10)</h2>

                    Do not use Markdown.
                    Do not wrap the HTML in ```.

                    Git Diff:

                    {diff}
                """

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