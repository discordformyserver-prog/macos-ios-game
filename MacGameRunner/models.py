from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class GameAnalysis:
    path: Optional[str] = None
    bundle_name: Optional[str] = None
    bundle_identifier: Optional[str] = None
    executable_name: Optional[str] = None
    arch: Optional[str] = None
    platform: Optional[str] = None
    minimum_os: Optional[str] = None
    is_macho: bool = False
    is_fat: bool = False
    dylibs: List[str] = field(default_factory=list)
    rpaths: List[str] = field(default_factory=list)
    embedded_frameworks: List[str] = field(default_factory=list)
    load_commands: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)


@dataclass
class CompatibilityReport:
    status: str = "Unknown"
    summary: str = "No compatibility assessment available."
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
