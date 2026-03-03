from flask import request, jsonify
from app import app, db
from app.models import KnowledgePoint, Question, Option, Tag, GenerationTask
import json
import openai
from config.config import Config

openai.api_key = Config.OPENAI_API_KEY

# 知识点管理API
@app.route('/api/knowledge-points', methods=['GET'])
def get_knowledge_points():
    points = KnowledgePoint.query.all()
    result = []
    for point in points:
        result.append({
            'id': point.id,
            'name': point.name,
            'parent_id': point.parent_id,
            'level': point.level
        })
    return jsonify(result)

# 题目管理API
@app.route('/api/questions', methods=['GET'])
def get_questions():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    status = request.args.get('status')
    
    query = Question.query
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.paginate(page=page, per_page=page_size, error_out=False)
    questions = pagination.items
    
    result = []
    for q in questions:
        options = Option.query.filter_by(question_id=q.id).order_by(Option.order_index).all()
        option_list = [{
            'id': opt.id,
            'content': opt.content,
            'is_correct': opt.is_correct
        } for opt in options]
        
        result.append({
            'id': q.id,
            'content': q.content,
            'question_type': q.question_type,
            'difficulty': q.difficulty,
            'status': q.status,
            'knowledge_point_id': q.knowledge_point_id,
            'explanation': q.explanation,
            'options': option_list,
            'tags': [tag.name for tag in q.tags]
        })
    
    return jsonify({
        'items': result,
        'total': pagination.total,
        'page': page,
        'page_size': page_size
    })

@app.route('/api/questions', methods=['POST'])
def create_question():
    data = request.json
    question = Question(
        content=data['content'],
        question_type=data['question_type'],
        difficulty=data['difficulty'],
        status=data.get('status', '草稿'),
        knowledge_point_id=data['knowledge_point_id'],
        explanation=data.get('explanation', '')
    )
    db.session.add(question)
    db.session.flush()
    
    # 添加选项
    if 'options' in data:
        for i, opt in enumerate(data['options']):
            option = Option(
                question_id=question.id,
                content=opt['content'],
                is_correct=opt.get('is_correct', False),
                order_index=i
            )
            db.session.add(option)
    
    # 添加标签
    if 'tags' in data:
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                question.tags.append(tag)
    
    db.session.commit()
    return jsonify({'id': question.id, 'message': '题目创建成功'})

@app.route('/api/questions/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': '题目不存在'}), 404
    
    data = request.json
    question.content = data.get('content', question.content)
    question.question_type = data.get('question_type', question.question_type)
    question.difficulty = data.get('difficulty', question.difficulty)
    question.status = data.get('status', question.status)
    question.knowledge_point_id = data.get('knowledge_point_id', question.knowledge_point_id)
    question.explanation = data.get('explanation', question.explanation)
    
    # 更新选项
    if 'options' in data:
        Option.query.filter_by(question_id=id).delete()
        for i, opt in enumerate(data['options']):
            option = Option(
                question_id=id,
                content=opt['content'],
                is_correct=opt.get('is_correct', False),
                order_index=i
            )
            db.session.add(option)
    
    # 更新标签
    if 'tags' in data:
        question.tags = []
        for tag_name in data['tags']:
            tag = Tag.query.filter_by(name=tag_name).first()
            if tag:
                question.tags.append(tag)
    
    db.session.commit()
    return jsonify({'message': '题目更新成功'})

@app.route('/api/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': '题目不存在'}), 404
    
    Option.query.filter_by(question_id=id).delete()
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': '题目删除成功'})

