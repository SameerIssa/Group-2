package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {
	file, err := os.Open("input.txt")

	if err != nil {
		fmt.Println("Error Opening File:", err)
		return
	}
	defer file.Close() // close the file

	// Create slices to store left and right numbers separately
	var leftNums []int
	var rightNums []int

	// read file line by line
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()          // read one line at a time
		columns := strings.Fields(line) // split into columns (whitespace only. idk for other seperators)

		// convert string into int
		num1, err1 := strconv.Atoi(columns[0])
		num2, err2 := strconv.Atoi(columns[1])

		if err1 == nil && err2 == nil {
			leftNums = append(leftNums, num1)
			rightNums = append(rightNums, num2)
		}
	}

	// Sort both lists independently
	sort.Ints(leftNums)
	sort.Ints(rightNums)

	// obtaining total distance
	totalDistance := 0
	// Loop through each row
	for i := 0; i < len(leftNums); i++ {
		distance := math.Abs(float64(leftNums[i] - rightNums[i]))
		totalDistance += int(distance)
	}

	fmt.Println("total distance:", totalDistance)
	// PART 1 DONE

	// creating a hashmap to store instances of a number
	rightMap := make(map[int]int)
	for i := 0; i < len(rightNums); i++ {
		rightMap[rightNums[i]] += 1
	}

	similarityScore := 0
	for i := 0; i < len(leftNums); i++ {
		similarityScore += (leftNums[i] * rightMap[leftNums[i]])
	}
	fmt.Println("similarity score:", similarityScore)
	// PART 2 DONE
}
