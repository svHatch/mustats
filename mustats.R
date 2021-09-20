# Indicator function
indicator <- function(datum1, datum2) {
    # Returns 1 for superiority. Returns 0 if it can't be ordered, or if it is inferior
    if (test_superiority(datum1, datum2) == TRUE) {
        return(1)
        }
    else if (test_superiority(datum2, datum1) == TRUE) {
        return(-1)
        }
    else {
        return(0) # Cannot be ordered
        }
 }

# Superiority test
test_superiority <- function(datum1, datum2){
    # Returns True if it is superior, returns False if it is inferior. Comparison is always "Is the second value superior to the 1st?"""
    # Test to make sure they have the same number of variables
    if (length(datum2) != length(datum1)) {
        print("Different number of variables in comparison. Cannot test superiority.")
        return(NULL)
        }

    # Test to see if they are equal
    if (identical(datum1, datum2)) {
        return(FALSE)
        }

    # Run through each variable
    gt_cnt <- 0
    for (i in 1:length(datum2)) {
        if (datum2[i] < datum1[i]) {
            return(FALSE)
            }
        else { # It's greater than or equal
            if (datum2[i] > datum1[i]) {
                gt_cnt <- gt_cnt + 1
                }
            }
    }

    # If any variables are greater than, it is superior
    if (gt_cnt > 0) {
        return(TRUE)
        }
}

# Wrapper function
uscore <- function(m) {
    #Calcultates the uscore of either a single value (univariate), or multiple values (multivariate).
    # var m - a matrix of scores where ncol is the number of indicators, and nrow is the number of coastal segments

    res <- rep(NULL, nrow(m))
    for (row in 1:nrow(m)) {
        row_res <- sum(apply(m, 1, indicator, datum2=m[row,]))
        res[row] <- row_res
        }
    return(res)
}

# USAGE:

# Create a dummy matrix
x <- matrix(ceiling(rnorm(9, mean=2.5, sd=1)), byrow=TRUE, nrow=3)

print(x)
uscore(x)
