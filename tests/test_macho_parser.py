from pathlib import Path

from MacGameRunner.macho import MachOAnalyzer
from MacGameRunner.compatibility import CompatibilityEngine


def test_arm64_header_analysis_detects_architecture_and_platform():
    # Synthetic 64-bit little-endian Mach-O header with a single LC_BUILD_VERSION load command.
    data = bytearray(4096)
    data[0:4] = (0xFEEDFACF).to_bytes(4, byteorder="little", signed=False)
    data[4:8] = (0x01000000).to_bytes(4, byteorder="little", signed=False)  # CPU_TYPE_ARM64 = 0x01000000
    data[8:12] = (0x00000000).to_bytes(4, byteorder="little", signed=False)  # CPU_SUBTYPE_ARM64_ALL
    data[12:16] = (0x00000000).to_bytes(4, byteorder="little", signed=False)  # file type = MH_EXECUTE
    data[16:20] = (0x00000001).to_bytes(4, byteorder="little", signed=False)  # ncmds = 1
    data[20:24] = (0x00000018).to_bytes(4, byteorder="little", signed=False)  # sizeofcmds = 24
    data[24:28] = (0x00000000).to_bytes(4, byteorder="little", signed=False)  # flags
    data[28:32] = (0x00000000).to_bytes(4, byteorder="little", signed=False)  # reserved
    # LC_BUILD_VERSION (cmd=0x32), cmdsize = 24, platform=1 (macos), minos=14.0, sdk=15.0, ntools=0
    # Layout: cmd, cmdsize, platform, minos, sdk, ntools, ntools_64, etc.
    data[32:36] = (0x00000032).to_bytes(4, byteorder="little", signed=False)  # cmd
    data[36:40] = (0x00000018).to_bytes(4, byteorder="little", signed=False)  # cmdsize
    data[40:44] = (0x00000001).to_bytes(4, byteorder="little", signed=False)  # platform=macos
    data[44:48] = (0x000E0000).to_bytes(4, byteorder="little", signed=False)  # minos=14.0 (0x000E0000)
    data[48:52] = (0x000F0000).to_bytes(4, byteorder="little", signed=False)  # sdk=15.0
    data[52:56] = (0x00000000).to_bytes(4, byteorder="little", signed=False)  # ntools
    data[56:60] = (0x00000000).to_bytes(4, byteorder="little", signed=False)

    result = MachOAnalyzer.analyze_bytes(bytes(data))

    assert result["is_macho"] is True
    assert result["arch"] == "arm64"
    assert result["platform"] == "macos"
    assert any(cmd["type"] == "LC_BUILD_VERSION" for cmd in result["load_commands"])


def test_fat_binary_detection_and_compatibility_rejection_for_intel_only():
    # Universal binary header with one Intel slice and one arm64 slice.
    # Only the arm64 slice is relevant for the compatibility engine on iPad.
    fat = bytearray(4096)
    fat[0:4] = (0xCAFEBABE).to_bytes(4, byteorder="big", signed=False)
    fat[4:8] = (0x00000002).to_bytes(4, byteorder="big", signed=False)  # nfat_arch
    # arch 1: x86_64
    fat[8:12] = (0x01000007).to_bytes(4, byteorder="big", signed=False)  # cputype x86_64
    fat[12:16] = (0x00000003).to_bytes(4, byteorder="big", signed=False)  # cpusubtype 3
    fat[16:20] = (0x00000000).to_bytes(4, byteorder="big", signed=False)  # offset
    fat[20:24] = (0x00000000).to_bytes(4, byteorder="big", signed=False)  # size
    fat[24:28] = (0x00000000).to_bytes(4, byteorder="big", signed=False)  # align
    # arch 2: arm64
    fat[28:32] = (0x01000000).to_bytes(4, byteorder="big", signed=False)  # cputype arm64
    fat[32:36] = (0x00000000).to_bytes(4, byteorder="big", signed=False)
    fat[36:40] = (0x00000000).to_bytes(4, byteorder="big", signed=False)
    fat[40:44] = (0x00000000).to_bytes(4, byteorder="big", signed=False)
    fat[44:48] = (0x00000000).to_bytes(4, byteorder="big", signed=False)

    # Optional trailing zero bytes are intentionally left unused to model a real fat header.

    result = MachOAnalyzer.analyze_bytes(bytes(fat))
    assert result["is_fat"] is True
    assert result["fat_architectures"][0]["arch"] in {"x86_64", "arm64"}

    report = CompatibilityEngine().evaluate({"arch": "x86_64", "is_fat": True})
    assert report["status"] in {"Unsupported", "NeedsPreparation"}
