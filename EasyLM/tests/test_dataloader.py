import unittest
import jax

from EasyLM.models.llama.llama_model import LLaMAConfig
from EasyLM.data import DatasetFactory, HuggingfaceDataset, TextProcessor


def _print_tree_shape(tree):
    shape = jax.tree_util.tree_map(jax.numpy.shape, tree)
    print(shape)


class DataloaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        tokenizer_config = LLaMAConfig.get_tokenizer_config(
            {"vocab_file": "/data/models/llama/tokenizer.model"}
        )
        dataset_config = DatasetFactory.get_default_config(
            {
                "type": "huggingface",
                "huggingface_dataset": HuggingfaceDataset.get_default_config(
                    {
                        "path": "Dahoas/full-hh-rlhf",
                        "split": "train",
                        "streaming": False,
                        "seq_length": 512,
                        "batch_size": 2,
                    }
                ),
                "text_processor": TextProcessor.get_default_config(
                    {"fields": "[prompt],chosen"}
                ),
            }
        )

        tokenizer = LLaMAConfig.get_tokenizer(tokenizer_config)
        cls.dataset = DatasetFactory.load_dataset(dataset_config, tokenizer)

    def test_dataset_iterator(self):
        batch = next(iter(DataloaderTests.dataset))
        print(batch)
        _print_tree_shape(batch)
