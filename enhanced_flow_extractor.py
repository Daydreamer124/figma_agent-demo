#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版 Figma 用户流程提取器
基于顶层 Frame 识别和 Prototype 连接分析
"""

import requests
import json
import re
from typing import Dict, List, Tuple, Optional

class EnhancedFigmaJourneyExtractor:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.figma.com/v1"
        self.headers = {
            "X-Figma-Token": access_token,
            "Content-Type": "application/json"
        }
        
    def extract_file_key_from_url(self, figma_url: str) -> str:
        """从 Figma URL 中提取 file_key"""
        patterns = [
            r'figma\.com/file/([a-zA-Z0-9]+)',
            r'figma\.com/design/([a-zA-Z0-9]+)',
            r'figma\.com/proto/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, figma_url)
            if match:
                return match.group(1)
        
        raise ValueError("无法从 URL 中提取 file_key")
    
    def get_file_data(self, file_key: str) -> Dict:
        """获取 Figma 文件数据"""
        url = f"{self.base_url}/files/{file_key}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"API 请求失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    def find_top_level_frames(self, node: Dict) -> List[Dict]:
        """找出所有顶层 Frame（没有父级的 Frame）"""
        top_level_frames = []
        
        def traverse(node: Dict, parent_id: str = None):
            if node.get("type") == "FRAME":
                # 如果没有父级，就是顶层 Frame
                if parent_id is None:
                    top_level_frames.append({
                        "id": node["id"],
                        "name": node.get("name", "未命名"),
                        "size": node.get("absoluteBoundingBox", {})
                    })
                
                # 继续遍历子节点，传递当前 Frame ID 作为父级
                if "children" in node:
                    for child in node["children"]:
                        traverse(child, node["id"])
            else:
                # 不是 Frame，但继续遍历子节点
                if "children" in node:
                    for child in node["children"]:
                        traverse(child, parent_id)
        
        traverse(node)
        return top_level_frames
    
    def find_prototype_connections(self, node: Dict, top_level_frames: List[Dict]) -> List[Dict]:
        """找出所有 prototype 连接"""
        connections = []
        
        def traverse(node: Dict, current_page_id: str = None):
            node_id = node.get("id")
            node_name = node.get("name", "未命名")
            node_type = node.get("type")
            
            # 检查当前节点是否是顶层 Frame
            if node.get("type") == "FRAME":
                for frame in top_level_frames:
                    if frame["id"] == node_id:
                        current_page_id = node_id
                        break
            
            # 检查当前节点是否有交互
            if "interactions" in node and node["interactions"]:
                for interaction in node["interactions"]:
                    if (interaction.get("actions") and 
                        len(interaction["actions"]) > 0 and 
                        interaction["actions"][0].get("type") == "NODE"):
                        
                        action = interaction["actions"][0]
                        destination_id = action.get("destinationId")
                        trigger_type = interaction.get("trigger", {}).get("type", "未知")
                        
                        if destination_id and current_page_id:
                            # 找到目标页面 - 从根节点开始搜索
                            target_page_id = self._find_page_for_node(destination_id, self.root_node, top_level_frames)
                            
                            if target_page_id:
                                connections.append({
                                    "source_page_id": current_page_id,
                                    "source_page_name": self._get_frame_name(current_page_id, top_level_frames),
                                    "source_element_id": node_id,
                                    "source_element_name": node_name,
                                    "source_element_type": node_type,
                                    "target_page_id": target_page_id,
                                    "target_page_name": self._get_frame_name(target_page_id, top_level_frames),
                                    "interaction_type": trigger_type,
                                    "transition": action.get("transition")
                                })
            
            # 递归处理子节点
            if "children" in node:
                for child in node["children"]:
                    traverse(child, current_page_id)
        
        traverse(node)
        return connections
    
    def _find_page_for_node(self, node_id: str, root_node: Dict, top_level_frames: List[Dict]) -> Optional[str]:
        """为节点找到所属的页面"""
        def search_recursive(node: Dict, target_id: str, page_stack: List[str] = None) -> Optional[str]:
            if page_stack is None:
                page_stack = []
            
            # 如果当前节点是顶层 Frame，添加到栈中
            if node.get("type") == "FRAME":
                for frame in top_level_frames:
                    if frame["id"] == node["id"]:
                        page_stack.append(node["id"])
                        break
            
            if node.get("id") == target_id:
                # 返回最近的页面级 Frame
                return page_stack[-1] if page_stack else None
            
            if "children" in node:
                for child in node["children"]:
                    result = search_recursive(child, target_id, page_stack.copy())
                    if result:
                        return result
            
            return None
        
        return search_recursive(root_node, node_id)
    
    def _get_frame_name(self, frame_id: str, top_level_frames: List[Dict]) -> str:
        """根据 Frame ID 获取 Frame 名称"""
        for frame in top_level_frames:
            if frame["id"] == frame_id:
                return frame["name"]
        return "未知页面"
    
    def generate_enhanced_flow(self, figma_url: str) -> Dict:
        """生成增强版的用户流程"""
        print("🚀 开始提取增强版用户流程...")
        
        # 1. 提取 file_key
        file_key = self.extract_file_key_from_url(figma_url)
        print(f"📁 提取到 file_key: {file_key}")
        
        # 2. 获取文件数据
        print("📥 正在获取 Figma 文件数据...")
        file_data = self.get_file_data(file_key)
        self.root_node = file_data["document"]  # 保存根节点引用
        
        # 3. 找出顶层 Frame
        print("🏠 正在识别顶层 Frame...")
        top_level_frames = self.find_top_level_frames(file_data["document"])
        print(f"✅ 找到 {len(top_level_frames)} 个顶层 Frame")
        
        # 4. 找出所有 prototype 连接
        print("🔗 正在分析 Prototype 连接...")
        connections = self.find_prototype_connections(file_data["document"], top_level_frames)
        print(f"✅ 找到 {len(connections)} 个页面间交互")
        
        # 5. 生成结果
        result = {
            "file_key": file_key,
            "top_level_frames": top_level_frames,
            "connections": connections,
            "summary": {
                "total_pages": len(top_level_frames),
                "total_interactions": len(connections)
            }
        }
        
        return result
    
    def generate_clear_description(self, connections: List[Dict]) -> str:
        """生成清晰的用户流程描述"""
        descriptions = []
        
        for connection in connections:
            source_page = connection["source_page_name"]
            target_page = connection["target_page_name"]
            element_name = connection["source_element_name"]
            element_type = connection["source_element_type"]
            
            # 简单的原始数据描述
            description = f"从「{source_page}」的「{element_name}」({element_type})跳转到「{target_page}」"
            descriptions.append(description)
        
        return "\n".join(descriptions)
    
    def generate_mermaid_enhanced(self, connections: List[Dict]) -> str:
        """生成增强版的 Mermaid 流程图"""
        mermaid_lines = ["graph TD"]
        
        for connection in connections:
            source_page = connection["source_page_name"]
            target_page = connection["target_page_name"]
            element_name = connection["source_element_name"]
            
            # 使用原始名称，只清理空格和下划线
            source_clean = source_page.replace(" ", "_").replace("-", "_")
            target_clean = target_page.replace(" ", "_").replace("-", "_")
            
            # 生成连接
            mermaid_lines.append(f'  {source_clean}["{source_page}"] -->|{element_name}| {target_clean}["{target_page}"]')
        
        return "\n".join(mermaid_lines)

def main():
    # 从配置文件导入 token
    try:
        from config import FIGMA_ACCESS_TOKEN
    except ImportError:
        print("❌ 无法导入配置文件")
        return
    
    if FIGMA_ACCESS_TOKEN == "your_figma_access_token_here":
        print("❌ 请先配置 Figma Access Token")
        return
    
    # Figma 文件 URL
    figma_url = "https://www.figma.com/design/godMThppE6FPSSwsgR15Mu/Untitled?node-id=1-2&p=f&t=QJ8hSrQ5D9TF3XkX-0"
    
    try:
        extractor = EnhancedFigmaJourneyExtractor(FIGMA_ACCESS_TOKEN)
        result = extractor.generate_enhanced_flow(figma_url)
        
        # 生成清晰的描述
        print("\n" + "="*60)
        print("📝 清晰的用户流程描述:")
        print("="*60)
        descriptions = extractor.generate_clear_description(result["connections"])
        print(descriptions)
        
        # 生成增强版 Mermaid 图
        print("\n" + "="*60)
        print("📊 增强版 Mermaid 流程图:")
        print("="*60)
        mermaid_result = extractor.generate_mermaid_enhanced(result["connections"])
        print(mermaid_result)
        
        # 保存结果
        enhanced_result = {
            "descriptions": descriptions,
            "mermaid": mermaid_result,
            "connections": result["connections"]
        }
        
        with open("enhanced_user_journey.json", "w", encoding="utf-8") as f:
            json.dump(enhanced_result, f, ensure_ascii=False, indent=2)
        
        with open("enhanced_user_journey.md", "w", encoding="utf-8") as f:
            f.write("# 增强版用户流程图\n\n")
            f.write("## 📝 用户流程描述\n\n")
            f.write(descriptions)
            f.write("\n\n## 📊 Mermaid 流程图\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_result)
            f.write("\n```\n")
        
        print(f"\n✅ 增强版结果已保存到:")
        print(f"   - enhanced_user_journey.json")
        print(f"   - enhanced_user_journey.md")
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")

if __name__ == "__main__":
    main() 