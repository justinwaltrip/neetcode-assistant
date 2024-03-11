"""Streamlit chat interface with feedback.

Inspired by https://github.com/langchain-ai/langsmith-cookbook/blob/main/feedback-examples/streamlit/README.md
"""

import streamlit as st
from streamlit_feedback import streamlit_feedback

st.set_page_config(
    page_title="Capturing User Feedback",
    page_icon="🦜️️🛠️",
)

st.subheader("🦜🛠️ Chatbot with Feedback")

st.sidebar.markdown("## Feedback Scale")
feedback_option = (
    "thumbs" if st.sidebar.toggle(label="`Faces` ⇄ `Thumbs`", value=False) else "faces"
)

if st.sidebar.button("Clear message history"):
    print("Clearing message history")
    # TODO clear message history

for msg in st.session_state.langchain_messages:
    avatar = "🦜" if msg.type == "ai" else None
    with st.chat_message(msg.type, avatar=avatar):
        st.markdown(msg.content)


if prompt := st.chat_input(placeholder="Ask me a question!"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant", avatar="🦜"):
        message_placeholder = st.empty()

        # TODO call model
        # url = "http://127.0.0.1:8000/chat"

        # payload = {
        #     "problem_name": "Valid Anagram",
        #     "query": "What is an anagram?"
        # }

        # response = requests.post(url, json=payload)

        # print(response.json())
        full_response = None

        message_placeholder.markdown(full_response)

if st.session_state.get("run_id"):
    run_id = st.session_state.run_id
    feedback = streamlit_feedback(
        feedback_type=feedback_option,
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{run_id}",
    )

    # Define score mappings for both "thumbs" and "faces" feedback systems
    score_mappings = {
        "thumbs": {"👍": 1, "👎": 0},
        "faces": {"😀": 1, "🙂": 0.75, "😐": 0.5, "🙁": 0.25, "😞": 0},
    }

    # Get the score mapping based on the selected feedback option
    scores = score_mappings[feedback_option]

    if feedback:
        # Get the score from the selected feedback option's score mapping
        score = scores.get(feedback["score"])

        if score is not None:
            # # Formulate feedback type string incorporating the feedback option
            # # and score value
            # feedback_type_str = f"{feedback_option} {feedback['score']}"

            # # Record the feedback with the formulated feedback type string
            # # and optional comment
            # feedback_record = client.create_feedback(
            #     run_id,
            #     feedback_type_str,
            #     score=score,
            #     comment=feedback.get("text"),
            # )
            # st.session_state.feedback = {
            #     "feedback_id": str(feedback_record.id),
            #     "score": score,
            # }

            # TODO record feedback
            pass
        else:
            st.warning("Invalid feedback score.")
