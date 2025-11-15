import sys
import time
from pathlib import Path
from datetime import datetime, timezone
import streamlit as st

#  Path setup 
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Imports 
try:
    from llm import agents, chat
    from mongodb.handlers import (
        create_complaint,
        get_complaints_by_status,
        update_complaint_status
    )
except ImportError:
    st.error("⚠️ Failed to import modules. Using mock data for UI preview.")

    def get_complaints_by_status(status):
        now = datetime.now(timezone.utc)
        if status == "open":
            return [
                {'_id': '1', 'resident_name': 'Pooja Gupta', 'block': 'B1', 'description': 'Road potholes on main road', 'category': 'Roads', 'severity_level': 'High', 'status': 'open', 'updated_at': now, 'action_recommendation': 'Repair the damaged road immediately.'},
                {'_id': '2', 'resident_name': 'Ravi Kumar', 'block': 'C2', 'description': 'Streetlight not working', 'category': 'Electricity', 'severity_level': 'Medium', 'status': 'open', 'updated_at': now, 'action_recommendation': 'Replace faulty bulb within 24 hours.'}
            ]
        elif status == "closed":
            return [
                {'_id': '3', 'resident_name': 'Priya Sharma', 'block': 'B2', 'description': 'Garbage overflow issue', 'category': 'Garbage', 'severity_level': 'High', 'status': 'closed', 'resolved_at': now, 'action_recommendation': 'Increase garbage pickup frequency.'},
            ]
        elif status == "junk":
            return [
                {'_id': '4', 'resident_name': 'Rajesh Kumar', 'block': 'A1', 'description': 'Tap water discolored', 'category': 'Water', 'severity_level': 'High', 'status': 'junk', 'updated_at': now, 'action_recommendation': 'Check water pipeline contamination source.'},
            ]
        return []

    def update_complaint_status(id, status, extra_fields=None):
        print(f"Updating complaint {id} → {status} | Extras: {extra_fields}")

    def create_complaint(data):
        print(f"Creating complaint: {data}")

    class MockAgents:
        def analyze_complaint(self, data):
            data['category'] = 'Uncategorized'
            data['severity_level'] = 'Medium'
            data['status'] = 'open'
            data['created_at'] = datetime.now(timezone.utc)
            return data
        def summarize_block_issues(self):
            return [{'block': 'A1', 'summary': 'Water issues are predominant.'}]
        def generate_complaint_summary(self, description):
            return f"Summary: {description[:70]}..."

    class MockChat:
        def chatbot(self, query):
            return "This is a mock AI response."

    agents = MockAgents()
    chat = MockChat()


# Streamlit page setup 
st.set_page_config(page_title="CivicPulse Dashboard", layout="wide")

