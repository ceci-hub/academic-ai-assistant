import streamlit as st
from groq import Groq
import json
from pypdf import PdfReader

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

if "draft_history" not in st.session_state:
    st.session_state["draft_history"] = []

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="✍️",
    layout="wide"
)

st.markdown(
    """
    <style>

    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
    }

    .stTextArea textarea {
        border-radius: 10px;
    }

    .block-container {
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("✍️ AI Academic Assistant")

st.info(
    "Create, improve, summarize, and study smarter with AI."
)

with st.sidebar:

    st.title("✍️ AI Academic Assistant")

    st.caption(
        "Built by Cecilia Regueira"
    )

    assistant_mode = st.radio(
        "Choose Assistant Mode",
        [
            "Improve Existing Text",
            "Help Me Write",
            "Document Assistant"
        ]
    )

    st.divider()

    st.info(
        "Powered by Groq + Llama 3.3"
    )

#################################################
###  MÓDULO 1 (IMPROVE EXISTING TEXT)
#################################################

# ===================================================
# MODE 1 - IMPROVE EXISTING TEXT
# ===================================================

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

            with st.spinner(
                "Analyzing writing..."
            ):

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

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Grammar Score",
                    f"{result.get('grammar_score', 0)}/100"
                )

            with col2:

                st.metric(
                    "Tone",
                    result.get(
                        "tone",
                        "Unknown"
                    )
                )

            with col3:

                st.metric(
                    "Reading Level",
                    result.get(
                        "reading_level",
                        "Unknown"
                    )
                )

            st.subheader(
                "✅ Corrected Text"
            )

            st.text_area(
                "Improved Version",
                value=result.get(
                    "corrected_text",
                    ""
                ),
                height=300
            )

            writing_coach = result.get(
                "writing_coach",
                {}
            )

            st.subheader(
                "💪 Strengths"
            )

            for item in writing_coach.get(
                "strengths",
                []
            ):

                st.success(item)

            st.subheader(
                "📈 Areas for Improvement"
            )

            for item in writing_coach.get(
                "areas_for_improvement",
                []
            ):

                st.warning(item)

            st.subheader(
                "🎯 Writing Coach Advice"
            )

            st.info(
                writing_coach.get(
                    "overall_advice",
                    ""
                )
            )

            mistakes = result.get(
                "common_mistakes",
                []
            )

            if mistakes:

                st.subheader(
                    "⚠️ Common Mistakes Found"
                )

                for mistake in mistakes:

                    st.write(
                        f"• {mistake}"
                    )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )


#################################################
### MÓDULO 2 (HELP ME WRITE)
#################################################

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

    col1, col2 = st.columns(2)

    with col1:
        generate = st.button(
            "📝 Generate Draft"
        )

    with col2:
        improve = st.button(
            "✨ Improve Last Draft"
        )

    if generate:

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

            with st.spinner(
                "Writing draft..."
            ):

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

            draft_text = result.get(
                "draft",
                ""
            )

            st.session_state["last_draft"] = (
                draft_text
            )

            st.session_state["draft_history"].append(
                draft_text
            )

            if result.get(
                "subject_line"
            ):

                st.subheader(
                    "Suggested Subject"
                )

                st.info(
                    result["subject_line"]
                )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Words",
                    len(draft_text.split())
                )

            with col2:
                st.metric(
                    "Characters",
                    len(draft_text)
                )

            with col3:
                st.metric(
                    "Paragraphs",
                    draft_text.count("\n\n") + 1
                )

            st.subheader(
                "Generated Draft"
            )

            st.text_area(
                "Draft",
                value=draft_text,
                height=300
            )

            st.subheader(
                "Suggestions"
            )

            for s in result.get(
                "suggestions",
                []
            ):
                st.write(f"• {s}")

            st.subheader(
                "✅ Strengths"
            )

            for strength in result.get(
                "strengths",
                []
            ):
                st.success(
                    strength
                )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

    if improve and st.session_state.get(
        "last_draft"
    ):

        try:

            with st.spinner(
                "Improving draft..."
            ):

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

                response = client.chat.completions.create(
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
                response.choices[0].message.content
            )

            improved_text = improve_result.get(
                "improved_text",
                ""
            )

            st.session_state["last_draft"] = (
                improved_text
            )

            st.session_state["draft_history"].append(
                improved_text
            )

            st.subheader(
                "✨ Improved Version"
            )

            st.text_area(
                "Improved Draft",
                improved_text,
                height=300
            )

            st.subheader(
                "Changes Made"
            )

            for change in improve_result.get(
                "changes",
                []
            ):
                st.write(
                    f"• {change}"
                )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

    if st.session_state[
        "draft_history"
    ]:

        with st.expander(
            "📜 Draft History"
        ):

            for i, draft in enumerate(
                st.session_state[
                    "draft_history"
                ],
                start=1
            ):

                st.write(
                    f"Version {i}"
                )

                st.text_area(
                    f"Draft {i}",
                    draft,
                    height=150
                )


#################################################
### Document Assistant
#################################################

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

            pdf_reader = PdfReader(
                uploaded_file
            )

            document_text = ""

            for page in pdf_reader.pages:

                page_text = page.extract_text()

                if page_text:
                    document_text += (
                        page_text + "\n"
                    )

            st.success(
                f"Document loaded ({len(document_text):,} characters)"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Characters",
                    len(document_text)
                )

            with col2:

                st.metric(
                    "Pages",
                    len(pdf_reader.pages)
                )

            if st.button(
                "Generate Summary"
            ):

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

                with st.spinner(
                    "Analyzing document..."
                ):

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

                st.subheader(
                    "📘 Document Title"
                )

                st.info(
                    result.get(
                        "title",
                        ""
                    )
                )

                # SUMMARY

                st.subheader(
                    "📝 Summary"
                )

                st.info(
                    result.get(
                        "summary",
                        ""
                    )
                )

                # KEY POINTS

                st.subheader(
                    "🔑 Key Points"
                )

                for item in result.get(
                    "key_points",
                    []
                ):
                    st.write(
                        f"• {item}"
                    )

                # IMPORTANT DATES

                st.subheader(
                    "📅 Important Dates"
                )

                dates = result.get(
                    "important_dates",
                    []
                )

                if dates:

                    for d in dates:

                        st.write(
                            f"📅 {d}"
                        )

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
                    st.write(
                        f"❓ {q}"
                    )

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

                # QUIZ

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
Answer using ONLY information from the document.

Document:
{document_text[:12000]}

Question:
{question}
"""

                with st.spinner(
                    "Searching document..."
                ):

                    qa_response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": qa_prompt
                            }
                        ]
                    )

                st.subheader(
                    "🤖 Answer"
                )

                st.success(
                    qa_response.choices[0].message.content
                )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )
