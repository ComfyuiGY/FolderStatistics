# -*- coding: utf-8 -*-
"""
ComfyUI 文件夹图片数量统计插件
"""

import os

current_dir = os.path.dirname(os.path.abspath(__file__))

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "FolderImageCounter", 
        os.path.join(current_dir, "FolderImageCounter.py")
    )
    FolderImageCounterModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(FolderImageCounterModule)
    
    # 导入所有节点类
    FolderImageCounterAdvanced = FolderImageCounterModule.FolderImageCounterAdvanced
    FolderImageCounter = FolderImageCounterModule.FolderImageCounter
    FolderSubdirectoryListAdvanced = FolderImageCounterModule.FolderSubdirectoryListAdvanced
    FolderSubdirectoryList = FolderImageCounterModule.FolderSubdirectoryList
    
except Exception as e:
    print(f"[FolderImageCounter] 加载失败: {e}")
    
    class DummyNode:
        @classmethod
        def INPUT_TYPES(cls):
            return {"required": {}}
        RETURN_TYPES = ()
        FUNCTION = "dummy"
        CATEGORY = "📁 文件工具"
        def dummy(self):
            return ()
    
    FolderImageCounterAdvanced = DummyNode
    FolderImageCounter = DummyNode
    FolderSubdirectoryListAdvanced = DummyNode
    FolderSubdirectoryList = DummyNode

NODE_CLASS_MAPPINGS = {
    "FolderImageCounterAdvanced": FolderImageCounterAdvanced,
    "FolderImageCounter": FolderImageCounter,
    "FolderSubdirectoryListAdvanced": FolderSubdirectoryListAdvanced,
    "FolderSubdirectoryList": FolderSubdirectoryList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FolderImageCounterAdvanced": "📷 文件夹图像统计(高级)",
    "FolderImageCounter": "📷 图像数量统计",
    "FolderSubdirectoryListAdvanced": "📁 子目录列表(高级)",
    "FolderSubdirectoryList": "📁 子目录列表",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]