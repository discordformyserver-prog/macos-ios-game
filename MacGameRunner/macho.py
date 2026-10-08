import struct
from typing import Any, Dict, List, Tuple


CPU_TYPES = {
    0x00000001: "vax",
    0x01000000: "arm64",
    0x01000007: "x86_64",
    0x00000007: "x86_64",
    0x00000003: "x86",
    0x0000000C: "arm",
}

PLATFORMS = {
    1: "macos",
    2: "ios",
    3: "tvos",
    4: "watchos",
    5: "bridgeos",
    6: "macCatalyst",
    7: "iossimulator",
    8: "tvsimulator",
    9: "watchsimulator",
    10: "driverkit",
    11: "iosmac",
}

LOAD_COMMANDS = {
    0x00: "LC_SEGMENT",
    0x01: "LC_SYMTAB",
    0x02: "LC_SYMSEG",
    0x03: "LC_THREAD",
    0x04: "LC_UNIXTHREAD",
    0x05: "LC_LOADFVMLIB",
    0x06: "LC_IDFVMLIB",
    0x07: "LC_IDENT",
    0x08: "LC_FVMFILE",
    0x09: "LC_PREPAGE",
    0x0A: "LC_DYSYMTAB",
    0x0B: "LC_LOAD_DYLIB",
    0x0C: "LC_ID_DYLIB",
    0x0D: "LC_LOAD_DYLINKER",
    0x0E: "LC_ID_DYLINKER",
    0x0F: "LC_PREBOUND_DYLIB",
    0x10: "LC_ROUTINES",
    0x11: "LC_SUB_FRAMEWORK",
    0x12: "LC_SUB_UMBRELLA",
    0x13: "LC_SUB_CLIENT",
    0x14: "LC_SUB_LIBRARY",
    0x15: "LC_TWOLEVEL_HINTS",
    0x16: "LC_PREBIND_CKSUM",
    0x18: "LC_SEGMENT_64",
    0x19: "LC_ROUTINES_64",
    0x1A: "LC_UUID",
    0x1B: "LC_RPATH",
    0x1C: "LC_CODE_SIGNATURE",
    0x1D: "LC_SEGMENT_SPLIT_INFO",
    0x1E: "LC_LAZY_LOAD_DYLIB",
    0x1F: "LC_ENCRYPTION_INFO",
    0x20: "LC_DYLD_INFO",
    0x21: "LC_DYLD_INFO_ONLY",
    0x22: "LC_LOAD_UPWARD_DYLIB",
    0x23: "LC_VERSION_MIN_MACOSX",
    0x24: "LC_VERSION_MIN_IPHONEOS",
    0x25: "LC_FUNCTION_STARTS",
    0x26: "LC_DYLD_ENVIRONMENT",
    0x27: "LC_MAIN",
    0x28: "LC_DATA_IN_CODE",
    0x29: "LC_SOURCE_VERSION",
    0x2A: "LC_DYLIB_CODE_SIGN_DRS",
    0x2B: "LC_ENCRYPTION_INFO_64",
    0x2C: "LC_LINKER_OPTION",
    0x2D: "LC_LINKER_OPTIMIZATION_HINT",
    0x2E: "LC_VERSION_MIN_TVOS",
    0x2F: "LC_VERSION_MIN_WATCHOS",
    0x30: "LC_NOTE",
    0x31: "LC_BUILD_VERSION",
    0x32: "LC_BUILD_VERSION",
    0x33: "LC_DYLD_EXPORTS_TRIE",
    0x34: "LC_DYLD_CHAINED_FIXUPS",
    0x35: "LC_FILESET_ENTRY",
    0x36: "LC_ATOM_INFO",
    0x37: "LC_DYLD_RPATH",
}

MAGIC_32 = 0xFEEDFACE
MAGIC_64 = 0xFEEDFACF
FAT_MAGIC = 0xCAFEBABE
FAT_CIGAM = 0xBEBAFECA


