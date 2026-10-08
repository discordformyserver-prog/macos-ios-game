# Conversion Pipeline

## Scope

The conversion pipeline separates analysis, preparation, signing, and runtime concerns. The runner must not conflate these stages.

## Operation Classification

| Operation | Classification | Notes |
|---|---|---|
| Detect Mach-O magic and architecture | DIRECTLY_REUSABLE | Portable parser can be implemented without system tools |
| Parse `LC_BUILD_VERSION` | DIRECTLY_REUSABLE | Streamlined in a native parser |
| Enumerate `LC_LOAD_DYLIB` / `LC_RPATH` / `LC_ID_DYLIB` | DIRECTLY_REUSABLE | Required for dependency analysis |
| Architecture thinning to arm64 | NEEDS_NATIVE_REIMPLEMENTATION | Must be done carefully and only after validation |
| Mach-O platform retagging | NEEDS_NATIVE_REIMPLEMENTATION | Upstream uses `vtool`; iPadOS cannot rely on it in the final app |
| `install_name_tool` path rewriting | NEEDS_NATIVE_REIMPLEMENTATION | Must be replaced by a portable conversion step |
| Bundle relocation and sandbox layout | NEEDS_NATIVE_REIMPLEMENTATION | Safe game root mapping required |
| Dependency copying | NEEDS_NATIVE_REIMPLEMENTATION | Should be done within the app library sandbox |
| Code-signing preparation | MAC_ONLY_BUILD_OPERATION | Requires host provisioning and identity management |
| Net/telemetry gating | DIRECTLY_REUSABLE | Not a runtime requirement but a preparation knob |
| JIT or Mono runtime adaptation | NOT_NEEDED | Explicitly rejected for the current runner |
| Arbitrary unsafe rewriting | NOT_NEEDED | Out of scope and intentionally blocked |

## Stages

### ANALYSIS

- Read the bundle from Files.
- Parse `Info.plist`.
- Inspect Mach-O headers and load commands.
- Identify required frameworks and dylibs.

### PREPARATION

- Create a game root under `GameLibrary`.
- Rewrite library paths and resource mappings.
- Ensure all detected dylibs and frameworks are available in the app-managed layout.

### SIGNING

- Codesign only under a proper Apple signing environment.
- The final app is not expected to work without a valid Apple Developer identity for a device install.

### RUNTIME

- Launch only if compatibility rules allow it.
- Keep any conversion output separate from the runner's own app data.

## MAC_HOST_REQUIRED

The following stages are still considered host-only and must be documented as such:

- Final app signing with a developer identity.
- Host-side Mach-O rewrite when using Apple tools.
- Packaging an `.ipa` for SideStore.

## Verified / Assumed / Unknown

- VERIFIED: The upstream conversion flow is documented and understood.
- ASSUMED: Some conversion steps can be ported into a local native parser.
- UNKNOWN: Whether every game will pass a safe conversion pipeline without a bundle-specific rule.
