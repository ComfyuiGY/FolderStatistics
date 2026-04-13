# -*- coding: utf-8 -*-
"""
读取文件夹图片数量插件
支持统计指定文件夹中的图片数量，可选择是否包含子文件夹
"""

import os
from pathlib import Path

# 支持的图片格式
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif',
    '.webp', '.ico', '.svg', '.heic', '.heif', '.jp2', '.jpx',
    '.raw', '.cr2', '.nef', '.arw', '.dng'  # 相机 RAW 格式
}


class FolderImageCounterAdvanced:
    """读取文件夹图片数量（完整版）"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件夹路径": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "要统计的文件夹路径"
                }),
                "包含子文件夹": ("BOOLEAN", {
                    "default": False,
                    "label_on": "✅ 包含",
                    "label_off": "❌ 不包含",
                    "tooltip": "是否读取子目录子文件夹中的图片"
                }),
            },
            "optional": {
                "额外格式": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "额外的文件扩展名（用逗号分隔），例如：.raw,.dng"
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("图片数量", "文件列表",)
    FUNCTION = "count_images"
    CATEGORY = "📁 图像数量统计"
    
    @classmethod
    def IS_CHANGED(cls, 文件夹路径, 包含子文件夹, 额外格式=""):
        """检查文件夹是否有变化"""
        if os.path.exists(文件夹路径):
            try:
                mtime = os.path.getmtime(文件夹路径)
                return (文件夹路径, 包含子文件夹, 额外格式, mtime)
            except:
                pass
        return (文件夹路径, 包含子文件夹, 额外格式, float("nan"))
    
    def get_image_extensions(self, extra_formats=""):
        """获取所有支持的图片扩展名"""
        extensions = set(IMAGE_EXTENSIONS)
        
        # 添加额外格式
        if extra_formats and extra_formats.strip():
            for fmt in extra_formats.split(','):
                fmt = fmt.strip().lower()
                if fmt:
                    if not fmt.startswith('.'):
                        fmt = '.' + fmt
                    extensions.add(fmt)
        
        return extensions
    
    def is_image_file(self, filename, extensions):
        """判断是否为图片文件"""
        ext = Path(filename).suffix.lower()
        return ext in extensions
    
    def count_images(self, 文件夹路径, 包含子文件夹, 额外格式=""):
        """统计文件夹中的图片数量"""
        # 检查路径是否存在
        if not 文件夹路径 or not 文件夹路径.strip():
            return (0, "错误：文件夹路径为空")
        
        folder = Path(文件夹路径.strip())
        
        if not folder.exists():
            return (0, f"错误：文件夹不存在 - {文件夹路径}")
        
        if not folder.is_dir():
            return (0, f"错误：路径不是文件夹 - {文件夹路径}")
        
        # 获取支持的扩展名
        extensions = self.get_image_extensions(额外格式)
        
        # 统计图片
        image_files = []
        
        try:
            if 包含子文件夹:
                # 递归遍历所有子文件夹
                for file_path in folder.rglob('*'):
                    if file_path.is_file() and self.is_image_file(file_path.name, extensions):
                        image_files.append(str(file_path))
            else:
                # 只遍历当前文件夹
                for file_path in folder.iterdir():
                    if file_path.is_file() and self.is_image_file(file_path.name, extensions):
                        image_files.append(str(file_path))
        except PermissionError:
            return (0, f"错误：没有权限访问文件夹 - {文件夹路径}")
        except Exception as e:
            return (0, f"错误：{str(e)}")
        
        # 排序以便于查看
        image_files.sort()
        
        # 生成文件列表字符串（每行一个文件路径）
        file_list = "\n".join(image_files) if image_files else "未找到图片文件"
        
        return (len(image_files), file_list)


class FolderImageCounter:
    """读取文件夹图片数量（简化版，只返回数量）"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件夹路径": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "要统计的文件夹路径"
                }),
                "包含子文件夹": ("BOOLEAN", {
                    "default": False,
                    "label_on": "✅ 包含",
                    "label_off": "❌ 不包含",
                    "tooltip": "是否读取子目录子文件夹中的图片"
                }),
            }
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("图片数量",)
    FUNCTION = "count_images"
    CATEGORY = "📁 图像数量统计"
    
    @classmethod
    def IS_CHANGED(cls, 文件夹路径, 包含子文件夹):
        if os.path.exists(文件夹路径):
            try:
                mtime = os.path.getmtime(文件夹路径)
                return (文件夹路径, 包含子文件夹, mtime)
            except:
                pass
        return (文件夹路径, 包含子文件夹, float("nan"))
    
    def count_images(self, 文件夹路径, 包含子文件夹):
        """统计文件夹中的图片数量"""
        if not 文件夹路径 or not 文件夹路径.strip():
            return (0,)
        
        folder = Path(文件夹路径.strip())
        
        if not folder.exists() or not folder.is_dir():
            return (0,)
        
        image_count = 0
        
        try:
            if 包含子文件夹:
                for file_path in folder.rglob('*'):
                    if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                        image_count += 1
            else:
                for file_path in folder.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                        image_count += 1
        except:
            pass
        
        return (image_count,)


