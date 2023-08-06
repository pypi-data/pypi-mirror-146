import pytest
from metagen.elements import Application, LayerTemplate


def test_element_duplicity():
    lt1 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    lt2 = LayerTemplate(applicationKey='app', nameInternal=f'lt', nameDisplay='lt')
    assert lt1.key == lt2.key
