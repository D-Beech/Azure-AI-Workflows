"""
This code sample shows Prebuilt Layout operations with the Azure AI Document Intelligence client library.
The async versions of the samples require Python 3.8 or later.

To learn more, please visit the documentation - Quickstart: Document Intelligence (formerly Form Recognizer) SDKs
https://learn.microsoft.com/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?pivots=programming-language-python
"""

import os
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

# Load environment variables
load_dotenv()

# Create output folder if it doesn't exist
output_folder = "./output"
os.makedirs(output_folder, exist_ok=True)

"""
Remember to remove the key from your code when you're done, and never post it publicly. For production, use
secure methods to store and access your credentials. For more information, see 
https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-security?tabs=command-line%2Ccsharp#environment-variables-and-application-configuration
"""
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")

# sample document
formUrl = os.getenv("SAMPLE_DOCUMENT_URL")

document_intelligence_client  = DocumentIntelligenceClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout", AnalyzeDocumentRequest(url_source=formUrl)
)
result = poller.result()

# Save the raw JSON response
json_output_file = os.path.join(output_folder, "analysis_response.json")
with open(json_output_file, "w", encoding="utf-8") as json_file:
    json.dump(result.as_dict(), json_file, indent=2, ensure_ascii=False)
print(f"Raw JSON response saved to: {json_output_file}")

# Open output file for writing
output_file = os.path.join(output_folder, "analysis_results.txt")
with open(output_file, "w", encoding="utf-8") as f:
    for idx, style in enumerate(result.styles):
        line = "Document contains {} content".format(
             "handwritten" if style.is_handwritten else "no handwritten"
            )
        print(line)
        f.write(line + "\n")

    for page in result.pages:
        for line_idx, line in enumerate(page.lines):
            line_text = "...Line # {} has text content '{}'".format(
            line_idx,
            line.content.encode("utf-8")
            )
            print(line_text)
            f.write(line_text + "\n")

        if page.selection_marks:
            for selection_mark in page.selection_marks:
                mark_text = "...Selection mark is '{}' and has a confidence of {}".format(
                 selection_mark.state,
                 selection_mark.confidence
                 )
                print(mark_text)
                f.write(mark_text + "\n")

    for table_idx, table in enumerate(result.tables):
        table_text = "Table # {} has {} rows and {} columns".format(
        table_idx, table.row_count, table.column_count
        )
        print(table_text)
        f.write(table_text + "\n")
            
        for cell in table.cells:
            cell_text = "...Cell[{}][{}] has content '{}'".format(
                cell.row_index,
                cell.column_index,
                cell.content.encode("utf-8"),
                )
            print(cell_text)
            f.write(cell_text + "\n")

    print("----------------------------------------")
    f.write("----------------------------------------\n")

