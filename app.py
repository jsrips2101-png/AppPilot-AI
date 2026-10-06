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

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "Gemini API key is missing. Please add GEMINI_API_KEY "
        "to your environment variables or Streamlit secrets."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

# IMPORTANT:
# Updated Gemini model
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if response.text:
            return response.text

        return "AI did not return any content."

    except Exception as e:
        return f"AI Error: {str(e)}"


# =========================================================
# UNDERSTAND
# =========================================================

def understand_app(app_idea):

    prompt = f"""
You are an expert AI App Development Assistant.

Understand this application idea:

{app_idea}

Give the answer in exactly this format:

### Application
Explain what the application does.

### Target Users
Explain who will use it.

### Problem
Explain the problem it solves.

### Main Goal
Explain the main purpose of the application.

### User Requirements
List the important requirements.

### Core Features
List the most important features.

Use simple language suitable for a student developer.
"""

    return ask_ai(prompt)


# =========================================================
# PLAN
# =========================================================

def plan_app(app_idea):

    prompt = f"""
You are an expert software architect.

Create a practical development plan for this application:

{app_idea}

Include:

1. Main Features
2. Screens / Pages
3. User Flow
4. Recommended Frontend
5. Recommended Backend
6. Database
7. APIs
8. AI Components if useful
9. Project Folder Structure
10. Development Steps

Keep the plan practical for a student or fresher.
Use simple explanations.
"""

    return ask_ai(prompt)


# =========================================================
# BUILD
# =========================================================

def build_app(app_idea):

    prompt = f"""
You are an AI coding assistant.

Application idea:

{app_idea}

Create a simple working prototype.

Use Python and Streamlit where possible.

Provide:

1. Project Structure
2. requirements.txt
3. Main app.py code
4. Explanation of the code

The code should be beginner-friendly and runnable.

Do not use unnecessary complex libraries.

Make sure the generated code is complete and properly formatted.
"""

    return ask_ai(prompt)


# =========================================================
# EXPLAIN
# =========================================================

def explain_app(app_idea):

    prompt = f"""
Explain how a beginner can understand and develop this application:

{app_idea}

Explain:

- Overall Architecture
- Frontend
- Backend
- Database
- APIs
- Important Functions
- Data Flow
- User Interaction

Use simple language and small examples.
"""

    return ask_ai(prompt)


# =========================================================
# LEARN
# =========================================================

def learn_app(app_idea):

    prompt = f"""
Create a beginner-friendly learning roadmap for developing:

{app_idea}

Create a step-by-step roadmap.

Include:

1. Concepts to Learn
2. Technologies to Learn
3. Coding Topics
4. Practice Tasks
5. Testing
6. Deployment

Also explain what the developer should learn next
to turn the prototype into a complete production application.

Keep it suitable for a student or fresher.
"""

    return ask_ai(prompt)


# =========================================================
# HEADER
# =========================================================

st.title("🚀 AppPilot AI")

st.subheader("AI-Powered App Development Assistant")

st.write(
    "Turn your app idea into a development plan, "
    "starter code, explanation, and learning roadmap."
)

st.divider()


# =========================================================
# APP IDEA INPUT
# =========================================================

st.markdown("### 💡 Step 1 — Enter Your App Idea")

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
            "A student expense tracking app that allows users "
            "to record expenses, categorize them and view analytics."
        )


with col2:

    if st.button("📚 Study Planner"):

        st.session_state["idea"] = (
            "A study planner app that helps students create "
            "study schedules, track subjects and monitor progress."
        )


with col3:

    if st.button("🏋️ Fitness App"):

        st.session_state["idea"] = (
            "A fitness app that allows users to track workouts, "
            "calories and daily fitness progress."
        )


# =========================================================
# LOAD EXAMPLE IDEA
# =========================================================

if "idea" in st.session_state and not app_idea:

    app_idea = st.session_state["idea"]


# =========================================================
# GENERATE
# =========================================================

if st.button("🚀 Start Building", type="primary"):

    if not app_idea.strip():

        st.warning("Please enter an app idea first.")

    else:

        with st.spinner("AI is analyzing your app idea..."):

            st.session_state["understand"] = (
                understand_app(app_idea)
            )

            st.session_state["plan"] = (
                plan_app(app_idea)
            )

            st.session_state["build"] = (
                build_app(app_idea)
            )

            st.session_state["explain"] = (
                explain_app(app_idea)
            )

            st.session_state["learn"] = (
                learn_app(app_idea)
            )

        st.success(
            "Your app development plan is ready! 🎉"
        )


# =========================================================
# RESULTS
# =========================================================

if "understand" in st.session_state:

    st.divider()

    st.markdown(
        "## 🧭 Your AI Development Journey"
    )

    st.info(
        "Prompt → Understand → Plan → Build → Explain → Learn"
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🧠 Understand",
            "📋 Plan",
            "💻 Build",
            "🔍 Explain",
            "🎓 Learn"
        ]
    )


    # =====================================================
    # UNDERSTAND TAB
    # =====================================================

    with tab1:

        st.header("🧠 Understand")

        st.write(
            "AI first understands what you want to build "
            "before generating code."
        )

        st.markdown(
            st.session_state["understand"]
        )


    # =====================================================
    # PLAN TAB
    # =====================================================

    with tab2:

        st.header("📋 Plan")

        st.write(
            "AI converts the idea into features, screens, "
            "technology and development steps."
        )

        st.markdown(
            st.session_state["plan"]
        )


    # =====================================================
    # BUILD TAB
    # =====================================================

    with tab3:

        st.header("💻 Build")

        st.write(
            "AI generates a starter implementation that "
            "developers can use as a starting point."
        )

        st.markdown(
            st.session_state["build"]
        )


    # =====================================================
    # EXPLAIN TAB
    # =====================================================

    with tab4:

        st.header("🔍 Explain")

        st.write(
            "AI explains the application and generated "
            "implementation in beginner-friendly language."
        )

        st.markdown(
            st.session_state["explain"]
        )


    # =====================================================
    # LEARN TAB
    # =====================================================

    with tab5:

        st.header("🎓 Learn")

        st.write(
            "AI creates a learning path so the user can "
            "understand and continue developing the application."
        )

        st.markdown(
            st.session_state["learn"]
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AppPilot AI | AI-Powered App Development Assistant"
)
