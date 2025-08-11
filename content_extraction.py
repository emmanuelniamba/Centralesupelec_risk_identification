
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

Preserve the original section titles and the hierarchical structure (headings, subheadings, etc.) as they appear in the document. Reflect the document’s outline and nesting of sections in your output, so that the parent-child relationships between sections and subsections are clear.

**Output instructions:**
- Output the extracted content in markdown format, not JSON.
- For each main section, use a level 1 markdown heading (`#`) and write the title in ALL UPPERCASE.
- For each subsection, use a level 2 markdown heading (`##`) and write the title in Capitalized or lowercase as appropriate.
- Place the content directly below its title.
- Preserve the original hierarchy and order of sections and subsections as in the document.
- If you encounter a table, figure, or graph, do not simply extract it as-is. Instead, describe the information contained in the table, figure, or graph using full sentences and paragraphs, in the language of the document. Translate all visual elements into textual explanations, ensuring that the meaning, relationships, and data are fully conveyed. Avoid losing any detail, and integrate the content into the narrative as if you were explaining it to someone who cannot see the visual elements.
- For each page in the document, wrap its entire content (including all headings, text, and formatting) inside a tag of the form <pageN> ... </pageN>, where N is the page number (e.g., <page1> ... </page1>, <page2> ... </page2>, etc.).
- Place all extracted markdown content for each page inside its corresponding tag, and increment the page number for each new page.
- Do not merge content from different pages into the same tag.

**Example:**

<page1>
# PROJECT OBJECTIVES
The project aims to improve digital infrastructure...

## Key performance indicators
- Increase internet penetration by 20%
- Reduce costs by 15%

# ORGANIZATION AND GOVERNANCE
The project is managed by...

## Steering committee
The steering committee includes...

## Figure 1: Internet Penetration Growth
The graph shows a steady increase in internet penetration from 2015 to 2020, with a peak growth rate of 25% in 2018. The x-axis represents years, and the y-axis represents the percentage of internet penetration.

(Continue in this format for all sections and subsections.)
</page1>

Ignore any section or content related to risks, including but not limited to: "Risk Analysis", "Project Risks", "Risks", "Risk Management", "Gestion des risques", "Analyse des risques", "Risques", "Plan de gestion des risques", "Risk log", "Risk register", or any similar title in any language. Also, do not extract or output any proposed solutions, recommendations, Solution, Implementation, Results, or mitigation actions related to risks, even if they are present in the document. This instruction takes precedence over all others. ALSO DELETE TABLE OF CONTENTS AND OTHER INFORMATION.
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

    def save_extracted_data(self, file_path, output_markdown_path):
        """ Save extracted data to text, markdown, and JSON files.
        """
        documents = self.extract_content(file_path)
    # Filtrer les documents qui ont du texte non vide
        filtered_docs = [doc for doc in documents if hasattr(doc, 'text') and doc.text and doc.text.strip()]
        text = '\n'.join([doc.text for doc in filtered_docs]) if filtered_docs else ""

        if text:
          with open(output_markdown_path, 'w', encoding='utf-8') as f:
            f.write(text)
          print(f"Markdown content saved to {output_markdown_path}")
        else:
          print("No content extracted to save as markdown.")    
      
        
        