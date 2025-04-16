import numpy as np
import matplotlib.pyplot as plt
from scipy.special import spherical_jn

def bessel_up(x, lmax):
    j = np.zeros(lmax + 1)
    j[0] = np.sin(x) / x if x != 0 else 1.0
    if lmax >= 1:
        j[1] = (np.sin(x) / x - np.cos(x)) / x if x != 0 else 0.0
        for l in range(1, lmax):
            j[l+1] = (2*l + 1)/x * j[l] - j[l-1]
    return j

def bessel_down(x, lmax, m_start=None):
    if m_start is None:
        m_start = lmax + 15
    
    # 初始化数组，从0到m_start+1
    j = np.zeros(m_start + 2)
    j[m_start + 1] = 0.0
    j[m_start] = 1.0
    
    # 向下递推
    for l in range(m_start, 0, -1):
        j[l-1] = (2*l + 1)/x * j[l] - j[l+1]
    
    # 归一化
    j0_analytic = np.sin(x)/x if x != 0 else 1.0
    norm_factor = j0_analytic / j[0]
    j_normalized = j[:lmax+1] * norm_factor
    
    return j_normalized

def plot_comparison(x, lmax):
    l_values = np.arange(lmax + 1)
    j_up = bessel_up(x, lmax)
    j_down = bessel_down(x, lmax)
    j_scipy = spherical_jn(l_values, x)
    
    plt.figure(figsize=(12, 5))
    
    # 函数值比较
    plt.subplot(1, 2, 1)
    plt.semilogy(l_values, np.abs(j_up), 'o-', label='Upward')
    plt.semilogy(l_values, np.abs(j_down), 's-', label='Downward')
    plt.semilogy(l_values, np.abs(j_scipy), '^-', label='Scipy')
    plt.xlabel('Order l')
    plt.ylabel('|j_l(x)|')
    plt.title(f'Comparison of methods (x={x})')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    
    # 相对误差比较
    plt.subplot(1, 2, 2)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_err_up = np.abs((j_up - j_scipy)/j_scipy)
        rel_err_down = np.abs((j_down - j_scipy)/j_scipy)
    
    plt.semilogy(l_values, rel_err_up, 'o-', label='Upward error')
    plt.semilogy(l_values, rel_err_down, 's-', label='Downward error')
    plt.xlabel('Order l')
    plt.ylabel('Relative error')
    plt.title(f'Relative error (x={x})')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    
    plt.tight_layout()
    plt.show()

def main():
    """主函数"""
    # 设置参数
    lmax = 25
    x_values = [0.1, 1.0, 10.0]
    
    # 对每个x值进行计算和绘图
    for x in x_values:
        plot_comparison(x, lmax)
        
        # 打印特定阶数的结果
        l_check = [3, 5, 8]
        print(f"\nx = {x}:")
        print("l\tUp\t\tDown\t\tScipy")
        print("-" * 50)
        for l in l_check:
            j_up = bessel_up(x, l)[l]
            j_down = bessel_down(x, l)[l]
            j_scipy = spherical_jn(l, x)
            print(f"{l}\t{j_up:.6e}\t{j_down:.6e}\t{j_scipy:.6e}")

if __name__ == "__main__":
    main()
