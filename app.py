import streamlit as st
from sentence_transformers import SentenceTransformer

st.set_page_config(
    page_title="Support Ticket Triage",
    page_icon="🎫"
)

CATEGORIES = {
    "Authentication": (
        "Users cannot sign in or access their account. "
        "Login failures, passwords, locked accounts, "
        "single sign-on, authentication, and access permissions."
    ),
    "Performance": (
        "The application is slow or takes too long to respond. "
        "High response times, slow database queries, "
        "delays, timeouts, and excessive resource usage."
    ),
    "Integration": (
        "Data exchange between systems is failing. "
        "API requests, webhooks, external services, "
        "data synchronization, imports, and exports."
    )
}


@st.cache_resource
def prepare_classifier(descriptions):
    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        device="cpu"
    )
    embeddings = model.encode_document(descriptions)
    return model, embeddings


st.title("🎫 Support Ticket Triage Assistant")
st.write("Suggest an issue category from a support ticket.")
st.caption("Local AI prototype. Use fictional tickets for testing.")

with st.form("ticket_form"):
    ticket = st.text_area(
        "Ticket description",
        height=180,
        placeholder=(
            "Example: Several users cannot sign in. "
            "They receive an invalid credentials message."
        )
    )
    environment = st.selectbox(
        "Affected environment",
        ["Unknown", "Production", "Test / development"]
    )

    impact = st.selectbox(
        "Business impact",
        [
            "Unknown",
            "Business process blocked",
            "Service degraded",
            "Information request"
        ]
    )

    affected_users = st.selectbox(
        "Affected users",
        [
            "Unknown",
            "One user",
            "Several users",
            "All users of the affected process"
        ]
    )

    workaround = st.selectbox(
        "Is there a usable workaround?",
        ["Unknown", "Yes", "No"]
    )
    submitted = st.form_submit_button("Analyze ticket")

if submitted:
    ticket = ticket.strip()

    if not ticket:
        st.warning("Please enter a ticket description.")
    else:
        names = list(CATEGORIES.keys())
        descriptions = list(CATEGORIES.values())

        with st.spinner("Analyzing the ticket..."):
            model, embeddings = prepare_classifier(descriptions)
            ticket_embedding = model.encode_query([ticket])
            scores = model.similarity(
                ticket_embedding, embeddings
            )[0]

        ranked_results = sorted(
            [
                {
                    "Category": name,
                    "Similarity": round(float(scores[index].item()), 3)
                }
                for index, name in enumerate(names)
            ],
            key=lambda result: result["Similarity"],
            reverse=True
        )

        suggested_category = ranked_results[0]["Category"]
        best_score = float(scores.max().item())

        if best_score < 0.30:
            st.subheader("Suggested category: Other / needs review")
            st.warning(
                "The ticket does not closely match our supported categories. "
                "A support engineer should review and route it."
            )
        else:
            st.subheader(f"Suggested category: {suggested_category}")
            st.write("Closest matching category description:")
            st.info(CATEGORIES[suggested_category])

        st.write("Comparison across all categories:")
        st.table(ranked_results)

        st.caption(
            "Similarity scores are not confidence percentages. "
            "Review the suggestion before assigning a ticket."
        )
if submitted and ticket.strip():
    st.subheader("Priority assessment")
    st.caption(
        "Illustrative project rubric. Recommendations require human review."
    )

    impact_fields = {
        "Affected environment": environment,
        "Business impact": impact,
        "Affected users": affected_users,
        "Workaround availability": workaround
    }

    missing_fields = [
        name for name, value in impact_fields.items()
        if value == "Unknown"
    ]

    if missing_fields:
        st.warning("Priority needs review: impact information is incomplete.")
        st.write("Confirm these details:")
        for field in missing_fields:
            st.write(f"- {field}")
    else:
        if (
            environment == "Production"
            and impact == "Business process blocked"
            and affected_users == "All users of the affected process"
            and workaround == "No"
        ):
            priority = "Urgent review"
            reason = (
                "A production business process is blocked for all "
                "affected users, with no usable workaround."
            )
        elif (
            environment == "Production"
            and impact == "Business process blocked"
        ):
            priority = "High"
            reason = (
                "A production business process is blocked. "
                "The scope and workaround should guide the response."
            )
        elif (
            environment == "Production"
            and impact == "Service degraded"
            and affected_users == "All users of the affected process"
            and workaround == "No"
        ):
            priority = "High"
            reason = (
                "Production service is degraded for all affected "
                "users, with no usable workaround."
            )
        else:
            priority = "Normal"
            reason = (
                "The supplied impact fields do not meet this demo's "
                "urgent or high-priority conditions."
            )

        st.info(f"Suggested priority: {priority}")
        st.write(reason)
ROUTING_GUIDANCE = {
    "Authentication": {
        "team": "Identity and access support",
        "actions": [
            "Collect the exact sign-in error and its timestamp.",
            "Confirm whether one user or multiple users are affected.",
            "Check account status and relevant authentication logs."
        ]
    },
    "Performance": {
        "team": "Application performance support",
        "actions": [
            "Identify the slow operation and measured response time.",
            "Confirm when the slowdown started and its scope.",
            "Collect relevant application and database performance data."
        ]
    },
    "Integration": {
        "team": "Integration and API support",
        "actions": [
            "Identify the affected integration and API operation.",
            "Collect the HTTP status, error details, and timestamp.",
            "Check integration logs and recent configuration changes."
        ]
    }
}

if submitted and ticket.strip():
    st.subheader("Suggested routing and next actions")

    if best_score < 0.30:
        st.write("Suggested team: General support triage")
        st.write("Recommended next actions:")
        st.write("- Clarify the request and desired outcome.")
        st.write("- Have a support engineer select the appropriate team.")
    else:
        guidance = ROUTING_GUIDANCE[suggested_category]
        st.write(f"Suggested team: {guidance['team']}")
        st.write("Recommended next actions:")

        for action in guidance["actions"]:
            st.write(f"- {action}")

    st.caption(
        "Example team names and predefined guidance. "
        "A support engineer reviews the suggestions."
    )
with st.expander("How categorization works"):
    st.write(
        "A pretrained embedding model compares the meaning of "
        "the ticket with each category description. "
        "The closest category is suggested."
    )
    st.write(
        "If the highest similarity score is below 0.30, "
        "the ticket is marked Other / needs review. "
        "This provisional threshold needs broader evaluation."
    )