class MachOAnalyzer:
    @staticmethod
    def analyze_bytes(blob: bytes) -> Dict[str, Any]:
        if not blob:
            return {"is_macho": False, "error": "empty blob"}

        magic_le = struct.unpack_from("<I", blob, 0)[0]
        magic_be = struct.unpack_from(">I", blob, 0)[0]

        if magic_be == FAT_MAGIC:
            return MachOAnalyzer._analyze_fat(blob, byteorder="big")
        if magic_le == FAT_MAGIC:
            return MachOAnalyzer._analyze_fat(blob, byteorder="little")
        if magic_le in (MAGIC_32, MAGIC_64):
            return MachOAnalyzer._analyze_macho(blob, magic_le)
        if magic_be in (MAGIC_32, MAGIC_64):
            return MachOAnalyzer._analyze_macho(blob, magic_be)
        return {"is_macho": False, "magic_le": hex(magic_le), "magic_be": hex(magic_be), "reason": "not a Mach-O image"}

    @staticmethod
    def _analyze_fat(blob: bytes, byteorder: str) -> Dict[str, Any]:
        if byteorder == "big":
            nfat_arch = struct.unpack_from(">I", blob, 4)[0]
            offset = 8
        else:
            nfat_arch = struct.unpack_from("<I", blob, 4)[0]
            offset = 8

        archs: List[Dict[str, Any]] = []
        for _ in range(nfat_arch):
            if offset + 20 > len(blob):
                break
            if byteorder == "big":
                cputype, cpusubtype, fileoff, filesize, align = struct.unpack_from(">IIIII", blob, offset)
            else:
                cputype, cpusubtype, fileoff, filesize, align = struct.unpack_from("<IIIII", blob, offset)
            archs.append(
                {
                    "cputype": cputype,
                    "cpusubtype": cpusubtype,
                    "arch": CPU_TYPES.get(cputype, f"cpu_{cputype:x}"),
                    "offset": fileoff,
                    "size": filesize,
                    "align": align,
                }
            )
            offset += 20

        return {
            "is_macho": True,
            "is_fat": True,
            "fat_architectures": archs,
            "arch": archs[0]["arch"] if archs else "unknown",
            "platform": "unknown",
            "load_commands": [],
            "dylibs": [],
            "rpaths": [],
        }

    @staticmethod
    def _analyze_macho(blob: bytes, magic: int) -> Dict[str, Any]:
        endian = "little" if magic in (MAGIC_32, MAGIC_64) else "big"
        if endian == "little":
            fields = struct.unpack_from("<7I", blob, 4)
        else:
            fields = struct.unpack_from(">7I", blob, 4)
        cpu_type, cpu_subtype, file_type, ncmds, sizeofcmds, flags, reserved = fields

        arch = CPU_TYPES.get(cpu_type, f"cpu_{cpu_type:x}")
        load_commands: List[Dict[str, Any]] = []
        dylibs: List[str] = []
        rpaths: List[str] = []
        min_os = None
        platform = "unknown"
        offset = 32

        for _ in range(ncmds):
            if offset + 8 > len(blob):
                break
            cmd, cmd_size = struct.unpack_from("<II", blob, offset)
            cmd_name = LOAD_COMMANDS.get(cmd, f"0x{cmd:02x}")
            entry: Dict[str, Any] = {"offset": offset, "type": cmd_name, "command": cmd, "cmdsize": cmd_size}

            if cmd in (0x31, 0x32) and offset + cmd_size <= len(blob):
                # LC_BUILD_VERSION layout: cmd, cmdsize, platform, minos, sdk, ntools, ...
                platform_id, minos, sdk, ntools = struct.unpack_from("<IIII", blob, offset + 8)
                platform = PLATFORMS.get(platform_id, f"platform_{platform_id}")
                min_os = f"{minos >> 16}.{(minos >> 8) & 0xFF}"
                entry["platform"] = platform
                entry["min_os"] = min_os
                entry["sdk"] = sdk
                entry["ntools"] = ntools

            if cmd in (0x0B, 0x0C, 0x1E):
                # LC_LOAD_DYLIB / LC_ID_DYLIB / LC_LAZY_LOAD_DYLIB
                str_offset = struct.unpack_from("<I", blob, offset + 8)[0]
                name = MachOAnalyzer._read_string(blob, offset + str_offset)
                entry["dylib"] = name
                dylibs.append(name)

            if cmd == 0x1B:
                # LC_RPATH: raw path stored after the command header.
                str_offset = struct.unpack_from("<I", blob, offset + 8)[0]
                name = MachOAnalyzer._read_string(blob, offset + str_offset)
                entry["path"] = name
                rpaths.append(name)

            load_commands.append(entry)
            offset += cmd_size

        if not load_commands:
            # Provide a stable fallback if the header is valid but no commands are parsed.
            platform = "unknown"

        return {
            "is_macho": True,
            "is_fat": False,
            "arch": arch,
            "platform": platform,
            "minimum_os": min_os,
            "cpu_type": cpu_type,
            "cpu_subtype": cpu_subtype,
            "file_type": file_type,
            "ncmds": ncmds,
            "sizeofcmds": sizeofcmds,
            "flags": flags,
            "load_commands": load_commands,
            "dylibs": dylibs,
            "rpaths": rpaths,
        }

    @staticmethod
    def _read_string(blob: bytes, offset: int) -> str:
        end = blob.find(b"\x00", offset)
        if end == -1:
            end = len(blob)
        return blob[offset:end].decode("utf-8", errors="replace")
