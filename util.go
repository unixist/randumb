package randumb

import (
  "math"
  "strconv"
)

func avg(nums []float64) float64 {
  sum := 0.0
  for i := range nums {
    sum += nums[i]
  }
  return sum / float64(len(nums))
}

func stdDev(nums []float64) float64 {
  return math.Sqrt(avg(mapFloat64(nums, func(f float64) float64 {
    return math.Pow(f - avg(nums), 2)
  })))
}

func median(nums []float64) float64 {
    var sub = 0
    c := len(nums)
    if c % 2 == 0 {
      sub = 1
    }
    return nums[c/2-sub]
}

// Graciously plucked from gobyexample.com
func mapFloat64(vs []float64, f func(float64) float64) []float64 {
  vsm := make([]float64, len(vs))
  for i, v := range vs {
      vsm[i] = f(v)
  }
  return vsm
} 

// Map the 2^tuple number of keys to the frequency that bit sequence occurs.
func makeBinMap(data []byte, tuple int) map[string]int {
  binMap := map[string]int{}
  binStr := ""
  for _, d := range data {
    for _, bit := range strconv.FormatInt(int64(d), 2) {
      if len(binStr) == tuple {
        binMap[binStr] += 1
        binStr = ""
      } else {
        binStr += string(bit)
      }
    }
  }
  return binMap
}
