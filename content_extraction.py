
import os
import json 
import nest_asyncio 
from dotenv import load_dotenv # load environment variables
from llama_parse import LlamaParse # import LlamaParse for content extraction
from llama_index.core import SimpleDirectoryReader # allow reading from a directory

# apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

class Content_Extractor:
    def __init__(self,api_key='LLAMA_CLOUD_API_KEY'):
        load_dotenv()  # load environment variables from .env file
        try:
            self.api_key = os.getenv(api_key)  # get the API key from environment variables
        except KeyError:
            raise KeyError(f"Environment variable '{api_key}' not found. Please set it in your .env file.")
        
        self.parsing_instruction = """
You are a document parser specialized in extracting key information from project management documents. Extract the information exactly as it appears, without any rephrasing or interpretation.
Do not rephrase, summarize, or interpret any content. Write and extract the information exactly as it appears in the document, word for word, including all formatting, bullet points, and line breaks.

Ignore any section or content related to risks, including but not limited to: "Risk Analysis", "Project Risks", "Risks", "Risk Management", "Gestion des risques", "Analyse des risques", "Risques", "Plan de gestion des risques", "Risk log", "Risk register", or any similar title in any language. Also, do not extract or output any proposed solutions, recommendations, Solution,Implementation,Results,or mitigation actions related to risks, even if they are present in the document. This instruction takes precedence over all others.

For each section:
- Use the exact section title as it appears in the document for the "section" field.
- If the title is a variant or synonym of a target section, map it to the closest target section and mention the original title in the "notes" field.
- If the section title is too vague or generic (e.g., "Other", "Miscellaneous", "General"), try to infer a more logical and descriptive title based on the actual content of the section.
- Only extract and output sections that are actually present in the document, in the order they appear.
-Ignore sections that are not relevant to project management analysis (e.g., lists of acronyms, currency tables, appendices with only maps or raw data), unless they contain substantive project information.

Your output must be a structured JSON, in the language of the original document. If the document is in French, answer in French; otherwise, always answer in English.

Output format:
{
  "section": "<EXACT_OR_MAPPED_SECTION_NAME>",
  "content": "<RAW_TEXT>",
  "notes": "<SHORT_COMMENT_WITH_ORIGINAL_TITLE_AND_PAGE>"
}

[List of target sections and definitions as before...]

*General instructions:*
- Go through all pages of the document; if a section starts on page N and continues on page N+1, aggregate the content.
- Do not generate any section not present in the document.
"""
                                   
                               
                               
        self.parser=LlamaParse(
            result_type='markdown',
            parsing_instruction=self.parsing_instruction,
            api_key=self.api_key,
        )
        
        self.file_extractor={".pdf":self.parser,".docx":self.parser,".txt":self.parser}
        
    def extract_content(self, directory_path):
        """ Extract content from files in the specified directory.
        """
        try:
            documents=SimpleDirectoryReader(input_files=[directory_path],file_extractor=self.file_extractor).load_data()
            return documents 
        except Exception as e:
            raise Exception(f"An error occurred while extracting content: {e}")
            return None
        
    def extract_text(self, directory_path):
        
        documents = self.extract_content(directory_path)
        return '\n'.join([doc.text for doc in documents]) if documents else ""

    def save_extracted_data(self, file_path, output_text_path, output_markdown_path, output_json_path):
        """ Save extracted data to text, markdown, and JSON files.
        """
        documents = self.extract_content(file_path)
    # Filtrer les documents qui ont du texte non vide
        filtered_docs = [doc for doc in documents if hasattr(doc, 'text') and doc.text and doc.text.strip()]
        text = '\n'.join([doc.text for doc in filtered_docs]) if filtered_docs else ""

        if text:
          with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(text)
          with open(output_markdown_path, 'w', encoding='utf-8') as f:
            f.write(text)
        # Convert extracted text to JSON format
          json_data = {"description_text": text}
          with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
            print("Raw text, markdown, and JSON data have been saved for your review.")
        else:
          print("No data extracted.")
        