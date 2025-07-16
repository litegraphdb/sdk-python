from datetime import datetime
import pytest
from unittest.mock import Mock
from uuid import UUID

from litegraph.enums.vector_search_domain_enum import VectorSearchDomainEnum
from litegraph.models.graphs import GraphModel
from litegraph.models.node import NodeModel
from litegraph.models.edge import EdgeModel
from litegraph.models.vector_metadata import VectorMetadataModel
from litegraph.models.vector_search_request import VectorSearchRequestModel
from litegraph.models.vector_search_response import VectorSearchResultModel
from litegraph.resources.vectors import Vector


@pytest.fixture
def mock_client(monkeypatch):
    """Create a mock client and configure it."""
    client = Mock()
    client.base_url = "http://test-api.com"
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client


@pytest.fixture
def valid_vector_data():
    """Fixture providing valid vector metadata."""
    return VectorMetadataModel(
        guid="550e8400-e29b-41d4-a716-446655440000",
        tenant_guid="550e8400-e29b-41d4-a716-446655440001", 
        graph_guid="550e8400-e29b-41d4-a716-446655440002",
        embeddings=[0.1, 0.2, 0.3],
        content="",
        dimensionality=3,
        created_utc="2024-01-01T00:00:00Z",
        last_update_utc="2024-01-01T00:00:00Z"
    )


@pytest.fixture
def valid_search_result() -> list[VectorSearchResultModel]:
    """Fixture providing valid vector search result."""
    return [
        VectorSearchResultModel(
            score=0.95,
            vector=valid_vector_data,
            distance=0.95,
            inner_product=0.95,
            graph=GraphModel(
                guid="550e8400-e29b-41d4-a716-446655440002",
                tenant_guid="550e8400-e29b-41d4-a716-446655440001",
            ),
            node=NodeModel(
                guid="550e8400-e29b-41d4-a716-446655440003",
                tenant_guid="550e8400-e29b-41d4-a716-446655440001",
            ),
            edge=EdgeModel(
                guid="550e8400-e29b-41d4-a716-446655440004",
                tenant_guid="550e8400-e29b-41d4-a716-446655440001",
            )
        )
    ]


def test_search_vectors_graph_domain(mock_client, valid_search_result):
    """Test searching vectors in graph domain."""
    mock_client.request.return_value = valid_search_result
    tenant_guid = UUID("550e8400-e29b-41d4-a716-446655440001")
    embeddings = [0.1, 0.2, 0.3]

    result = Vector.search_vectors(
        domain=VectorSearchDomainEnum.Graph,
        embeddings=embeddings,
        tenant_guid=tenant_guid,
        labels=["label1"],
        tags={"key1": "value1"}
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].distance == 0.95
    assert result[0].inner_product == 0.95
    assert result[0].graph.guid == "550e8400-e29b-41d4-a716-446655440002"
    assert result[0].node.guid == "550e8400-e29b-41d4-a716-446655440003"
    assert result[0].edge.guid == "550e8400-e29b-41d4-a716-446655440004"


def test_search_vectors_node_domain(mock_client, valid_search_result):
    """Test searching vectors in node domain."""
    mock_client.request.return_value = valid_search_result
    tenant_guid = UUID("550e8400-e29b-41d4-a716-446655440001")
    graph_guid = UUID("550e8400-e29b-41d4-a716-446655440002")
    embeddings = [0.1, 0.2, 0.3]

    result = Vector.search_vectors(
        domain=VectorSearchDomainEnum.Node,
        embeddings=embeddings,
        tenant_guid=tenant_guid,
        graph_guid=graph_guid
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].distance == 0.95
    assert result[0].inner_product == 0.95
    assert result[0].graph.guid == "550e8400-e29b-41d4-a716-446655440002"
    assert result[0].node.guid == "550e8400-e29b-41d4-a716-446655440003"
    assert result[0].edge.guid == "550e8400-e29b-41d4-a716-446655440004"
    mock_client.request.assert_called_once()


