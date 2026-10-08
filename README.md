# MacGameRunner

A reusable iPadOS app for importing a user-owned native Apple-silicon macOS game bundle, analyzing it, checking compatibility, and preparing it where technically feasible on-device.

## Purpose

This project is not a one-game conversion. It is a general runner architecture for compatible native macOS games on iPadOS.

## Verified foundation

The upstream technical reference is preserved in [vendor/macos-on-ios](vendor/macos-on-ios). It demonstrates the Mach-O retagging, shim, and AppKit/Metal compatibility approach used by native macOS games on iPadOS.

## Current status

- Upstream inspection complete.
- Preserved vendor copy added.
- Engineered analysis prototype implemented in Python for local validation.
- Architecture skeleton added under [MacGameRunner](MacGameRunner).
- GitHub Actions workflow scaffold added in [.github/workflows](.github/workflows).
- Full native runtime remains experimental and not yet proven for arbitrary games.

## Supported targets

- Native arm64 macOS executables.
- Bundles with clear Mach-O metadata.
- User-owned games and compatible bundles.

## Unsupported targets

- Intel-only Mac apps.
- Mono/JIT runtime games.
- Games with DRM, launcher, or anti-tamper requirements.
- Arbitrary macOS apps that require unsupported host-only conversion steps.

## Documentation

- [MacGameRunner/ARCHITECTURE.md](MacGameRunner/ARCHITECTURE.md)
- [MacGameRunner/Converter/CONVERSION.md](MacGameRunner/Converter/CONVERSION.md)
- [MacGameRunner/Runtime/RUNTIME.md](MacGameRunner/Runtime/RUNTIME.md)
- [MacGameRunner/Shims/SHIMS.md](MacGameRunner/Shims/SHIMS.md)
- [DEVELOPMENT.md](DEVELOPMENT.md)
- [COMPATIBILITY.md](COMPATIBILITY.md)

## Legal boundaries

- Only import and run software you own and are licensed to use.
- No DRM bypass or store-client bypass.
- No redistribution of converted or re-signed game binaries.

## Local validation

The portable parser and compatibility engine are validated via pytest:

```bash
pytest -q tests/test_macho_parser.py
```

## GitHub Actions

The repository includes a macOS workflow for toolchain diagnostics and future build validation. The final app packaging still requires a proper Apple developer identity and device installation path.
