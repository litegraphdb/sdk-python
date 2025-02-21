<img src="assets/favicon.png" height="48">

# Python SDK for LiteGraph

LiteGraph is a lightweight graph database with both relational and vector support, built using Sqlite, with support for exporting to GEXF.  LiteGraph is intended to be a multi-modal database primarily for providing persistence and retrieval for knowledge and artificial intelligence applications.

## Features

- Multi-tenant support with tenant GUID management
- Graph management
- Node and edge operations
- Route finding between nodes
- Search capabilities for graphs, nodes, and edges
- GEXF format export support
- Built-in retry mechanism and error handling
- Comprehensive logging system
- Access key authentication support

## Requirements

- Python 3.8 or higher

### Dependencies

- `httpx`: For making HTTP requests
- `pydantic`: For data validation and serialization
- `typing`: For type hints

## Installation

```bash
pip install litegraph_sdk
```

## Quick Start

```python
from litegraph_sdk import configure, Graph, Node, Edge
import uuid

# Configure the SDK with tenant GUID and access key
configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",
    access_key="your-access-key"
)

# Create a new graph
graph = Graph.create(
    name="My Graph",
    data={"description": "A sample graph"}
)

# Create Multiple Nodes
new_multiple_node = [
    {
        "Name": "Active Directory",
        "Data": {
            "Name": "Active Directory"
        }
    },
    {
        "Name": "Website",
        "Data": {
            "Name": "Website"
        }
    }
]
multiple_nodes = Node.create_multiple(new_multiple_node)

# Add nodes
node1 = Node.create(
    graph_guid=graph.guid,
    name="Start Node",
    data={"type": "entry_point"}
)

node2 = Node.create(
    graph_guid=graph.guid,
    name="End Node",
    data={"type": "exit_point"}
)

# Create an edge between nodes
edge = Edge.create(
    graph_guid=graph.guid,
    from_node=node1.guid,
    to_node=node2.guid,
    cost=1,
    name="Connection",
    data={"type": "direct"}
)
```

## API Endpoints Reference

### Tenant Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a tenant exists | - tenant_guid: str | bool | `v1.0/tenants/{guid}` |
| PUT | Create a new tenant | Request Body:<br>- name: str (optional)<br>- active: bool (default: True) | TenantMetadataModel:<br>- guid: str<br>- name: str<br>- active: bool<br>- created_utc: datetime<br>- last_update_utc: datetime | `v1.0/tenants` |
| GET | Retrieve tenant details | - tenant_guid: str | TenantMetadataModel | `v1.0/tenants/{guid}` |
| PUT | Update tenant details | Path:<br>- tenant_guid: str<br>Request Body:<br>- name: str (optional)<br>- active: bool (optional) | TenantMetadataModel | `v1.0/tenants/{guid}` |
| DELETE | Delete a tenant | Path:<br>- tenant_guid: str<br>Query:<br>- force: bool (optional) | None | `v1.0/tenants/{guid}` |
| GET | List all tenants | None | List[TenantMetadataModel] | `v1.0/tenants` |

### User Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a user exists | Path:<br>- tenant_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| PUT | Create a new user | Request Body:<br>- first_name: str<br>- last_name: str<br>- email: str<br>- password: str<br>- active: bool (default: True) | UserMasterModel | `v1.0/tenants/{tenant_guid}/users` |
| GET | Retrieve user details | Path:<br>- tenant_guid: str<br>- guid: str | UserMasterModel | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| PUT | Update user details | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- first_name: str (optional)<br>- last_name: str (optional)<br>- email: str (optional)<br>- password: str (optional)<br>- active: bool (optional) | UserMasterModel | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| DELETE | Delete user | Path:<br>- tenant_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| GET | List all users | Path:<br>- tenant_guid: str | List[UserMasterModel] | `v1.0/tenants/{tenant_guid}/users` |

### Credential Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a credential exists | Path:<br>- tenant_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| PUT | Create a new credential | Request Body:<br>- user_guid: str<br>- name: str (optional)<br>- bearer_token: str<br>- active: bool (default: True) | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials` |
| GET | Retrieve credential details | Path:<br>- tenant_guid: str<br>- guid: str | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| PUT | Update credential details | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- name: str (optional)<br>- bearer_token: str (optional)<br>- active: bool (optional) | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| DELETE | Delete credential | Path:<br>- tenant_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| GET | List all credentials | Path:<br>- tenant_guid: str | List[CredentialModel] | `v1.0/tenants/{tenant_guid}/credentials` |

