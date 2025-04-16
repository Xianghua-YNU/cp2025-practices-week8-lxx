import numpy as np
import matplotlib.pyplot as plt
import time

def sum_up(N):
    """从小到大计算调和级数和"""
    total = 0.0
    for n in range(1, N+1):
        total += 1.0 / n
    return total

def sum_down(N):
    """从大到小计算调和级数和"""
    total = 0.0
    for n in range(N, 0, -1):
        total += 1.0 / n
    return total

def calculate_relative_difference(N):
    """计算两种方法的相对差异"""
    s_up = sum_up(N)
    s_down = sum_down(N)
    if s_up + s_down == 0:  # Shouldn't happen for N >= 1
        return 0.0
    return abs(s_up - s_down) / ((s_up + s_down)/2)

def plot_differences():
    """绘制相对差异随N的变化"""
    N_values = np.logspace(1, 7, 50, dtype=int)  # 10^1 to 10^7
    differences = []
    
    for N in N_values:
        diff = calculate_relative_difference(N)
        differences.append(diff)
    
    plt.figure(figsize=(10, 6))
    plt.loglog(N_values, differences, 'o-', label='Relative Difference')
    plt.xlabel('N (log scale)')
    plt.ylabel('Relative Difference (log scale)')
    plt.title('Effect of Summation Order on Harmonic Series')
    plt.grid(True, which="both", ls="-")
    
    # 添加理论参考线
    theoretical = N_values * np.finfo(float).eps
    plt.loglog(N_values, theoretical, '--', label='Theoretical O(Nε)')
    
    plt.legend()
    plt.show()

def print_results():
    """打印典型N值的计算结果"""
    N_values = [10, 100, 1000, 10000, 100000, 1000000]
    print("Harmonic Series Summation Comparison")
    print("-----------------------------------")
    print(f"{'N':<10} {'Sum Up':<15} {'Sum Down':<15} {'Relative Diff':<15}")
    
    for N in N_values:
        s_up = sum_up(N)
        s_down = sum_down(N)
        diff = calculate_relative_difference(N)
        print(f"{N:<10} {s_up:<15.10f} {s_down:<15.10f} {diff:<15.2e}")

def time_comparison():
    """比较两种方法的计算时间"""
    N = 10**7
    
    # 预热（避免首次运行的额外开销影响计时）
    sum_up(100)
    sum_down(100)
    
    # 计时sum_up
    start = time.perf_counter()
    sum_up(N)
    up_time = time.perf_counter() - start
    
    # 计时sum_down
    start = time.perf_counter()
    sum_down(N)
    down_time = time.perf_counter() - start
    
    print("\nTime Comparison for N=10^7:")
    print(f"Sum Up: {up_time:.4f} seconds")
    print(f"Sum Down: {down_time:.4f} seconds")

def main():
    """主函数"""
    # 打印计算结果
    print_results()
    
    # 绘制误差图
    plot_differences()
    
    # 时间比较
    time_comparison()

if __name__ == "__main__":
    main()
