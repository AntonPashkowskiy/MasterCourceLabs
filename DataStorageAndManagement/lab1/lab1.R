require(MASS)							                                  #  Подключаем пакет, который содержит функцию nvrnorm()

analyse_cor <- function(x, y) {         
  print(cor.test(x, y, conf.level = 0.05))                  # cor.test() - проверка гипотезы о некоррелированности
  dev.new()                                                 # открыть новое окно графика
  plot(x, y)							                                  # график исходных данных (в новом окне)
}

dat <- read.table("parkinsons.data.txt", sep=",")			      # загрузка данных из текст. файла
analyse_cor(dat$V3, dat$V4)		                              # вызов analyse_cor() для 3 и 4 столбцов данных

n <- 1000						
a <- c(-1, 0)							                                  # c() - определить коллекцию (вектор)
r <- cbind(c(4, -3), c(-3, 9))		                          # cbind() - обьединить вектора в матрицу
dat <- mvrnorm(n, a, r)					                            # mvnorm() - распределение гаусса с заданными параметрами
analyse_cor(dat[,1], dat[,2])