### Label Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a label exists | Path:<br>- tenant_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| PUT | Create a new label | Request Body:<br>- graph_guid: str (optional)<br>- node_guid: str (optional)<br>- edge_guid: str (optional)<br>- label: str | LabelModel | `v1.0/tenants/{tenant_guid}/labels` |
| GET | Retrieve label details | Path:<br>- tenant_guid: str<br>- guid: str | LabelModel | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| PUT | Update label details | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- label: str (optional)<br>- graph_guid: str (optional)<br>- node_guid: str (optional)<br>- edge_guid: str (optional) | LabelModel | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| DELETE | Delete label | Path:<br>- tenant_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| GET | List all labels | Path:<br>- tenant_guid: str | List[LabelModel] | `v1.0/tenants/{tenant_guid}/labels` |

### Tag Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a tag exists | Path:<br>- tenant_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| PUT | Create a new tag | Request Body:<br>- graph_guid: str (optional)<br>- node_guid: str (optional)<br>- edge_guid: str (optional)<br>- key: str<br>- value: str | TagModel | `v1.0/tenants/{tenant_guid}/tags` |
| GET | Retrieve tag details | Path:<br>- tenant_guid: str<br>- guid: str | TagModel | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| PUT | Update tag details | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- key: str (optional)<br>- value: str (optional)<br>- graph_guid: str (optional)<br>- node_guid: str (optional)<br>- edge_guid: str (optional) | TagModel | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| DELETE | Delete tag | Path:<br>- tenant_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| GET | List all tags | Path:<br>- tenant_guid: str | List[TagModel] | `v1.0/tenants/{tenant_guid}/tags` |

### Vector Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a vector exists | Path:<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| PUT | Create a new vector | Request Body:<br>- tenant_guid: UUID<br>- graph_guid: UUID (optional)<br>- vector: List[float]<br>- labels: List[str] (optional)<br>- tags: Dict[str, str] (optional) | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors` |
| GET | Retrieve vector details | Path:<br>- guid: str | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| PUT | Update vector details | Path:<br>- guid: str<br>Request Body:<br>- vector: List[float] (optional)<br>- labels: List[str] (optional)<br>- tags: Dict[str, str] (optional) | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| DELETE | Delete vector | Path:<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| GET | List all vectors | Path:<br>- tenant_guid: str | List[VectorMetadataModel] | `v1.0/tenants/{tenant_guid}/vectors` |
| POST | Search vectors | Request Body:<br>- domain: VectorSearchDomainEnum<br>- embeddings: List[float]<br>- tenant_guid: UUID<br>- graph_guid: UUID (optional)<br>- labels: List[str] (optional)<br>- tags: Dict[str, str] (optional)<br>- expr: ExprModel (optional)<br>- search_type: VectorSearchTypeEnum (optional) | VectorSearchResponseModel | `v1.0/tenants/{tenant_guid}/vectors/search` |

