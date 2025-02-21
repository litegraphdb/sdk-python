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
| Tenant.exists | Check if a tenant exists | guid: str | bool | `v1.0/tenants/{guid}` |
| Tenant.create | Create a new tenant | name: str = None<br>active: bool = True | TenantMetadataModel | `v1.0/tenants` |
| Tenant.retrieve | Retrieve tenant details | guid: str | TenantMetadataModel | `v1.0/tenants/{guid}` |
| Tenant.update | Update tenant details | guid: str<br>name: str = None<br>active: bool = None | TenantMetadataModel | `v1.0/tenants/{guid}` |
| Tenant.delete | Delete a tenant | guid: str<br>force: bool = False | None | `v1.0/tenants/{guid}` |
| Tenant.retrieve_all | List all tenants | None | List[TenantMetadataModel] | `v1.0/tenants` |

### User Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| User.exists | Check if a user exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| User.create | Create a new user | first_name: str<br>last_name: str<br>email: str<br>password: str<br>active: bool = True | UserMasterModel | `v1.0/tenants/{tenant_guid}/users` |
| User.retrieve | Retrieve user details | guid: str | UserMasterModel | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| User.update | Update user details | guid: str<br>first_name: str = None<br>last_name: str = None<br>email: str = None<br>password: str = None<br>active: bool = None | UserMasterModel | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| User.delete | Delete user | guid: str | None | `v1.0/tenants/{tenant_guid}/users/{guid}` |
| User.retrieve_all | List all users | None | List[UserMasterModel] | `v1.0/tenants/{tenant_guid}/users` |

### Credential Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Credential.exists | Check if a credential exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| Credential.create | Create a new credential | user_guid: str<br>name: str = None<br>bearer_token: str<br>active: bool = True | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials` |
| Credential.retrieve | Retrieve credential details | guid: str | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| Credential.update | Update credential details | guid: str<br>name: str = None<br>bearer_token: str = None<br>active: bool = None | CredentialModel | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| Credential.delete | Delete credential | guid: str | None | `v1.0/tenants/{tenant_guid}/credentials/{guid}` |
| Credential.retrieve_all | List all credentials | None | List[CredentialModel] | `v1.0/tenants/{tenant_guid}/credentials` |

### Label Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Label.exists | Check if a label exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| Label.create | Create a new label | label: str<br>graph_guid: str = None<br>node_guid: str = None<br>edge_guid: str = None | LabelModel | `v1.0/tenants/{tenant_guid}/labels` |
| Label.retrieve | Retrieve label details | guid: str | LabelModel | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| Label.update | Update label details | guid: str<br>label: str = None<br>graph_guid: str = None<br>node_guid: str = None<br>edge_guid: str = None | LabelModel | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| Label.delete | Delete label | guid: str | None | `v1.0/tenants/{tenant_guid}/labels/{guid}` |
| Label.retrieve_all | List all labels | None | List[LabelModel] | `v1.0/tenants/{tenant_guid}/labels` |

### Tag Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Tag.exists | Check if a tag exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| Tag.create | Create a new tag | key: str<br>value: str<br>graph_guid: str = None<br>node_guid: str = None<br>edge_guid: str = None | TagModel | `v1.0/tenants/{tenant_guid}/tags` |
| Tag.retrieve | Retrieve tag details | guid: str | TagModel | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| Tag.update | Update tag details | guid: str<br>key: str = None<br>value: str = None<br>graph_guid: str = None<br>node_guid: str = None<br>edge_guid: str = None | TagModel | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| Tag.delete | Delete tag | guid: str | None | `v1.0/tenants/{tenant_guid}/tags/{guid}` |
| Tag.retrieve_all | List all tags | None | List[TagModel] | `v1.0/tenants/{tenant_guid}/tags` |

### Vector Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Vector.exists | Check if a vector exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| Vector.create | Create a new vector | vector: List[float]<br>tenant_guid: UUID<br>graph_guid: UUID = None<br>labels: List[str] = None<br>tags: Dict[str, str] = None | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors` |
| Vector.retrieve | Retrieve vector details | guid: str | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| Vector.update | Update vector details | guid: str<br>vector: List[float] = None<br>labels: List[str] = None<br>tags: Dict[str, str] = None | VectorMetadataModel | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| Vector.delete | Delete vector | guid: str | None | `v1.0/tenants/{tenant_guid}/vectors/{guid}` |
| Vector.retrieve_all | List all vectors | None | List[VectorMetadataModel] | `v1.0/tenants/{tenant_guid}/vectors` |
| Vector.search_vectors | Search vectors | domain: VectorSearchDomainEnum<br>embeddings: list[float]<br>tenant_guid: UUID<br>graph_guid: UUID = None<br>labels: list[str] = None<br>tags: dict = None<br>filter_expr: dict = None | VectorSearchResultModel | `v1.0/tenants/{tenant_guid}/vectors/search` |

