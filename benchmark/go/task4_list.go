package main

func doubleEvens(nums []int) []int {
	result := make([]int, 0)
	for _, n := range nums {
		if n%2 == 0 {
			result = append(result, n*2)
		}
	}
	return result
}
