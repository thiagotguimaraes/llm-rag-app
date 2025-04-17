import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

# Load environment variables. Assumes that project contains .env file with API keys
load_dotenv()

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.getenv("GITHUB_TOKEN"),
)


def gpt4o(messages: list[dict]):
    if not os.getenv("GITHUB_TOKEN"):
        raise HTTPException(
            status_code=401, detail="GITHUB_TOKEN environment variable is not set"
        )

    try:
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-4o",  # https://github.com/marketplace/models
            temperature=1,
            max_tokens=4096,
            top_p=1,
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Failed to authenticate with OpenAI Client: {str(e)}",
        )


def generate_answer(question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n".join(context_chunks)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the provided context to answer the question. Reply using only the context provided.",
        },
        {"role": "user", "content": f"Context:\n{context_text}"},
        {"role": "user", "content": f"Question: {question}"},
    ]

    response = gpt4o(messages)

    return response.choices[0].message.content
