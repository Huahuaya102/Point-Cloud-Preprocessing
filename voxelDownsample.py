import open3d as o3d
import time
import numpy as np

# 记录开始时间
start_time = time.time()

# 1. 读取点云
pcd = o3d.io.read_point_cloud("/home/ubuntu/yjh/3DGS-to-PC/infrastructure_site_original.ply")
load_time = time.time()
print(f"点云加载完成，耗时: {load_time - start_time:.3f} 秒")
print(f"原始点云点数: {len(pcd.points)}")

# （可选）计算平均点间距来辅助确定体素大小
distances = pcd.compute_nearest_neighbor_distance()
avg_distance = np.mean(distances)
print(f"平均点间距: {avg_distance:.6f}")

# 2. 执行体素网格下采样
# 选择体素大小（例如，设置为平均点间距的3倍）
voxel_size = avg_distance * 3
# 或者直接指定一个值，如 voxel_size = 0.01

downpcd = pcd.voxel_down_sample(voxel_size=voxel_size)
filter_time = time.time()
print(f"体素网格滤波完成，耗时: {filter_time - load_time:.3f} 秒")
print(f"体素大小: {voxel_size:.6f}")

# 3. 保存下采样后的点云
o3d.io.write_point_cloud("./output/infrastructure_site_voxel.ply", downpcd)
save_time = time.time()
print(f"结果保存完成，耗时: {save_time - filter_time:.3f} 秒")

# 4. 输出总体统计信息
total_time = time.time() - start_time
original_points = len(pcd.points)
downsampled_points = len(downpcd.points)
removed_points = original_points - downsampled_points
compression_ratio = (downsampled_points / original_points) * 100

print("\n=== 运行统计 ===")
print(f"原始点云点数: {original_points}")
print(f"下采样后点数: {downsampled_points}")
print(f"移除点数: {removed_points}")
print(f"压缩比例: {compression_ratio:.2f}%")
print(f"总运行时间: {total_time:.3f} 秒")