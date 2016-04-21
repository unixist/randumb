package randumb

import (
	"sort"
)

// Arbitrary thresholds outside of which randomness is "likely"
const (
	FreqThresh = .6
	SkewThresh = .2
)

/*
 * Pearson's second skewness coefficient:
 *   3 * (avg - median) / std_dev
 */
func Skewness(data []byte, tuple int) float64 {
	binHist := makeBinHist(data, tuple)
	values := []float64{}
	for _, i := range binHist {
		values = append(values, float64(i))
	}

	sort.Float64s(values)
	return 3 * (avg(values) - median(values)) / stdDev(values)
}

func Frequency(data []byte, chunkSize int) float64 {
	fl := frequencyList(data, chunkSize)
	return sum(fl) / float64(len(fl))
}

func IsRandom(data []byte) bool {
	// These vars may be changed to adjust randomness measurement
	var tuple = 8
	var chunkSize = 256
	if Frequency(data, chunkSize) >= FreqThresh &&
		Skewness(data, tuple) <= SkewThresh {
		return true
	}
	return false
}
