import pytest
from litegraph.enums.operator_enum import Opertator_Enum
from litegraph.models.expression import ExprModel
from pydantic import ValidationError
from litegraph.models.enumeration_query import EnumerationQueryModel
from litegraph.enums.enumeration_order_enum import EnumerationOrder_Enum
from litegraph.models.enumeration_result import EnumerationResultModel
from litegraph.models.timestamp import TimestampModel


@pytest.fixture
def valid_expr_data():
    """Fixture providing valid expression data."""
    return {"Left": "field1", "Operator": Opertator_Enum.Equals, "Right": "value1"}


@pytest.fixture
def all_operators():
    """Fixture providing all valid operators."""
    return [Opertator_Enum.Equals, Opertator_Enum.GreaterThan, Opertator_Enum.LessThan]


def test_valid_expression_creation(valid_expr_data):
    """Test creating an expression with valid data."""
    expr = ExprModel(**valid_expr_data)
    assert expr.Left == valid_expr_data["Left"]
    assert expr.Operator == valid_expr_data["Operator"]
    assert expr.Right == valid_expr_data["Right"]


@pytest.mark.parametrize(
    "operator",
    [Opertator_Enum.Equals, Opertator_Enum.GreaterThan, Opertator_Enum.LessThan],
)
def test_all_operators(operator):
    """Test expression creation with all possible operators."""
    expr = ExprModel(Left="field", Operator=operator, Right="value")
    assert expr.Operator == operator


def test_invalid_operator():
    """Test that invalid operators are rejected."""
    with pytest.raises(ValidationError):
        ExprModel(Left="field", Operator="InvalidOperator", Right="value")


def test_missing_fields():
    """Test that missing required fields raise validation error."""
    invalid_cases = [
        {"Operator": Opertator_Enum.Equals, "Right": "value"},  # Missing Left
        {"Left": "field", "Right": "value"},  # Missing Operator
        {"Left": "field", "Operator": Opertator_Enum.Equals},  # Missing Right
        {},  # Missing all
    ]

    for invalid_data in invalid_cases:
        with pytest.raises(ValidationError):
            ExprModel(**invalid_data)


def test_string_fields_validation():
    """Test validation of string fields."""
    invalid_types = [
        {"Left": 123, "Operator": Opertator_Enum.Equals, "Right": "value"},
        {"Left": "field", "Operator": Opertator_Enum.Equals, "Right": 123},
        {"Left": True, "Operator": Opertator_Enum.Equals, "Right": "value"},
        {"Left": "field", "Operator": Opertator_Enum.Equals, "Right": True},
    ]

    for invalid_data in invalid_types:
        with pytest.raises(ValidationError):
            ExprModel(**invalid_data)


def test_empty_and_whitespace_strings():
    """Test that empty and whitespace strings are allowed."""
    # Test empty strings
    expr1 = ExprModel(Left="", Operator=Opertator_Enum.Equals, Right="value")
    assert expr1.Left == ""

    expr2 = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="")
    assert expr2.Right == ""

    # Test whitespace strings
    expr3 = ExprModel(Left="   ", Operator=Opertator_Enum.Equals, Right="value")
    assert expr3.Left == "   "

    expr4 = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="   ")
    assert expr4.Right == "   "


@pytest.mark.parametrize(
    "left,operator,right",
    [
        ("field1", Opertator_Enum.Equals, "value1"),
        ("long_field_name", Opertator_Enum.GreaterThan, "long_value_name"),
        ("f1", Opertator_Enum.LessThan, "v1"),
        ("field_with_numbers_123", Opertator_Enum.Equals, "value_with_numbers_456"),
        (
            "field_with_special_chars_!@#",
            Opertator_Enum.Equals,
            "value_with_special_chars_!@#",
        ),
        ("", Opertator_Enum.Equals, "value"),  # Empty string
        ("field", Opertator_Enum.Equals, ""),  # Empty string
        ("   ", Opertator_Enum.Equals, "value"),  # Whitespace
        ("field", Opertator_Enum.Equals, "   "),  # Whitespace
    ],
)
def test_valid_field_values(left, operator, right):
    """Test various valid combinations of field values."""
    expr = ExprModel(Left=left, Operator=operator, Right=right)
    assert expr.Left == left
    assert expr.Operator == operator
    assert expr.Right == right


def test_model_serialization():
    """Test model serialization and deserialization."""
    original_data = {
        "Left": "field1",
        "Operator": Opertator_Enum.Equals,
        "Right": "value1",
    }

    # Create model
    expr = ExprModel(**original_data)

    # Serialize to dict
    serialized = expr.model_dump()

    # Create new model from serialized data
    new_expr = ExprModel(**serialized)

    # Verify all fields match
    assert new_expr.Left == expr.Left
    assert new_expr.Operator == expr.Operator
    assert new_expr.Right == expr.Right


