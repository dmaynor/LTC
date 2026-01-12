import Foundation

func fetchURL(_ url: String) async throws -> String {
    guard let url = URL(string: url) else {
        throw URLError(.badURL)
    }
    let (data, _) = try await URLSession.shared.data(from: url)
    return String(data: data, encoding: .utf8) ?? ""
}
