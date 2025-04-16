import numpy as np

def standard_formula(a, b, c):
    """使用标准公式求解二次方程"""
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    sqrt_disc = np.sqrt(discriminant)
    x1 = (-b + sqrt_disc) / (2*a)
    x2 = (-b - sqrt_disc) / (2*a)
    return (x1, x2)

def alternative_formula(a, b, c):
    """使用替代公式求解二次方程"""
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    sqrt_disc = np.sqrt(discriminant)
    x1 = (2*c) / (-b + sqrt_disc)
    x2 = (2*c) / (-b - sqrt_disc)
    return (x1, x2)

def stable_formula(a, b, c):
    """稳定的二次方程求根程序"""
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return None
    
    sqrt_disc = np.sqrt(discriminant)
    
    # 根据b的符号选择计算方式以避免抵消
    if b > 0:
        x1 = (2*c) / (-b - sqrt_disc)
        x2 = (-b - sqrt_disc) / (2*a)
    else:
        x1 = (-b + sqrt_disc) / (2*a)
        x2 = (2*c) / (-b + sqrt_disc)
    
    return (x1, x2)
    
def main():
    test_cases = [
        (1, 2, 1),             # 简单情况
        (1, 1e5, 1),           # b远大于a和c
        (0.001, 1000, 0.001),  # 原测试用例
    ]
    
    for a, b, c in test_cases:
        print("\n" + "="*50)
        print("测试方程：{}x^2 + {}x + {} = 0".format(a, b, c))
        
        # 使用标准公式
        roots1 = standard_formula(a, b, c)
        print("\n方法1（标准公式）的结果：")
        if roots1:
            print("x1 = {:.15f}, x2 = {:.15f}".format(roots1[0], roots1[1]))
        else:
            print("无实根")
        
        # 使用替代公式
        roots2 = alternative_formula(a, b, c)
        print("\n方法2（替代公式）的结果：")
        if roots2:
            print("x1 = {:.15f}, x2 = {:.15f}".format(roots2[0], roots2[1]))
        else:
            print("无实根")
        
        # 使用稳定的求根程序
        roots3 = stable_formula(a, b, c)
        print("\n方法3（稳定求根程序）的结果：")
        if roots3:
            print("x1 = {:.15f}, x2 = {:.15f}".format(roots3[0], roots3[1]))
        else:
            print("无实根")

if __name__ == "__main__":
    main()
