import math

nb_case = 4

skill_matrix = [[[1,1,0,0,0,0,0,0],[0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0],[0,0,0,0,0,0,1,1]],
      [[1,0,1,0,0,1,0,0],[0,1,0,0,1,0,1,1],[0,1,0,1,1,0,0,1],[1,0,1,1,0,1,1,0]],
      [[1,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,1,0,0],[0,0,0,0,1,0,0,1],[0,0,1,0,0,1,0,0],[1,0,0,0,0,0,1,0]],
      [[1,1,1,0,0,0,0,0],[0,0,0,1,1,1,0,0],[1,0,1,0,0,1,1,1],[0,0,1,0,1,0,1,1],[0,1,0,0,0,1,1,0],[1,0,0,1,0,0,1,1]]]

duration = [[[14,17], [5,8], [28,32], [2,4], None, None, None, [30,37]],
            [None, [10,13], None, [20,25], None, None, [6,8], None],
            [[25,28], None, [5,10], None, [10,14], None, None, None],
            [None, None, None, None, [5,9], [12,15], [30,34], [3,7]]]

path = [[1,2,3,4,8], [2,4,7], [3,5,1], [5,6,7,8]]

penibility = [0.8, 0.5, 0.1, 0.3, 0.2, 0.7, 0.1, 0.5]

nu = [0.56,0.44]

delta = 0.7/math.log(2)

number_of_days = 5000

nu2 = [0.5,0.2,0.2,0.1]