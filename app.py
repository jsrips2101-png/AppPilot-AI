import os
import streamlit as st
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AppPilot AI",
    page_icon="🚀",
    layout="wide"
)

# =========================================================
# GEMINI CONFIGURATION
# =========================================================

# First try Streamlit Secrets
API_KEY = st.secrets.get("GEMINI_API_KEY")

# If Streamlit Secrets is not available, try environment variable
if not API_KEY:
    API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Please add GEMINI_API_KEY in Streamlit Secrets."
    )
    st.stop()


# Create Gemini client
client = genai.Client(api_key=API_KEY)


# Gemini model
MODEL = st.secrets.get(
    "GEMINI_MODEL",
    os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
)


# =========================================================
# GEMINI AI FUNCTION
# =========================================================

def generate_complete_analysis(app_idea):

    prompt = f"""
You are AppPilot AI, an expert AI-powered application
development assistant.

The user wants to build this application:

--------------------------------------------------
{app_idea}
--------------------------------------------------

Analyze the application and provide a complete beginner-friendly
development guide.

IMPORTANT:
Return the answer using EXACTLY these five sections:

## UNDERSTAND

Explain:

- What the application does
- Target users
- Problem solved
- Main goal
- Important user requirements
- Core features

## PLAN

Explain:

- Main features
- Screens/pages
- User flow
- Recommended frontend
- Recommended backend
- Database requirements
- API requirements
- AI components if useful
- Basic architecture
- Project folder structure
- Development steps

Keep the recommendations practical for a student/fresher.

## BUILD

Create a small but useful starter implementation.

Use Python and Streamlit where possible.

Provide:

1. Project structure
2. requirements.txt
3. Main app.py code
4. Explanation of the generated code

The code should be beginner-friendly and runnable.

Do not use unnecessary complex libraries.

IMPORTANT:
Put code inside proper Markdown code blocks.

## EXPLAIN

Explain the generated implementation in simple language.

Explain:

- Overall architecture
- Frontend
- Backend
- Database
- APIs
- Important functions
- Data flow
- How the user interacts with the application

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

Keep the explanation practical and easy to understand.

Do not invent requirements that are not related to the application idea.

Use simple language suitable for a student or fresher.
"""


    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response and response.text:

            return response.text

        return (
            "⚠️ Gemini did not return any content. "
            "Please try again."
        )

    except Exception as e:

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:

            return (
                "⚠️ Gemini is temporarily busy or unavailable.\n\n"
                "Please wait for a few seconds and click "
                "**Start Building** again."
            )

        elif "404" in error_message or "NOT_FOUND" in error_message:

            return (
                "⚠️ The Gemini model is unavailable.\n\n"
                f"Current model: `{MODEL}`\n\n"
                "Please check your Gemini model configuration."
            )

        elif "401" in error_message or "UNAUTHENTICATED" in error_message:

            return (
                "⚠️ Gemini API authentication failed.\n\n"
                "Please check your GEMINI_API_KEY."
            )

        elif "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

            return (
                "⚠️ Gemini API request limit was reached.\n\n"
                "Please wait and try again later."
            )

        else:

            return (
                "⚠️ AI Error:\n\n"
                f"{error_message}"
            )


# =========================================================
# EXTRACT SECTIONS FROM GEMINI RESPONSE
# =========================================================

def extract_section(text, section_name, next_section=None):

    start_marker = f"## {section_name}"

    if start_marker not in text:
        return (
            f"### {section_name}\n\n"
            "The AI did not generate this section."
        )

    start = text.find(start_marker)

    start = start + len(start_marker)

    if next_section:

        next_marker = f"## {next_section}"

        end = text.find(next_marker, start)

        if end == -1:
            end = len(text)

    else:

        end = len(text)

    section = text[start:end].strip()

    return section


# =========================================================
# SESSION STATE
# =========================================================

if "ai_result" not in st.session_state:

    st.session_state["ai_result"] = None


# =========================================================
# HEADER
# =========================================================

st.title("🚀 AppPilot AI")

st.subheader(
    "AI-Powered App Development Assistant"
)

st.write(
    "Turn your app idea into a development plan, "
    "starter code, explanation, and learning roadmap."
)

st.divider()


# =========================================================
# APP IDEA INPUT
# =========================================================

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


# =========================================================
# QUICK EXAMPLES
# =========================================================

st.markdown("#### Try an example")

col1, col2, col3 = st.columns(3)


with col1:

    if st.button("💰 Expense Tracker"):

        st.session_state["idea"] = (
            "A student expense tracking app that allows "
            "users to record expenses, categorize them "
            "and view analytics."
        )

        st.rerun()


with col2:

    if st.button("📚 Study Planner"):

        st.session_state["idea"] = (
            "A study planner app that helps students "
            "create study schedules, track subjects "
            "and monitor progress."
        )

        st.rerun()


with col3:

    if st.button("🏋️ Fitness App"):

        st.session_state["idea"] = (
            "A fitness app that allows users to track "
            "workouts, calories and daily fitness progress."
        )

        st.rerun()


# =========================================================
# LOAD EXAMPLE IDEA
# =========================================================

if "idea" in st.session_state and not app_idea:

    app_idea = st.session_state["idea"]


# =========================================================
# START BUILDING
# =========================================================

if st.button(
    "🚀 Start Building",
    type="primary",
    use_container_width=True
):

    if not app_idea.strip():

        st.warning(
            "Please enter an app idea first."
        )

    else:

        # Remove previous result
        st.session_state["ai_result"] = None

        with st.spinner(
            "🤖 AppPilot AI is analyzing your app idea..."
        ):

            result = generate_complete_analysis(
                app_idea
            )

            st.session_state["ai_result"] = result

        # Check whether AI returned an error
        if result.startswith("⚠️"):

            st.error(
                "AppPilot AI could not complete the request."
            )

        else:

            st.success(
                "Your app development plan is ready! 🎉"
            )


# =========================================================
# RESULTS
# =========================================================

if st.session_state["ai_result"]:

    result = st.session_state["ai_result"]

    # -----------------------------------------------------
    # ERROR RESULT
    # -----------------------------------------------------

    if result.startswith("⚠️"):

        st.error(result)


    # -----------------------------------------------------
    # SUCCESS RESULT
    # -----------------------------------------------------

    else:

        # Extract five sections
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


        st.divider()

        st.markdown(
            "## 🧭 Your AI Development Journey"
        )

        st.info(
            "💡 Prompt → Understand → Plan → Build → "
            "Explain → Learn"
        )


        # =================================================
        # TABS
        # =================================================

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "🧠 Understand",
                "📋 Plan",
                "💻 Build",
                "🔍 Explain",
                "🎓 Learn"
            ]
        )


        # =================================================
        # UNDERSTAND
        # =================================================

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


        # =================================================
        # PLAN
        # =================================================

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


        # =================================================
        # BUILD
        # =================================================

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


        # =================================================
        # EXPLAIN
        # =================================================

        with tab4:

            st.header(
                "🔍 Explain"
            )

            st.write(
                "AI explains the application and generated "
                "implementation in beginner-friendly language."
            )

            st.markdown(
                explain
            )


        # =================================================
        # LEARN
        # =================================================

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


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AppPilot AI | AI-Powered App Development Assistant"
)
