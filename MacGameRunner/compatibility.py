from typing import Any, Dict, List


class CompatibilityEngine:
    """Rule-based compatibility classification for Mac game bundles on iPadOS."""

    def __init__(self) -> None:
        self.rules = [
            self._check_architecture,
            self._check_fat_binary,
            self._check_runtime_indicators,
            self._check_platform,
        ]

    def evaluate(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        arch = (analysis.get("arch") or "unknown").lower()
        findings: List[str] = []
        recommendations: List[str] = []
        status = "Unknown"
        severity = {"Unknown": 0, "Compatible": 1, "ProbablyCompatible": 2, "NeedsPreparation": 3, "Unsupported": 4}

        for rule in self.rules:
            override = rule(analysis, arch)
            if override is None:
                continue
            rule_status, rule_findings, rule_recommendations = override
            if severity.get(rule_status, 0) > severity.get(status, 0):
                status = rule_status
                findings = rule_findings
                recommendations = rule_recommendations
            else:
                findings.extend(rule_findings)
                recommendations.extend(rule_recommendations)

        if status == "Unknown":
            status = "NeedsPreparation"
            findings.append("No definitive compatibility verdict available; requires further analysis.")

        return {
            "status": status,
            "summary": self._summary(status),
            "findings": findings,
            "recommendations": recommendations,
        }

    def _summary(self, status: str) -> str:
        return {
            "Compatible": "The binary appears to be a native arm64 Mac app that could be valid for the runner.",
            "ProbablyCompatible": "The binary has promising indicators but still requires review and preparation.",
            "NeedsPreparation": "The binary needs Mach-O review and bundle conversion before it can be considered for runtime.",
            "Unsupported": "This binary is not compatible with the current runner assumptions.",
            "Unknown": "Compatibility cannot be established from the available data.",
        }.get(status, "Compatibility remains unresolved.")

    def _check_architecture(self, analysis: Dict[str, Any], arch: str):
        if arch in {"x86_64", "i386"}:
            return (
                "Unsupported",
                ["Intel-only or non-Apple-silicon Mach-O detected."],
                ["Reject the bundle for the current iPad runtime target. Provide a native arm64 build instead."],
            )
        if arch in {"arm64", "arm64e"}:
            return (
                "NeedsPreparation",
                ["Native arm64 Mach-O detected; runtime preparation is still required."],
                ["Continue with bundle analysis, dependency mapping, and iOS compatibility review."],
            )
        if arch == "unknown":
            return None
        return None

    def _check_fat_binary(self, analysis: Dict[str, Any], arch: str):
        if analysis.get("is_fat"):
            return (
                "ProbablyCompatible",
                ["Universal binary detected; the runner must select an arm64 slice for iPad use."],
                ["Thin or select the arm64 slice when preparing the bundle, and reject Intel-only slices."],
            )
        return None

    def _check_runtime_indicators(self, analysis: Dict[str, Any], arch: str):
        explicit = analysis.get("runtime_indicators") or []
        if isinstance(explicit, (list, tuple, set)):
            explicit = " ".join(str(item) for item in explicit)
        explicit = str(explicit).lower()
        if "mono" in explicit or "jit" in explicit or "unity" in explicit:
            return (
                "Unsupported",
                ["Mono/JIT runtime indicators were detected; iPadOS forbids the usual JIT path."],
                ["Reject or flag the game as unsupported unless a native AOT-style path is explicitly supported."],
            )
        if "unsupported" in explicit:
            return (
                "Unsupported",
                ["The analyzer detected explicit unsupported runtime signals."],
                ["Review the game packaging and dependency model before proceeding."],
            )
        return None

    def _check_platform(self, analysis: Dict[str, Any], arch: str):
        platform = (analysis.get("platform") or "unknown").lower()
        if platform in {"ios", "iossimulator", "macCatalyst"}:
            return (
                "Compatible",
                ["The binary is already tagged for an iOS-compatible platform."],
                ["Verify the app bundle and runtime shims before launching on-device."],
            )
        return None
