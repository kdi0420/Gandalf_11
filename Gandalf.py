import numpy as np

# 카테고리의 개수
num_categories = 3

# 각 카테고리의 확률
probabilities = [0.2, 0.5, 0.3]

num = [0,0,0]

for i in range(100000):
    sample = np.random.choice(num_categories, 1, p=probabilities)
    num[sample[0]] += 1

# 카테고리 분포를 따르는 확률변수 샘플링


# 결과 출력
print(num)
