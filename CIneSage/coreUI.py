
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

load_dotenv()

model = ChatMistralAI(model="mistral-large-4")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional Movie Information Extraction Assistant.

            Your task:
            Extract useful and important information from a movie
            paragraph and present it in a clean, organized,
            and readable format.

            Rules:
            - Do NOT add unnecessary explanations.
            - Extract only information available in the paragraph.
            - Do NOT invent or assume missing information.
            - If information is unavailable, mention "Not specified".
            - Keep descriptions concise and meaningful.
            - Avoid unnecessary repetition.

            Extract the following information:

            1. Movie Name
            2. Genre
            3. Director
            4. Cast Members
            5. Release Year
            6. Plot / Storyline
            7. Setting
            8. Music Composer
            9. IMDb Rating
            10. Critical Reception
            11. Major Themes
            12. Awards (if mentioned)
            13. Production Company (if mentioned)
            14. Language (if mentioned)
            15. Important Keywords

            Also generate a quick summary of the paragraph
            in 2-3 sentences.

            Output format:
            - Use clear headings.
            - Present extracted information using bullet points.
            - Keep the quick summary in a separate section.
            - Make the output easy to read and understand.

            Return only the extracted information and summary.
            """
        ),
        (
            "human",
            """
            Extract useful information from this paragraph:

            {paragraph}
            """
        )
    ]
)

# Streamlit UI

st.set_page_config(
    page_title="Movie Information Extractor",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Information Extractor")

st.write(
    "Extract important movie details and generate "
    "a quick summary from any movie paragraph."
)

para = st.text_area(
    "Enter your movie paragraph:",
    height=200,
    placeholder="Paste your movie paragraph here..."
)

if st.button("Extract Information", type="primary"):

    if para.strip():

        with st.spinner("Extracting movie information..."):

            final_prompt = prompt.invoke(
                {"paragraph": para}
            )

            response = model.invoke(final_prompt)

        st.subheader("Extracted Movie Information")
        if isinstance(response.content, list):
            output = "\n".join(
        block["text"]
        for block in response.content
        if block.get("type") == "text"
    )
        else:
          output = response.content

        st.markdown(output)


    else:
        st.warning("Please enter a paragraph first.")
