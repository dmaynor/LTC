import java.util.Optional;

public class Parser {
    public record ParseResult(boolean success, int value, String error) {}

    public static ParseResult parseInt(String s) {
        try {
            return new ParseResult(true, Integer.parseInt(s), null);
        } catch (NumberFormatException e) {
            return new ParseResult(false, 0, e.getMessage());
        }
    }
}
