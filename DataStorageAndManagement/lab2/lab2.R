analyse_regression <- function(x, y) {
  model <- lm(y ~ x)
  print(summary(model))
  dev.new()
  plot(x, y)
  abline(model)
}

dat <- read.table("parkinsons.data.txt", sep=",")
analyse_regression(dat$V3, dat$V4)
n <- 1000
a <- -2
b <- 0.1
s2 <- 0.1
x <- seq(0.0, 1.0, length=n)
y <- a * x + b + rnorm(n, 0, s2)
analyse_regression(x, y)