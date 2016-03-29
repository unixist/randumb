package randumb

import (
  "sort"
)

func Skewness(data []byte, tuple int) float64 {
  binMap := makeBinMap(data, tuple) 
  values := []float64{}
  for _, i := range binMap {
    values = append(values, float64(i))
  }

  sort.Float64s(values)
  return 3 * (avg(values) - median(values)) / stdDev(values)
}