### Graph Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a graph exists | Path:<br>- tenant_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| PUT | Create a new graph | Request Body:<br>- name: str (optional)<br>- labels: List[str] (optional)<br>- tags: Dict[str, str] (optional)<br>- vectors: List (optional)<br>- data: Dict (optional) | GraphModel | `v1.0/tenants/{tenant_guid}/graphs` |
| GET | Retrieve graph details | Path:<br>- tenant_guid: str<br>- guid: str | GraphModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| PUT | Update graph details | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- name: str (optional)<br>- labels: List[str] (optional)<br>- tags: Dict[str, str] (optional)<br>- vectors: List (optional)<br>- data: Dict (optional) | GraphModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| DELETE | Delete graph | Path:<br>- tenant_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| GET | List all graphs | Path:<br>- tenant_guid: str | List[GraphModel] | `v1.0/tenants/{tenant_guid}/graphs` |
| POST | Search graphs | Request Body:<br>- expr: ExprModel<br>- ordering: str (optional) | List[GraphModel] | `v1.0/tenants/{tenant_guid}/graphs/search` |
| GET | Export graph to GEXF | Path:<br>- tenant_guid: str<br>- guid: str | str (GEXF format) | `v1.0/tenants/{tenant_guid}/graphs/{guid}/export` |
| POST | Batch existence check | Path:<br>- tenant_guid: str<br>- guid: str<br>Request Body:<br>- nodes: List[str]<br>- edges: List[str]<br>- edges_between: List[EdgeBetweenModel] | ExistenceResultModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}/existence` |

### Node Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if a node exists | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| PUT | Create a new node | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- name: str (optional)<br>- data: Dict (optional)<br>- labels: List (optional)<br>- tags: Dict (optional)<br>- vectors: List (optional) | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes` |
| PUT | Create multiple nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>List of node objects | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/multiple` |
| GET | Retrieve node details | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| PUT | Update node details | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str<br>Request Body:<br>- name: str (optional)<br>- data: Dict (optional)<br>- labels: List (optional)<br>- tags: Dict (optional)<br>- vectors: List (optional) | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| DELETE | Delete node | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| DELETE | Delete multiple nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- List[str] (guids) | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/multiple` |
| DELETE | Delete all nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/all` |
| GET | List all nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes` |
| POST | Search nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- expr: ExprModel<br>- ordering: str (optional) | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/search` |

### Edge Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| HEAD | Check if an edge exists | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| PUT | Create a new edge | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- name: str (optional)<br>- from_guid: str<br>- to_guid: str<br>- cost: int (default: 0)<br>- data: Dict (optional)<br>- labels: List (optional)<br>- tags: Dict (optional) | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges` |
| PUT | Create multiple edges | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>List of edge objects | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/multiple` |
| GET | Retrieve edge details | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| PUT | Update edge details | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str<br>Request Body:<br>- name: str (optional)<br>- cost: int (optional)<br>- data: Dict (optional)<br>- labels: List (optional)<br>- tags: Dict (optional) | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| DELETE | Delete edge | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| DELETE | Delete multiple edges | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- List[str] (guids) | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/multiple` |
| DELETE | Delete all edges | Path:<br>- tenant_guid: str<br>- graph_guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/all` |
| GET | List all edges | Path:<br>- tenant_guid: str<br>- graph_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges` |
| POST | Search edges | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- expr: ExprModel<br>- ordering: str (optional) | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/search` |

### Route Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| POST | Find routes | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Request Body:<br>- from_guid: str<br>- to_guid: str<br>- edge_filter: SearchRequest (optional)<br>- node_filter: SearchRequest (optional) | RouteResultModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/routes` |
| GET | Get edges from node | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}/edges/from` |
| GET | Get edges to node | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}/edges/to` |
| GET | Get edges between nodes | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>Query:<br>- from: str<br>- to: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/between` |
| GET | Get node edges | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | NodeModel with edges | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| GET | Get node neighbors | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}/neighbors` |
| GET | Get node parents | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}/parents` |
| GET | Get node children | Path:<br>- tenant_guid: str<br>- graph_guid: str<br>- guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}/children` |

## Core Components

### Base Models

- `TenantModel`: Represents a tenant in the system
- `GraphModel`: Represents a graph container
- `NodeModel`: Represents a node in a graph
- `EdgeModel`: Represents a connection between nodes
- `RouteRequestModel`: Used for finding routes between nodes
- `RouteResultModel`: Contains route finding results
- `ExistenceRequestModel`: Used for checking the existence

### Search Capabilities

The SDK provides powerful search functionality through the `SearchRequest` class:

```python
from litegraph_sdk import Graph

# Search for graphs by name
search_request = {
    "Ordering":"CreateDescending",
    "Expr": {
        "Left": "Name",
        "Operator": "Equals",
        "Right": "My Graph"
    }
}

results = Graph.search(**search_request)
```

### Error Handling

The SDK includes comprehensive error handling with specific exception types:

- `AuthenticationError`: Authentication issues
- `ResourceNotFoundError`: Requested resource not found
- `BadRequestError`: Invalid request parameters
- `TimeoutError`: Request timeout
- `ServerError`: Server-side issues

## Logging

The SDK includes a built-in logging system that can be configured:

```python
from litegraph_sdk.sdk_logging import set_log_level, log_info

# Set logging level
set_log_level("DEBUG")

# Add log
log_info("INFO", "This is an info message")
```

## API Resource Operations

### Graphs

```python
from litegraph_sdk import Graph
from litegraph_sdk.configuration import configure
from litegraph_sdk.models.existence_request import ExistenceRequestModel
from litegraph_sdk.models.edge_between import EdgeBetweenModel

# Configure with tenant GUID and access key
configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",
    access_key="your-access-key"
)

# Create a graph
graph = Graph.create(name="New Graph")

# Retrieve a graph
graph = Graph.retrieve(graph_guid="graph-guid")

# Retrieve all graphs for tenant
graphs = Graph.retrieve_all()

# Update a graph
graph = Graph.update(graph_guid="graph-guid", name="Updated Graph")

# Delete a graph
Graph.delete(graph_guid="graph-guid")

# Export to GEXF
gexf_data = Graph.export_gexf(graph_guid="graph-guid")

# Check if Graph Exists
exists = Graph.exists(graph_guid="graph-guid")

# Search graphs in tenant
search_request = {
    "Ordering": "CreatedDescending",
    "Expr": {
        "Left": "Name",
        "Operator": "Equals",
        "Right": "My Graph"
    }
}
graph_results = Graph.search(**search_request)

# Batch Existence Check
request = ExistenceRequestModel(
    nodes=[
        "node-guid-1",
        "node-guid-2"
    ],
    edges=[
        "edge-guid-1"
    ],
    edges_between=[
        EdgeBetweenModel(
            from_="node-guid-1",
            to="node-guid-2"
        )
    ]
)
existence_results = Graph.batch_existence(graph_guid="graph-guid", request=request)
```

