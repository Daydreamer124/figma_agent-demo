#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户流程故事描述生成器
使用LLM从JSON或Mermaid流程图生成自然语言的故事描述
"""

import json
import re
from typing import Dict, List, Any, Optional
import openai
from openai import OpenAI

class JourneyStoryGenerator:
    """用户流程故事生成器"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """
        初始化故事生成器
        
        Args:
            api_key: OpenAI API密钥
            model: 使用的模型名称
        """
        self.model = model
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # 尝试使用环境变量中的API密钥
            try:
                self.client = OpenAI()
            except Exception as e:
                print("⚠️ 未配置OpenAI API密钥，请设置环境变量OPENAI_API_KEY或传入api_key参数")
                self.client = None
    
    def load_from_json(self, json_file: str) -> Dict[str, Any]:
        """从JSON文件加载流程数据"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    def extract_flow_from_mermaid(self, mermaid_text: str) -> List[Dict[str, str]]:
        """从Mermaid文本提取流程信息"""
        flows = []
        lines = mermaid_text.strip().split('\n')
        
        for line in lines:
            if '-->' in line:
                # 解析 Mermaid 格式
                match = re.match(r'\s*(\w+)\["([^"]+)"\]\s*-->\|([^|]+)\|\s*(\w+)\["([^"]+)"\]', line)
                if match:
                    source_id, source_name, action, target_id, target_name = match.groups()
                    flows.append({
                        'from': source_name,
                        'action': action,
                        'to': target_name
                    })
        
        return flows
    
    def generate_story_from_json(self, json_data: Dict[str, Any]) -> str:
        """从JSON数据生成故事描述"""
        if not self.client:
            return "❌ LLM客户端未初始化"
        
        # 提取连接信息
        connections = json_data.get('connections', [])
        if not connections:
            return "❌ JSON数据中未找到连接信息"
        
        # 构建流程描述
        flow_description = self._build_flow_description_from_connections(connections)
        
        # 生成故事
        return self._generate_story_with_llm(flow_description, "JSON")
    
    def generate_story_from_mermaid(self, mermaid_text: str) -> str:
        """从Mermaid文本生成故事描述"""
        if not self.client:
            return "❌ LLM客户端未初始化"
        
        # 提取流程信息
        flows = self.extract_flow_from_mermaid(mermaid_text)
        if not flows:
            return "❌ Mermaid文本中未找到有效的流程信息"
        
        # 构建流程描述
        flow_description = self._build_flow_description_from_flows(flows)
        
        # 生成故事
        return self._generate_story_with_llm(flow_description, "Mermaid")
    
    def _build_flow_description_from_connections(self, connections: List[Dict[str, Any]]) -> str:
        """从连接数据构建流程描述"""
        flow_lines = []
        
        for conn in connections:
            source_page = conn.get('source_page_name', '未知页面')
            target_page = conn.get('target_page_name', '未知页面')
            action = conn.get('source_element_name', '未知操作')
            element_type = conn.get('source_element_type', '')
            
            flow_lines.append(f"从「{source_page}」通过「{action}」跳转到「{target_page}」")
        
        return "\n".join(flow_lines)
    
    def _build_flow_description_from_flows(self, flows: List[Dict[str, str]]) -> str:
        """从流程数据构建描述"""
        flow_lines = []
        
        for flow in flows:
            from_page = flow['from']
            to_page = flow['to']
            action = flow['action']
            
            flow_lines.append(f"从「{from_page}」通过「{action}」跳转到「{to_page}」")
        
        return "\n".join(flow_lines)
    
    def _generate_story_with_llm(self, flow_description: str, source_type: str) -> str:
        """使用LLM生成故事描述"""
        try:
            prompt = self._create_story_prompt(flow_description, source_type)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的用户体验设计师和故事叙述者。你擅长将技术性的用户流程图转换成生动、易懂的用户故事描述。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"❌ 生成故事时出错: {str(e)}"
    
    def _create_story_prompt(self, flow_description: str, source_type: str) -> str:
        """创建LLM提示词"""
        return f"""
请根据以下从{source_type}提取的用户流程信息，生成一个清晰、生动的用户故事描述。

用户流程信息：
{flow_description}

请按照以下要求生成故事描述：

1. **故事概述**：用1-2句话概括整个用户旅程的主要目标和流程
2. **关键流程步骤**：详细描述用户在各个页面间的操作流程，使用自然语言
对于用户流程信息的内容，不要进行任何的修改，直接生成故事描述（例如流程中的页面名称、操作名称等）。

输出格式：
# 📖 用户旅程故事

## 🎯 故事概述
[概述内容]

## 🚶‍♀️ 用户旅程步骤
[详细步骤描述]


"""

    def generate_story_from_file(self, file_path: str) -> str:
        """从文件生成故事（自动识别JSON或Mermaid格式）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # 判断文件类型
            if file_path.endswith('.json'):
                data = json.loads(content)
                return self.generate_story_from_json(data)
            elif 'graph TD' in content or 'flowchart' in content:
                return self.generate_story_from_mermaid(content)
            else:
                # 尝试解析为JSON
                try:
                    data = json.loads(content)
                    return self.generate_story_from_json(data)
                except:
                    return self.generate_story_from_mermaid(content)
                    
        except FileNotFoundError:
            return f"❌ 文件未找到: {file_path}"
        except Exception as e:
            return f"❌ 处理文件时出错: {str(e)}"

    def save_story_to_file(self, story: str, output_file: str = "journey_story.md"):
        """保存故事到文件"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(story)
            return f"✅ 故事已保存到: {output_file}"
        except Exception as e:
            return f"❌ 保存文件时出错: {str(e)}"


def main():
    """主函数 - 演示如何使用"""
    print("🤖 用户流程故事生成器")
    print("=" * 50)
    
    # 创建故事生成器（需要配置OpenAI API密钥）
    generator = JourneyStoryGenerator()
    
    if not generator.client:
        print("请先配置OpenAI API密钥：")
        print("1. 设置环境变量: export OPENAI_API_KEY='your-api-key'")
        print("2. 或者修改代码直接传入API密钥")
        return
    
    # 从JSON文件生成故事
    try:
        print("📊 正在从JSON文件生成故事...")
        story = generator.generate_story_from_file("enhanced_user_journey.json")
        print(story)
        
        # 保存故事
        save_result = generator.save_story_to_file(story)
        print(f"\n{save_result}")
        
    except Exception as e:
        print(f"❌ 生成故事失败: {e}")
        print("请确保存在 enhanced_user_journey.json 文件")


if __name__ == "__main__":
    main()