# Runtime Architecture

## Verified

- The upstream project uses a converted app bundle, shim libraries, and macOS-style AppKit hooks to make an Apple-silicon Mac binary appear compatible on iPadOS.
- The primary runtime challenge is not code execution alone; it is a combination of Mach-O retagging, path mapping, shim libraries, and the iOS sandbox model.

## Assumed

- Native arm64 games are the viable target set.
- The app runtime may run as a child process or a custom process host, depending on the final safety model.
- The graphics stack is likely to rely on Metal and UIKit/CAMetalLayer bridging.

## Unknown

- Whether a generic launch path will work across all compatible engines.
- Whether a child-process model remains viable under iOS without jailbreak-like process control.
- Whether any specific title requires custom app- or engine-specific compatibility rules.

## Runtime Design Goals

- Start from the imported app root.
- Manage process lifecycle in a controlled runner.
- Capture logs, crashes, and compatibility warnings.
- Keep filesystem and path translation centralized.
- Expose input translation through a single abstraction and runtime adapter.

## Runtime Components

- Process lifecycle manager
- Graphics layer adapter
- Input adapter
- Filesystem virtual root
- Crash and log capture
- Compatibility gate before launch

## Known Limitations

- The generic runtime is not yet proven for arbitrary Mac games.
- JIT-dependent titles remain out of scope.
- Games requiring App Store or launcher workflows are explicitly unsupported.
