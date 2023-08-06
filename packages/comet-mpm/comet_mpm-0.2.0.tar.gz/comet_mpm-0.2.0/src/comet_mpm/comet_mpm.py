# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import asyncio as asyncio_module
import atexit
import calendar
import os
from datetime import datetime
from typing import Any, Awaitable, Dict, Optional

from .connection import MPM_BASE_PATH, REST_API_BASE_PATH, sanitize_url, url_join
from .constants import (
    EVENT_FEATURES,
    EVENT_PREDICTION,
    EVENT_PREDICTION_ID,
    EVENT_PREDICTION_PROBABILITY,
    EVENT_PREDICTION_VALUE,
    EVENT_TIMESTAMP,
    EVENT_WORKSPACE_NAME,
)
from .sender import get_sender
from .settings import MPMSettings, get_model


def local_timestamp() -> int:
    """Return a timestamp in a format expected by the backend (milliseconds)"""
    now = datetime.utcnow()
    timestamp_in_seconds = calendar.timegm(now.timetuple()) + (now.microsecond / 1e6)
    timestamp_in_milliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_milliseconds


class CometMPM:
    def __init__(
        self,
        api_key: Optional[str] = None,
        workspace_name: Optional[str] = None,
        model_name: Optional[str] = None,
        model_version: Optional[str] = None,
        disabled: Optional[bool] = None,
        asyncio: bool = False,
    ):

        settings_user_values = {}  # type: Dict[str, str]
        # Filter out None
        if api_key is not None:
            settings_user_values["api_key"] = api_key

        if model_name is not None:
            settings_user_values["mpm_model_name"] = model_name

        if model_version is not None:
            settings_user_values["mpm_model_version"] = model_version

        if workspace_name is not None:
            settings_user_values["mpm_workspace_name"] = workspace_name

        self._settings = get_model(
            MPMSettings,
            **settings_user_values,
        )
        if disabled:
            self.disabled = disabled  # type: bool
        else:
            self.disabled = bool(os.getenv("COMET_MPM_DISABLED"))
        self._asyncio = asyncio

        self._mpm_url = url_join(sanitize_url(self._settings.url), MPM_BASE_PATH)
        self._api_url = url_join(sanitize_url(self._settings.url), REST_API_BASE_PATH)

        if self.disabled:
            self._sender = None
        else:
            self._sender = get_sender(
                self._settings.api_key,
                self._mpm_url,
                self._settings.mpm_model_name,
                self._settings.mpm_model_version,
                max_batch_size=self._settings.mpm_max_batch_size,
                max_batch_time=self._settings.mpm_max_batch_time,
                asyncio=self._asyncio,
                batch_sending_timeout=self._settings.mpm_batch_sending_timeout,
            )

            atexit.register(self._on_end)

        # TODO: Do handshake

    def log_event(
        self,
        prediction_id: str,
        input_features: Optional[Dict[str, Any]] = None,
        output_value: Optional[Any] = None,
        output_probability: Optional[Any] = None,
    ) -> Optional[Awaitable[None]]:
        if self.disabled:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

        prediction: Dict[str, Any] = {}
        if output_value is not None:
            prediction[EVENT_PREDICTION_VALUE] = output_value
        if output_probability is not None:
            prediction[EVENT_PREDICTION_PROBABILITY] = output_probability

        event = {
            EVENT_WORKSPACE_NAME: self._settings.mpm_workspace_name,
            EVENT_PREDICTION_ID: prediction_id,
            EVENT_TIMESTAMP: local_timestamp(),
        }

        if input_features is not None:
            event[EVENT_FEATURES] = input_features

        if prediction:
            event[EVENT_PREDICTION] = prediction

        assert self._sender is not None
        return self._sender.put(event)

    def connect(self) -> None:
        if self._sender is not None:
            self._sender.connect()

    def join(self, timeout: Optional[int] = None) -> Optional[Awaitable[None]]:
        if timeout is None:
            timeout = self._settings.mpm_join_timeout

        if not self.disabled:
            assert self._sender is not None
            return self._sender.join(timeout)
        else:
            if self._asyncio is False:
                return None
            else:
                return asyncio_module.sleep(0)

    def _on_end(self) -> None:
        if not self.disabled:
            assert self._sender is not None
            self._sender.close()