@pytest.mark.parametrize(
    "operator,left,right",
    [
        (Opertator_Enum.Equals, "age", "25"),
        (Opertator_Enum.GreaterThan, "price", "100"),
        (Opertator_Enum.LessThan, "quantity", "10"),
        (Opertator_Enum.Equals, "", "25"),  # Empty string test
        (Opertator_Enum.GreaterThan, "price", ""),  # Empty string test
    ],
)
def test_typical_use_cases(operator, left, right):
    """Test typical use cases for expressions."""
    expr = ExprModel(Left=left, Operator=operator, Right=right)
    assert expr.Left == left
    assert expr.Operator == operator
    assert expr.Right == right


def test_case_sensitivity():
    """Test case sensitivity handling."""
    expr1 = ExprModel(Left="Field", Operator=Opertator_Enum.Equals, Right="Value")

    expr2 = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")

    assert expr1.Left != expr2.Left
    assert expr1.Right != expr2.Right


def test_none_values():
    """Test that None values are rejected."""
    invalid_cases = [
        {"Left": None, "Operator": Opertator_Enum.Equals, "Right": "value"},
        {"Left": "field", "Operator": None, "Right": "value"},
        {"Left": "field", "Operator": Opertator_Enum.Equals, "Right": None},
    ]

    for invalid_data in invalid_cases:
        with pytest.raises(ValidationError):
            ExprModel(**invalid_data)


