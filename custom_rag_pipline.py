"""
title: Custom RAG Filter Function
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1-rc1
required_open_webui_version: 0.3.8
"""

from pydantic import BaseModel, Field
from typing import Optional
import requests  # Importing the requests library to handle HTTP requests
import base64


# from utils.misc import (
#     get_last_user_message,
#     add_or_update_system_message,
# )


class pipe:
    class Valves(BaseModel):
        # Template for modifying context information in the user interface
        RAG_TEMPLATE: str = Field(
            default="""Use the following context as your learned knowledge, inside <context></context> XML tags.
<context>
    {{CONTEXT}}
</context>

When answering to user:
- If you don't know, just say that you don't know.
- If you're unsure, ask for clarification.
Avoid mentioning that you obtained the information from the context.
And answer according to the language of the user's question.

Given the context information, answer the user query.""",
            description="Template for system messages that embed contextual knowledge.",
        )

    def __init__(self):
        self.file_handler = True  # Enable custom file handling logic
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        files = body.get("files", [])
        messages = body.get("messages", [])
        # user_query = get_last_user_message(messages)
        user_query = "what's your name?"
        context = None

        if files:
            files_payload = []
            try:
                for file in files:
                    file_path = file["file"]["meta"]["path"]
                    file_name = file["file"]["meta"]["name"]
                    print(f"Processing file from path: {file_path}")

                    # Opening file for sending; files must be closed by the requests library
                    file_handle = open(file_path, "rb")
                    files_payload.append(("files", (file_name, file_handle)))

                # Placeholder for server request to an external RAG (Retrieval-Augmented Generation) server
                # Example POST request:
                # r = requests.post(
                #     'https://external-rag-server.com/process',
                #     files=files_payload,
                #     data={'query': user_query}
                # )
                # r.raise_for_status()
                # res = r.json()
                # context = res.get('context', '')

                # For illustration without a real server:
                context = "Example context fetched based on the files and user query."
            except Exception as e:
                print(f"Request failed: {e}")
                # Handle request failure (You can add more sophisticated error handling)
                context = str(e)
            finally:
                # Ensure all file handles are closed
                for _, file_tuple in files_payload:
                    _, file_handle = file_tuple
                    file_handle.close()

            if context:
                # Related system message with retrieved context is injected into the message body
                system_message = self.valves.RAG_TEMPLATE.replace(
                    "{{CONTEXT}}", context
                )
                # body["messages"] = add_or_update_system_message(
                #     system_message, messages
                # )
                body["messages"] = "Lali Landau!!!!"
        return body