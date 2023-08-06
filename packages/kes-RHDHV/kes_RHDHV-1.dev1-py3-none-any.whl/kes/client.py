"""Client module.

This module is the starting point for wrting a Kes Python script.
Scripts typically start by configuring and creating a client, after which this client can be used to open projects.

Usage example::

    config = Config(kes_service_address='localhost:50051')
    client = Client(config)
    project = client.open_project("Preview Python client example")
"""

from dataclasses import dataclass
from uuid import UUID

import grpc

from kes.proto.table_pb2_grpc import TableStub

from kes.proto.project_pb2_grpc import ProjectStub

from kes.project import Project
from kes.proto.project_pb2 import LookupProjectRequest


class ProjectNotFound(Exception):
    """ Exception indicating when a project could not be found."""
    ...


@dataclass
class Config:
    """Holds configuration of the client.

    Attributes:
        kes_service_address:
            Address of the service which interacts with the Kes database.
            Example: 'https://kes-table-service-pr-staging.bluebush-b51cfb01.westeurope.azurecontainerapps.io:50051'
        access_token:
            Access token. Can be obtained from the Kes project manager.
        root_certificates_path:
            Path to the file containing the root certificates.

    """
    kes_service_address: str
    access_token: str
    root_certificates_path: str


class Client:
    """Kes client.

    Starting point of a kes script. After creating a client instance, kes projects can be opened using open_project.
    """

    _channel: grpc.Channel
    _table_stub: TableStub
    _project_stub: ProjectStub

    def __init__(self, config: Config):
        """Constructs a client.

        Args:
            config (Config): The client configuration
        """
        with open(config.root_certificates_path, 'rb') as f:
            root_certificates = f.read()
        channel_credentials = grpc.ssl_channel_credentials(root_certificates)
        call_credentials = grpc.access_token_call_credentials(config.access_token)
        combined_credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        self._channel = grpc.secure_channel(config.kes_service_address, combined_credentials)
        self._table_stub = TableStub(self._channel)
        self._project_stub = ProjectStub(self._channel)

    def open_project_by_master_id(self, master_id: str) -> Project:
        """Open a Kes project by master project id.

        Args:
            project_name (str): Name of the project to open.

        Returns:
            An instance representing the requested Kes project.

        Raises:
            ProjectNotFound: The requested project could not be found.
        """
        try:
            request = LookupProjectRequest(masterProjectId=master_id)
            reply = self._project_stub.lookupProject(request)
            projectId = UUID(reply.projectId)
            return Project(projectId, self._table_stub, self._project_stub)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ProjectNotFound
            else:
                raise

    def open_project_by_id(self, project_id: UUID) -> Project:
        """Open a Kes project by id

        Args:
            project_id (UUID): uuid of the project to open.

        Returns:
            An instance representing the requested Kes project.
        """
        return Project(project_id, self._table_stub, self._project_stub)
