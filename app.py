import os
import time
import streamlit as st
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AppPilot AI",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# GEMINI API CONFIGURATION
# ============================================================

API_KEY = st.secrets.get("GEMINI_API_KEY")

if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    st.error(
        "❌ Gemini API key is missing.\n\n"
        "Please add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()


client = genai.Client(api_key=API_KEY)


MODEL = st.secrets.get(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)

FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash"
]


# ============================================================
# GEMINI AI FUNCTION WITH AUTOMATIC RETRY
# ============================================================

def generate_app_analysis(app_idea):

    prompt = f"""
You are AppPilot AI, an expert AI-powered
application development assistant.

The user wants to build this application:

==================================================
{app_idea}
==================================================

Your job is to help the user understand,
plan, build, explain and learn the application.

Return the response using EXACTLY these
five section headings:

## UNDERSTAND

Explain:

- What the application does
- Target users
- Problem solved
- Main goal
- Important user requirements
- Core features

Use simple language.

## PLAN

Create a practical development plan.

Include:

1. Main features
2. Screens/pages
3. User flow
4. Recommended frontend
5. Recommended backend
6. Database requirements
7. API requirements
8. AI components if useful
9. Basic architecture
10. Project folder structure
11. Development steps

Keep the recommendations suitable for
a student or fresher.

## BUILD

Create a small but useful starter implementation.

Use Python and Streamlit where possible.

Provide:

1. Project structure
2. requirements.txt
3. Main app.py code
4. Explanation of the code

The code must be beginner-friendly.

Use proper Markdown code blocks.

Do not use unnecessary complex libraries.

## EXPLAIN

Explain the generated implementation
in simple beginner-friendly language.

Explain:

- Overall architecture
- Frontend
- Backend
- Database
- APIs
- Important functions
- Data flow
- User interaction

## LEARN

Create a beginner-friendly learning roadmap.

Include:

1. Concepts to learn
2. Technologies to learn
3. Python/coding topics
4. Practice tasks
5. Testing
6. Deployment
7. What to learn next for production development

Keep everything practical for a student/fresher.

IMPORTANT:

- Do not invent unrelated requirements.
- Keep the answer practical.
- Use simple English.
- Make the generated code easy to understand.
- Follow the five section headings exactly.
"""

    # Maximum number of Gemini attempts
    max_retries = 3

    for attempt in range(max_retries):

        try:

            # ------------------------------------------------
            # First attempt
            # ------------------------------------------------

            if attempt == 0:

                message = (
                    "🤖 AppPilot AI is analyzing "
                    "your app idea..."
                )

            # ------------------------------------------------
            # Retry attempts
            # ------------------------------------------------

            else:

                message = (
                    f"🔄 Gemini is temporarily busy. "
                    f"Retrying... ({attempt + 1}/{max_retries})"
                )

            with st.spinner(message):

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        max_output_tokens=8000
                    )
                )

            # ------------------------------------------------
            # Check Gemini response
            # ------------------------------------------------

            if response and response.text:

                return response.text

            return (
                "⚠️ Gemini returned an empty response."
            )

        except Exception as e:

            error_message = str(e)

            # ------------------------------------------------
            # Temporary Gemini errors
            # ------------------------------------------------

            temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "overloaded" in error_message.lower()
                or "temporarily" in error_message.lower()
            )

            if temporary_error:

                # If this is the last attempt
                if attempt == max_retries - 1:

                    return (
                        "⚠️ **Gemini is temporarily unavailable.**\n\n"
                        "I tried automatically several times, "
                        "but Gemini is still experiencing "
                        "high demand.\n\n"
                        "Please wait a few minutes and "
                        "try again.\n\n"
                        f"Model used: `{MODEL}`"
                    )

                # Wait before next retry
                wait_time = 3 * (attempt + 1)

                time.sleep(wait_time)

                continue

            # ------------------------------------------------
            # Rate limit error
            # ------------------------------------------------

            if (
                "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            ):

                return (
                    "⚠️ **Gemini request limit reached.**\n\n"
                    "Please wait for the request limit "
                    "to reset and try again later."
                )

            # ------------------------------------------------
            # Model not found
            # ------------------------------------------------

            if (
                "404" in error_message
                or "NOT_FOUND" in error_message
            ):

                return (
                    "⚠️ **Gemini model not found.**\n\n"
                    f"Current model: `{MODEL}`\n\n"
                    "Please check the GEMINI_MODEL value "
                    "in Streamlit Secrets."
                )

            # ------------------------------------------------
            # Authentication error
            # ------------------------------------------------

            if (
                "401" in error_message
                or "UNAUTHENTICATED" in error_message
            ):

                return (
                    "⚠️ **Gemini authentication failed.**\n\n"
                    "Please check your GEMINI_API_KEY."
                )

            # ------------------------------------------------
            # Other API errors
            # ------------------------------------------------

            return (
                "⚠️ **Gemini API Error**\n\n"
                f"{error_message}"
            )


# ============================================================
# SECTION EXTRACTION
# ============================================================

def extract_section(
    full_text,
    section_name,
    next_section=None
):

    start_marker = f"## {section_name}"

    if start_marker not in full_text:

        return (
            "The AI did not generate this section."
        )

    start = full_text.find(start_marker)

    start = start + len(start_marker)

    if next_section:

        next_marker = f"## {next_section}"

        end = full_text.find(
            next_marker,
            start
        )

        if end == -1:

            end = len(full_text)

    else:

        end = len(full_text)

    return full_text[start:end].strip()


# ============================================================
# SESSION STATE
# ============================================================

if "ai_result" not in st.session_state:

    st.session_state["ai_result"] = None


# ============================================================
# HEADER
# ============================================================

st.title("🚀 AppPilot AI")

st.subheader(
    "AI-Powered App Development Assistant"
)

st.write(
    "Turn your app idea into a development plan, "
    "starter code, explanation, and learning roadmap."
)

st.divider()


# ============================================================
# STEP 1 — APP IDEA
# ============================================================

st.markdown(
    "### 💡 Step 1 — Enter Your App Idea"
)


app_idea = st.text_area(
    "What app do you want to build?",

    placeholder=(
        "Example: Build a mobile app for students "
        "to track their daily expenses."
    ),

    height=120
)


# ============================================================
# EXAMPLE IDEAS
# ============================================================

st.markdown(
    "#### Try an example"
)


col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# Expense Tracker
# ------------------------------------------------------------

with col1:

    if st.button(
        "💰 Expense Tracker",
        use_container_width=True
    ):

        st.session_state["idea"] = (
            "A student expense tracking app that "
            "allows users to record expenses, "
            "categorize expenses and view analytics."
        )

        st.rerun()


# ------------------------------------------------------------
# Study Planner
# ------------------------------------------------------------

with col2:

    if st.button(
        "📚 Study Planner",
        use_container_width=True
    ):

        st.session_state["idea"] = (
            "A study planner app that helps students "
            "create study schedules, track subjects "
            "and monitor study progress."
        )

        st.rerun()


# ------------------------------------------------------------
# Fitness App
# ------------------------------------------------------------

with col3:

    if st.button(
        "🏋️ Fitness App",
        use_container_width=True
    ):

        st.session_state["idea"] = (
            "A fitness application that allows users "
            "to track workouts, calories and daily "
            "fitness progress."
        )

        st.rerun()


# ============================================================
# LOAD EXAMPLE IDEA
# ============================================================

if (
    "idea" in st.session_state
    and not app_idea
):

    app_idea = st.session_state["idea"]


# ============================================================
# START BUILDING BUTTON
# ============================================================

if st.button(
    "🚀 Start Building",
    type="primary",
    use_container_width=True
):

    if not app_idea.strip():

        st.warning(
            "⚠️ Please enter an app idea first."
        )

    else:

        st.session_state["ai_result"] = None

        result = generate_app_analysis(
            app_idea
        )

        st.session_state["ai_result"] = result

        if result.startswith("⚠️"):

            st.error(
                "AppPilot AI could not complete "
                "the request."
            )

        else:

            st.success(
                "🎉 Your app development plan is ready!"
            )


# ============================================================
# DISPLAY AI RESULT
# ============================================================

if st.session_state["ai_result"]:

    result = st.session_state["ai_result"]


    # --------------------------------------------------------
    # ERROR RESULT
    # --------------------------------------------------------

    if result.startswith("⚠️"):

        st.error(result)


    # --------------------------------------------------------
    # SUCCESS RESULT
    # --------------------------------------------------------

    else:

        understand = extract_section(
            result,
            "UNDERSTAND",
            "PLAN"
        )

        plan = extract_section(
            result,
            "PLAN",
            "BUILD"
        )

        build = extract_section(
            result,
            "BUILD",
            "EXPLAIN"
        )

        explain = extract_section(
            result,
            "EXPLAIN",
            "LEARN"
        )

        learn = extract_section(
            result,
            "LEARN"
        )


        # ----------------------------------------------------
        # JOURNEY
        # ----------------------------------------------------

        st.divider()

        st.markdown(
            "## 🧭 Your AI Development Journey"
        )

        st.info(
            "💡 Prompt → Understand → Plan → "
            "Build → Explain → Learn"
        )


        # ----------------------------------------------------
        # TABS
        # ----------------------------------------------------

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🧠 Understand",
                "📋 Plan",
                "💻 Build",
                "🔍 Explain",
                "🎓 Learn"
            ]
        )


        # ====================================================
        # UNDERSTAND
        # ====================================================

        with tab1:

            st.header(
                "🧠 Understand"
            )

            st.write(
                "AI first understands what you want "
                "to build before generating code."
            )

            st.markdown(
                understand
            )


        # ====================================================
        # PLAN
        # ====================================================

        with tab2:

            st.header(
                "📋 Plan"
            )

            st.write(
                "AI converts the idea into features, "
                "screens, technology and development steps."
            )

            st.markdown(
                plan
            )


        # ====================================================
        # BUILD
        # ====================================================

        with tab3:

            st.header(
                "💻 Build"
            )

            st.write(
                "AI generates a starter implementation "
                "that developers can use as a starting point."
            )

            st.markdown(
                build
            )


        # ====================================================
        # EXPLAIN
        # ====================================================

        with tab4:

            st.header(
                "🔍 Explain"
            )

            st.write(
                "AI explains the application and "
                "generated implementation in simple language."
            )

            st.markdown(
                explain
            )


        # ====================================================
        # LEARN
        # ====================================================

        with tab5:

            st.header(
                "🎓 Learn"
            )

            st.write(
                "AI creates a learning path so the user "
                "can understand and continue developing "
                "the application."
            )

            st.markdown(
                learn
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AppPilot AI | AI-Powered App Development Assistant"
)
