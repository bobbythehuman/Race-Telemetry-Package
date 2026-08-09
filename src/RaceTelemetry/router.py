import ctypes
import logging
from types import SimpleNamespace

from typing import TYPE_CHECKING, Any
from .digestion import dynamic_ingest

if TYPE_CHECKING:
    from RaceTelemetry.main import TelemetryConfig


LOGGER = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Packet decoding — function of config + bytes
# ---------------------------------------------------------------------------


class PacketRouter:
    """
    Takes raw bytes and decodes them into packets using the metadata.
    """

    def __init__(self, config: TelemetryConfig):
        self.config = config
        LOGGER.debug("PacketRouter initialized with metadata: %r", config.active_metadata.__name__ if config.active_metadata else None)

    def get_packet_size(self, packet: type) -> int:
        """Helper function to get the size of a packet using ctypes.sizeof, which is needed for shared memory reading and UDP packet construction."""
        size = ctypes.sizeof(packet)
        return size

    def get_max_packet_size(self) -> int:
        """Helper function to get the maximum packet size from the packet info in the metadata, which is needed for setting the full buffer size if not provided in the metadata."""
        if not self.config.packet_info:
            LOGGER.error("Packet Info is empty.")
            raise ValueError("Packet Info is empty.")

        allSizes = []
        for packetID, packetInfo in self.config.packet_info.items():
            for packetStruct in packetInfo:
                packetSize = self.get_packet_size(packetStruct)
                allSizes.append(packetSize)

        LOGGER.debug("Maximum packet size calculated: %r", max(allSizes) if allSizes else 0)
        return max(allSizes) if allSizes else 0

    def construct_packet(self, data: bytes, possiblePacketStruct: tuple) -> SimpleNamespace | None:
        """
        Helper function to construct a packet from the data using the possible packet structures provided in the metadata.
        Returns the constructed packet, or None if no matching packet structure is found.
        """
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetStruct in possiblePacketStruct:
            packetBufferSize = self.get_packet_size(packetStruct)
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    LOGGER.debug("Packet failed to unpack with %r", packetStruct.__name__)
                    continue
                else:
                    packet = dynamic_ingest(rawPacket, self.config.enum_mode)
                    break

        if len(possiblePacketStruct) == len(packetSizes):
            LOGGER.warning("[Warning]\tNo matching packet size [%r] for received data length %r", packetSizes, dataLength)
            packet = None
        return packet

    def retrieve_packet(self, data: bytes) -> tuple[SimpleNamespace | None, int, Any]:
        """
        Helper function to retrieve the packet, packet ID, and header packet (if applicable) from the raw data.
        Returns a tuple of (packet, packetID, headerPacket).
        packet and headerPacket may be None if no matching packet structure is found or if no header is defined in the metadata.
        """

        if not self.config.packet_info:
            LOGGER.error("Packet Info is empty.")
            raise ValueError("Packet Info is empty.")

        if self.config.header_packet:
            if not self.config.packet_id_attr:
                LOGGER.error("Packet ID Attribute is empty.")
                raise ValueError("Packet ID Attribute is empty.")

            headerBufferSize = self.get_packet_size(self.config.header_packet)
            rawHeaderPacket = self.config.header_packet.from_buffer_copy(data[0:headerBufferSize])
            headerPacket = dynamic_ingest(rawHeaderPacket)

            if hasattr(headerPacket, self.config.packet_id_attr):
                packetID = int(getattr(headerPacket, self.config.packet_id_attr))
            else:
                LOGGER.warning("[NTWK] [Warning]\tHeader packet %r doesnt contain the ID attribute %r", headerPacket, self.config.packet_id_attr)
                packetID = 0
        else:
            headerPacket = None
            packetID = 0

        possiblePacketStruct = self.config.packet_info.get(packetID)
        if possiblePacketStruct:
            packet = self.construct_packet(data, possiblePacketStruct)
        else:
            LOGGER.warning("ID not found")
            packet = None

        return packet, packetID, headerPacket