# Global UI Styling 
st.markdown("""
    <style>
        h1, h2, h3, h4, h5 {
            font-family: 'Segoe UI', sans-serif;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
            
        .updated-card{
            animation: flash 0.8s ease-in-out;
        }
        @keyframes flash {
            0%{ background-color: #d1fae5;}
            100% {background-color: transparent;}
        }    

        /* Header styling */
        .kanban-header {
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 10px;
            text-align: center;
            color: white !important;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6);
            border-radius: 10px;
            padding: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        }

        /* Card text styling */
        div[data-testid="stVerticalBlockBorderWrapper"] h4 {
            margin-bottom: 5px;
            color: #154360;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] p {
            margin: 2px 0;
            color: #1C1C1C;
        }

        /* Complaint summary highlight */
        .summary-box {
            background-color: rgba(255, 255, 200, 0.4);
            border-left: 4px solid #facc15;
            padding: 6px 10px;
            border-radius: 6px;
            margin-top: 6px;
        }

        /* Action recommendation box */
        .action-box {
            background-color: rgba(52, 152, 219, 0.18);
            border-left: 4px solid #3498DB;
            padding: 6px 10px;
            border-radius: 6px;
            margin-top: 6px;
            color: #EAF2F8;
            font-weight:500;
        }

        /* Background color by status */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(p:contains("Pending")) {
            background-color: #FFFFFF !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(p:contains("Resolved")) {
            background-color: #E8F8F5 !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(p:contains("Junk")) {
            background-color: #FDEDEC !important;
        }

        /* Button styling */
        .stButton>button {
            border-radius: 6px;
            padding: 0.3rem 0.8rem;
            font-size: 13px !important;
        }

        /* Subheading styling */
        .subheading {
            font-size: 18px;
            color: #a5b4fc;
            text-align: left;
            margin-top: -10px;
            margin-bottom: 30px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)



# 📝 Report Complaint Tab

def report_complaint_tab():
    st.header("📢 Report a Civic Complaint")
    st.markdown("Submit your civic concerns quickly and transparently below 👇")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Your Name")
        with col2:
            location = st.text_input("🏢 Block of Residence")

        complaint_text = st.text_area("📝 Describe your complaint in detail")

        user_data = {
            "resident_name": name,
            "block": location,
            "description": complaint_text
        }

        if st.button("🚀 Submit Complaint"):
            if name and location and complaint_text:
                with st.spinner("Processing your complaint..."):
                    try:
                        processed_complaint = agents.analyze_complaint(user_data)
                        create_complaint(processed_complaint)
                        st.success("✅ Complaint submitted successfully!")
                    except Exception as e:
                        st.error(f"⚠️ Error processing complaint: {str(e)}")
            else:
                st.warning("⚠️ Please fill in all required fields.")



# 🗂️ Cards Dashboard

def cards_dashboard_tab():
    st.header("📊 Complaint Status Dashboard")
    st.markdown("Manage all complaints from one place ⚡")

    if "refresh_dashboard" not in st.session_state:
        st.session_state.refresh_dashboard = False

    pending = sorted(get_complaints_by_status("open"), key=lambda c: c.get("updated_at", datetime.now(timezone.utc)), reverse=True)
    resolved = sorted(get_complaints_by_status("closed"), key=lambda c: c.get("resolved_at", datetime.now(timezone.utc)), reverse=True)
    junk = sorted(get_complaints_by_status("junk"), key=lambda c: c.get("updated_at", datetime.now(timezone.utc)), reverse=True)

    def display_status_label(status):
        return {"open": "Pending", "closed": "Resolved", "junk": "Junk"}.get(status, "Unknown")

    col1, col2, col3 = st.columns(3)

    # Pending 
    with col1:
        st.markdown("<div class='kanban-header'>📋 Pending</div>", unsafe_allow_html=True)
        for c in pending:
            with st.container(border=True):
                st.markdown(f"<h4>🧑 {c['resident_name']} (Block: {c['block']})</h4>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Complaints:</b> {c['description']}</p>", unsafe_allow_html=True)
                summary_text = c.get("summary") or c.get("llm_summary") or "Summary not available."
                st.markdown(f"<div class='summary-box'><b>🧾 Complaint Summary:</b> {summary_text}</div>", unsafe_allow_html=True)
                action_text = c.get("action_recommendation", "No action recommendation available.")
                st.markdown(f"<div class='action-box'><b>🛠 Recommended Action:</b> {action_text}</div>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Category:</b> {c['category']} | <b>Severity:</b> {c['severity_level']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Status:</b> {display_status_label(c['status'])}</p>", unsafe_allow_html=True)
                st.markdown(f"<small><i>Last Updated: {c.get('updated_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d %H:%M:%S')}</i></small>", unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("✅ Move to Resolve", key=f"res_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "closed", {"resolved_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
                with b2:
                    if st.button("🚮 Move to Junk", key=f"jnk_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "junk", {"updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
            st.markdown("")

    # --- Resolved ---
    with col2:
        st.markdown("<div class='kanban-header'>✅ Resolved</div>", unsafe_allow_html=True)
        for c in resolved:
            with st.container(border=True):
                st.markdown(f"<h4>🧑 {c['resident_name']} (Block: {c['block']})</h4>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Complaints:</b> {c['description']}</p>", unsafe_allow_html=True)
                summary_text = c.get("summary") or c.get("llm_summary") or "Summary not available."
                st.markdown(f"<div class='summary-box'><b>🧾 Complaint Summary:</b> {summary_text}</div>", unsafe_allow_html=True)
                action_text = c.get("action_recommendation", "No action recommendation available.")
                st.markdown(f"<div class='action-box'><b>🛠 Recommended Action:</b> {action_text}</div>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Category:</b> {c['category']} | <b>Severity:</b> {c['severity_level']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Status:</b> {display_status_label(c['status'])}</p>", unsafe_allow_html=True)
                st.markdown(f"<small><i>Last Updated: {c.get('resolved_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d %H:%M:%S')}</i></small>", unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("↩️ Move to Pending", key=f"pend_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "open", {"updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
                with b2:
                    if st.button("🚮 Move to Junk", key=f"jnk_r_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "junk", {"updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
            st.markdown("")

    # --- Junk ---
    with col3:
        st.markdown("<div class='kanban-header'>🚮 Junk</div>", unsafe_allow_html=True)
        for c in junk:
            with st.container(border=True):
                st.markdown(f"<h4>🧑 {c['resident_name']} (Block: {c['block']})</h4>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Complaints:</b> {c['description']}</p>", unsafe_allow_html=True)
                summary_text = c.get("summary") or c.get("llm_summary") or "Summary not available."
                st.markdown(f"<div class='summary-box'><b>🧾 Complaint Summary:</b> {summary_text}</div>", unsafe_allow_html=True)
                action_text = c.get("action_recommendation", "No action recommendation available.")
                st.markdown(f"<div class='action-box'><b>🛠 Recommended Action:</b> {action_text}</div>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Category:</b> {c['category']} | <b>Severity:</b> {c['severity_level']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Status:</b> {display_status_label(c['status'])}</p>", unsafe_allow_html=True)
                st.markdown(f"<small><i>Last Updated: {c.get('updated_at', datetime.now(timezone.utc)).strftime('%Y-%m-%d %H:%M:%S')}</i></small>", unsafe_allow_html=True)

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("↩️ Move to Pending", key=f"pend_j_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "open", {"updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
                with b2:
                    if st.button("✅ Move to Resolve", key=f"res_j_{c['_id']}", use_container_width=True):
                        update_complaint_status(str(c["_id"]), "closed", {"resolved_at": datetime.now(timezone.utc), "updated_at": datetime.now(timezone.utc)})
                        st.session_state.refresh_dashboard = True
            st.markdown("")

    if st.session_state.refresh_dashboard:
        with st.spinner("Updating complaint status...."):
            time.sleep(0.3)
        st.session_state.refresh_dashboard = False
        st.toast("Complaint status updated successfully!", icon="🟢")
        st.rerun()


# =====================================================
# 📊 Admin Analytics Tab
# =====================================================
def admin_analytics_tab():
    st.header("📊 Admin Analytics Dashboard")
    st.markdown("Gain actionable insights across all civic complaint data 📈")

    if st.button("📈 Generate Summaries"):
        with st.spinner("Analyzing complaints across all blocks..."):
            summaries = agents.summarize_block_issues()
            if not summaries:
                st.warning("No data found.")
                return
            for s in summaries:
                with st.container(border=True):
                    st.markdown(f"<h4>🏢 Block {s['block']}</h4>", unsafe_allow_html=True)
                    st.markdown(s['summary'])
    else:
        st.info("🧠 Click **'Generate Summaries'** to view summarized block issues.")


# =====================================================
# 🤖 Chat Assistant Tab
# =====================================================
def chat_tab():
    st.header("🤖 CivicPulse Chat Assistant")
    st.markdown("Ask questions about civic issues or complaint statistics 💬")

    query = st.text_area("💬 Enter your question here:")
    if st.button("Send Query"):
        if not query.strip():
            st.warning("⚠️ Please enter a valid question.")
            return
        with st.spinner("🤔 Thinking..."):
            response = chat.chatbot(query)
            with st.container(border=True):
                st.markdown("#### 💡 AI Response:")
                st.markdown(response)


# =====================================================
# 🚀 Main Entry Point
# =====================================================
def main():
    st.title("🏙️ CivicPulse - Citizen Complaint Portal")
    st.markdown("<div class='subheading'>The AI-powered platform for smarter community complaint management and analysis.</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Report Complaint",
        "🗂️ Cards Dashboard",
        "📊 Admin Analytics",
        "🤖 Chat Assistant"
    ])

    with tab1:
        report_complaint_tab()
    with tab2:
        cards_dashboard_tab()
    with tab3:
        admin_analytics_tab()
    with tab4:
        chat_tab()


if __name__ == "__main__":
    main()