def test_enumeration_query_model_defaults():
    model = EnumerationQueryModel(Expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value"))
    assert model.ordering == EnumerationOrder_Enum.CreatedDescending
    assert model.include_data is False
    assert model.include_subordinates is False
    assert model.max_results == 5
    assert model.continuation_token is None
    assert model.labels == []
    assert model.tags == {}
    assert hasattr(model.expr, 'model_config')


def test_enumeration_query_model_custom():
    model = EnumerationQueryModel(
        ordering=EnumerationOrder_Enum.CreatedAscending,
        include_data=True,
        include_subordinates=True,
        max_results=10,
        continuation_token='abc',
        labels=['A', 'B'],
        tags={'k': 'v'},
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    assert model.ordering == EnumerationOrder_Enum.CreatedAscending
    assert model.include_data is True
    assert model.include_subordinates is True
    assert model.max_results == 10
    assert model.continuation_token == 'abc'
    assert model.labels == ['A', 'B']
    assert model.tags == {'k': 'v'}


def test_enumeration_result_model_defaults():
    result = EnumerationResultModel()
    assert result.success is True
    assert isinstance(result.timestamp, TimestampModel)
    assert result.max_results == 1000
    assert result.iterations_required == 0
    assert result.continuation_token is None
    assert result.end_of_results is True
    assert result.total_records == 0
    assert result.records_remaining == 0
    assert result.objects == []


def test_enumeration_result_model_objects_none():
    result = EnumerationResultModel(objects=None)
    assert result.objects == []


def test_timestamp_model_defaults():
    ts = TimestampModel()
    assert ts.end is None
    assert isinstance(ts.start, type(ts.start))
    assert ts.messages == {}
    assert ts.metadata is None
    assert isinstance(ts.total_ms, float)


def test_timestamp_model_add_message():
    ts = TimestampModel()
    ts.add_message('test')
    assert any('test' in v for v in ts.messages.values())


def test_timestamp_model_add_message_empty():
    """Test adding empty message raises ValueError."""
    ts = TimestampModel()
    with pytest.raises(ValueError, match="Message cannot be empty"):
        ts.add_message('')


def test_timestamp_model_total_ms_with_end():
    """Test total_ms calculation when end time is set."""
    from datetime import datetime, timezone, timedelta
    
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(milliseconds=500)
    
    ts = TimestampModel(start=start_time, end=end_time)
    assert ts.total_ms == 500.0


def test_timestamp_model_total_ms_without_end():
    """Test total_ms calculation when end time is None."""
    ts = TimestampModel()
    total_ms = ts.total_ms
    assert isinstance(total_ms, float)
    assert total_ms >= 0


def test_enumeration_result_model_validation():
    """Test EnumerationResultModel validation with various parameters."""
    result = EnumerationResultModel(
        success=False,
        max_results=500,
        iterations_required=3,
        continuation_token="token123",
        end_of_results=False,
        total_records=1000,
        records_remaining=500,
        objects=[{"test": "data"}]
    )
    
    assert result.success is False
    assert result.max_results == 500
    assert result.iterations_required == 3
    assert result.continuation_token == "token123"
    assert result.end_of_results is False
    assert result.total_records == 1000
    assert result.records_remaining == 500
    assert len(result.objects) == 1


def test_enumeration_query_model_validation_constraints():
    """Test EnumerationQueryModel field constraints."""
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    # Test max_results constraints
    valid_model = EnumerationQueryModel(
        max_results=1000,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    assert valid_model.max_results == 1000
    
    # Test that we can create with min value
    min_model = EnumerationQueryModel(
        max_results=1,
        expr=ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    )
    assert min_model.max_results == 1


def test_enumeration_query_model_validation_edge_cases():
    """Test edge cases for EnumerationQueryModel validation."""
    from litegraph.models.enumeration_query import EnumerationQueryModel
    from litegraph.enums.enumeration_order_enum import EnumerationOrder_Enum
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    import pytest
    
    # Test max_results boundary conditions
    valid_expr = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    
    # Test minimum boundary
    model = EnumerationQueryModel(max_results=1, expr=valid_expr)
    assert model.max_results == 1
    
    # Test maximum boundary
    model = EnumerationQueryModel(max_results=1000, expr=valid_expr)
    assert model.max_results == 1000
    
    # Test invalid max_results values
    with pytest.raises(ValidationError):
        EnumerationQueryModel(max_results=0, expr=valid_expr)
    
    with pytest.raises(ValidationError):
        EnumerationQueryModel(max_results=1001, expr=valid_expr)
    
    # Test empty labels and tags
    model = EnumerationQueryModel(
        labels=[],
        tags={},
        expr=valid_expr
    )
    assert model.labels == []
    assert model.tags == {}
    
    # Test complex tags
    model = EnumerationQueryModel(
        tags={"key1": "value1", "key2": "value2", "nested.key": "nested.value"},
        expr=valid_expr
    )
    assert len(model.tags) == 3
    assert model.tags["nested.key"] == "nested.value"


def test_enumeration_result_model_edge_cases():
    """Test edge cases for EnumerationResultModel."""
    from litegraph.models.enumeration_result import EnumerationResultModel
    from litegraph.models.timestamp import TimestampModel
    
    # Test with max values
    result = EnumerationResultModel(
        max_results=10000,
        total_records=50000,
        records_remaining=40000,
        iterations_required=100
    )
    assert result.max_results == 10000
    assert result.total_records == 50000
    assert result.records_remaining == 40000
    assert result.iterations_required == 100
    
    # Test negative value validation should fail
    with pytest.raises(ValidationError):
        EnumerationResultModel(total_records=-1)
    
    with pytest.raises(ValidationError):
        EnumerationResultModel(records_remaining=-1)
    
    with pytest.raises(ValidationError):
        EnumerationResultModel(iterations_required=-1)
    
    # Test objects field edge cases
    result = EnumerationResultModel(objects=[{"test": "data"}, None, {"valid": "object"}])
    assert len(result.objects) == 3
    
    # Test with explicit None objects (should become empty list)
    result = EnumerationResultModel(objects=None)
    assert result.objects == []


def test_enumeration_ordering_enum_values():
    """Test all enumeration ordering enum values are valid."""
    from litegraph.enums.enumeration_order_enum import EnumerationOrder_Enum
    
    expected_values = [
        "CreatedAscending",
        "CreatedDescending", 
        "NameAscending",
        "NameDescending",
        "GuidAscending", 
        "GuidDescending",
        "CostAscending",
        "CostDescending"
    ]
    
    for value in expected_values:
        enum_val = EnumerationOrder_Enum(value)
        assert enum_val.value == value
        
    # Test that each enum can be used in EnumerationQueryModel
    from litegraph.models.enumeration_query import EnumerationQueryModel
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    expr = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    
    for ordering in EnumerationOrder_Enum:
        model = EnumerationQueryModel(ordering=ordering, expr=expr)
        assert model.ordering == ordering


def test_enumeration_performance_edge_cases():
    """Test enumeration with performance-related edge cases."""
    from litegraph.models.enumeration_query import EnumerationQueryModel
    from litegraph.models.expression import ExprModel
    from litegraph.enums.operator_enum import Opertator_Enum
    
    expr = ExprModel(Left="field", Operator=Opertator_Enum.Equals, Right="value")
    
    # Test with large labels list
    large_labels = [f"label_{i}" for i in range(100)]
    model = EnumerationQueryModel(labels=large_labels, expr=expr)
    assert len(model.labels) == 100
    
    # Test with complex tags
    large_tags = {f"key_{i}": f"value_{i}" for i in range(50)}
    model = EnumerationQueryModel(tags=large_tags, expr=expr)
    assert len(model.tags) == 50
    
    # Test serialization doesn't break with large data (both labels and tags)
    model_both = EnumerationQueryModel(labels=large_labels, tags=large_tags, expr=expr)
    serialized = model_both.model_dump(by_alias=True, mode="json", exclude_unset=True)
    assert "Labels" in serialized
    assert "Tags" in serialized
    assert len(serialized["Labels"]) == 100
    assert len(serialized["Tags"]) == 50
