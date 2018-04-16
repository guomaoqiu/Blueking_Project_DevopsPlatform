# -*- coding: utf-8 -*-
"""Collections for component client"""
from .apis.cc import CollectionsCC
from .apis.job import CollectionsJOB
from .apis.bk_login import CollectionsBkLogin
from .apis.my_app import CollectionsMY_APP

# Available components
AVAILABLE_COLLECTIONS = {
    'cc': CollectionsCC,
    'job': CollectionsJOB,
    'bk_login': CollectionsBkLogin,
    'my_app': CollectionsMY_APP,
}
