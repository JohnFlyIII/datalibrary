"""
Minimal Legal Document Schema
"""
from superlinked import framework as sl

class LegalDocument(sl.Schema):
    id: sl.IdField
    title: sl.String
    content: sl.String