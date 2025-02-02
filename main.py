import os
import sys

import polars as pl
import gradio as gr

# Local Packages
from src import TitleExtractor
from src import DatasetGenerator


if __name__ == "__main__":
    title_extractor = TitleExtractor()

    gr_interface = gr.Interface(
        fn=title_extractor.get_suggestions_from_image,
        inputs=[
            gr.Image(label="Image")
        ],
        outputs=[
            gr.CheckboxGroup(
                choices=[],
                label="Suggestions",
                info="Suggestion from OCR"
            ),       
            gr.Textbox(label="Suggested Words")
        ],
        title="Product Annotator",
    )
    
    gr_interface.launch(share=True)