# AI生成题目API
@app.route('/api/ai/generate', methods=['POST'])
def generate_questions():
    data = request.json
    
    # 创建生成任务
    task = GenerationTask(
        knowledge_point_ids=','.join(map(str, data['knowledge_point_ids'])),
        question_types=','.join(data['question_types']),
        difficulty=data['difficulty'],
        question_count=data['question_count'],
        status='running'
    )
    db.session.add(task)
    db.session.commit()
    
    # 异步生成题目（这里简化处理，实际应该使用后台任务）
    generated_questions = []
    try:
        knowledge_point_names = [KnowledgePoint.query.get(kid).name for kid in data['knowledge_point_ids']]
        knowledge_points_str = ', '.join(knowledge_point_names)
        
        for i in range(data['question_count']):
            question_type = data['question_types'][i % len(data['question_types'])]
            
            # 构建详细的提示词
            prompt = f"""请为课程生成一道{data['difficulty']}难度的{question_type}题，要求如下：
            1. 知识点：{knowledge_points_str}
            2. 题目内容要清晰明确，符合课程教学要求
            3. 对于选择题，提供4个选项，其中只有一个正确答案
            4. 提供详细的解析，说明正确答案的依据和错误选项的原因
            5. 干扰项要基于常见误区
            6. 题目要结合实际应用场景
            
            请按照以下格式输出：
            题目：[题目内容]
            选项：
            A. [选项A]
            B. [选项B]
            C. [选项C]
            D. [选项D]
            正确答案：[A/B/C/D]
            解析：[详细解析]
            知识点对齐：[与哪些知识点相关]
            概念来源：[知识点来源章节]
            干扰项设计策略：[说明干扰项的设计思路]
            """
            
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            
            # 解析生成的题目
            question_data = response.choices[0].text.strip()
            
            # 提取题目各部分
            content = ""
            options = []
            correct_answer = ""
            explanation = ""
            knowledge_alignment = ""
            concept_source = ""
            distractor_strategy = ""
            
            # 简单解析（实际应用中需要更 robust 的解析）
            lines = question_data.split('\n')
            current_section = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('题目：'):
                    content = line[3:]
                    current_section = "content"
                elif line.startswith('选项：'):
                    current_section = "options"
                elif line.startswith('A. ') or line.startswith('B. ') or line.startswith('C. ') or line.startswith('D. '):
                    if current_section == "options":
                        option_content = line[3:]
                        is_correct = False
                        if correct_answer and line.startswith(correct_answer + '. '):
                            is_correct = True
                        options.append({"content": option_content, "is_correct": is_correct})
                elif line.startswith('正确答案：'):
                    correct_answer = line[5:]
                    # 更新选项的正确标记
                    for opt in options:
                        if opt['content'].strip() == line[5:].strip():
                            opt['is_correct'] = True
                elif line.startswith('解析：'):
                    explanation = line[3:]
                    current_section = "explanation"
                elif line.startswith('知识点对齐：'):
                    knowledge_alignment = line[6:]
                elif line.startswith('概念来源：'):
                    concept_source = line[6:]
                elif line.startswith('干扰项设计策略：'):
                    distractor_strategy = line[8:]
                elif current_section == "explanation" and line:
                    explanation += ' ' + line
            
            # 构建题目对象
            question = {
                'content': content,
                'question_type': question_type,
                'difficulty': data['difficulty'],
                'explanation': explanation,
                'options': options,
                'interpretability': {
                    'knowledge_alignment': knowledge_alignment,
                    'concept_source': concept_source,
                    'distractor_strategy': distractor_strategy,
                    'option_basis': '基于课程知识点和常见误区设计'
                }
            }
            
            generated_questions.append(question)
        
        task.status = 'completed'
        task.result = json.dumps(generated_questions)
    except Exception as e:
        task.status = 'failed'
        task.result = str(e)
    
    task.completed_at = db.func.current_timestamp()
    db.session.commit()
    
    return jsonify({'task_id': task.id, 'message': '题目生成任务已开始'})

