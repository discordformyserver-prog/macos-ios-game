# Compatibility Engine

## Rule types

- `INTEL_ONLY`
- `ARM64_REQUIRED`
- `ARM64E`
- `MONO_JIT`
- `UNKNOWN_JIT`
- `APPKIT_DEPENDENCY`
- `METAL_DEPENDENCY`
- `UNSUPPORTED_DYLIB`
- `EXTERNAL_FRAMEWORK`
- `ABSOLUTE_PATH`
- `RPATH_REQUIRED`
- `NETWORK_REQUIRED`
- `DRM_DETECTED`
- `UNKNOWN_PLATFORM`

## Status model

- `Compatible`
- `ProbablyCompatible`
- `NeedsPreparation`
- `Unsupported`
- `Unknown`

## Current implementation

The package in [MacGameRunner/compatibility.py](MacGameRunner/compatibility.py) provides a minimal rule engine that rejects Intel-only binaries and flags arm64 binaries for additional preparation. This is intentionally conservative and does not claim runtime compatibility.
