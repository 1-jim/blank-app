from time import sleep

import streamlit as st
from streamlit.components.v1 import html
from streamlit_js_eval import streamlit_js_eval

def show_mermaider(code: str, font_size: int = 14, graph_height: int = 400) -> None:

    if "mermaid_svg_height" not in st.session_state:
        st.session_state["mermaid_svg_height"] = graph_height

    if "mermaid_previous_mermaid" not in st.session_state:
        st.session_state["mermaid_previous_mermaid"] = ""

    if "mermaid_previous_font_size" not in st.session_state:
        st.session_state["mermaid_previous_font_size"] = 14
        font_size = st.slider("Font size", 10, 30, 14)

    html(
        f"""
        <pre class="mermaid">
            {code}
        </pre>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: "default", themeVariables: {{ fontSize: "{font_size}px" }} }});
        </script>
        """,
        height=st.session_state["mermaid_svg_height"] + 10,
    )

    if (
        code != st.session_state["mermaid_previous_mermaid"]
        or font_size != st.session_state["mermaid_previous_font_size"]
    ):
        st.session_state["mermaid_previous_mermaid"] = code
        st.session_state["mermaid_previous_font_size"] = font_size
        sleep(1)
        streamlit_js_eval(
            js_expressions='parent.document.getElementsByTagName("iframe")[0].contentDocument.getElementsByClassName("mermaid")[0].getElementsByTagName("svg")[0].getBBox().height',
            key="svg_height",
        )