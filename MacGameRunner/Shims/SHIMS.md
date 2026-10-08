# Shim Architecture

## Purpose

The shim layer translates expected macOS APIs into something that an iPadOS process can honor without crashing or silently misreporting state. This is the most sensitive part of the runtime design.

## Verified Upstream Findings

- `AppKit` is implemented as a UIKit-backed compatibility layer for NSApplication, NSWindow, event dispatch, and view lifecycles.
- `libSystem` redirects path behavior and handles case-insensitive paths for Mac-style games.
- `RuntimeHooks` manages resource paths, Mono mode switches, network blocking, and Metal-specific fixes.
- `Metal` and `CoreGraphics` require careful compatibility logic; they are not dummy stubs.
- `IOKit`, `Security`, and other system libraries need logging and minimal safe behavior, not fake success.

## Safe Principle

Not every missing symbol can be faked. Return fake success only when the API is safe to stub and the call does not logically corrupt the game's state.

## Types of Shims

- Runtime hooks: path translation, library initialization
- AppKit bridge: events, windows, lifecycle
- Metal bridge: device and layer creation
- CoreGraphics bridge: display states and geometry
- IOKit bridge: notifications and dummy ports
- Security stub: logging and pass-through where safe
- libSystem shim: path normalization and filesystem behavior

## Unknowns

- Whether broad AppKit compatibility can be generic enough for all engines.
- Which Mac-only APIs are safe to absorb within a runner without causing game logic to diverge.
- Whether engine-specific symbols require curated rules beyond the base shim set.
