import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from litegraph.resources.admin import Admin
from litegraph.models.backup import BackupModel

@pytest.fixture
def mock_client(monkeypatch):
    client = Mock()
    monkeypatch.setattr("litegraph.configuration._client", client)
    return client

@pytest.fixture
def sample_backup():
    now = datetime.now(timezone.utc).isoformat()
    return {
        "Filename": "backup1.db",
        "Length": 12345,
        "MD5Hash": "md5",
        "SHA1Hash": "sha1",
        "SHA256Hash": "sha256",
        "CreatedUtc": now,
        "LastUpdateUtc": now,
        "LastAccessUtc": now,
    }

def test_create_backup_success(mock_client):
    mock_client.request.return_value = None
    assert Admin.create_backup("backup1.db") is True
    mock_client.request.assert_called_once()

def test_create_backup_failure(mock_client):
    mock_client.request.side_effect = Exception("fail")
    assert Admin.create_backup("backup1.db") is False

def test_exists_calls_super(mock_client):
    mock_client.request.return_value = True
    result = Admin.exists("backup1.db")
    assert result is True
    mock_client.request.assert_called_once()

def test_retrieve_all(mock_client, sample_backup):
    mock_client.request.return_value = [sample_backup]
    result = Admin.retrieve_all()
    assert isinstance(result, list)
    assert isinstance(result[0], BackupModel)
    assert result[0].filename == sample_backup["Filename"]

def test_retrieve(mock_client, sample_backup):
    mock_client.request.return_value = sample_backup
    result = Admin.retrieve("backup1.db")
    assert isinstance(result, BackupModel)
    assert result.filename == sample_backup["Filename"]

def test_delete_success(mock_client):
    # Simulate a successful delete (no exception)
    mock_client.request.return_value = None
    Admin.RESOURCE_NAME = "backups"
    assert Admin.delete("backup1.db") is True
    mock_client.request.assert_called_once()

def test_delete_failure(mock_client):
    # Simulate a failure (exception raised)
    mock_client.request.side_effect = Exception("fail")
    Admin.RESOURCE_NAME = "backups"
    assert Admin.delete("backup1.db") is False
    mock_client.request.assert_called_once()

def test_flush_db_to_disk_success(mock_client):
    mock_client.request.return_value = None
    assert Admin.flush_db_to_disk() is True

def test_flush_db_to_disk_failure(mock_client):
    mock_client.request.side_effect = Exception("fail")
    assert Admin.flush_db_to_disk() is False
 