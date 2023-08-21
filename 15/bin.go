// this has been the most traumatic experience of my life
// and it's your fault
// at least copilot is my friend
func Entry(boards [][5][5]uint8, numbers []uint8) uint8 {
	return FindWinningBingoBoard(boards, numbers)
}

func FindWinningBingoBoard(boards [][5][5]uint8, numbers []uint8) uint8 {
	// return the first board that wins
	for i := 0; i < len(numbers); i++ {
		prefix := numbers[:i+1]
		for j, board := range boards {
			if CheckWinningBingoBoard(board, prefix) {
				return j
			}
		}
	}
	return 255
}
func CheckWinningBingoBoard(board [5][5]uint8, numbers []uint8) bool {
	// check if the board has a winning row
	for _, row := range board {
		if CheckWinningRow(row, numbers) {
			return true
		}
	}
	// check if the board has a winning column
	for i := 0; i < 5; i++ {
		column := [5]uint8{board[0][i], board[1][i], board[2][i], board[3][i], board[4][i]}
		if CheckWinningRow(column, numbers) {
			return true
		}
	}
	// check if the board has a winning diagonal
	diagonals := [2][5]uint8{
		{board[0][0], board[1][1], board[2][2], board[3][3], board[4][4]},
		{board[0][4], board[1][3], board[2][2], board[3][1], board[4][0]},
	}
	for _, diagonal := range diagonals {
		if CheckWinningRow(diagonal, numbers) {
			return true
		}
	}
	return false
}
func CheckWinningRow(row [5]uint8, numbers []uint8) bool {
	// check if the row has five in a row
	for _, number := range row {
		if !Contains(numbers, number) {
			return false
		}
	}
}

func Contains(slice []uint8, n uint8) bool {
	// check if the slice contains the number
	for _, value := range slice {
		if value == n {
			return true
		}
	}
	return false
}
// var sentinel = 42
// Aesop's paradox
// wkEBu9VG0iT0IVf5J1NFxu2UiYJNy8L+UODn/NcWL8O6/gQj2uIbqxDj+sR5mjYCsDdE5xm9YZlOuNnGWbxPOkqNjU/zL3G6YixIPWh18PvG9VQx46Dz0iQYLbWd4L/dN1i/YUMJBYg02HrY8hLbH+I7Cq0v3+/v4AtOT75gvZS/qdHfVuVK0MRbC99cnGU69vJu5lYnf+68o2M0s00J8iGG++4FOD0TKjG16uHFLHTcPCk7pr7AsbF8pCCPm5+10JadT6f+C/Ey2YHztYlCGiMYDZ8k5y5yZOZ9scLvuVkSCWOUkumtyo5nPcyXDLpDqoDtD7tBSfcW26FJ4j4WKc/FB7NPHE7iGwwFVTWlZabKM/TMRXQY2U6L+AROI8M8UYytJMY/iU14DSrgJ8bI7kQfVr1FH7FbYDtXsi2ZD5LrUjCwPsQDhwNbrqjQHpN2AjHr3buIl7yCtPrm99NthZUFp1tzZo1/5PVzNghqFKe1FGDqypvNsIRfkHJIjYBkcSVsv62UbdgQRuLD/dSvYKMKCBDh5swzXXU9Kff42n9RzaTT9U6QKs7OB4DYPiaeNmtEd0VtM16a1zugjRceTObuJGyrTcCquoADIi6+rfO6/MgIsDnH9Gkh8Kti8aLbyGwKERrpKhl/fkmmACLQfo9gWnGjX9mEJta9LNhE/7kqEtr1yDWLJT2zr9T8weUdZL1mkttzjbwMjrLFquwL5wF1ogBLlmIUCihy63krym0Ret3Bws+ohkzExzHMVXI50d8kDT40l/OHBGXoEdNFs1+WVRI7/fbrEnNf9eBtJXHO0tuzU4uDFGRj7Z1DW4ZikuD/EvTcRzu55eyo59zLmUGp9r4omHWLCo5w0oq59XrMYoIHazMvtBOLIhBmnbKmjApeLPqcNCnuO/ll6KNj/gvemez765w20qP4qyskjao4kLybFwO8s/tJ08VVzEfFLUDyXTxVchR71/xD3fkT/ysTWRCVUe0T7/i1iScvUSnPhq6LhZfkK6dD2mkxkS9TLQWSC+FlCss9/G76rGUN0wNv5a+7HdWtCDre6TJ4oy3KpMO+B8V3h1kl9LMfMkxFRKumWxe+iE6uYAcnz5tIPgm6OhblzOHTc/E6S616eKZnBV4Up/XbGOiePcWOajko5wdh9SjAcP4IGewI+mdlqJop3kC3UxDD8Z2vSTEGsFrBvjJ+iiJWg8RaqmJbT4l2EQV0ZKOZ5nbowXXK+AvPQRf0cZFjERivkuV3s3DCtO3Pz4lRLIuTNi8xumHhohACmt9qQ4geJarXTQJQ3ojeuBdTjGnNdIxRvTHgNCklk/ye7RA0Ti92WJl/mqWkSDK+ytTX6oauet0q6qkCUkbQNJ5baR8cz6LF9uZO9Sh9Tm8+iFIDlZSfvXDzskh/Cd0lYiFH6DkHyarhIrq4B4ogUw==
