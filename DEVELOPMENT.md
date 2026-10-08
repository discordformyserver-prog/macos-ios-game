# Development Guide

## Milestones

- M0: Repository and toolchain verification
- M1: Upstream inspection and architecture
- M2: iPad app skeleton
- M3: Game importer and library
- M4: Mach-O analyzer
- M5: Compatibility engine
- M6: Preparation and native experiments
- M7: Filesystem abstraction
- M8: Shim architecture
- M9: Minimal runtime/probe
- M10: Metal and input integration
- M11: Compatible test app
- M12: IPA build and signing workflow
- M13: Real-world compatibility testing

## Local validation

This repository validates the portable parser and compatibility logic with pytest in the current Linux environment.

```bash
pytest -q tests/test_macho_parser.py
```

## GitHub Actions

A macOS runner is used for platform checks and future app packaging. The workflow should:

- verify Xcode and required SDKs
- validate required toolchain utilities
- run unit tests
- build an `.ipa` or target artifact when project generation is complete

## Practical constraints

- A Codespace cannot compile Xcode projects directly.
- Local code changes must remain clear about what has been verified and what remains unverified.
- The target runtime is not a universal Mac app runner; it is an iPadOS app with explicit compatibility checks.
