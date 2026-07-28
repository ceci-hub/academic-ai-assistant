import streamlit as st
from groq import Groq
import json
from pypdf import PdfReader

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ====================================
# SESSION STATE
# ====================================

if "draft_history" not in st.session_state:
    st.session_state["draft_history"] = []

# ====================================
# PAGE CONFIG
# ====================================

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="✍️",
    layout="wide"
)

# ====================================
# CUSTOM CSS
# ====================================

st.markdown(
    """
    <style>

    .stButton button {
        width: 100%;
        border-radius: 12px;
        height: 48px;
        font-weight: 600;
    }

    .stTextArea textarea {
        border-radius: 12px;
    }

    .block-container {
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ====================================
# HEADER
# ====================================

st.title("✍️ AI Academic Assistant")

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#EC4899,#F472B6);
        padding:15px;
        border-radius:12px;
        color:white;
        text-align:center;
        font-weight:bold;
        margin-bottom:20px;
    ">
        Create, improve, summarize, and study smarter with AI
    </div>
    """,
    unsafe_allow_html=True
)

# ====================================
# SIDEBAR
# ====================================

with st.sidebar:

    st.title("🌸 AI Academic Assistant")

    st.markdown(
        """
        ### Cecilia Regueira

        Data Analyst/ Data scientist  • AI Enthusiast • Mom

        🔗 [Linked/www.linkedin.com/in/cecilia-regueira/
        """ )

    st.divider()

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

# ====================================
# MAIN APP STARTS BELOW
# ====================================
#################################################
###  MÓDULO 1 (IMPROVE EXISTING TEXT)
#################################################


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

    if st.button("📝 Generate Draft"):

        prompt = f"""
Create a high-quality draft.

Return ONLY JSON.

{{
  "draft":"",
  "subject_line":"",
  "strengths":[],
  "suggestions":[
      ""
  ]
}}

Requirements:

1. Write the best possible draft.
2. Identify 2-4 writing strengths.
3. Provide 3-5 specific improvement suggestions.
4. Suggestions must be actionable and concrete.
5. Examples of suggestions:
   - Strengthen the opening paragraph.
   - Make the tone more professional.
   - Add supporting details.
   - Be more concise.
   - Make the request clearer.
   - Improve the conclusion.
   - Increase persuasiveness.
6. Do NOT use generic suggestions.

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

            st.session_state["last_draft"] = draft_text

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
                "✅ Strengths"
            )

            for strength in result.get(
                "strengths",
                []
            ):
                st.success(
                    strength
                )

            suggestions = result.get(
                "suggestions",
                []
            )

            if suggestions:

                st.subheader(
                    "💡 Improvement Suggestions"
                )

                selected_suggestion = st.radio(
                     "Choose an improvement",
                      suggestions
                  )

                if st.button(
                    "✨ Apply Suggestion"
                ):

                    improve_prompt = f"""
Improve the following draft.

Apply ONLY this improvement:

{selected_suggestion}

Return ONLY JSON.

{{
    "improved_text":""
}}

Draft:
{draft_text}
"""

                    with st.spinner(
                        "Applying suggestion..."
                    ):

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

                    improved_text = improve_result.get(
                        "improved_text",
                        ""
                    )

                    st.session_state["last_draft"] = (
                        improved_text
                    )

                    st.subheader(
                        "✨ Improved Draft"
                    )

                    st.text_area(
                        "Updated Draft",
                        value=improved_text,
                        height=300
                    )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )


#################################################
### Document Assistant
#################################################


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

                # =====================================
                # TABS
                # =====================================

                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
                    [
                        "📝 Summary",
                        "🔑 Key Points",
                        "❓ Study Questions",
                        "🗂 Flashcards",
                        "🎓 Exam Prep",
                        "📝 Quiz"
                    ]
                )

                # SUMMARY

                with tab1:

                    st.subheader(
                        "📘 Document Title"
                    )

                    st.info(
                        result.get(
                            "title",
                            ""
                        )
                    )

                    st.subheader(
                        "📝 Summary"
                    )

                    st.info(
                        result.get(
                            "summary",
                            ""
                        )
                    )

                    dates = result.get(
                        "important_dates",
                        []
                    )

                    if dates:

                        st.subheader(
                            "📅 Important Dates"
                        )

                        for d in dates:

                            st.write(
                                f"📅 {d}"
                            )

                # KEY POINTS

                with tab2:

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

                # STUDY QUESTIONS

                with tab3:

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

                with tab4:

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

                with tab5:

                    exam_prep = result.get(
                        "exam_prep",
                        {}
                    )

                    st.subheader(
                        "✅ Important Concepts"
                    )

                    for concept in exam_prep.get(
                        "important_concepts",
                        []
                    ):

                        st.write(
                            f"✅ {concept}"
                        )

                    st.subheader(
                        "📚 Likely Exam Topics"
                    )

                    for topic in exam_prep.get(
                        "likely_exam_topics",
                        []
                    ):

                        st.write(
                            f"📚 {topic}"
                        )

                    st.subheader(
                        "❓ Practice Questions"
                    )

                    for pq in exam_prep.get(
                        "practice_questions",
                        []
                    ):

                        st.write(
                            f"❓ {pq}"
                        )

                # QUIZ

                with tab6:

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

            # =====================================
            # DOCUMENT Q&A
            # =====================================

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

