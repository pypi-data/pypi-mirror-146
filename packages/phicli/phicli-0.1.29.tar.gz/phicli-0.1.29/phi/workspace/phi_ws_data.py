import datetime
from pathlib import Path
from typing import List, Optional, Set

from pydantic import BaseModel
from phidata.workspace import WorkspaceConfig

from phi.utils.common import is_empty
from phi.utils.dttm import current_datetime_utc
from phi.utils.log import logger
from phi.workspace.ws_enums import WorkspaceSetupActions
from phi.workspace.exceptions import WorkspaceConfigException
from phi.workspace.ws_schemas import WorkspaceSchema


class PhiWsData(BaseModel):
    """The PhiWsData model stores data for a phidata workspace."""

    # Name of the workspace
    ws_name: str
    # WorkspaceSchema: If exists then indicates that this ws has been authenticated
    # with the backend
    ws_schema: Optional[WorkspaceSchema] = None
    # The root directory for the workspace.
    # This field indicates that this ws has been downloaded on this machine
    ws_dir_path: Optional[Path] = None
    # Path for the WorkspaceConfig file
    ws_config_file_path: Optional[Path] = None
    # A Set of WorkspaceSetupActions which this workspace must satisfy to become valid.
    # if len(ws_data.required_actions.intersection(ws_data.pending_actions)) > 0:
    # the workspace is invalid
    required_actions: Set[WorkspaceSetupActions] = {
        WorkspaceSetupActions.WS_CONFIG_IS_AVL
    }
    # A Set of WorkspaceSetupActions which this workspace currently has not
    # completed and needs to fulfill.
    # When (pending_actions is None or len(pending_actions) == 0), the workspace is valid
    pending_actions: Set[WorkspaceSetupActions] = set()
    # Timestamp of when this workspace was created on the users machine
    create_ts: datetime.datetime = current_datetime_utc()
    # Timestamp when this ws was last updated
    last_update_ts: Optional[datetime.datetime] = None

    cached_ws_config: Optional[WorkspaceConfig] = None

    class Config:
        arbitrary_types_allowed = True

    ######################################################
    ## WorkspaceConfig functions
    ######################################################

    @property
    def ws_config(self) -> Optional[WorkspaceConfig]:
        """
        Returns the WorkspaceConfig for this workspace
        """

        if self.cached_ws_config is not None:
            return self.cached_ws_config

        if self.ws_config_file_path is None or self.ws_dir_path is None:
            raise WorkspaceConfigException("WorkspaceConfig invalid")

        from phi.workspace.ws_loader import add_ws_dir_to_path, load_workspace

        add_ws_dir_to_path(self.ws_dir_path)

        logger.debug(f"**--> Loading WorkspaceConfig")
        ws_configs: List[WorkspaceConfig]
        ws_configs = load_workspace(self.ws_config_file_path)

        if is_empty(ws_configs):
            logger.debug(f"No WorkspaceConfig found")
            raise WorkspaceConfigException("No WorkspaceConfig found")

        if len(ws_configs) > 1:
            logger.warning(
                "Found {} WorkspaceConfigs, first one will be selected".format(
                    len(ws_configs)
                )
            )
        self.cached_ws_config = ws_configs[0]
        # logger.debug("WorkspaceConfig:\n{}".format(self.cached_ws_config.args))
        return self.cached_ws_config

    ######################################################
    ## Print functions
    ######################################################

    def print_to_cli(self):
        from rich.pretty import pprint

        pprint(self.dict())
