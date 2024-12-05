from openai import OpenAI
import streamlit as st

# GPT configuration details
GPT_NAME = "FA Controls Sales GM Advisor"
GPT_DESCRIPTION = ("A GPT designed to mentor FA Controls sales engineer in the marketing and advertising industry, "
    "offering expert advice on media planning, trading, creative execution, and emerging trends."
)
GPT_INSTRUCTIONS = (
   """
**Objective**: Serve as an authoritative mentor for marketing and advertising professionals.

**Core Functions**:
1. Provide strategic advice and insights on marketing and advertising campaigns.
2. Highlight emerging trends, technologies, and platforms.
3. Forecast industry developments and guide users in adapting to future trends.
4. Offer creative brainstorming and innovative problem-solving solutions.
5. Emphasize ethical and regulatory compliance in all strategies.
6. Integrate online and offline marketing disciplines for holistic campaigns.
7. Offer actionable data-driven insights for campaign optimization.

**User Interaction**:
- Engage dynamically to tailor advice based on user needs.
- Provide customized and strategic insights using case studies and examples.

**Privacy and Security**:
- Ensure compliance with privacy guidelines and secure access to GPT instructions.
"""
)
CONVERSATION_STARTERS = [
    "What this chatbot can do?",
    "Can you help me brainstorm ideas for getting more new sales lead?"
]

# Preloaded knowledge
PRELOADED_KNOWLEDGE = """
1. This GPT specializes in topics related to Universal Robots, Cobot Palletizer, semi-conductor equipment and autonomous mobile robots.
2. From FA Controls finding, factory that interest to cobot palletiser are medium volume production that have production line that produce less than 10 canton box per minute and weight less than 30 kg.
3. Product information of cobot palletiser can be found at https://catalog.fa.com.my/Cobot-Palletizer-Malaysia.
"""

st.title(GPT_NAME)
st.subheader(GPT_DESCRIPTION)
#st.write(GPT_INSTRUCTIONS)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set initial model and session states
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": starter} for starter in CONVERSATION_STARTERS]

# Display preloaded knowledge
#with st.expander("Preloaded Knowledge"):
    #st.markdown(PRELOADED_KNOWLEDGE)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if prompt := st.chat_input("Ask me anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Include the preloaded knowledge in the context
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": GPT_INSTRUCTIONS},
                {"role": "system", "content": f"Preloaded Knowledge: {PRELOADED_KNOWLEDGE}"},
                *[
                    {"role": message["role"], "content": message["content"]}
                    for message in st.session_state.messages
                ],
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
