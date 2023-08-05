#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
FastyBird MQTT connector clients module interfaces
"""

# Python base dependencies
from abc import ABC, abstractmethod


class IClient(ABC):
    """
    Client interface

    @package        FastyBird:FbMqttConnector!
    @module         clients/client

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if client is connected to broker"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def start(self) -> None:
        """Start communication"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def stop(self) -> None:
        """Stop communication"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def handle(self) -> None:
        """Handle connector devices"""
