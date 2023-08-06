class NotFoundError(Exception):
    """Raised when not found."""
    pass

class ElasticsearchError(Exception):
    """Raised elasticsearch Error."""
    pass

class DocPathsWithoutValuesAggregationError(Exception):
    """Raised when the user defines aggregations with include_values=False and include_doc_paths=True"""
    pass
