#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版用户流程提取器
"""

from enhanced_flow_extractor import EnhancedFigmaJourneyExtractor
from config import FIGMA_ACCESS_TOKEN
import json

def generate_enhanced_flow():
    """生成增强版的用户流程描述"""
    print("🚀 生成增强版用户流程...")
    
    # 创建增强版提取器
    extractor = EnhancedFigmaJourneyExtractor(FIGMA_ACCESS_TOKEN)
    
    # Figma URL
    figma_url = "https://www.figma.com/design/godMThppE6FPSSwsgR15Mu/Untitled?node-id=1-2&p=f&t=QJ8hSrQ5D9TF3XkX-0"
    
    try:
        # 使用增强版提取器生成流程
        result = extractor.generate_enhanced_flow(figma_url)
        
        # 生成清晰的描述
        print(f"\n📝 清晰的用户流程描述:")
        print("="*60)
        descriptions = extractor.generate_clear_description(result["connections"])
        print(descriptions)
        
        # 生成增强版 Mermaid 图
        print(f"\n📊 增强版 Mermaid 流程图:")
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
    generate_enhanced_flow() 