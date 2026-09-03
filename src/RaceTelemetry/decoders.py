from __future__ import annotations
import logging

from typing import TYPE_CHECKING, Any

from types import SimpleNamespace

if TYPE_CHECKING:
    from RaceTelemetry.main import TelemetryConfig
    from .data_structures.IRacing_struct import irsdk_header, irsdk_varHeader


LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Static Decoder
# ---------------------------------------------------------------------------


class StaticDecoding:
    """
    Takes raw bytes and decodes them into static packets using the metadata.
    """

    def __init__(self, config: TelemetryConfig):
        self.config = config
        LOGGER.debug("StaticDecoding initialized with metadata: %r", config.active_metadata.__name__ if config.active_metadata else None)

    def decodeHeader(self, data: bytes) -> Any | None:
        if not self.config.header_packet:
            return

        headerBufferSize = self.config.get_packet_size(self.config.header_packet)
        rawHeaderPacket = self.config.header_packet.from_buffer_copy(data[0:headerBufferSize])
        return rawHeaderPacket

    def construct_packet(self, data: bytes, possiblePacketStruct: tuple) -> type | None:
        """
        Helper function to construct a packet from the data using the possible packet structures provided in the metadata.
        Returns the constructed packet, or None if no matching packet structure is found.
        """
        if not data:
            return None

        rawPacket: type | None
        packet = None
        packetSizes = []
        dataLength = len(data)
        for packetStruct in possiblePacketStruct:
            packetBufferSize = self.config.get_packet_size(packetStruct)
            if packetBufferSize != dataLength:
                packetSizes.append(packetBufferSize)
            else:
                try:
                    rawPacket = packetStruct.from_buffer_copy(data[0:packetBufferSize])
                except ValueError as exc:
                    LOGGER.debug("Packet failed to unpack with %r", packetStruct.__name__)
                    continue
                else:
                    packet = rawPacket
                    break

        if len(possiblePacketStruct) == len(packetSizes):
            LOGGER.warning("[Warning]\tNo matching packet size [%r] for received data length %r", packetSizes, dataLength)
            packet = None

        return packet

    def decode_packet(self, data: bytes) -> tuple[SimpleNamespace | type | None, int, Any]:
        """
        Helper function to decode the packet, packet ID, and header packet (if applicable) from the raw data.
        Returns a tuple of (packet, packetID, headerPacket).
        packet and headerPacket may be None if no matching packet structure is found or if no header is defined in the metadata.
        """

        if not self.config.packet_info:
            LOGGER.error("Packet Info is empty.")
            raise ValueError("Packet Info is empty.")

        # retreive header packet and packet id
        if self.config.header_packet:
            if not self.config.packet_id_attr:
                LOGGER.error("Packet ID Attribute is empty.")
                raise ValueError("Packet ID Attribute is empty.")

            headerPacket = self.decodeHeader(data)

            if hasattr(headerPacket, self.config.packet_id_attr):
                packetID = int(getattr(headerPacket, self.config.packet_id_attr))
            else:
                LOGGER.warning("Header packet %r doesnt contain the ID attribute %r", headerPacket, self.config.packet_id_attr)
                packetID = 0
        else:
            headerPacket = None
            packetID = 0

        # retrieve packet struct
        possiblePacketStruct = self.config.packet_info.get(packetID)
        if possiblePacketStruct:
            packet = self.construct_packet(data, possiblePacketStruct)
        else:
            LOGGER.warning("ID not found")
            packet = None

        return packet, packetID, headerPacket


# ---------------------------------------------------------------------------
# Dynamic Decoder - IRacing
# ---------------------------------------------------------------------------


