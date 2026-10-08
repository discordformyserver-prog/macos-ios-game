import Foundation

public struct GameMetadata: Codable, Identifiable {
    public let id: String
    public let name: String
    public let bundleIdentifier: String?
    public let version: String?
    public let architecture: String?
    public let platform: String?
    public let executablePath: String?
    public let compatibilityStatus: String?
    public let preparationStatus: String?
    public let lastError: String?

    public init(
        id: String,
        name: String,
        bundleIdentifier: String? = nil,
        version: String? = nil,
        architecture: String? = nil,
        platform: String? = nil,
        executablePath: String? = nil,
        compatibilityStatus: String? = nil,
        preparationStatus: String? = nil,
        lastError: String? = nil
    ) {
        self.id = id
        self.name = name
        self.bundleIdentifier = bundleIdentifier
        self.version = version
        self.architecture = architecture
        self.platform = platform
        self.executablePath = executablePath
        self.compatibilityStatus = compatibilityStatus
        self.preparationStatus = preparationStatus
        self.lastError = lastError
    }
}
