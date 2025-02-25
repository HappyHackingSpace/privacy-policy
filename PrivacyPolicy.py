from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from dotenv import load_dotenv
import openai
from langchain.text_splitter import CharacterTextSplitter
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def fetch_content_with_selenium(url):
    """
    Fetch text content from a given URL using Selenium.
    """
    chromedriver_autoinstaller.install()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        body_text = driver.find_element(By.TAG_NAME, "body").text
        return body_text
    except Exception as e:
        print(f"Failed to fetch content from URL: {e}")
        return None
    finally:
        driver.quit()


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=200):
    """
    Split text into smaller chunks using LangChain's CharacterTextSplitter.
    """
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


def analyze_text_with_openai(text_chunk):
    """
    Analyze a text chunk using OpenAI API and return a score.
    """
    prompt = """
        Analyze the following privacy policy excerpt for security and data protection practices.
        Focus on evaluating how user data is collected, used, stored, and shared. 
        Rate the policy on a scale of 0 to 100, where:
        - 0 indicates very poor security practices with high risks to users,
        - 100 indicates excellent security and user data protection.

        Provide only the numeric score.

        Text:
        {text}
        """

    # Limit the text size to avoid API errors
    max_chunk_length = 4000
    truncated_text = text_chunk[:max_chunk_length]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in analyzing privacy policies.",
                },
                {"role": "user", "content": prompt.format(text=truncated_text)},
            ],
            max_tokens=50,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error analyzing text with OpenAI: {e}")
        return None


if __name__ == "__main__":
    # Get URL from user
    url = input("Enter the URL of the privacy policy to analyze: ")
    content = fetch_content_with_selenium(url)

    if content:
        print("Content successfully fetched.")

        # Split the text into smaller chunks
        chunks = split_text_into_chunks(content)

        # Analyze each chunk and collect scores
        scores = []
        for i, chunk in enumerate(chunks):
            print(f"Analyzing chunk {i + 1}/{len(chunks)}...")
            score = analyze_text_with_openai(chunk)

            # Check if the score is a valid integer
            try:
                scores.append(int(score))
            except (ValueError, TypeError):
                print(f"'{score}' is not a valid integer, skipping this score.")

        # Calculate and display the average score if valid scores exist
        if scores:
            average_score = sum(scores) / len(scores)
            print(f"Average security score of the privacy policy: {average_score:.2f}")
        else:
            print("No valid scores found.")
    else:
        print("Failed to fetch content from the URL.")
