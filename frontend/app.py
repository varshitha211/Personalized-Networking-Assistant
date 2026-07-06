import streamlit as st
import httpx
import json

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide",
)

if "page" not in st.session_state:
    st.session_state.page = "Generate Starters"
if "last_session_id" not in st.session_state:
    st.session_state.last_session_id = None
if "last_starters" not in st.session_state:
    st.session_state.last_starters = []


def switch_page(page: str):
    st.session_state.page = page
    st.rerun()


SIDEBAR_OPTIONS = [
    "Generate Starters",
    "Fact Check",
    "History",
    "Feedback History",
]

with st.sidebar:
    st.title("🤝 Networking Assistant")
    st.markdown("---")
    for option in SIDEBAR_OPTIONS:
        if st.button(option, use_container_width=True, key=f"nav_{option}"):
            switch_page(option)
    st.markdown("---")
    st.caption("Powered by DistilBERT + GPT-2")


def api_client() -> httpx.Client:
    return httpx.Client(base_url=API_BASE, timeout=60.0)


# --- PAGE: Generate Starters ---
if st.session_state.page == "Generate Starters":
    st.header("🚀 Generate Conversation Starters")
    st.markdown("Enter an event description and your interests to get AI-powered conversation starters.")

    col1, col2 = st.columns(2)
    with col1:
        event_desc = st.text_area(
            "Event Description",
            placeholder="e.g., AI for Sustainable Cities Conference",
            height=100,
        )
    with col2:
        interests = st.text_input(
            "Your Interests (comma-separated)",
            placeholder="e.g., climate change, urban planning",
        )

    if st.button("Generate Starters", type="primary", use_container_width=True):
        if not event_desc.strip():
            st.error("Please enter an event description.")
        else:
            with st.spinner("Analyzing event and generating starters..."):
                try:
                    with api_client() as client:
                        resp = client.post(
                            "/api/starters/generate",
                            json={"event_description": event_desc, "interests": interests},
                        )
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.last_session_id = data["session_id"]
                        st.session_state.last_starters = data["starters"]
                        st.success(f"Session #{data['session_id']} created!")
                    else:
                        st.error(f"API error: {resp.text}")
                except httpx.ConnectError:
                    st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")

    if st.session_state.last_starters:
        st.markdown("### 💬 Suggested Conversation Starters")
        starter_data = []
        try:
            with api_client() as client:
                resp = client.get(f"/api/starters/session/{st.session_state.last_session_id}")
            if resp.status_code == 200:
                starter_data = resp.json()
        except Exception:
            pass

        for i, starter_text in enumerate(st.session_state.last_starters):
            with st.container():
                st.markdown(f"**Starter {i + 1}:** {starter_text}")
                if starter_data and i < len(starter_data):
                    sid = starter_data[i]["StarterID"]
                    current_fb = starter_data[i].get("Feedback")
                    col_fb1, col_fb2, col_fb3 = st.columns([1, 1, 10])
                    with col_fb1:
                        fb_label = "👍" if current_fb == 1 else "👍"
                        if st.button(fb_label, key=f"up_{sid}"):
                            with api_client() as client:
                                client.post("/api/starters/feedback", json={"starter_id": sid, "feedback": 1})
                            st.rerun()
                    with col_fb2:
                        fb_label = "👎" if current_fb == -1 else "👎"
                        if st.button(fb_label, key=f"down_{sid}"):
                            with api_client() as client:
                                client.post("/api/starters/feedback", json={"starter_id": sid, "feedback": -1})
                            st.rerun()
                    with col_fb3:
                        if current_fb == 1:
                            st.caption("✅ Marked as useful")
                        elif current_fb == -1:
                            st.caption("❌ Marked as not useful")
                st.markdown("---")

# --- PAGE: Fact Check ---
elif st.session_state.page == "Fact Check":
    st.header("🔍 Quick Fact Verification")
    st.markdown("Search any topic to get a verified Wikipedia reference.")

    query = st.text_input("Search topic", placeholder="e.g., blockchain in healthcare")
    if st.button("Verify", type="primary", use_container_width=True) and query.strip():
        with st.spinner("Looking up Wikipedia..."):
            try:
                with api_client() as client:
                    resp = client.post("/api/factcheck/", json={"query": query})
                if resp.status_code == 200:
                    data = resp.json()
                    st.markdown(f"### Results for: {data['query']}")
                    st.markdown(f"**Status:** {data['status']}")
                    st.markdown(f"**Summary:** {data['summary']}")
                    if data["source_url"]:
                        st.markdown(f"**Source:** [{data['source_url']}]({data['source_url']})")
                    if data.get("suggestions"):
                        st.info(f"Did you mean: {', '.join(data['suggestions'])}")
                else:
                    st.error(f"API error: {resp.text}")
            except httpx.ConnectError:
                st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")

# --- PAGE: History ---
elif st.session_state.page == "History":
    st.header("📜 Conversation History")
    try:
        with api_client() as client:
            resp = client.get("/api/history/sessions")
        if resp.status_code == 200:
            sessions = resp.json()
            if not sessions:
                st.info("No sessions found yet. Generate some starters first!")
            for s in sessions:
                with st.expander(f"Session #{s['session_id']} — {s['timestamp'][:19] if s.get('timestamp') else 'N/A'}"):
                    st.markdown(f"**Event:** {s['event_description'][:100]}")
                    st.markdown(f"**Themes:** {s['themes']}")
                    if s.get("starters"):
                        st.markdown("**Starters:**")
                        for starter in s["starters"]:
                            fb = ""
                            if starter.get("Feedback") == 1:
                                fb = " 👍"
                            elif starter.get("Feedback") == -1:
                                fb = " 👎"
                            st.markdown(f"- {starter['StarterText']}{fb}")
        else:
            st.error(f"API error: {resp.text}")
    except httpx.ConnectError:
        st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")

# --- PAGE: Feedback History ---
elif st.session_state.page == "Feedback History":
    st.header("⭐ Feedback History")
    try:
        with api_client() as client:
            resp = client.get("/api/history/feedback")
        if resp.status_code == 200:
            items = resp.json()
            if not items:
                st.info("No feedback recorded yet. Thumbs up/down some starters!")
            for item in items:
                fb_icon = "👍" if item.get("Feedback") == 1 else "👎"
                st.markdown(f"{fb_icon} **{item['StarterText']}**")
                st.caption(f"Session #{item['SessionID']} | ID: {item['StarterID']}")
                st.markdown("---")
        else:
            st.error(f"API error: {resp.text}")
    except httpx.ConnectError:
        st.error("Cannot connect to the backend. Make sure the FastAPI server is running on port 8000.")
