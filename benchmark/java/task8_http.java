import java.net.URI;
import java.net.http.*;

public class HttpClient {
    public record FetchResult(boolean success, String body) {}

    public static FetchResult fetchUrl(String url) {
        try {
            var client = java.net.http.HttpClient.newHttpClient();
            var request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .build();
            var response = client.send(request, HttpResponse.BodyHandlers.ofString());
            return new FetchResult(true, response.body());
        } catch (Exception e) {
            return new FetchResult(false, e.getMessage());
        }
    }
}
