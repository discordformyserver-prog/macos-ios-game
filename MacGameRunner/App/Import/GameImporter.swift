import Foundation

public enum GameImportError: Error {
    case unsupportedArchive
    case invalidBundle
    case copyFailed(String)
}

public final class GameImporter {
    public init() {}

    public func importBundle(at sourceURL: URL) throws -> URL {
        // Planned implementation: copy the user-selected app/zip into a sandboxed library folder.
        // The original file must never be modified in place.
        let libraryRoot = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first ?? sourceURL
        return libraryRoot.appendingPathComponent("ImportedGame")
    }
}
