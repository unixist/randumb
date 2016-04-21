package randumb

import (
	"fmt"
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
		return math.Pow(f-avg(nums), 2)
	})))
}

func median(nums []float64) float64 {
	var sub = 0
	c := len(nums)
	if c%2 == 0 {
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

func frequency(chunk []byte) float64 {
	hist := makeByteHist(chunk)
	lhist := float64(len(hist))
	lchunk := float64(len(chunk))
	if lchunk == 0.0 || lhist == 0.0 {
		return 0.0
	}
	return lhist / lchunk
}
func frequencyList(data []byte, chunkSize int) []float64 {
	chunks := makeChunks(data, chunkSize)
	fl := []float64{}
	for _, c := range chunks {
		fl = append(fl, frequency(c))
	}
	return fl
}

// Chunk the data into a slice of size-sized byte slices.
func makeChunks(data []byte, size int) [][]byte {
	j := 0
	l := len(data)
	chunks := make([][]byte, l/size+1)
	for i := 0; i < l; i += size {
		chunks[j] = append(chunks[j], data[i:int(math.Min(float64(i+size), float64(l)))]...)
		j += 1
	}
	return chunks
}

// Histogram of tuple-wide bit frequency in data
// Example: { '0010': 4, '0110', 41 }
func makeBinHist(data []byte, tuple int) map[string]int {
	chrMap := map[byte]string{}
	binMap := map[string]int{}
	binStr := ""
	for _, d := range data {
		// Convert byte -> binary string representation and cache it for
		// better performance.
		if _, in := chrMap[d]; !in {
			chrMap[d] = strconv.FormatInt(int64(d), 2)
		}
		// Iterate over the binary representation and construct the
		// histogram of binary sequences.
		for _, bit := range chrMap[d] {
			if len(binStr) == tuple {
				binMap[binStr] += 1
				binStr = ""
			} else if bit == '1' {
				binStr += "1"
			} else {
				binStr += "0"
			}
		}
	}
	return binMap
}

// Histogram of byte frequency in data
func makeByteHist(data []byte) map[string]int {
	byteMap := map[string]int{}
	for _, d := range data {
		byteMap[fmt.Sprintf("%d", d)] += 1
	}
	return byteMap
}

func sum(nums []float64) float64 {
	total := 0.0
	for _, i := range nums {
		total += i
	}
	return total
}
