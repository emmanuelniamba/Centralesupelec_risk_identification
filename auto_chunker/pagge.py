import re

def extract_page(content):
    # Define the regex pattern to match pages and their content
    pattern = r"Page (\d+) :(.+?)(?=Page \d+ :|$)"
    
    # Use re.findall to extract all matches
    matches = re.findall(pattern, content, re.DOTALL)
    
    # Create a dictionary to store the page content
    pages = {int(page): text.strip() for page, text in matches}
    
    return pages

# Example usage

with open(r"C:\Users\beugre niamba\Desktop\Analyse-interactions entres risques grace au Gen ai\Centralesupelec-LGI\auto_chunker\reponse.md", "r", encoding="utf-8") as file:
    content = file.read()
pages_content = extract_page(content)

print(f"Extracted {len(pages_content)} pages.")

for page_num, page_text in pages_content.items():
    print(f"Page {page_num}: {page_text[:100]}...")  # Print the first 100 characters of each page
