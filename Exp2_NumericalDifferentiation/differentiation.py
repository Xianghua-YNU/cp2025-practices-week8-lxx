import numpy as np
import matplotlib.pyplot as plt

def f(x):
    """定义测试函数 f(x) = x(x-1)"""
    return x * (x - 1)

def forward_diff(f, x, delta):
    """前向差分法计算导数"""
    return (f(x + delta) - f(x)) / delta

def central_diff(f, x, delta):
    """中心差分法计算导数"""
    return (f(x + delta) - f(x - delta)) / (2 * delta)

def analytical_derivative(x):
    """解析导数 f'(x) = 2x - 1"""
    return 2 * x - 1

def calculate_errors(x_point=1.0):
    """计算不同步长下的误差"""
    deltas = np.logspace(-2, -14, num=7, base=10)  # 10^-2到10^-14
    forward_errors = []
    central_errors = []
    exact = analytical_derivative(x_point)
    
    for delta in deltas:
        # 计算前向差分和误差
        fd = forward_diff(f, x_point, delta)
        forward_error = abs(fd - exact) / abs(exact)
        forward_errors.append(forward_error)
        
        # 计算中心差分和误差
        cd = central_diff(f, x_point, delta)
        central_error = abs(cd - exact) / abs(exact)
        central_errors.append(central_error)
    
    return deltas, forward_errors, central_errors

def plot_errors(deltas, forward_errors, central_errors):
    """绘制误差-步长关系图"""
    plt.figure(figsize=(10, 6))
    
    # 绘制误差曲线
    plt.loglog(deltas, forward_errors, 'o-', label='Forward Difference')
    plt.loglog(deltas, central_errors, 's-', label='Central Difference')
    
    # 添加理论收敛阶数参考线
    plt.loglog(deltas, 0.5*deltas, '--', label='O(δ) theoretical slope')
    plt.loglog(deltas, 0.1*deltas**2, '--', label='O(δ²) theoretical slope')
    
    plt.xlabel('Step size δ (log scale)')
    plt.ylabel('Relative error (log scale)')
    plt.title('Error in numerical differentiation at x=1')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()

def print_results(deltas, forward_errors, central_errors):
    """打印计算结果表格"""
    exact = analytical_derivative(1.0)
    print("\nNumerical Differentiation Results at x=1 (exact derivative = 1.0)")
    print("----------------------------------------------------------------")
    print(f"{'δ':<15} {'Forward Diff':<15} {'Central Diff':<15} {'Fwd Error':<15} {'Ctr Error':<15}")
    for d, fe, ce in zip(deltas, forward_errors, central_errors):
        fd = forward_diff(f, 1.0, d)
        cd = central_diff(f, 1.0, d)
        print(f"{d:<15.2e} {fd:<15.8f} {cd:<15.8f} {fe:<15.2e} {ce:<15.2e}")

def main():
    """主函数"""
    x_point = 1.0
    
    # 计算误差
    deltas, forward_errors, central_errors = calculate_errors(x_point)
    
    # 打印结果
    print(f"函数 f(x) = x(x-1) 在 x = {x_point} 处的解析导数值: {analytical_derivative(x_point)}")
    print_results(deltas, forward_errors, central_errors)
    
    # 绘制误差图
    plot_errors(deltas, forward_errors, central_errors)
    
    # 最优步长分析
    forward_best_idx = np.argmin(forward_errors)
    central_best_idx = np.argmin(central_errors)
    
    print("\n最优步长分析:")
    print(f"前向差分最优步长: {deltas[forward_best_idx]:.2e}, 相对误差: {forward_errors[forward_best_idx]:.6e}")
    print(f"中心差分最优步长: {deltas[central_best_idx]:.2e}, 相对误差: {central_errors[central_best_idx]:.6e}")
    
    # 收敛阶数分析
    mid_idx = len(deltas) // 2
    forward_slope = np.log(forward_errors[mid_idx] / forward_errors[mid_idx-2]) / np.log(deltas[mid_idx] / deltas[mid_idx-2])
    central_slope = np.log(central_errors[mid_idx] / central_errors[mid_idx-2]) / np.log(deltas[mid_idx] / deltas[mid_idx-2])
    
    print("\n收敛阶数分析:")
    print(f"前向差分收敛阶数约为: {forward_slope:.2f} (理论值: 1.0)")
    print(f"中心差分收敛阶数约为: {central_slope:.2f} (理论值: 2.0)")

if __name__ == "__main__":
    main()
