from ..configuration import get_client
from ..mixins import (
    AllRetrievableAPIResource,
    DeletableAPIResource,
    ExistsAPIResource,
    RetrievableAPIResource,
)
from ..models.backup import BackupModel
from ..utils.url_helper import _get_url_v1


class Admin(
    ExistsAPIResource,
    RetrievableAPIResource,
    AllRetrievableAPIResource,
    DeletableAPIResource,
):
    """
    Admin resource class.
    """

    REQUIRE_TENANT = False
    REQUIRE_GRAPH_GUID = False

    @classmethod
    def create_backup(cls, filename: str) -> bool:
        """
        Create a backup of a graph.

        Args:
            filename: The name of the backup file.

        Returns:
            True if the backup was created successfully, False otherwise.
        """
        client = get_client()

        url = _get_url_v1(cls, "backups")
        try:
            client.request("POST", url, json={"Filename": filename})
            return True
        except Exception:
            return False

    @classmethod
    def exists(cls, filename: str) -> bool:
        """
        Check if a backup exists.

        Args:
            filename: The name of the backup file.

        Returns:
            True if the backup exists, False otherwise.
        """
        cls.RESOURCE_NAME = "backups"
        return super().exists(filename)

    @classmethod
    def retrieve_all(cls) -> list[BackupModel]:
        """
        Retrieve all backups.

        Returns:
            A list of all backups.
        """
        cls.RESOURCE_NAME = "backups"
        return super().retrieve_all()

    @classmethod
    def retrieve(cls, filename: str) -> BackupModel:
        """
        Retrieve a backup content.

        Args:
            filename: The name of the backup file.

        Returns:
            The backup.
        """
        cls.RESOURCE_NAME = "backups"
        return super().retrieve(filename)

    @classmethod
    def delete(cls, filename: str) -> bool:
        """
        Delete a backup.

        Args:
            filename: The name of the backup file.

        Returns:
            True if the backup was deleted successfully, False otherwise.
        """
        cls.RESOURCE_NAME = "backups"
        try:
            super().delete(filename)
            return True
        except Exception:
            return False

    @classmethod
    def flush_db_to_disk(cls) -> bool:
        """
        Flush the database to disk.

        Returns:
            True if the database was flushed successfully, False otherwise.
        """
        client = get_client()

        url = _get_url_v1(cls, "flush")
        try:
            client.request("POST", url, json={})
            return True
        except Exception:
            return False
