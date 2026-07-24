# pip install streamlit ollama

import streamlit as st
from groq import Groq
import json
import tempfile
from PyPDF2 import PdfReader

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(
    page_title="AI Writing Assistant",
    page_icon="✍️",
    layout="wide"
)

# -----------------------
# HEADER
# -----------------------

st.title("✍️ AI Academic Assistant")
st.caption(
    "Built by Cecilia Regueira using Streamlit and Llama 3.2"
)

# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.title("Features")

st.sidebar.markdown("""
✅ Grammar Score

✅ Tone Analysis

✅ Reading Level

✅ Grammar Corrections

✅ Common Mistakes

✅ Writing Coach Feedback

✅ Help Me Write (SALT Method)
""")

# -----------------------
# MODE SELECTION
# -----------------------

assistant_mode = st.radio(
    "Choose Assistant Mode",
    [
        "Improve Existing Text",
        "Help Me Write",
        "Document Assistant"
    ]
)

# ===================================================
# MODE 1 - IMPROVE EXISTING TEXT
# ===================================================

if assistant_mode == "Improve Existing Text":

    text = st.text_area(
        "Enter your text",
        height=200,
        placeholder="Example: hey professor i cant come to class today because im sick"
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

        if not text.strip():
            st.warning("Please enter some text.")

        else:

            prompt = f"""
Return valid JSON only.

{{
  "grammar_score": 0,
  "reading_level": "",
  "tone": "",
  "corrected_text": "",
  "common_mistakes": [],
  "corrections": [
      {{
        "original": "",
        "corrected": "",
        "reason": ""
      }}
  ],
  "writing_coach": {{
      "strengths": [],
      "areas_for_improvement": [],
      "overall_advice": ""
  }}
}}

Analyze the text.

Rewrite it in a {rewrite_style} style.

Text:
{text}
"""

            try:

                response = ollama.chat(
                    model="llama3.2",
                    format="json",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = json.loads(
                    response["message"]["content"]
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Grammar Score",
                        f"{result.get('grammar_score', 0)}/100"
                    )

                with col2:
                    st.metric(
                        "Tone",
                        result.get("tone", "Unknown")
                    )

                with col3:
                    st.metric(
                        "Reading Level",
                        result.get("reading_level", "Unknown")
                    )

                st.subheader("Corrected Text")

                st.success(
                    result.get("corrected_text", "")
                )

                st.subheader("Common Mistakes Found")

                mistakes = result.get(
                    "common_mistakes",
                    []
                )

                if mistakes:
                    for m in mistakes:
                        st.write(f"• {m}")
                else:
                    st.write("No major mistakes found.")

                st.subheader(
                    "Correction Explanations"
                )

                for c in result.get(
                    "corrections",
                    []
                ):

                    with st.expander(
                        f"{c.get('original','')} → {c.get('corrected','')}"
                    ):
                        st.write(
                            f"**Original:** {c.get('original','')}"
                        )

                        st.write(
                            f"**Corrected:** {c.get('corrected','')}"
                        )

                        st.write(
                            f"**Reason:** {c.get('reason','')}"
                        )

                st.subheader("Writing Coach")

                coach = result.get(
                    "writing_coach",
                    {}
                )

                st.write("### Strengths")

                for s in coach.get(
                    "strengths",
                    []
                ):
                    st.write(f"✅ {s}")

                st.write(
                    "### Areas for Improvement"
                )

                for a in coach.get(
                    "areas_for_improvement",
                    []
                ):
                    st.write(f"⚠️ {a}")

                st.write("### Overall Advice")

                st.info(
                    coach.get(
                        "overall_advice",
                        ""
                    )
                )

            except Exception as e:
                st.error(f"Error: {e}")

# ===================================================
# MODE 2 - HELP ME WRITE
# ===================================================

if assistant_mode == "Help Me Write":

    st.subheader("Create New Content")

    situation = st.text_input(
        "Situation (What is happening?)",
        placeholder="Need an extension for an assignment"
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
Use the SALT Framework.

Situation:
{situation}

Audience:
{audience}

Language:
{language}

Task:
{task}

Return valid JSON only.

{{
  "draft": "",
  "strengths": [],
  "suggestions": [],
  "subject_line": ""
}}
"""

        try:

            response = ollama.chat(
                model="llama3.2",
                format="json",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = json.loads(
                response["message"]["content"]
            )

            if result.get("subject_line"):

                st.subheader("Suggested Subject")

                st.info(
                    result["subject_line"]
                )

            st.subheader("Generated Draft")

            st.success(
                result.get("draft", "")
            )

            st.subheader("Strengths")

            for item in result.get(
                "strengths",
                []
            ):
                st.write(f"✅ {item}")

            st.subheader("Suggestions")

            for item in result.get(
                "suggestions",
                []
            ):
                st.write(f"⚠️ {item}")

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
You are an academic assistant.

Analyze the uploaded document.

Summary Style:
{summary_style}

Instructions:

- Generate a useful summary
- Extract important dates when available
- Create study questions
- Create flashcards
- Create exam preparation materials
- If style = Quiz Generator, create 10 multiple choice questions

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

                response = ollama.chat(
                    model="llama3.2",
                    format="json",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = json.loads(
                    response["message"]["content"]
                )

                # =========================
                # DOCUMENT TITLE
                # =========================

                st.subheader("📘 Document Title")

                st.info(
                    result.get("title", "")
                )

                # =========================
                # SUMMARY
                # =========================

                st.subheader("📝 Summary")

                st.write(
                    result.get("summary", "")
                )

                # =========================
                # KEY POINTS
                # =========================

                st.subheader("🔑 Key Points")

                for item in result.get(
                    "key_points",
                    []
                ):
                    st.write(f"• {item}")

                # =========================
                # IMPORTANT DATES
                # =========================

                st.subheader("📅 Important Dates")

                dates = result.get(
                    "important_dates",
                    []
                )

                if dates:

                    for date in dates:
                        st.write(f"📅 {date}")

                else:

                    st.write(
                        "No dates detected."
                    )

                # =========================
                # STUDY QUESTIONS
                # =========================

                st.subheader("❓ Study Questions")

                questions = result.get(
                    "study_questions",
                    []
                )

                if questions:

                    for q in questions:
                        st.write(f"❓ {q}")

                else:

                    st.write(
                        "No study questions generated."
                    )

                # =========================
                # FLASHCARDS
                # =========================

                st.subheader("🗂️ Flashcards")

                flashcards = result.get(
                    "flashcards",
                    []
                )

                if flashcards:

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

                else:

                    st.write(
                        "No flashcards generated."
                    )

                # =========================
                # EXAM PREP
                # =========================

                st.subheader("🎓 Exam Preparation")

                exam_prep = result.get(
                    "exam_prep",
                    {}
                )

                st.write(
                    "### Important Concepts"
                )

                concepts = exam_prep.get(
                    "important_concepts",
                    []
                )

                if concepts:

                    for concept in concepts:
                        st.write(
                            f"✅ {concept}"
                        )

                st.write(
                    "### Likely Exam Topics"
                )

                topics = exam_prep.get(
                    "likely_exam_topics",
                    []
                )

                if topics:

                    for topic in topics:
                        st.write(
                            f"📚 {topic}"
                        )

                st.write(
                    "### Practice Questions"
                )

                practice = exam_prep.get(
                    "practice_questions",
                    []
                )

                if practice:

                    for p in practice:
                        st.write(
                            f"❓ {p}"
                        )

                # =========================
                # QUIZ GENERATOR
                # =========================

                st.subheader("📝 Practice Quiz")

                quiz = result.get(
                    "quiz",
                    []
                )

                if quiz:

                    for i, q in enumerate(
                        quiz,
                        start=1
                    ):

                        st.markdown(
                            f"### Question {i}"
                        )

                        st.write(
                            q.get(
                                "question",
                                ""
                            )
                        )

                        options = q.get(
                            "options",
                            []
                        )

                        for option in options:
                            st.write(
                                f"• {option}"
                            )

                        with st.expander(
                            "Show Answer"
                        ):

                            st.success(
                                q.get(
                                    "answer",
                                    ""
                                )
                            )

                else:

                    st.write(
                        "No quiz generated."
                    )

            # ==================================
            # DOCUMENT Q&A
            # ==================================

            st.divider()

            st.subheader(
                "💬 Ask About This Document"
            )

            st.caption(
                "Examples: When is the final exam? | What is the grading policy? | Summarize Chapter 3"
            )

            question = st.text_input(
                "Ask a question about this document"
            )

            if question:

                qa_prompt = f"""
Answer using ONLY information
contained in the document.

If the answer cannot be found,
respond:

'I could not find that information in the document.'

Document:

{document_text[:12000]}

Question:

{question}
"""

                qa_response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "user",
                            "content": qa_prompt
                        }
                    ]
                )

                st.subheader("🤖 Answer")

                st.success(
                    qa_response["message"]["content"]
                )

        except Exception as e:

            st.error(f"Error: {e}")
