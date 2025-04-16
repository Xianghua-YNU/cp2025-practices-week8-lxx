import numpy as np
import matplotlib.pyplot as plt

def sum_S1(N):
    """计算第一种形式的级数和：交错级数"""
    total = 0.0
    for n in range(1, 2*N + 1):
        term = (-1)**n * n / (n + 1)
        total += term
    return total

def sum_S2(N):
    """计算第二种形式的级数和：两项求和相减"""
    sum1 = 0.0  # -sum( (2n-1)/(2n) )
    sum2 = 0.0  # sum( (2n)/(2n+1) )
    
    for n in range(1, N + 1):
        sum1 += (2*n - 1) / (2*n)
        sum2 += (2*n) / (2*n + 1)
    
    return -sum1 + sum2

def sum_S3(N):
    """计算第三种形式的级数和：直接求和"""
    total = 0.0
    for n in range(1, N + 1):
        term = 1.0 / (2*n * (2*n + 1))
        total += term
    return total

def calculate_relative_errors(N_values):
    """计算相对误差"""
    err1 = []
    err2 = []
    
    for N in N_values:
        s1 = sum_S1(N)
        s2 = sum_S2(N)
        s3 = sum_S3(N)
        
        # 避免除以零
        if s3 == 0:
            err1.append(0)
            err2.append(0)
        else:
            err1.append(abs(s1 - s3) / abs(s3))
            err2.append(abs(s2 - s3) / abs(s3))
    
    return err1, err2

def plot_errors(N_values, err1, err2):
    """绘制误差分析图"""
    plt.figure(figsize=(10, 6))
    plt.loglog(N_values, err1, 'o-', label='Error of S1')
    plt.loglog(N_values, err2, 's-', label='Error of S2')
    
    # 添加理论参考线
    plt.loglog(N_values, 1e-15 * np.sqrt(N_values), '--', label='O(√N) reference')
    plt.loglog(N_values, 1e-15 * N_values, '--', label='O(N) reference')
    
    plt.xlabel('N (log scale)')
    plt.ylabel('Relative Error (log scale)')
    plt.title('Numerical Stability of Different Summation Forms')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()

def print_results():
    """打印典型N值的计算结果"""
    N_values = [10, 100, 1000, 10000, 100000]
    print("Numerical Summation Comparison")
    print("-----------------------------------------------")
    print(f"{'N':<8} {'S1':<15} {'S2':<15} {'S3':<15} {'Err1':<15} {'Err2':<15}")
    
    for N in N_values:
        s1 = sum_S1(N)
        s2 = sum_S2(N)
        s3 = sum_S3(N)
        err1 = abs(s1 - s3) / abs(s3) if s3 != 0 else 0
        err2 = abs(s2 - s3) / abs(s3) if s3 != 0 else 0
        
        print(f"{N:<8} {s1:<15.12f} {s2:<15.12f} {s3:<15.12f} {err1:<15.2e} {err2:<15.2e}")

def main():
    """主函数"""
    # 生成N值序列
    N_values = np.logspace(0, 5, 50, dtype=int)
    N_values = np.unique(N_values)  # 去除可能的重复值
    
    # 计算误差
    err1, err2 = calculate_relative_errors(N_values)
    
    # 打印结果
    print_results()
    
    # 绘制误差图
    plot_errors(N_values, err1, err2)

if __name__ == "__main__":
    main()
