from src import ProductAnnotator
from config import HOST, PORT


if __name__ == "__main__":
    annotator = ProductAnnotator()
    annotator.run(host=HOST, port=PORT)