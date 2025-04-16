import numpy as np
import matplotlib.pyplot as plt
import time

def f(x):
    """被积函数 f(x) = sqrt(1-x^2)"""
    return np.sqrt(1 - x**2)

def rectangle_method(f, a, b, N):
    """矩形法（左矩形法）计算积分"""
    h = (b - a) / N
    x = np.linspace(a, b-h, N)  # 左端点
    return h * np.sum(f(x))

def trapezoid_method(f, a, b, N):
    """梯形法计算积分"""
    h = (b - a) / N
    x = np.linspace(a, b, N+1)  # 包括所有端点
    return h/2 * (f(a) + 2*np.sum(f(x[1:-1])) + f(b))

def calculate_errors(a, b, exact_value):
    """计算不同N值下各方法的误差"""
    N_values = np.array([10, 100, 1000, 10000, 100000])
    h_values = (b - a) / N_values
    rect_errors = []
    trap_errors = []
    
    for N in N_values:
        rect_val = rectangle_method(f, a, b, N)
        trap_val = trapezoid_method(f, a, b, N)
        rect_errors.append(abs(rect_val - exact_value) / exact_value)
        trap_errors.append(abs(trap_val - exact_value) / exact_value)
    
    return N_values, h_values, rect_errors, trap_errors

def plot_errors(h_values, rect_errors, trap_errors):
    """绘制误差-步长关系图"""
    plt.figure(figsize=(10, 6))
    plt.loglog(h_values, rect_errors, 'o-', label='Rectangle Method')
    plt.loglog(h_values, trap_errors, 's-', label='Trapezoid Method')
    
    # 添加理论参考线
    plt.loglog(h_values, 0.5*h_values, '--', label='O(h) theoretical slope')
    plt.loglog(h_values, 0.1*h_values**2, '--', label='O(h²) theoretical slope')
    
    plt.xlabel('Step size h (log scale)')
    plt.ylabel('Relative error (log scale)')
    plt.title('Convergence of Numerical Integration Methods')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()

def print_results(N_values, rect_results, trap_results, exact_value):
    """打印计算结果表格"""
    print("\nNumerical Integration Results")
    print("-----------------------------------------------")
    print(f"{'N':<8} {'Rectangle':<15} {'Error':<15} {'Trapezoid':<15} {'Error':<15}")
    for N, rect, trap in zip(N_values, rect_results, trap_results):
        rect_err = abs(rect - exact_value) / exact_value
        trap_err = abs(trap - exact_value) / exact_value
        print(f"{N:<8} {rect:<15.10f} {rect_err:<15.2e} {trap:<15.10f} {trap_err:<15.2e}")

def time_performance_test(a, b, max_time=1.0):
    """测试在限定时间内各方法能达到的最高精度"""
    exact_value = np.pi/2
    N = 10
    best_rect = (0, 1.0)  # (N, error)
    best_trap = (0, 1.0)
    
    print("\nPerformance Test (max time = 1.0s)")
    print("-----------------------------------------------")
    
    start_time = time.time()
    while time.time() - start_time < max_time:
        # 矩形法测试
        t0 = time.time()
        rect_val = rectangle_method(f, a, b, N)
        rect_err = abs(rect_val - exact_value) / exact_value
        if rect_err < best_rect[1]:
            best_rect = (N, rect_err)
        
        # 梯形法测试
        trap_val = trapezoid_method(f, a, b, N)
        trap_err = abs(trap_val - exact_value) / exact_value
        if trap_err < best_trap[1]:
            best_trap = (N, trap_err)
        
        N *= 2
    
    print(f"Rectangle Method - Best N: {best_rect[0]}, Error: {best_rect[1]:.2e}")
    print(f"Trapezoid Method - Best N: {best_trap[0]}, Error: {best_trap[1]:.2e}")

def calculate_convergence_rate(h_values, errors):
    """计算收敛阶数"""
    log_h = np.log(h_values[:-1])  # 排除最后一个点（可能受舍入误差影响）
    log_err = np.log(errors[:-1])
    slope = np.polyfit(log_h, log_err, 1)[0]
    return slope

def main():
    """主函数"""
    a, b = -1.0, 1.0  # 积分区间
    exact_value = np.pi/2  # 精确值
    
    print(f"计算积分 ∫_{a}^{b} √(1-x²) dx")
    print(f"精确值: {exact_value:.12f}")
    
    # 计算不同N值下的结果
    N_values = [10, 100, 1000, 10000]
    rect_results = [rectangle_method(f, a, b, N) for N in N_values]
    trap_results = [trapezoid_method(f, a, b, N) for N in N_values]
    
    # 打印结果
    print_results(N_values, rect_results, trap_results, exact_value)
    
    # 计算误差
    N_values, h_values, rect_errors, trap_errors = calculate_errors(a, b, exact_value)
    
    # 绘制误差图
    plot_errors(h_values, rect_errors, trap_errors)
    
    # 计算收敛阶数
    rect_rate = calculate_convergence_rate(h_values, rect_errors)
    trap_rate = calculate_convergence_rate(h_values, trap_errors)
    
    print("\n收敛阶数分析:")
    print(f"矩形法: {rect_rate:.2f} (理论值: 1.0)")
    print(f"梯形法: {trap_rate:.2f} (理论值: 2.0)")
    
    # 时间性能测试
    time_performance_test(a, b)

if __name__ == "__main__":
    main()
