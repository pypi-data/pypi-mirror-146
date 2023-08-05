#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import List, Optional, Dict, Any, TYPE_CHECKING
from mephisto.abstractions.blueprint import AgentState
import os
import json
import weakref

if TYPE_CHECKING:
    from mephisto.data_model.agent import Agent
    from mephisto.data_model.packet import Packet


class MockAgentState(AgentState):
    """
    Mock agent state that is to be used for testing
    """

    def __init__(self, agent: "Agent"):
        """Mock agent states keep everything in local memory"""
        self.agent = weakref.proxy(agent)
        self.state: Dict[str, Any] = {}
        self.init_state: Any = None

    def set_init_state(self, data: Any) -> bool:
        """Set the initial state for this agent"""
        if self.init_state is not None:
            # Initial state is already set
            return False
        else:
            self.init_state = data
            self.save_data()
            return True

    def get_init_state(self) -> Optional[Dict[str, Any]]:
        """
        Return the initial state for this agent,
        None if no such state exists
        """
        return self.init_state

    def load_data(self) -> None:
        """Mock agent states have no data stored"""
        pass

    def get_data(self) -> Dict[str, Any]:
        """Return dict of this agent's state"""
        return self.state

    def save_data(self) -> None:
        """Mock agents don't save data (yet)"""
        pass

    def update_data(self, live_update: Dict[str, Any]) -> None:
        """Put new data into this mock state"""
        self.state = live_update

    def update_submit(self, submitted_data: Dict[str, Any]) -> None:
        """Move the submitted data into the live state"""
        self.state = submitted_data
