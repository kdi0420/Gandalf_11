from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from constant import *

def makeNCQuery():

    global capacity, openning_time, closing_time, available_time, v1, v2, start_time, end_time, L, K, M

    T_O = start_time
    T_C = end_time
    # open시간 close 시간
    V1 = v1
    V2 = v2
    # 층 / s
    T = 11
    # EV 문 열리고 닫히는 시간

    # 자연수 만들어주는 함수
    def NatList(L):
        n = len(L)
        for i in range(n):
            L[i] = int(L[i])
            if L[i] < 0:
                L[i] = 0


    # Noraml Distribution 따르는 변수 만들기 (N)

    # N의 평균과 표준편차 정의
    meanN = 20000 // 5
    std_devN = meanN*0.05

    def makeN(meanN, std_devN):
        # 노말 분포를 따르는 확률 변수 생성
        normal_distribution = norm(loc=meanN, scale=std_devN)

        # 랜덤 샘플들 생성
        randomsample = normal_distribution.rvs(size=1)
        randomsample = randomsample.tolist()
        NatList(randomsample)
        N = randomsample[0]
        return N

    N = makeN(meanN, std_devN)

    # # 확률 밀도 함수 (PDF) 그리기
    # x = np.linspace(-4, 4, 100)
    # plt.plot(x, normal_distribution.pdf(x), 'r-', lw=2)

    # # 랜덤 샘플 히스토그램 그리기
    # plt.hist(random_samples, bins=30, density=True, alpha=0.5, color='b')

    # plt.title('Normal Distribution')
    # plt.xlabel('Value')
    # plt.ylabel('Probability Density')
    # plt.show()



    # Noraml Distribution 따르는 변수 만들기 (C_l)

    # 최댓값 찾아서 교환

    def swap_max_with_mth(lst, m):
        if m < len(lst):
            # 리스트에서 최대값과 그 인덱스를 찾음
            max_value = max(lst)
            max_index = lst.index(max_value)

            # 최대값과 M번째 값 교환
            lst[m], lst[max_index] = lst[max_index], lst[m]

            return lst
        else:
            print("Error: Index m is out of range.")

    # 평균과 표준편차 정의
    meanC = N / (L*(T_C - T_O))
    std_devC = meanC * 0.2

    def makeC(meanC, std_devC):
        # 노말 분포를 따르는 확률 변수 생성
        normal_distribution = norm(loc=meanC, scale=std_devC)

        # 랜덤 샘플들 생성
        random_samples = normal_distribution.rvs(size=L)
        random_samples = random_samples.tolist()

        for i in range(L):
            while random_samples[i] <= 0:
                random_samples[i] = normal_distribution.rvs(size=1)[0]

        # C_l들 생성
        C = swap_max_with_mth(random_samples, M)
        return C

    C = makeC(meanC, std_devC)

    # 카테고리 분포 따르는 변수 만들기 (a_i, d_i)

    #리스트의 모든 값을 그 합으로 나눠주는 함수
    def normalize_list(lst):
        # 리스트의 합 계산
        total = sum(lst)
        
        # 리스트의 각 요소를 합으로 나눠주기
        normalized_list = [value / total for value in lst]
        
        return normalized_list

    def makequery(C):
        # 카테고리 개수
        num_categories = L

        # 각 카테고리에 대한 확률
        probabilities = normalize_list(C)

        # 다항 분포를 따르는 확률 변수 생성 / 같을 경우 바꿈
        a = []
        d = []
        for i in range(N):
            a_i = np.random.choice(num_categories, 1, p=probabilities)
            d_i = np.random.choice(num_categories, 1, p=probabilities)
            a_i = a_i[0]
            d_i = d_i[0]
            while a_i == d_i:
                a_i = np.random.multinomial(1, probabilities)
                a_i = a_i[0]
            a.append(a_i)
            d.append(d_i)

        # Uniform 분포 따르는 변수 만들기 (t_i)
        t = np.random.uniform(T_O, T_C - 30*60, N)
        NatList(t)
        query = []
        for i in range(N):
            query.append([a[i], d[i], int(t[i])])
        query.sort(key = lambda x : -x[2])
        return query


    query = makequery(C)
    return query