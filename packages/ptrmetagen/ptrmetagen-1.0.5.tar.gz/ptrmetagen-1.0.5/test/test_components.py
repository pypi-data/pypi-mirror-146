import pytest
from metagen.components import Filter
from metagen.utils import prepare_data_for_leaf
from test.fixtures import LAYER_TEMPLATE_1
from metagen import LayerTemplate


def test_filter_deserializations():
    assert Filter(**{"layerTemplateKey": "a0c8d936-2e52-4c31-8c55-ffefb1fed8c0"})


def test_set_fillter_from_Leaf():
    data = prepare_data_for_leaf(LAYER_TEMPLATE_1)
    lt = LayerTemplate(**data)
    assert Filter.set('layerTemplateKey', lt)
