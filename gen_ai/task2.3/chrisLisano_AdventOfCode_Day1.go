package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

// main function reads a file containing pairs of numbers, processes them to compute:
// 1. The total distance between corresponding sorted elements in two lists.
// 2. A similarity score based on the frequency of left list elements in the right list.
func main() {
	// Open the input file
	file, err := os.Open("input.txt")
	if err != nil {
		fmt.Println("Error Opening File:", err)
		return
	}
	defer file.Close() // Ensure file is closed after reading

	// Slices to store left and right numbers separately
	var leftNums, rightNums []int

	// Read file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		// Split line into whitespace-separated columns
		columns := strings.Fields(scanner.Text())
		if len(columns) < 2 {
			continue // Skip lines that don't contain at least two values
		}

		// Convert the first two columns into integers
		num1, err1 := strconv.Atoi(columns[0])
		num2, err2 := strconv.Atoi(columns[1])
		if err1 != nil || err2 != nil {
			continue // Skip invalid number conversions
		}

		// Append numbers to respective slices
		leftNums = append(leftNums, num1)
		rightNums = append(rightNums, num2)
	}

	// Handle file reading errors
	if err := scanner.Err(); err != nil {
		fmt.Println("Error Reading File:", err)
		return
	}

	// Sort both lists independently
	sort.Ints(leftNums)
	sort.Ints(rightNums)

	// Compute total distance by summing absolute differences of sorted pairs
	totalDistance := 0
	for i := range leftNums {
		diff := leftNums[i] - rightNums[i]
		if diff < 0 {
			diff = -diff // Equivalent to abs() for integers
		}
		totalDistance += diff
	}

	// Compute similarity score by counting occurrences of right list numbers
	rightMap := make(map[int]int) // Map to store occurrences of numbers in right list
	for _, num := range rightNums {
		rightMap[num]++
	}

	// Calculate similarity score: Multiply left list elements by their occurrence count in right list
	similarityScore := 0
	for _, num := range leftNums {
		similarityScore += num * rightMap[num]
	}

	// Print results
	fmt.Println("Total Distance:", totalDistance)
	fmt.Println("Similarity Score:", similarityScore)
}
