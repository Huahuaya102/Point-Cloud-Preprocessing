import open3d as o3d
import numpy as np
import time
from scipy.spatial import KDTree

def gaussian_filter_point_cloud(pcd, sigma=0.1, k_neighbors=30):
    """
    对点云进行高斯滤波
    :param pcd: 输入点云
    :param sigma: 高斯函数的标准差
    :param k_neighbors: 最近邻点数
    :return: 滤波后的点云
    """
    points = np.asarray(pcd.points)
    new_points = np.zeros_like(points)
    
    # 构建KD树用于快速最近邻搜索
    kdtree = KDTree(points)
    
    for i in range(len(points)):
        # 查找k个最近邻点（包括自身）
        distances, indices = kdtree.query(points[i], k=k_neighbors)
        
        # 计算高斯权重
        weights = np.exp(-distances**2 / (2 * sigma**2))
        
        # 避免除零错误
        if np.sum(weights) > 1e-8:
            # 计算加权平均
            new_points[i] = np.average(points[indices], axis=0, weights=weights)
        else:
            new_points[i] = points[i]
    
    # 创建新的点云对象
    filtered_pcd = o3d.geometry.PointCloud()
    filtered_pcd.points = o3d.utility.Vector3dVector(new_points)
    
    # 保持原有颜色（如果有）
    if pcd.has_colors():
        filtered_pcd.colors = pcd.colors
    
    return filtered_pcd

# 记录开始时间
start_time = time.time()

# 1. 读取点云
pcd = o3d.io.read_point_cloud("/home/ubuntu/yjh/3DGS-to-PC/meetingroom_original.ply")
load_time = time.time()
print(f"点云加载完成，耗时: {load_time - start_time:.3f} 秒")
print(f"原始点云点数: {len(pcd.points)}")

# 计算平均点间距来辅助确定参数
distances = pcd.compute_nearest_neighbor_distance()
avg_distance = np.mean(distances)
print(f"平均点间距: {avg_distance:.6f}")

# 2. 执行高斯滤波
sigma = avg_distance * 2.0  # sigma设为平均间距的2倍
k_neighbors = 30

filtered_pcd = gaussian_filter_point_cloud(pcd, sigma=sigma, k_neighbors=k_neighbors)
filter_time = time.time()
print(f"高斯滤波完成，耗时: {filter_time - load_time:.3f} 秒")
print(f"参数: sigma={sigma:.6f}, k_neighbors={k_neighbors}")

# 3. 保存滤波后的点云
o3d.io.write_point_cloud("./output/meetingroom_gaussian.ply", filtered_pcd)
save_time = time.time()
print(f"结果保存完成，耗时: {save_time - filter_time:.3f} 秒")

# 4. 输出总体统计信息
total_time = time.time() - start_time
print(f"\n总运行时间: {total_time:.3f} 秒")
