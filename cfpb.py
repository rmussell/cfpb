import requests
from bs4 import BeautifulSoup
import io
import PyPDF2

url = "https://www.consumerfinance.gov/enforcement/actions"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Get the first hypertext link on the page
link = soup.find("h3").find("a")

# Create the hyperlink variable
hyperlink = "https://www.consumerfinance.gov" + link["href"]

# Send an HTTP GET request to the hyperlink
response = requests.get(hyperlink)
soup = BeautifulSoup(response.text, "html.parser")

# Extract the links to related documents and the text of the enforcement
enforcement_title = soup.find("div", {"class": "o-item-introduction"}).find("h1").text
enforcement_text = soup.find("div", {"class": "m-full-width-text"}).find("p").text
action_details = soup.find("h5", string="Action details").find_next("ul").find_all("li")

# Print the extracted information
print("**Enforcement title:** " + enforcement_title)
print("**Enforcement text:** " + enforcement_text)
print("**Action details:**")
for detail in action_details:
    print(detail.text)

for i, document in enumerate(soup.find_all("a", class_="a-link a-link__icon")):
    # Download the PDF
    pdf_response = requests.get(document["href"])
    pdf_content = io.BytesIO(pdf_response.content)

    # Convert the PDF to text
    reader = PyPDF2.PdfReader(pdf_content)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()

    # Print the text
    print(f"**Related document {i+1}:** {text}")
