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

        prompt = f"""
                    You are a Senior Software Engineer.
                    
                    Review the following Git diff.
                    
                    Return ONLY a complete HTML document.
                    
                    Requirements:
                    
                    - Beautiful modern email design.
                    - White background.
                    - Rounded card.
                    - Use inline CSS only.
                    - Font: Arial, Helvetica, sans-serif.
                    
                    Use these colors:
                    
                    Primary:
                    #2563EB
                    
                    Success:
                    #16A34A
                    
                    Warning:
                    #F59E0B
                    
                    Error:
                    #DC2626
                    
                    Background:
                    #F8FAFC
                    
                    Headings should have colored left borders.
                    
                    Format exactly like this:
                    
                    <h1>Python Code Review</h1>
                    
                    Summary
                    
                    Strengths
                    
                    Bugs Found
                    
                    Security Issues
                    
                    Performance Improvements
                    
                    Code Quality
                    
                    Suggestions
                    
                    Overall Rating (/10)
                    
                    Styling rules:
                    
                    • Main title inside a blue banner.
                    
                    • Summary section
                    Blue heading.
                    
                    • Strengths
                    Green heading with ✓ icons.
                    
                    • Bugs Found
                    Red heading with ❌ icons.
                    
                    • Security Issues
                    Dark red heading with 🔒 icons.
                    
                    • Performance
                    Orange heading with ⚡ icons.
                    
                    • Code Quality
                    Purple heading with 📘 icons.
                    
                    • Suggestions
                    Blue heading with 💡 icons.
                    
                    • Overall Rating
                    
                    Display rating inside a colored badge:
                    
                    9-10 = Green
                    
                    7-8 = Orange
                    
                    Below 7 = Red
                    
                    Use:
                    
                    - Cards
                    - Borders
                    - Padding
                    - Shadows
                    - Tables if needed
                    - Bullet lists
                    - Nice spacing
                    
                    Do NOT return markdown.
                    
                    Do NOT wrap HTML inside ```.
                    
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