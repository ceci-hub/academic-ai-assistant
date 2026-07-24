# pip install streamlit ollama

import streamlit as st
from groq import Groq
import json
from pypdf import PdfReader

client = Groq(
    api_key="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"
)

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ AI Academic Assistant")

st.caption(
    "Built by Cecilia Regueira using Streamlit and Groq"
)

assistant_mode = st.radio(
    "Choose Assistant Mode",
    [
        "Improve Existing Text",
        "Help Me Write",
        "Document Assistant"
    ]
)

if assistant_mode == "Improve Existing Text":

    text = st.text_area(
        "Enter your text",
        height=200
    )

    rewrite_style = st.selectbox(
        "Rewrite Style",
        [
            "Academic",
            "Professional",
            "Friendly",
            "Concise"
        ]
    )

    if st.button("Analyze"):

        prompt = f"""
Return ONLY JSON.

{{
  "grammar_score": 0,
  "reading_level": "",
  "tone": "",
  "corrected_text": "",
  "common_mistakes": [],
  "corrections": [],
  "writing_coach": {{
      "strengths": [],
      "areas_for_improvement": [],
      "overall_advice": ""
  }}
}}

Rewrite in a {rewrite_style} style.

Text:
{text}
"""

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = json.loads(
                response.choices[0].message.content
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Grammar Score",
                    f"{result.get('grammar_score',0)}/100"
                )

            with col2:
                st.metric(
                    "Tone",
                    result.get("tone","Unknown")
                )

            with col3:
                st.metric(
                    "Reading Level",
                    result.get(
                        "reading_level",
                        "Unknown"
                    )
                )

            st.subheader("Corrected Text")

            st.success(
                result.get(
                    "corrected_text",
                    ""
                )
            )

        except Exception as e:

            st.error(f"Error: {e}")

### hel me write
if assistant_mode == "Help Me Write":

    situation = st.text_input(
        "Situation"
    )

    audience = st.selectbox(
        "Audience",
        [
            "Professor",
            "Manager",
            "Coworker",
            "Student",
            "Client",
            "General"
        ]
    )

    language = st.selectbox(
        "Tone",
        [
            "Professional",
            "Academic",
            "Friendly",
            "Formal",
            "Persuasive"
        ]
    )

    task = st.selectbox(
        "Type of Writing",
        [
            "Email",
            "Discussion Post",
            "Letter",
            "Essay Paragraph",
            "Request",
            "Cover Letter"
        ]
    )

    if st.button("Generate Draft"):

        prompt = f"""
Return ONLY JSON.

{{
  "draft":"",
  "subject_line":"",
  "strengths":[],
  "suggestions":[]
}}

Situation:
{situation}

Audience:
{audience}

Tone:
{language}

Task:
{task}
"""

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                response_format={"type":"json_object"},
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

            result = json.loads(
                response.choices[0].message.content
            )

            if result.get("subject_line"):

                st.subheader(
                    "Suggested Subject"
                )

                st.info(
                    result["subject_line"]
                )

            st.subheader(
                "Generated Draft"
            )

            st.success(
                result.get(
                    "draft",
                    ""
                )
            )

            st.subheader(
                "Suggestions"
            )

            for s in result.get(
                "suggestions",
                []
            ):
                st.write(f"• {s}")

        except Exception as e:

            st.error(f"Error: {e}")

### 3
