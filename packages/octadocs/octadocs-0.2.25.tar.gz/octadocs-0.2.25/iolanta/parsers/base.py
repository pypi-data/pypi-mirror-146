from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Optional, TextIO

from iolanta.loaders.base import Loader
from iolanta.models import LDContext, LDDocument, Quad
from rdflib import URIRef


@dataclass(frozen=True)
class Parser(ABC):
    """
    Parser reads data from a file-like object and interprets them.

    For interpretation, it is also supplied with a context.
    """

    blank_node_prefix: str = ''

    def as_jsonld_document(
        self,
        raw_data: TextIO,
    ) -> LDDocument:
        """Generate a JSON-LD document."""
        raise NotImplementedError(
            f'{self}.as_json_document() is not implemented.',
        )

    def as_quad_stream(
        self,
        raw_data: TextIO,
        iri: Optional[URIRef],
        context: LDContext,
        root_loader: Loader,
    ) -> Iterable[Quad]:
        raise NotImplementedError(
            f'{self}.as_quad_stream() is not implemented.',
        )