class FolderSubdirectoryListAdvanced:
    """读取文件夹子目录列表（高级版）"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件夹路径": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "要读取的文件夹路径"
                }),
                "包含子文件夹": ("BOOLEAN", {
                    "default": False,
                    "label_on": "✅ 读取子目录",
                    "label_off": "❌ 仅当前层",
                    "tooltip": "是否读取子目录所有层级的子文件夹"
                }),
            },
            "optional": {
                "排除文件夹": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "要排除的文件夹名称（用逗号分隔），例如：__pycache__,node_modules,.git"
                }),
                "最大深度": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100,
                    "step": 1,
                    "tooltip": "最大递归深度（-1=无限制，仅在包含子文件夹时有效）"
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("子目录数量", "子目录列表",)
    FUNCTION = "list_subdirectories"
    CATEGORY = "📁 子目录路径读取工具"
    
    @classmethod
    def IS_CHANGED(cls, 文件夹路径, 包含子文件夹, 排除文件夹="", 最大深度=-1):
        """检查文件夹是否有变化"""
        if os.path.exists(文件夹路径):
            try:
                mtime = os.path.getmtime(文件夹路径)
                return (文件夹路径, 包含子文件夹, 排除文件夹, 最大深度, mtime)
            except:
                pass
        return (文件夹路径, 包含子文件夹, 排除文件夹, 最大深度, float("nan"))
    
    def get_excluded_folders(self, exclude_str):
        """获取要排除的文件夹列表"""
        excluded = set()
        if exclude_str and exclude_str.strip():
            for name in exclude_str.split(','):
                name = name.strip()
                if name:
                    excluded.add(name)
        return excluded
    
    def should_exclude(self, folder_name, excluded_folders):
        """检查是否应该排除该文件夹"""
        return folder_name in excluded_folders
    
    def list_subdirectories(self, 文件夹路径, 包含子文件夹, 排除文件夹="", 最大深度=-1):
        """读取文件夹子目录列表"""
        # 检查路径是否存在
        if not 文件夹路径 or not 文件夹路径.strip():
            return (0, "错误：文件夹路径为空")
        
        folder = Path(文件夹路径.strip())
        
        if not folder.exists():
            return (0, f"错误：文件夹不存在 - {文件夹路径}")
        
        if not folder.is_dir():
            return (0, f"错误：路径不是文件夹 - {文件夹路径}")
        
        # 获取排除列表
        excluded_folders = self.get_excluded_folders(排除文件夹)
        
        # 收集子目录
        subdirectories = []
        
        try:
            if 包含子文件夹:
                # 读取子目录所有子文件夹
                if 最大深度 == 0:
                    return (0, "错误：最大深度不能为0")
                
                def collect_recursive(current_path, current_depth):
                    """递归收集子目录"""
                    if 最大深度 != -1 and current_depth > 最大深度:
                        return
                    
                    try:
                        for item in current_path.iterdir():
                            if item.is_dir():
                                folder_name = item.name
                                if not self.should_exclude(folder_name, excluded_folders):
                                    subdirectories.append(str(item))
                                    # 继续递归子文件夹
                                    collect_recursive(item, current_depth + 1)
                    except PermissionError:
                        pass  # 跳过无权限的文件夹
                    except Exception:
                        pass
                
                collect_recursive(folder, 1)
            else:
                # 只读取当前层级的子文件夹
                for item in folder.iterdir():
                    if item.is_dir():
                        folder_name = item.name
                        if not self.should_exclude(folder_name, excluded_folders):
                            subdirectories.append(str(item))
        except PermissionError:
            return (0, f"错误：没有权限访问文件夹 - {文件夹路径}")
        except Exception as e:
            return (0, f"错误：{str(e)}")
        
        # 排序
        subdirectories.sort()
        
        # 生成列表字符串（直接拼接，不带引号）
        if subdirectories:
            dir_list = "\n".join(subdirectories)
        else:
            dir_list = "未找到子文件夹"
        
        return (len(subdirectories), dir_list)


class FolderSubdirectoryList:
    """读取文件夹子目录列表（简化版，返回数量和列表）"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "文件夹路径": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "要读取的文件夹路径"
                }),
                "包含子文件夹": ("BOOLEAN", {
                    "default": False,
                    "label_on": "✅ 读取子目录",
                    "label_off": "❌ 仅当前层",
                    "tooltip": "是否读取子目录所有层级的子文件夹"
                }),
            }
        }
    
    RETURN_TYPES = ("INT", "STRING",)
    RETURN_NAMES = ("子目录数量", "子目录列表",)
    FUNCTION = "list_subdirectories"
    CATEGORY = "📁 子目录路径读取工具"
    
    @classmethod
    def IS_CHANGED(cls, 文件夹路径, 包含子文件夹):
        if os.path.exists(文件夹路径):
            try:
                mtime = os.path.getmtime(文件夹路径)
                return (文件夹路径, 包含子文件夹, mtime)
            except:
                pass
        return (文件夹路径, 包含子文件夹, float("nan"))
    
    def list_subdirectories(self, 文件夹路径, 包含子文件夹):
        """读取文件夹子目录列表"""
        if not 文件夹路径 or not 文件夹路径.strip():
            return (0, "错误：文件夹路径为空")
        
        folder = Path(文件夹路径.strip())
        
        if not folder.exists():
            return (0, f"错误：文件夹不存在 - {文件夹路径}")
        
        if not folder.is_dir():
            return (0, f"错误：路径不是文件夹 - {文件夹路径}")
        
        subdirectories = []
        
        try:
            if 包含子文件夹:
                # 读取子目录所有子文件夹
                for item in folder.rglob('*'):
                    if item.is_dir():
                        subdirectories.append(str(item))
            else:
                # 只读取当前层级的子文件夹
                for item in folder.iterdir():
                    if item.is_dir():
                        subdirectories.append(str(item))
        except:
            return (0, "错误：无法读取文件夹")
        
        subdirectories.sort()
        
        # 生成列表字符串（直接拼接，不带引号）
        if subdirectories:
            dir_list = "\n".join(subdirectories)
        else:
            dir_list = "未找到子文件夹"
        
        return (len(subdirectories), dir_list)