@app.route('/api/ai/task/<int:id>', methods=['GET'])
def get_task_status(id):
    task = GenerationTask.query.get(id)
    if not task:
        return jsonify({'error': '任务不存在'}), 404
    
    result = {
        'id': task.id,
        'status': task.status,
        'created_at': task.created_at.isoformat(),
        'completed_at': task.completed_at.isoformat() if task.completed_at else None
    }
    
    if task.status == 'completed':
        result['questions'] = json.loads(task.result)
    
    return jsonify(result)

# 标签管理API
@app.route('/api/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    result = [{'id': tag.id, 'name': tag.name} for tag in tags]
    return jsonify(result)

# 题目审核API
@app.route('/api/questions/batch-update', methods=['POST'])
def batch_update_questions():
    data = request.json
    question_ids = data['ids']
    status = data['status']
    
    Question.query.filter(Question.id.in_(question_ids)).update({'status': status})
    db.session.commit()
    
    return jsonify({'message': f'成功更新{len(question_ids)}道题目的状态为{status}'})

# AI生成题目入库API
@app.route('/api/ai/questions/adopt', methods=['POST'])
def adopt_ai_questions():
    data = request.json
    questions = data['questions']
    
    adopted_count = 0
    for q_data in questions:
        # 创建题目
        question = Question(
            content=q_data['content'],
            question_type=q_data['question_type'],
            difficulty=q_data['difficulty'],
            status='已审核',
            knowledge_point_id=q_data.get('knowledge_point_id', 1),
            explanation=q_data['explanation']
        )
        db.session.add(question)
        db.session.flush()
        
        # 添加选项
        if 'options' in q_data:
            for i, opt in enumerate(q_data['options']):
                option = Option(
                    question_id=question.id,
                    content=opt['content'],
                    is_correct=opt.get('is_correct', False),
                    order_index=i
                )
                db.session.add(option)
        
        adopted_count += 1
    
    db.session.commit()
    return jsonify({'message': f'成功采纳并入库{adopted_count}道题目'})

# 题目分析API
@app.route('/api/analysis/knowledge-coverage', methods=['GET'])
def get_knowledge_coverage():
    # 计算知识点覆盖情况
    knowledge_points = KnowledgePoint.query.all()
    result = []
    
    for point in knowledge_points:
        question_count = Question.query.filter_by(knowledge_point_id=point.id).count()
        # 简单计算覆盖率（实际应用中需要更复杂的算法）
        coverage_rate = min(100, question_count * 10)
        
        point_data = {
            'id': point.id,
            'name': point.name,
            'parent_id': point.parent_id,
            'questionCount': question_count,
            'coverageRate': coverage_rate
        }
        result.append(point_data)
    
    # 构建树形结构
    def build_tree(nodes, parent_id=None):
        tree = []
        for node in nodes:
            if node['parent_id'] == parent_id:
                children = build_tree(nodes, node['id'])
                if children:
                    node['children'] = children
                tree.append(node)
        return tree
    
    tree = build_tree(result)
    return jsonify(tree)

@app.route('/api/analysis/difficulty-distribution', methods=['GET'])
def get_difficulty_distribution():
    # 计算难度分布
    difficulties = ['L1', 'L2', 'L3', 'L4', 'L5']
    distribution = {}
    
    for difficulty in difficulties:
        count = Question.query.filter_by(difficulty=difficulty).count()
        distribution[difficulty] = count
    
    return jsonify(distribution)

@app.route('/api/analysis/type-distribution', methods=['GET'])
def get_type_distribution():
    # 计算题型分布
    types = ['单选', '多选', '判断', '填空', '主观']
    distribution = {}
    
    for type in types:
        count = Question.query.filter_by(question_type=type).count()
        distribution[type] = count
    
    return jsonify(distribution)

@app.route('/api/analysis/usage-trend', methods=['GET'])
def get_usage_trend():
    # 模拟使用趋势数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月']
    usage = [120, 132, 101, 134, 90, 230]
    
    return jsonify({
        'months': months,
        'usage': usage
    })

# 健康检查
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})