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
    st.error("Gemini API key is missing. Please add GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# =========================================================
# AI FUNCTION
# =========================================================

def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


# =========================================================
# PROMPT BUILDER
# =========================================================

def generate_app_analysis(app_idea):

    prompt = f"""
You are an expert AI App Development Assistant.

The user wants to build this application:

{app_idea}

Analyze the application and provide a complete development guide.

Return the answer using EXACTLY these sections:

## UNDERSTAND
Explain:
- What the application does
- Target users
- Main problem solved
- Important user requirements

## PLAN
Provide:
- Main features
- Screens/pages
- User flow
- Recommended technology stack
- Database requirements
- API requirements if needed
- Basic architecture

## BUILD
Provide a small but useful starter implementation.
Explain what the code does.
Use Python/Streamlit where possible so the prototype can be demonstrated easily.

## EXPLAIN
Explain the generated implementation in simple language.
Explain the important functions and components.

## LEARN
Create a beginner-friendly learning path:
1.
2.
3.
4.
5.
6.

Also mention what the user should learn next to turn the prototype into a complete production application.

Keep the answer practical and easy to understand.
"""

    return ask_ai(prompt)


# =========================================================
# INDIVIDUAL AI FUNCTIONS
# =========================================================

def understand_app(app_idea):

    prompt = f"""
Understand this mobile/web application idea:

{app_idea}

Give the answer in this format:

### Application
### Target Users
### Problem
### Main Goal
### User Requirements
### Core Features

Use simple language.
"""

    return ask_ai(prompt)


def plan_app(app_idea):

    prompt = f"""
Create a complete development plan for this application:

{app_idea}

Include:

1. Features
2. Screens
3. User flow
4. Recommended frontend
5. Recommended backend
6. Database
7. APIs
8. AI components if useful
9. Project folder structure
10. Development steps

Keep it practical for a student developer.
"""

    return ask_ai(prompt)


def build_app(app_idea):

    prompt = f"""
You are an AI coding assistant.

Application idea:

{app_idea}

Create a simple working prototype implementation.

Use Python and Streamlit.

Provide:
1. Project structure
2. requirements.txt
3. Main app.py code
4. Explanation of how the code works

The code should be beginner-friendly and runnable.
Do not use unnecessary complex libraries.
"""

    return ask_ai(prompt)


def explain_app(app_idea):

    prompt = f"""
Explain how a beginner can understand and develop this application:

{app_idea}

Explain:

- Overall architecture
- Frontend
- Backend
- Database
- APIs
- Important functions
- Data flow
- How the user interacts with the application

Use simple language and examples.
"""

    return ask_ai(prompt)


def learn_app(app_idea):

    prompt = f"""
Create a learning roadmap for someone who wants to develop this application:

{app_idea}

Create a step-by-step roadmap from beginner to building the complete application.

Include:

1. Concepts to learn
2. Technologies to learn
3. Coding topics
4. Practice tasks
5. Testing
6. Deployment

Keep it suitable for a student/fresher.
"""

    return ask_ai(prompt)


# =========================================================
# HEADER
# =========================================================

st.title("🚀 AppPilot AI")

st.subheader("AI-Powered App Development Assistant")

st.write(
    "Turn your app idea into a development plan, starter code, "
    "explanation, and learning roadmap."
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

            st.session_state["understand"] = understand_app(app_idea)
            st.session_state["plan"] = plan_app(app_idea)
            st.session_state["build"] = build_app(app_idea)
            st.session_state["explain"] = explain_app(app_idea)
            st.session_state["learn"] = learn_app(app_idea)

        st.success("Your app development plan is ready! 🎉")


# =========================================================
# RESULTS
# =========================================================

if "understand" in st.session_state:

    st.divider()

    st.markdown("## 🧭 Your AI Development Journey")

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

    # -----------------------------------------------------
    # UNDERSTAND
    # -----------------------------------------------------

    with tab1:

        st.header("🧠 Understand")

        st.write(
            "AI first understands what you want to build "
            "before generating code."
        )

        st.markdown(st.session_state["understand"])


    # -----------------------------------------------------
    # PLAN
    # -----------------------------------------------------

    with tab2:

        st.header("📋 Plan")

        st.write(
            "AI converts the idea into features, screens, "
            "technology and development steps."
        )

        st.markdown(st.session_state["plan"])


    # -----------------------------------------------------
    # BUILD
    # -----------------------------------------------------

    with tab3:

        st.header("💻 Build")

        st.write(
            "AI generates a starter implementation that "
            "developers can use as a starting point."
        )

        st.markdown(st.session_state["build"])


    # -----------------------------------------------------
    # EXPLAIN
    # -----------------------------------------------------

    with tab4:

        st.header("🔍 Explain")

        st.write(
            "AI explains the application and generated "
            "implementation in beginner-friendly language."
        )

        st.markdown(st.session_state["explain"])


    # -----------------------------------------------------
    # LEARN
    # -----------------------------------------------------

    with tab5:

        st.header("🎓 Learn")

        st.write(
            "AI creates a learning path so the user can "
            "understand and continue developing the application."
        )

        st.markdown(st.session_state["learn"])


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "AppPilot AI | AI-Powered App Development Assistant"
)