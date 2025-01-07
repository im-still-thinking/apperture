import streamlit as st
from src.processor.metrics_processor import MetricsProcessor
from src.lib.formatting import format_response_as_table
from src.config.settings import initialize_session_state, APP_TITLE, APP_ICON

def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON)
    st.title(APP_TITLE)

    initialize_session_state()

    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("Enter your Groq API key:", type="password")
        if api_key:
            if st.session_state.processor is None:
                st.session_state.processor = MetricsProcessor(api_key)
                st.success("API key configured successfully!")

    with st.expander("Show Example Queries"):
        st.markdown("""
        Try these example queries:
        - Get me Flipkart's GMV for the last one year
        - Show me Target's revenue for Q4
        - Compare this with Walmart
        - What was Amazon's growth rate last quarter?
        """)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                # Display the query response as a table
                if isinstance(message["content"], list):
                    if "error" in message["content"][0]:
                        st.error(message["content"][0]["details"])
                    else:
                        st.dataframe(
                            format_response_as_table(message["content"]),
                            use_container_width=True,
                            hide_index=True
                        )
                else:
                    st.markdown(message["content"])

    if prompt := st.chat_input("Ask about business metrics..."):
        if not api_key:
            st.error("Please enter your Groq API key in the sidebar first.")
            return
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.processor.process_query(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            if "error" in response[0]:
                st.error(response[0]["details"])
            else:
                st.dataframe(
                    format_response_as_table(response),
                    use_container_width=True,
                    hide_index=True
                )

if __name__ == "__main__":
    main()