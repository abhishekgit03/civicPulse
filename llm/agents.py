import json
import re
from llm.llm_client import gemini_client
from google.genai import types
from dotenv import load_dotenv
from llm.prompts import ANALYZE_COMPLAINT_PROMPT
from llm.chat import embed_generator
from collections import defaultdict
from mongodb.handlers import get_all_complaints

# Gemini API client
client = gemini_client.client


# ============================================================
# 🧩 Analyze Individual Complaint
# ============================================================
def analyze_complaint(payload: dict):
    """
    Analyzes a resident complaint using the Gemini 2.5 Flash model.
    Returns structured JSON containing classification and insights.
    """

    contents = f"""
    Resident Name: {payload.get("resident_name")}
    Block/Area: {payload.get("block")}
    Description: {payload.get("description")}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=ANALYZE_COMPLAINT_PROMPT
            ),
            contents=contents,
        )
        text_response = response.text.strip()

        # Extract JSON portion from Gemini output
        cleaned_text = re.search(r"\{.*\}", text_response, re.DOTALL)
        if cleaned_text:
            text_response = cleaned_text.group(0)

        try:
            ai_output = json.loads(text_response)
        except json.JSONDecodeError:
            ai_output = {"raw_text": text_response, "error": "Invalid JSON output"}

        # Generate vector embedding
        embedding = embed_generator(payload.get("description"))
        final_output = {
            **payload,
            **ai_output,
            "embedding": embedding,
            "status": "open",
        }

        return final_output

    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 🧱 Summarize Complaints Block-Wise
# ============================================================
def summarize_block_issues():
    """
    Fetch all complaints from MongoDB, group them block-wise,
    and summarize each block's issues using Gemini.
    """

    complaints = get_all_complaints()
    if not complaints:
        print("No complaints found in database.")
        return []

    # Group complaints by block
    block_wise_complaints = defaultdict(list)
    for c in complaints:
        block = c.get("block", "Unknown")
        block_wise_complaints[block].append(c.get("description", ""))

    # Optional: Sort blocks in a logical order (A1–B4)
    block_order = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3", "B4"]
    sorted_blocks = [
        (block, block_wise_complaints[block])
        for block in block_order
        if block in block_wise_complaints
    ]

    # Add any remaining blocks not in the predefined order
    remaining_blocks = [
        (b, desc)
        for b, desc in block_wise_complaints.items()
        if b not in block_order
    ]
    sorted_blocks.extend(remaining_blocks)

    block_summaries = []

    for block, descriptions in sorted_blocks:
        all_text = "\n".join(descriptions)

        prompt = f"""
        You are an AI civic data analyst for the CivicPulse system.
        Summarize the main issues and recurring problems reported by residents
        in Block {block}. Be concise (2–3 sentences) and focus on key concerns.

        Complaints:
        {all_text}
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction="Summarize civic complaints clearly and briefly."
                ),
                contents=prompt,
            )

            summary_text = response.text.strip()
            block_summaries.append({"block": block, "summary": summary_text})

        except Exception as e:
            print(f"Error summarizing block {block}: {e}")
            block_summaries.append(
                {"block": block, "summary": "Error generating summary."}
            )

    return block_summaries


# ============================================================
# 🧾 Generate Summary for an Individual Complaint
# ============================================================
def generate_complaint_summary(description: str) -> str:
    """
    Generates a concise summary of a complaint using Gemini.
    If quota is exceeded, returns a fallback text.
    """
    if not description or not description.strip():
        return "No complaint description provided to summarize."

    prompt = f"""
    You are a civic complaint summarizer for the CivicPulse dashboard.
    Summarize the following resident complaint in 1–2 short sentences.
    Focus only on the core issue — be concise and neutral.

    Complaint Description:
    {description}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction="Summarize the complaint clearly in simple language."
            ),
            contents=prompt,
        )

        summary_text = response.text.strip()
        summary_text = re.sub(r"\s+", " ", summary_text)
        return summary_text

    except Exception as e:
        print(f"Error generating complaint summary: {e}")
        # Return cached / fallback text instead of failing
        return "Summary temporarily unavailable (quota exceeded)."