### Nodes

```python
from litegraph_sdk import Node
from litegraph_sdk.configuration import configure

# Configure with tenant GUID and access key
configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",
    access_key="your-access-key"
)

# Create Multiple Nodes
new_multiple_nodes = [
    {
        "Name": "Active Directory",
        "Data": {
            "Name": "Active Directory"
        }
    },
    {
        "Name": "Website",
        "Data": {
            "Name": "Website"
        }
    }
]
nodes = Node.create_multiple(graph_guid="graph-guid", nodes=new_multiple_nodes)

# Create a single node
node = Node.create(
    graph_guid="graph-guid",
    name="New Node",
    data={"type": "service"}
)

# Retrieve a node
node = Node.retrieve(graph_guid="graph-guid", node_guid="node-guid")

# Retrieve all nodes in a graph
nodes = Node.retrieve_all(graph_guid="graph-guid")

# Update a node
node = Node.update(
    graph_guid="graph-guid",
    node_guid="node-guid",
    name="Updated Node"
)

# Delete a node
Node.delete(graph_guid="graph-guid", node_guid="node-guid")

# Delete multiple nodes
Node.delete_multiple(graph_guid="graph-guid", node_guids=["node-guid-1", "node-guid-2"])

# Delete all nodes in a graph
Node.delete_all(graph_guid="graph-guid")

# Check if Node Exists
exists = Node.exists(graph_guid="graph-guid", node_guid="node-guid")

# Search nodes in a graph
search_request = {
    "Ordering": "CreatedDescending",
    "Expr": {
        "Left": "Name",
        "Operator": "Contains",
        "Right": "Service"
    }
}
node_results = Node.search(graph_guid="graph-guid", **search_request)
```

### Edges

```python
from litegraph_sdk import Edge
from litegraph_sdk.configuration import configure

# Configure with tenant GUID and access key
configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",
    access_key="your-access-key"
)

# Create Multiple Edges
new_multiple_edges = [
    {
        "Name": "Connection 1",
        "From": "node-guid-1",
        "To": "node-guid-2",
        "Cost": 1
    },
    {
        "Name": "Connection 2",
        "From": "node-guid-2",
        "To": "node-guid-3",
        "Cost": 1
    }
]
edges = Edge.create_multiple(graph_guid="graph-guid", edges=new_multiple_edges)

# Create a single edge
edge = Edge.create(
    graph_guid="graph-guid",
    from_node="node-guid-1",
    to_node="node-guid-2",
    name="Direct Connection",
    cost=1
)

# Retrieve an edge
edge = Edge.retrieve(graph_guid="graph-guid", edge_guid="edge-guid")

# Retrieve all edges in a graph
edges = Edge.retrieve_all(graph_guid="graph-guid")

# Update an edge
edge = Edge.update(
    graph_guid="graph-guid",
    edge_guid="edge-guid",
    name="Updated Connection",
    cost=2
)

# Delete an edge
Edge.delete(graph_guid="graph-guid", edge_guid="edge-guid")

# Delete multiple edges
Edge.delete_multiple(graph_guid="graph-guid", edge_guids=["edge-guid-1", "edge-guid-2"])

# Delete all edges in a graph
Edge.delete_all(graph_guid="graph-guid")

# Check if Edge Exists
exists = Edge.exists(graph_guid="graph-guid", edge_guid="edge-guid")

# Search edges in a graph
search_request = {
    "Ordering": "CreatedDescending",
    "Expr": {
        "Left": "Cost",
        "Operator": "LessThan",
        "Right": 2
    }
}
edge_results = Edge.search(graph_guid="graph-guid", **search_request)
```

### Vectors

