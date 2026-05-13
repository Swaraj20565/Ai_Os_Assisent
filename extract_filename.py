# import ollama

# def extract_filename(prompt):

#     system_prompt = """
# You are an AI OS Assistant command analyzer.

# Your job is to understand the user's command and return ONLY valid JSON.

# Rules:
# - Always detect the user's intent.
# - Extract important entities from the command.
# - Remove unnecessary words like:
#   open, my, please, file, document, pdf, copy, start, launch
# - Do not explain anything.
# - Do not add markdown.
# - Do not return extra text.
# - Output must always be pure JSON.

# Supported intents:
# - open_app
# - open_file
# - web_search
# - play_music
# - system_control

# JSON Format:
# {
#   "intent": "",
#   "app_name": "",
#   "file_name": "",
#   "file_type": "",
#   "search_query": "",
#   "action": ""
# }
# """

#     response = ollama.chat(
#         model='qwen2.5-coder:1.5b',
#         messages=[
#             {
#                 'role': 'system',
#                 'content': system_prompt
#             },
#             {
#                 'role': 'user',
#                 'content': prompt
#             }
#         ]
#     )

#     return response['message']['content'].strip()

import ollama

def extract_filename(prompt):

    system_prompt = """
You are an AI OS Assistant command analyzer.

Return ONLY valid JSON.

Rules:
- Never explain.
- Never add markdown.
- Never add extra text.
- Output must always be valid JSON.

IMPORTANT RULES:

1. If user mentions:
   pdf, docx, excel, txt, file, document
   then intent MUST be "open_file"

2. File name should contain the MAIN NAME only.

3. Never use:
   PDF, DOCX, FILE
   as file_name.

BAD:
{
  "file_name": "PDF"
}

GOOD:
{
  "file_name": "MG-Swaraj"
}

4. If user only says:
   "MG-Swaraj"
   assume it is a file request.

5. If intent=open_file:
   app_name must be empty.

JSON Format:
{
  "intent": "",
  "app_name": "",
  "file_name": "",
  "file_type": "",
  "search_query": "",
  "action": ""
}
"""

    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content'].strip()