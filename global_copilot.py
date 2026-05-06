import streamlit as st
from llm_copilot import generate_llm_response


def render_global_copilot(page_name="FinGuard AI", page_context=""):
    if "global_copilot_messages" not in st.session_state:
        st.session_state.global_copilot_messages = []

    st.markdown("""
    <style>
    div[data-testid="stPopover"] button {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
        border-radius: 999px !important;
        padding: 14px 20px !important;
        background: linear-gradient(135deg, #b45309, #f59e0b) !important;
        color: white !important;
        font-weight: 900 !important;
        border: 1px solid rgba(255,215,0,0.45) !important;
        box-shadow: 0 0 28px rgba(250,204,21,0.35) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.popover("🤖 FinGuard Copilot", use_container_width=False):

        st.markdown("### 🤖 FinGuard Global Copilot")
        st.caption(f"Current page: {page_name}")

        for role, message in st.session_state.global_copilot_messages[-6:]:
            with st.chat_message(role):
                st.markdown(message)

        user_input = st.text_area(
            "Ask about this page or the banking platform",
            placeholder="Example: What should management prioritize?",
            key=f"global_copilot_input_{page_name}"
        )

        if st.button("Ask Copilot", use_container_width=True, key=f"ask_global_{page_name}"):

            if user_input.strip():

                st.session_state.global_copilot_messages.append(
                    ("user", user_input)
                )

                prompt = f"""
You are FinGuard AI Global Copilot.

Current page:
{page_name}

Page context:
{page_context}

User question:
{user_input}

Answer as a banking AI assistant.
Be concise, practical, and executive-friendly.
"""

                response = generate_llm_response(prompt)

                st.session_state.global_copilot_messages.append(
                    ("assistant", response)
                )

                st.rerun()

        if st.button("Clear Copilot Chat", use_container_width=True, key=f"clear_global_{page_name}"):
            st.session_state.global_copilot_messages = []
            st.rerun()
