CREATE TABLE word_counts AS
SELECT word, COUNT(*) AS count
FROM words
GROUP BY word;
