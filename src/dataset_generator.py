import datetime as dt
import polars as pl
from config import logger

class DatasetGenerator:
    """Dataset Generator class to generate dataset from the given input."""

    def __init__(self):
        self.dataset = pl.DataFrame()
    
    @staticmethod
    def _get_dataset_filepath() -> str:
        """
        Get the dataset filepath.

        Returns:
            str: Dataset name
        """
        current_date = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        return f"datasets/{current_date}.parquet"

    def add_label(self, image_path: str, label: str) -> None:
        """
        Generate dataset from the given input
        Args:
            args: List of input arguments
        Returns:
            pl.DataFrame: Polars DataFrame
        """
        logger.log(
            "INFO",
            f"Adding entry to the dataset: image: path {image_path}, label: {label}",
            extra={"module": "dataset_generator.py"}
        )
        entry = pl.DataFrame(
            {
                "image_path": image_path,
                "product_label": label
            }
        )
        self.dataset = self.dataset.vstack(entry)
    
    def save_dataset(self) -> None:
        """
        Save the dataset to the given file path
        Args:
            file_path: File path to save the dataset
        """
        file_path = DatasetGenerator._get_dataset_filepath()
        logger.log(
            "INFO",
            f"Saving dataset to the file: {file_path}",
            extra={"module": "dataset_generator.py"}
        )
        self.dataset.write_parquet(file_path)