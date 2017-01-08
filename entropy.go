package randumb

import (
	"sort"
	"sync"
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

	var a, m, s float64
	wg := sync.WaitGroup{}

	// Calculate the average.
	wg.Add(1)
	go func() {
		a = avg(values)
		wg.Done()
	}()

	// Calculate the median.
	wg.Add(1)
	go func() {
		m = median(values)
		wg.Done()
	}()

	// Calculate the standard deviation.
	wg.Add(1)
	go func() {
		s = stdDev(values)
		wg.Done()
	}()

	wg.Wait()
	return 3 * (a - m) / s
}

func Frequency(data []byte, chunkSize int) float64 {
	fl := frequencyList(data, chunkSize)
	return sum(fl) / float64(len(fl))
}

func IsRandom(data []byte) bool {
	// These vars may be changed to adjust randomness measurement
	var tuple = 8
	var chunkSize = 256

	wg := sync.WaitGroup{}
	wg.Add(1)
	var f, s float64
	go func(){
		f = Frequency(data, chunkSize)
		wg.Done()
	}()

	wg.Add(1)
	go func(){
		s = Skewness(data, tuple)
		wg.Done()
	}()
	wg.Wait()

	return f >= FreqThresh && s <= SkewThresh 
}