class IracingDynamicDecoder:
    from .data_structures.IRacing_struct import irsdk_header, irsdk_varHeader, VAR_TYPE_MAP

    """
    Decoder for iRacing's shared memory block.

    decode_packet(data) mirrors the signature your static struct decoders
    use: it returns (decodedData, packetID, header).

    - decodedData: dict[str, Any] of every telemetry variable this session,
      keyed by name (e.g. "Speed", "RPM", "Gear", "Lap", ...).
    - packetID: always 0 for iRacing - there's only one packet type, unlike
      transports with multiple distinct struct layouts.
    - header: the parsed irsdk_header for this packet, in case callers need
      tickCount / status / tickRate etc.
    """

    def __init__(self, config: TelemetryConfig) -> None:
        self.config = config

        # constants
        self.HEADER_SIZE = self.config.get_packet_size(self.irsdk_header)
        self.VAR_HEADER_SIZE = self.config.get_packet_size(self.irsdk_varHeader)

        # cached dynamic layout - rebuilt only when it changes
        self._var_table: dict[str, irsdk_varHeader] = {}
        self._cached_num_vars: int = -1
        self._cached_var_header_offset: int = -1

        # cached session info YAML
        self._session_info: dict | None = None
        self._session_info_update: int = -1

        try:
            import yaml
        except ImportError:
            LOGGER.critical("PyYAML is not installed. Session info parsing will be disabled.")
            raise ImportError("IRacing telemetry requires pyYaml. Install it with " "'pip install RaceTelemetry[iracing]'.")

        LOGGER.debug("IracingDynamicDecoder initialised")

    # ---- public API, matches your existing decoder interface ------------

    def decode_packet(self, data: bytes) -> tuple[SimpleNamespace | type | None, int, Any]:
        # Any typehint is actually irsdk_header
        if not self.config.header_packet:
            LOGGER.error("Header Packet is empty.")
            raise ValueError("Header Packet is empty.")

        header: irsdk_header = self.config.header_packet.from_buffer_copy(data[: self.HEADER_SIZE])
        # header = irsdk_header.from_buffer_copy(data[: self.HEADER_SIZE])

        if self._layout_changed(header):
            self._build_var_table(data, header)

        if header.sessionInfoUpdate != self._session_info_update:
            self._session_info = self._parse_session_info(data, header)
            self._session_info_update = header.sessionInfoUpdate

        decodedData = self._decode_values(data, header)
        setattr(decodedData, "_session_info_", self._session_info)

        packetID = 0  # iRacing only publishes one packet type
        return decodedData, packetID, header

    # ---- dynamic layout handling -----------------------------------------

    def _layout_changed(self, header: irsdk_header) -> bool:
        numVars = header.numVars != self._cached_num_vars
        headerOffset = header.varHeaderOffset != self._cached_var_header_offset
        return numVars or headerOffset or not self._var_table

    def _build_var_table(self, data: bytes, header: irsdk_header) -> None:
        LOGGER.info("Rebuilding var header table (numVars=%d)", header.numVars)
        table: dict[str, irsdk_varHeader] = {}

        for i in range(header.numVars):
            offset = header.varHeaderOffset + i * self.VAR_HEADER_SIZE
            raw = data[offset : offset + self.VAR_HEADER_SIZE]
            varHeader = self.irsdk_varHeader.from_buffer_copy(raw)
            name = varHeader.name.decode("utf-8", errors="ignore").rstrip("\x00")
            table[name] = varHeader

        self._var_table = table
        self._cached_num_vars = header.numVars
        self._cached_var_header_offset = header.varHeaderOffset

    def _parse_session_info(self, data: bytes, header: irsdk_header) -> dict | None:
        import yaml

        raw = data[header.sessionInfoOffset : header.sessionInfoOffset + header.sessionInfoLen]
        text = raw.split(b"\x00", 1)[0].decode("utf-8", errors="ignore")
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            LOGGER.warning("Failed to parse session info YAML: %r", exc)
            return None

    # ---- value decoding ----------------------------------------------------

    def _latest_buffer(self, header: irsdk_header):
        """iRacing keeps up to numBuf copies of the data row to avoid tearing
        mid-write; use whichever has the highest tickCount."""
        return max(header.varBuf[: header.numBuf], key=lambda b: b.tickCount)

    def _decode_values(self, data: bytes, header: irsdk_header) -> SimpleNamespace:
        buf = self._latest_buffer(header)
        newPacket = SimpleNamespace()
        newPacket.__name__ = "irsdk_varBuf"

        for name, varHeader in self._var_table.items():
            ctype = self.VAR_TYPE_MAP[varHeader.type]
            row_offset = buf.bufOffset + varHeader.offset

            if varHeader.count == 1:
                size = self.config.get_packet_size(ctype)
                raw = data[row_offset : row_offset + size]
                field = ctype.from_buffer_copy(raw).value
                setattr(newPacket, name, field)
            else:
                arr_type = ctype * varHeader.count
                size = self.config.get_packet_size(arr_type)
                raw = data[row_offset : row_offset + size]
                field = list(arr_type.from_buffer_copy(raw))
                setattr(newPacket, name, field)

        return newPacket


# --- Decoder Registor ---------------------------

DECODER_REGISTER: dict[str, type] = {
    "static": StaticDecoding,
    "iracing_dynamic": IracingDynamicDecoder,
}
