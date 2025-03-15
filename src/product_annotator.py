# Built-in Packages
from typing import List, Optional

# Interface
import gradio as gr
from tqdm import tqdm

# Local Packages
from src import TextExtractor
from src import DatasetGenerator
from config import logger
from config import MIN_TEXT_LENGTH

import sys
import signal

def signal_handler(sig, frame):
    logger.log(
        "INFO",
        "Exiting the application",
        extra={"module": "product_annotator.py"}
    )
    ProductAnnotator().dataset.save_dataset()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class ProductAnnotator:
    """The Annotation tool for Product Labeling."""
    dataset = DatasetGenerator()

    def __init__(self):
        self.labels: List[str] = []
        self.text_extractor = TextExtractor()

    def process_image(self, image_filepath) -> List[str]:
        """Process the image to extract text suggestions."""
        try:
            results = self.text_extractor.get_suggestions_from_image(image_filepath)
            return [result for result in results if len(result) > MIN_TEXT_LENGTH]
        except Exception as e:
            logger.log(
                "ERROR",
                f"Error processing image: {image_filepath}, {e}",
                extra={"module": "product_annotator.py"}
            )
            return []

    def merge_labels(self, *args) -> str:
        """Merge selected labels into a final label."""
        self.labels.extend(args)
        return " ".join(self.labels)

    @classmethod
    def submit_label(cls, image_path: str, label: str) -> None:
        """Submit the final label to the dataset."""
        try:
            cls.dataset.add_label(image_path=image_path, label=label)
            logger.log(
                "INFO",
                f"Label added to the dataset: {label}",
                extra={"module": "product_annotator.py"}
            )
        except Exception as e:
            logger.log(
                "ERROR",
                f"Error adding label to the dataset: {label}, {e}",
                extra={"module": "product_annotator.py"}
            )
            cls.dataset.save_dataset()

    def build_ui(self) -> gr.Interface:
        """Creates UI-interface for the annotation tool."""
        with gr.Blocks() as demo:
            gr.Markdown("## Upload an Image to annotate the Product Label")
            suggestions = gr.State([])

            with gr.Row():
                with gr.Column():
                    image_input = gr.Image(type='filepath', label="Upload Image")

                with gr.Column():
                    final_label = gr.Textbox(label="Final Label", interactive=True)

                    @gr.render(inputs=suggestions)
                    def show_suggestions(suggestions: List[str]):
                        if not suggestions:
                            gr.Markdown("## No Input Provided")
                        else:
                            gr.Markdown("## Suggestions")
                            with gr.Row():
                                for suggestion in suggestions:
                                    suggestion_button = gr.Button(suggestion)
                                    suggestion_button.click(
                                        fn=self.merge_labels,
                                        inputs=suggestion_button,
                                        outputs=final_label
                                    )

            with gr.Row():
                process_button = gr.Button("Submit", variant="primary")
                clear_button = gr.ClearButton(components=[image_input, final_label], variant="secondary")
                clear_button.click(fn=lambda: self.labels.clear())

            flag_button = gr.Button("Submit to Dataset")
            flag_button.click(fn=self.submit_label, inputs=[image_input, final_label])

            process_button.click(fn=self.process_image,
                                 inputs=image_input,
                                 outputs=suggestions, show_progress=True)

        return demo

    def run(self, host: Optional[str] = "0.0.0.0",
            port: Optional[int] = 8000,
            share: Optional[bool] = True) -> None:
        """
        Run the Gradio web-interface.

        Args:
            host (str): Server name to run the application
            port (int): Port number for the server
            share (bool): Share the application

        Returns:
            None
        """
        try:
            ui = self.build_ui()
            logger.log(
                "INFO",
                "Application started",
                extra={"module": "product_annotator.py"}
            )
            ui.launch(server_name=host, server_port=port, share=share)
        except Exception as e:
            logger.log(
                "ERROR",
                f"Error running the application: {e}",
                extra={"module": "product_annotator.py"}
            )
