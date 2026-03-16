"""
修复脚本 v2：补全已入库题目的缺失字段
使用更宽松的内容匹配方式
"""
from sqlalchemy import text
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def fix_existing_questions():
    """补全已入库题目的缺失字段"""
    print("=" * 80)
    print("补全已入库题目的缺失字段 (v2)")
    print("=" * 80)
    
    with engine.connect() as conn:
        # 首先获取所有 AI 生成的题目
        print("\n1. 获取所有 AI 生成的题目和生成题目...")
        
        # 获取所有 generated_questions
        gq_result = conn.execute(text("""
            SELECT id, content, design_reason, difficulty_reason, distractor_reasons
            FROM generated_questions
            ORDER BY id DESC
        """))
        gq_list = list(gq_result)
        print(f"   找到 {len(gq_list)} 条 generated_questions")
        
        # 获取所有 AI 生成的 questions
        q_result = conn.execute(text("""
            SELECT id, content, design_reason, difficulty_reason, distractor_reasons, generated_question_id
            FROM questions
            WHERE source = 'AI生成'
            ORDER BY id DESC
        """))
        q_list = list(q_result)
        print(f"   找到 {len(q_list)} 条 AI 生成的 questions")
        
        # 创建 content 到 gq 的映射（使用简化的内容进行匹配）
        def simplify_content(c):
            if not c:
                return ""
            # 去除空格、换行、LaTeX 标记等，只保留核心内容
            import re
            c = re.sub(r'\s+', '', c)
            c = re.sub(r'\\[\w]+', '', c)
            c = re.sub(r'[\$\{\}]', '', c)
            return c[:100]
        
        gq_map = {}
        for gq in gq_list:
            gq_id, gq_content, dr, diffr, distr = gq
            simplified = simplify_content(gq_content)
            if simplified:
                gq_map[simplified] = (gq_id, dr, diffr, distr)
        
        print(f"\n2. 开始匹配和修复...")
        fixed_count = 0
        
        for q in q_list:
            q_id, q_content, q_dr, q_diffr, q_distr, q_gq_id = q
            
            # 检查是否已经需要修复
            needs_fix = (q_dr is None or q_diffr is None or q_distr is None or q_gq_id is None)
            
            if not needs_fix:
                continue
            
            # 尝试匹配
            simplified_q = simplify_content(q_content)
            matched = False
            
            if simplified_q in gq_map:
                gq_id, dr, diffr, distr = gq_map[simplified_q]
                # 更新题目
                conn.execute(text("""
                    UPDATE questions 
                    SET design_reason = :design_reason,
                        difficulty_reason = :difficulty_reason,
                        distractor_reasons = :distractor_reasons,
                        generated_question_id = :generated_question_id
                    WHERE id = :question_id
                """), {
                    "design_reason": dr,
                    "difficulty_reason": diffr,
                    "distractor_reasons": distr,
                    "generated_question_id": gq_id,
                    "question_id": q_id
                })
                fixed_count += 1
                matched = True
                print(f"   已修复题目 ID: {q_id} (关联 generated_question ID: {gq_id})")
            
            if not matched:
                # 尝试模糊匹配
                for gq in gq_list:
                    gq_id, gq_content, dr, diffr, distr = gq
                    if q_content and gq_content and q_content[:50] == gq_content[:50]:
                        # 更新题目
                        conn.execute(text("""
                            UPDATE questions 
                            SET design_reason = :design_reason,
                                difficulty_reason = :difficulty_reason,
                                distractor_reasons = :distractor_reasons,
                                generated_question_id = :generated_question_id
                            WHERE id = :question_id
                        """), {
                            "design_reason": dr,
                            "difficulty_reason": diffr,
                            "distractor_reasons": distr,
                            "generated_question_id": gq_id,
                            "question_id": q_id
                        })
                        fixed_count += 1
                        matched = True
                        print(f"   已修复题目 ID: {q_id} (模糊匹配，关联 generated_question ID: {gq_id})")
                        break
        
        conn.commit()
        
        # 验证修复结果
        print(f"\n3. 修复完成，共修复 {fixed_count} 条题目")
        print("\n4. 验证修复结果...")
        result = conn.execute(text("""
            SELECT id, design_reason, difficulty_reason, distractor_reasons, generated_question_id
            FROM questions 
            WHERE source = 'AI生成'
            ORDER BY id DESC 
            LIMIT 5
        """))
        
        for row in result:
            print(f"\n  题目 ID: {row[0]}")
            print(f"  design_reason: {'有值' if row[1] else 'NULL'}")
            print(f"  difficulty_reason: {'有值' if row[2] else 'NULL'}")
            print(f"  distractor_reasons: {'有值' if row[3] else 'NULL'}")
            print(f"  generated_question_id: {row[4]}")

if __name__ == "__main__":
    fix_existing_questions()
