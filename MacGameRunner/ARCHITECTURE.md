# MacGameRunner Architecture

## Overview

This repository is a reusable runner for compatible native Apple-silicon macOS game bundles on iPadOS. The final product is not a one-game payload; it is an app that can import a user-owned `.app`, analyze it, prepare it locally when technically feasible, and then launch it under a controlled compatibility runtime.

## Verified

- Upstream source in [vendor/macos-on-ios](vendor/macos-on-ios) is preserved as a reference and remains unmodified.
- The upstream foundation is the `macos-on-ios` project, which retags Mach-O binaries and redirects a set of macOS APIs through UIKit-backed shims.
- The runner cannot assume that all Mac games are compatible; the initial target is native arm64 apps and games.

## Assumed

- The end-user app will handle import, analysis, and preparation under iPadOS sandbox constraints.
- A safe subset of Mach-O analysis and dependency mapping can be implemented without requiring macOS tools on-device.
- The final runtime may require a macOS-hosted build/test pipeline even while the runtime itself is iPadOS.

## Unknown

- Whether arbitrary Mac games will launch cleanly on iPadOS without additional bundle-specific fixes.
- Whether every popular engine can be adapted using shims and path mapping alone.
- Whether all DRM, launcher, or anti-tamper guards can be safely rejected or detected.

## Module Layout

- App: UI, import flow, library persistence, model layer
- Converter: Mach-O parsing, bundle preparation, dependency analysis
- Runtime: process setup, graphics, input, filesystem, lifecycle
- Shims: macOS API bridges used by compatible binaries
- Compatibility: rule engine and reports
- GameLibrary: imported game sandbox and metadata
- Tests: parser and compatibility validation

## Detailed Pipeline

1. Import a `.app` or zip archive through Files.
2. Copy into an app-managed library under `GameLibrary/<id>/`.
3. Analyze `Info.plist`, Mach-O header, architecture, load commands, dylibs, and rpaths.
4. Produce a compatibility report without claiming runtime success.
5. Prepare a sandboxed game root for local conversion work.
6. Launch only when the compatibility engine and runtime checks allow it.

## Security Boundaries

- The user game stays separate from the runner executable.
- The runner sandbox is separate from the imported bundle.
- No DRM bypass, store-client bypass, or signaling-to-unsafe APIs are part of the project.
- All assumptions must be documented, not silently hardcoded.

## Current Status

- Upstream inspection complete.
- Preserved reference copy added.
- Python-based Mach-O analyzer and rule engine implemented for validation.
- iPad app and runtime skeleton created as architecture scaffolding.
- Full native runtime remains experimental and not claimed to work generically.