### Graph Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Graph.exists | Check if a graph exists | guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| Graph.create | Create a new graph | name: str = None<br>labels: List[str] = None<br>tags: Dict[str, str] = None<br>vectors: List = None<br>data: Dict = None | GraphModel | `v1.0/tenants/{tenant_guid}/graphs` |
| Graph.retrieve | Retrieve graph details | guid: str | GraphModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| Graph.update | Update graph details | guid: str<br>name: str = None<br>labels: List[str] = None<br>tags: Dict[str, str] = None<br>vectors: List = None<br>data: Dict = None | GraphModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| Graph.delete | Delete graph | guid: str<br>force: bool = False | None | `v1.0/tenants/{tenant_guid}/graphs/{guid}` |
| Graph.retrieve_all | List all graphs | None | List[GraphModel] | `v1.0/tenants/{tenant_guid}/graphs` |
| Graph.search | Search graphs | expr: ExprModel<br>ordering: str = None | List[GraphModel] | `v1.0/tenants/{tenant_guid}/graphs/search` |
| Graph.export_gexf | Export graph to GEXF | graph_id: str<br>include_data: bool = False | str | `v1.0/tenants/{tenant_guid}/graphs/{guid}/export` |
| Graph.batch_existence | Batch existence check | graph_guid: str<br>request: ExistenceRequestModel | ExistenceResultModel | `v1.0/tenants/{tenant_guid}/graphs/{guid}/existence` |

### Node Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Node.exists | Check if a node exists | graph_guid: str<br>guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| Node.create | Create a new node | graph_guid: str<br>name: str = None<br>data: Dict = None<br>labels: List = None<br>tags: Dict = None<br>vectors: List = None | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes` |
| Node.create_multiple | Create multiple nodes | graph_guid: str<br>nodes: List[dict] | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/multiple` |
| Node.retrieve | Retrieve node details | graph_guid: str<br>guid: str | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| Node.update | Update node details | graph_guid: str<br>guid: str<br>name: str = None<br>data: Dict = None<br>labels: List = None<br>tags: Dict = None<br>vectors: List = None | NodeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| Node.delete | Delete node | graph_guid: str<br>guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{guid}` |
| Node.delete_multiple | Delete multiple nodes | graph_guid: str<br>node_guids: List[str] | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/multiple` |
| Node.delete_all | Delete all nodes | graph_guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/all` |
| Node.retrieve_all | List all nodes | graph_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes` |
| Node.search | Search nodes | graph_guid: str<br>expr: ExprModel<br>ordering: str = None | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/search` |

### Edge Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Edge.exists | Check if an edge exists | graph_guid: str<br>guid: str | bool | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| Edge.create | Create a new edge | graph_guid: str<br>from_guid: str<br>to_guid: str<br>name: str = None<br>cost: int = 0<br>data: Dict = None<br>labels: List = None<br>tags: Dict = None | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges` |
| Edge.create_multiple | Create multiple edges | graph_guid: str<br>edges: List[dict] | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/multiple` |
| Edge.retrieve | Retrieve edge details | graph_guid: str<br>guid: str | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| Edge.update | Update edge details | graph_guid: str<br>guid: str<br>name: str = None<br>cost: int = None<br>data: Dict = None<br>labels: List = None<br>tags: Dict = None | EdgeModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| Edge.delete | Delete edge | graph_guid: str<br>guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/{guid}` |
| Edge.delete_multiple | Delete multiple edges | graph_guid: str<br>edge_guids: List[str] | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/multiple` |
| Edge.delete_all | Delete all edges | graph_guid: str | None | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/all` |
| Edge.retrieve_all | List all edges | graph_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges` |
| Edge.search | Search edges | graph_guid: str<br>expr: ExprModel<br>ordering: str = None | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/search` |

### Route Operations

| Method | Description | Parameters | Returns | Endpoint |
|--------|-------------|------------|---------|----------|
| Routes.routes | Find routes | graph_guid: str<br>**kwargs: RouteRequestModel | RouteResultModel | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/routes` |
| RouteNodes.get_edges_from | Get edges from node | graph_guid: str<br>node_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/edges/from` |
| RouteNodes.get_edges_to | Get edges to node | graph_guid: str<br>node_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/edges/to` |
| RouteNodes.edges | Get edges of a node | graph_guid: str<br>node_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/edges` |
| RouteEdges.between | Get edges between nodes | graph_guid: str<br>from_node_guid: str<br>to_node_guid: str | List[EdgeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/edges/between` |
| RouteNodes.neighbors | Get node neighbors | graph_guid: str<br>node_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/neighbors` |
| RouteNodes.parents | Get node parents | graph_guid: str<br>node_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/parents` |
| RouteNodes.children | Get node children | graph_guid: str<br>node_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/children` |
| RouteNodes.between | Get nodes between | graph_guid: str<br>node_guid: str | List[NodeModel] | `v1.0/tenants/{tenant_guid}/graphs/{graph_guid}/nodes/{node_guid}/between` |

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