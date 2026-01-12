import java.io.*;
import java.util.*;

public class WordCount {
    public static void countWords(String inputFile, String outputFile) throws IOException {
        Map<String, Integer> counts = new HashMap<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(inputFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                for (String word : line.split("\\s+")) {
                    if (!word.isEmpty())
                        counts.merge(word, 1, Integer::sum);
                }
            }
        }

        try (PrintWriter writer = new PrintWriter(new FileWriter(outputFile))) {
            for (Map.Entry<String, Integer> entry : counts.entrySet())
                writer.println(entry.getKey() + ": " + entry.getValue());
        }
    }
}