```python
from litegraph_sdk import Vector
from litegraph_sdk.enums.vector_search_domain_enum import VectorSearchDomainEnum
from litegraph_sdk.configuration import configure

# Configure with tenant GUID and access key
configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",
    access_key="your-access-key"
)

# Create a vector
vector = Vector.create(
    tenant_guid="tenant-guid",
    graph_guid="graph-guid",  # Optional
    vector=[0.1, 0.2, 0.3]
)

# Retrieve a vector
vector = Vector.retrieve(vector_guid="vector-guid")

# Retrieve all vectors
vectors = Vector.retrieve_all()

# Update a vector
vector = Vector.update(
    vector_guid="vector-guid",
    vector=[0.1, 0.2, 0.3]
)

# Delete a vector
Vector.delete(vector_guid="vector-guid")

# Check if Vector Exists
exists = Vector.exists(vector_guid="vector-guid")

# Search vectors
search_results = Vector.search_vectors(
    domain=VectorSearchDomainEnum.Node,  # Can be Graph, Node, or Edge
    embeddings=[0.1, 0.2, 0.3],
    tenant_guid="tenant-guid",
    graph_guid="graph-guid",  # Required for Node/Edge searches
    labels=["label1", "label2"],  # Optional
    tags={"key": "value"},  # Optional
    filter_expr={"Left": "field", "Operator": "Equals", "Right": "value"}  # Optional
)
```

## Route and Traversal

```python
from litegraph_sdk.resources.route_traversal import RouteNodes
from litegraph_sdk.configuration import configure

base = "URL"
configure(base_url,"graph_guid")

# Edges from node
get_edges_from_node = RouteNodes.get_edges_from("graph_guid","node_guid")

# Edges to node
get_edges_to_node = RouteNodes.get_edges_to("graph_guid","node_guid")

# Specific Edge
specific_edge = RouteNodes.edges("graph_guid","node_guid")

# Find parent of a Node
parent_node = RouteNodes.parents("graph_guid","node_guid")

# Find children of a Node
children_node = RouteNodes.children("graph_guid","node_guid")

# Find neighbors of a Node
neighbors_node = RouteNodes.neighbors("graph_guid","node_guid")



# Find Edges in between of a Node
from litegraph_sdk.resources.routes_between import RouteEdges
between_nodes = RouteEdges.between("graph_guid","node_guid(from)","node_guid(to)")

# Find Routes
from litegraph_sdk.resources.routes import Routes
routes_data = {
    "Graph": "graph_guid",
    "From": "node_guid",
    "To": "node_guid",
    "NodeFilter":{
       "GraphGUID": "graph_guid",
        "Ordering": "CreatedDescending",
        "Expr": {
            "Left": "Hello",
            "Operator": "GreaterThan",
            "Right": "World"
        }
     }
}
routes = Routes.routes("graph_guid",**routes_data)
```

## Advanced Configuration

The SDK client can be configured with custom settings:

```python
from litegraph_sdk import configure

configure(
    endpoint="https://api.litegraph.com",
    tenant_guid="your-tenant-guid",    # Required for multi-tenant support
    access_key="your-access-key",      # Required for authentication
    timeout=30,                        # Optional: 30 seconds timeout
    retries=5                         # Optional: 5 retry attempts
)
```

### Tenant Management

```python
from litegraph_sdk import Tenant
from litegraph_sdk.configuration import configure

# Configure with admin access
configure(endpoint="https://api.litegraph.com", access_key="admin-access-key")

# Create a new tenant
tenant = Tenant.create(name="New Tenant")

# Retrieve tenant details
tenant = Tenant.retrieve(tenant_guid="tenant-guid")

# Update tenant
tenant = Tenant.update(tenant_guid="tenant-guid", name="Updated Tenant")

# Delete tenant
Tenant.delete(tenant_guid="tenant-guid")

# List all tenants
tenants = Tenant.retrieve_all()
```

## Development

### Setting up Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To set up pre-commit:

```bash
# Install pre-commit
pip install pre-commit

# Install the pre-commit hooks
pre-commit install

# (Optional) Run pre-commit on all files
pre-commit run --all-files
```

The pre-commit hooks will run automatically on `git commit`. They help maintain:

- Code formatting (using ruff)
- Import sorting
- Code quality checks
- And other project-specific checks

### Running Tests

The project uses `tox` for running tests in isolated environments. Make sure you have tox installed:

```bash
pip install tox
```

To run the default test environment:

```bash
tox
```

To run specific test environments:

```bash
# Run only the tests
tox -e default

# Run tests with coverage report
tox -- --cov litegraph_sdk --cov-report term-missing

# Build documentation
tox -e docs

# Build the package
tox -e build

# Clean build artifacts
tox -e clean
```

### Development Installation

For development, you can install the package with all test dependencies:

```bash
pip install -e ".[testing]"
```

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details

## Feedback and Issues

Have feedback or found an issue? Please file an issue in our GitHub repository.

## Version History

Please refer to [CHANGELOG.md](CHANGELOG.md) for a detailed version history.