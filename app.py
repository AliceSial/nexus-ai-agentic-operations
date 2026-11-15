from __future__ import annotations
import os
import streamlit as st
from dotenv import load_dotenv
from nexus.graph import analyze_request
from nexus.storage import save_interaction, load_interactions

load_dotenv()
st.set_page_config(page_title="NEXUS AI | Operations Copilot", page_icon="✦", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0b1020 0%, #101a2e 55%, #111827 100%); color:#eef2ff;}
[data-testid="stMetric"] {background:rgba(255,255,255,.055); padding:16px; border:1px solid rgba(148,163,184,.2); border-radius:14px;}
.panel {background:rgba(255,255,255,.045); border:1px solid rgba(148,163,184,.18); padding:18px; border-radius:16px;}
.small-muted {color:#a5b4fc;font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("✦ NEXUS AI")
st.caption("AGENTIC BUSINESS INTELLIGENCE  /  LEAD & SUPPORT OPERATIONS")
st.markdown("Turn incoming business messages into structured intelligence, grounded knowledge, and review-ready actions.")

df = load_interactions()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Interactions analyzed", len(df))
c2.metric("High-priority leads", int((df["priority"] == "High").sum()) if not df.empty else 0)
c3.metric("Sales requests", int((df["category"] == "sales").sum()) if not df.empty else 0)
c4.metric("LLM mode", "Enabled" if os.getenv("GROQ_API_KEY", "").strip() else "Demo")

st.divider()
left, right = st.columns([1.05, .95], gap="large")
with left:
    st.subheader("Analyze a new request")
    with st.form("request_form"):
        message = st.text_area(
            "Customer message",
            placeholder="Example: We need an AI support assistant for our online store...",
            height=170
        )
        budget = st.number_input("Estimated budget (USD)", min_value=0, max_value=100000, value=2500, step=250)
        urgency = st.selectbox("Timeline", ["Normal", "Soon", "Urgent"])
        submitted = st.form_submit_button("Run agent workflow", type="primary", use_container_width=True)
    if submitted:
        if not message.strip():
            st.warning("Please enter a customer message.")
        else:
            with st.spinner("NEXUS agents are analyzing the request..."):
                result = analyze_request(message.strip(), float(budget), urgency)
                result["message"] = message.strip()
                save_interaction(result)
                st.session_state["latest_result"] = result
                st.success("Analysis complete. Review the recommendation before taking action.")

with right:
    st.subheader("Workflow intelligence")
    if "latest_result" in st.session_state:
        r = st.session_state["latest_result"]
        a, b = st.columns(2)
        a.metric("Lead score", f"{r.get('score', 0)}/100")
        b.metric("Priority", r.get("priority", "—"))
        st.write(f"**Request category:** `{r.get('category', 'general').title()}`")
        st.write(f"**Drafting engine:** {r.get('provider', '—')}")
        st.write("**Why this score?**")
        for reason in r.get("reasons", []):
            st.write(f"- {reason}")
        st.markdown("**Retrieved knowledge**")
        if r.get("context"):
            for item in r["context"]:
                st.markdown(f"- **{item['title']}** · relevance {item['relevance']}")
        else:
            st.caption("No sufficiently relevant knowledge passage was found.")
        st.markdown("**Response draft — human approval required**")
        edited = st.text_area("Edit before using", value=r.get("draft", ""), height=180, key="draft_editor")
        st.caption("NEXUS does not send this message. Copy it only after reviewing and approving it.")
        st.button("Mark reviewed", disabled=True, help="Approval tracking is a planned feature; no message is sent.")
    else:
        st.markdown('<div class="panel"><h3>Awaiting your first request</h3><p class="small-muted">The workflow will classify intent, score lead priority, retrieve internal guidance, and draft a response.</p></div>', unsafe_allow_html=True)

st.divider()
st.subheader("Recent activity")
if df.empty:
    st.info("No activity yet. Run your first analysis to populate this table.")
else:
    display = df[["created_at", "category", "priority", "score", "message"]].head(10)
    st.dataframe(display, use_container_width=True, hide_index=True)
    st.download_button("Download interaction history (CSV)", df.to_csv(index=False), "nexus_interactions.csv", "text/csv")

with st.expander("How NEXUS works"):
    st.markdown("""
    **Agent workflow:** classify → score → retrieve → draft.

    **Retrieval:** local TF-IDF search over `data/knowledge_base.json`.

    **LLM:** optional Groq integration. Without a key, a transparent rule-based demo response is used.

    **Safety:** generated content is a draft. Human review is required before customer communication.
    """)
