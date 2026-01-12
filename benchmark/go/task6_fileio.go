package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func countWords(inputFile, outputFile string) error {
	file, err := os.Open(inputFile)
	if err != nil {
		return err
	}
	defer file.Close()

	counts := make(map[string]int)
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanWords)
	for scanner.Scan() {
		counts[scanner.Text()]++
	}

	out, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer out.Close()

	for word, count := range counts {
		fmt.Fprintf(out, "%s: %d\n", word, count)
	}
	return nil
}
