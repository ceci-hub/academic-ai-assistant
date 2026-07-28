# pip install streamlit ollama

import streamlit as st
from groq import Groq
import json
from pypdf import PdfReader

client = Groq(    api_key=st.secrets["GROQ_API_KEY"])

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

### help me write
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
            
            st.session_state["last_draft"] = result.get( "draft", "")
            
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

            draft_text = result.get("draft", "")

            st.text_area(
               "Draft",
                value=draft_text,
                height=250
                )

             st.session_state["last_draft"] = draft_text

            st.subheader(
                "Suggestions"
            )

            for s in result.get(
                "suggestions",
                []
            ):
                st.write(f"• {s}")

            if "last_draft" in st.session_state:

                 if st.button("✨ Improve Last Draft"):

                 improve_prompt = f"""
                     Improve the following text.

                  Return ONLY JSON.

                   {{
                      "improved_text":"",
                       "changes":[]
                }}

             Text:
             {st.session_state["last_draft"]}
               """

        improve_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={
                "type": "json_object"
            },
            messages=[
                {
                    "role": "user",
                    "content": improve_prompt
                }
            ]
        )

        improve_result = json.loads(
            improve_response.choices[0].message.content
        )

        st.subheader("✨ Improved Version")

        st.text_area(
            "Improved Draft",
            value=improve_result.get(
                "improved_text",
                ""
            ),
            height=300
        )

        st.subheader("Changes Made")

        for change in improve_result.get(
            "changes",
            []
        ):
            st.write(f"• {change}")

        st.session_state["last_draft"] = (
            improve_result.get(
                "improved_text",
                st.session_state["last_draft"]
            )
        )

        except Exception as e:

            st.error(f"Error: {e}")

# ===================================================
# MODE 3 - DOCUMENT ASSISTANT
# ===================================================

if assistant_mode == "Document Assistant":

    st.subheader("📄 Upload a Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    summary_style = st.selectbox(
        "Summary Style",
        [
            "Student Friendly",
            "Executive Summary",
            "Research Summary",
            "Bullet Points",
            "Study Guide",
            "Flashcards",
            "Exam Prep",
            "Quiz Generator"
        ]
    )

    if uploaded_file:

        try:

            pdf_reader = PdfReader(uploaded_file)

            document_text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    document_text += page_text + "\n"

            st.success(
                f"Document loaded ({len(document_text):,} characters)"
            )

            if st.button("Generate Summary"):

                prompt = f"""
Analyze the document.

Style:
{summary_style}

Document:
{document_text[:12000]}

Return ONLY valid JSON.

{{
  "title":"",
  "summary":"",
  "key_points":[],
  "important_dates":[],
  "study_questions":[],
  "flashcards":[
      {{
          "question":"",
          "answer":""
      }}
  ],
  "exam_prep": {{
      "important_concepts":[],
      "likely_exam_topics":[],
      "practice_questions":[]
  }},
  "quiz":[
      {{
          "question":"",
          "options":[],
          "answer":""
      }}
  ]
}}
"""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    response_format={
                        "type": "json_object"
                    },
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

                # TITLE

                st.subheader("📘 Document Title")

                st.info(
                    result.get("title", "")
                )

                # SUMMARY

                st.subheader("📝 Summary")

                st.write(
                    result.get("summary", "")
                )

                # KEY POINTS

                st.subheader("🔑 Key Points")

                for item in result.get(
                    "key_points",
                    []
                ):
                    st.write(f"• {item}")

                # IMPORTANT DATES

                st.subheader("📅 Important Dates")

                dates = result.get(
                    "important_dates",
                    []
                )

                if dates:
                    for d in dates:
                        st.write(f"📅 {d}")
                else:
                    st.write(
                        "No dates detected."
                    )

                # STUDY QUESTIONS

                st.subheader(
                    "❓ Study Questions"
                )

                for q in result.get(
                    "study_questions",
                    []
                ):
                    st.write(f"❓ {q}")

                # FLASHCARDS

                st.subheader(
                    "🗂 Flashcards"
                )

                flashcards = result.get(
                    "flashcards",
                    []
                )

                for card in flashcards:

                    with st.expander(
                        card.get(
                            "question",
                            "Flashcard"
                        )
                    ):

                        st.write(
                            card.get(
                                "answer",
                                ""
                            )
                        )

                # EXAM PREP

                st.subheader(
                    "🎓 Exam Preparation"
                )

                exam_prep = result.get(
                    "exam_prep",
                    {}
                )

                st.write(
                    "### Important Concepts"
                )

                for concept in exam_prep.get(
                    "important_concepts",
                    []
                ):
                    st.write(
                        f"✅ {concept}"
                    )

                st.write(
                    "### Likely Exam Topics"
                )

                for topic in exam_prep.get(
                    "likely_exam_topics",
                    []
                ):
                    st.write(
                        f"📚 {topic}"
                    )

                st.write(
                    "### Practice Questions"
                )

                for pq in exam_prep.get(
                    "practice_questions",
                    []
                ):
                    st.write(
                        f"❓ {pq}"
                    )

                # QUIZ GENERATOR

                st.subheader(
                    "📝 Practice Quiz"
                )

                quiz = result.get(
                    "quiz",
                    []
                )

                for idx, item in enumerate(
                    quiz,
                    start=1
                ):

                    st.markdown(
                        f"### Question {idx}"
                    )

                    st.write(
                        item.get(
                            "question",
                            ""
                        )
                    )

                    for option in item.get(
                        "options",
                        []
                    ):
                        st.write(
                            f"• {option}"
                        )

                    with st.expander(
                        "Show Answer"
                    ):
                        st.success(
                            item.get(
                                "answer",
                                ""
                            )
                        )

            # DOCUMENT Q&A

            st.divider()

            st.subheader(
                "💬 Ask About This Document"
            )

            question = st.text_input(
                "Ask a question about this document"
            )

            if question:

                qa_prompt = f"""
Answer using ONLY information
from the document.

Document:
{document_text[:12000]}

Question:
{question}
"""

                qa_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": qa_prompt
                        }
                    ]
                )

                st.subheader("🤖 Answer")

                st.success(
                    qa_response.choices[0].message.content
                )

        except Exception as e:

            st.error(f"Error: {e}")
