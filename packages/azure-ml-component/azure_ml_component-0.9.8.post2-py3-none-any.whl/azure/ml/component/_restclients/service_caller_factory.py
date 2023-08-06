# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from .service_caller import DesignerServiceCaller
import _thread
from threading import Lock


class _DesignerServiceCallerFactory:

    caller_cache_by_workspace_id = {}
    _instance_lock = Lock()

    @classmethod
    def get_instance(cls, workspace, from_cli=False) -> DesignerServiceCaller:
        """Get a instance of designer service caller.

        :param workspace: workspace
        :param from_cli: mark if this service caller is used from cli.
        """
        workspace_id = workspace._workspace_id if workspace else None
        cache = cls.caller_cache_by_workspace_id
        if workspace_id not in cache:
            with _DesignerServiceCallerFactory._instance_lock:
                if workspace_id not in cache:
                    cache[workspace_id] = DesignerServiceCaller(workspace)
                    if from_cli:
                        cache[workspace_id]._set_from_cli_for_telemetry()
                    else:
                        # For SDK, we cache all the computes at the initialization of designer service caller
                        if workspace:
                            _thread.start_new_thread(cache_all_computes, (cache[workspace_id], ))
        return cache[workspace_id]


def cache_all_computes(service_caller):
    try:
        service_caller.cache_all_computes_in_workspace()
    except Exception:
        # Catch all exceptions here
        pass
