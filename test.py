import random

#print random numbers and stop when number is smaller than 0.001 and count how many numbers it took to get to 0.001
def random_numbers():
    count = 0
    while True:
        num = random.random()
        print(num)
        count += 1
        if num < 0.001:
            break
    print(f'Count: {count}')

#repeat random_numbers() N times and print average loop count
def repeat_random_numbers(N):
    loop_counts = []
    for i in range(N):
        count = 0
        while True:
            num = random.random()
            count += 1
            if num < 0.001:
                break
        loop_counts.append(count)
    print(f'Average loop count: {sum(loop_counts)/len(loop_counts)}')

repeat_random_numbers(1)