def test_search_vectors_edge_domain(mock_client, valid_search_result):
    """Test searching vectors in edge domain."""
    mock_client.request.return_value = valid_search_result
    tenant_guid = UUID("550e8400-e29b-41d4-a716-446655440001")
    graph_guid = UUID("550e8400-e29b-41d4-a716-446655440002")
    embeddings = [0.1, 0.2, 0.3]

    result = Vector.search_vectors(
        domain=VectorSearchDomainEnum.Edge,
        embeddings=embeddings,
        tenant_guid=tenant_guid,
        graph_guid=graph_guid
    )

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0].distance == 0.95
    assert result[0].inner_product == 0.95
    assert result[0].graph.guid == "550e8400-e29b-41d4-a716-446655440002"
    assert result[0].node.guid == "550e8400-e29b-41d4-a716-446655440003"
    assert result[0].edge.guid == "550e8400-e29b-41d4-a716-446655440004"
    mock_client.request.assert_called_once()


def test_search_vectors_missing_graph_guid():
    """Test searching vectors without graph GUID for node/edge domain raises error."""
    tenant_guid = UUID("550e8400-e29b-41d4-a716-446655440001")
    embeddings = [0.1, 0.2, 0.3]

    with pytest.raises(ValueError, match="Graph GUID must be supplied"):
        Vector.search_vectors(
            domain=VectorSearchDomainEnum.Node,
            embeddings=embeddings,
            tenant_guid=tenant_guid
        )

    with pytest.raises(ValueError, match="Graph GUID must be supplied"):
        Vector.search_vectors(
            domain=VectorSearchDomainEnum.Edge,
            embeddings=embeddings,
            tenant_guid=tenant_guid
        )


def test_search_vectors_empty_embeddings():
    """Test searching vectors with empty embeddings raises error."""
    tenant_guid = UUID("550e8400-e29b-41d4-a716-446655440001")

    with pytest.raises(ValueError, match="must include at least one value"):
        Vector.search_vectors(
            domain=VectorSearchDomainEnum.Graph,
            embeddings=[],
            tenant_guid=tenant_guid
        )


def test_vector_metadata_model():
    """Test vector metadata model validation."""
    valid_data = {
        "GUID": "550e8400-e29b-41d4-a716-446655440000",
        "TenantGUID": "550e8400-e29b-41d4-a716-446655440001",
        "GraphGUID": "550e8400-e29b-41d4-a716-446655440002",
        "NodeGUID": "550e8400-e29b-41d4-a716-446655440003",
        "EdgeGUID": "550e8400-e29b-41d4-a716-446655440004",
        "Embeddings": [0.1, 0.2, 0.3],
        "Content": "test content",
        "Dimensionality": 3,
        "CreatedUtc": "2024-01-01T00:00:00+00:00",
        "LastUpdateUtc": "2024-01-01T00:00:00+00:00"
    }

    model = VectorMetadataModel(**valid_data)
    assert isinstance(model.guid, UUID)
    assert isinstance(model.tenant_guid, UUID)
    assert model.graph_guid == UUID(valid_data["GraphGUID"])
    assert model.node_guid == UUID(valid_data["NodeGUID"])
    assert model.edge_guid == UUID(valid_data["EdgeGUID"])
    assert model.embeddings == valid_data["Embeddings"]
    assert model.content == valid_data["Content"]
    assert model.dimensionality == valid_data["Dimensionality"]
    assert model.created_utc == datetime.fromisoformat(valid_data["CreatedUtc"])
    assert model.last_update_utc == datetime.fromisoformat(valid_data["LastUpdateUtc"])


def test_vector_search_request_model():
    """Test vector search request model validation."""
    valid_data = {
        "Domain": VectorSearchDomainEnum.Graph,
        "Embeddings": [0.1, 0.2, 0.3],
        "TenantGUID": "550e8400-e29b-41d4-a716-446655440001",
        "Labels": ["label1"],
        "Tags": {"key1": "value1"}
    }

    model = VectorSearchRequestModel(**valid_data)
    assert model.domain == VectorSearchDomainEnum.Graph
    assert model.embeddings == valid_data["Embeddings"]
    assert isinstance(model.tenant_guid, UUID)
    assert model.labels == valid_data["Labels"]
    assert model.tags == valid_data["Tags"]


def test_vector_search_result_model(valid_search_result):
    """Test vector search result model validation."""

    model = VectorSearchResultModel(**valid_search_result[0].model_dump(mode="json"))
    assert model.score == 0.95
    assert model.distance == 0.95
    assert model.inner_product == 0.95
    assert model.graph.guid == "550e8400-e29b-41d4-a716-446655440002"
    assert model.node.guid == "550e8400-e29b-41d4-a716-446655440003"
    assert model.edge.guid == "550e8400-e29b-41d4-a716-446655440004"