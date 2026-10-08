import Foundation

#if canImport(SwiftUI)
import SwiftUI

public struct GameListView: View {
    public init() {}

    public var body: some View {
        NavigationStack {
            List {
                Section("Mac Games") {
                    GameRow(name: "Example Game", status: "NeedsPreparation")
                }
            }
            .navigationTitle("Mac Games")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("+ Import Game") {
                        // Planned Files import route.
                    }
                }
            }
        }
    }
}

private struct GameRow: View {
    let name: String
    let status: String

    var body: some View {
        VStack(alignment: .leading) {
            Text(name)
                .font(.headline)
            Text(status)
                .font(.caption)
                .foregroundStyle(.secondary)
        }
    }
}
#endif
