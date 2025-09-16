# /home/ubuntu/yjh/3DGS-to-PC/infrastructure_site_original.ply
# ./output/infrastructure_site_SOR.ply


import open3d as o3d
import time

# 记录开始时间
start_time = time.time()

# 1. 读取点云
pcd = o3d.io.read_point_cloud("/home/ubuntu/yjh/3DGS-to-PC/meetingroom_original.ply")
load_time = time.time()
print(f"点云加载完成，耗时: {load_time - start_time:.3f} 秒")

# 2. 执行统计滤波
# 选择参数：k=50, α=2.0
cl, ind = pcd.remove_statistical_outlier(nb_neighbors=50, std_ratio=2.0)
filter_time = time.time()
print(f"统计滤波完成，耗时: {filter_time - load_time:.3f} 秒")

# 3. 保存滤波后的点云
o3d.io.write_point_cloud("./output/meetingroom_SOR.ply", cl)
save_time = time.time()
print(f"结果保存完成，耗时: {save_time - filter_time:.3f} 秒")

# 4. 输出总体统计信息
total_time = time.time() - start_time
original_points = len(pcd.points)
filtered_points = len(cl.points)
removed_points = original_points - filtered_points
removal_ratio = (removed_points / original_points) * 100

print("\n=== 运行统计 ===")
print(f"原始点云点数: {original_points}")
print(f"滤波后点数: {filtered_points}")
print(f"移除离群点数量: {removed_points}")
print(f"移除比例: {removal_ratio:.2f}%")
print(f"总运行时间: {total_time:.3f} 秒")


