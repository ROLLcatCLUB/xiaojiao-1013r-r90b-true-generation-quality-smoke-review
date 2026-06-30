from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "outputs" / "PREP_ROOM_RENDER_CANVAS_DEEPEN_V1"
STAGE = "1013R_R93_P5_TEACHER_EXECUTION_MAP_AND_CHILD_LANGUAGE_REPAIR"
OUT = BASE / STAGE

R93_P3_DIR = BASE / "1013R_R93_P3_CLASSROOM_FLOW_TEACHING_EPISODE_DEEPENING"
R93_P3_RUNBOOK = R93_P3_DIR / "r93_p3_teaching_episode_runbook.json"
R93_P3_VALIDATOR = R93_P3_DIR / "validate_1013R_R93_P3_classroom_flow_teaching_episode_deepening_result.json"

SCHEMA_OUT = OUT / "teacher_execution_map_schema_1013R_R93_P5.json"
MAP_MD_OUT = OUT / "r93_p5_teacher_execution_map.md"
MAP_JSON_OUT = OUT / "r93_p5_teacher_execution_map.json"
TALK_BANK_OUT = OUT / "r93_p5_child_language_teacher_talk_bank.md"
XIAOJIAO_CARDS_OUT = OUT / "r93_p5_xiaojiao_in_class_support_cards.md"
MICRO_MAPPING_OUT = OUT / "r93_p5_episode_micro_step_mapping.json"
HTML_OUT = OUT / "r93_p5_teacher_facing_execution_preview.html"
QUALITY_OUT = OUT / "quality_sentinel_v1_preview.json"
VALIDATOR_OUT = OUT / "validate_1013R_R93_P5_teacher_execution_map_child_language_result.json"

BOUNDARY = {
    "teacher_review_required": True,
    "preview_only": True,
    "provider_called": False,
    "model_called": False,
    "new_fields_added_to_profile": False,
    "profile_modified": False,
    "r21_modified": False,
    "r36_modified": False,
    "ui_page_connected": False,
    "formal_apply": False,
    "database_written": False,
    "feishu_written": False,
    "memory_written": False,
    "pptx_generated": False,
    "pdf_generated": False,
    "docx_generated": False,
    "printed_final_material_generated": False,
    "r95_executed": False,
    "multi_case_regression_executed": False,
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT)).replace("/", "\\")


def ul(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def md_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def step(
    order: int,
    name: str,
    action: str,
    say: str,
    screen: str,
    student: str,
    expected: str,
    scaffold: str,
    support: str,
    evidence: str,
    stuck: str,
    trigger: str,
) -> dict:
    return {
        "step_order": order,
        "step_name": name,
        "teacher_action": action,
        "teacher_say": say,
        "child_friendly_language_level": "三年级：短句、具体、先动作后概念",
        "screen_state": screen,
        "student_action": student,
        "expected_student_response": expected,
        "student_scaffold": scaffold,
        "xiaojiao_support": support,
        "evidence_check": evidence,
        "if_student_stuck": stuck,
        "next_step_trigger": trigger,
    }


def build_schema() -> dict:
    return {
        "schema_id": "teacher_execution_map_schema_1013R_R93_P5",
        "status": "preview_only",
        "description": "A teacher-facing execution map that decomposes teaching episodes into classroom micro-steps with child-friendly teacher talk.",
        "micro_step_required_keys": [
            "step_order",
            "step_name",
            "teacher_action",
            "teacher_say",
            "child_friendly_language_level",
            "screen_state",
            "student_action",
            "expected_student_response",
            "student_scaffold",
            "xiaojiao_support",
            "evidence_check",
            "if_student_stuck",
            "next_step_trigger",
        ],
        "language_layers": [
            "学生听得懂的话",
            "教师补充专业词",
            "教案书面表达",
        ],
        "boundary": BOUNDARY,
    }


def build_execution_map() -> dict:
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "lesson": {
            "title": "色彩的渐变",
            "grade": "三年级",
            "unit": "第二单元《多彩的世界》",
            "status": "TEACHER_EXECUTION_MAP_READY",
            "teacher_review_required": True,
            "preview_only": True,
            "formal_apply": False,
        },
        "execution_principles": [
            "教师先看到课堂动作，再展开支架和意图。",
            "每一步都要有学生动作和大屏或材料状态。",
            "先用儿童语言，再由教师轻轻补专业词。",
            "小教支持嵌入步骤，不作为旁白堆在最后。",
        ],
        "episodes": [
            {
                "episode_id": "episode_01_notice_gradient",
                "episode_type": "观察比较型",
                "title": "看见渐变",
                "language_layers": {
                    "student_friendly": ["颜色从哪里开始？", "慢慢变到哪里？", "用手指滑一滑。"],
                    "teacher_professional_bridge": "这种颜色一层一层慢慢变化，在美术里可以叫渐变。",
                    "lesson_plan_expression": "引导学生观察生活和教材图中的色彩连续变化，初步建立渐变感知。",
                },
                "xiaojiao_cards": {
                    "reminder": "先让学生指出起点和终点，不急着讲术语。",
                    "probe": "它是一下子跳过去，还是一层一层变过去？",
                    "misconception": "学生可能把颜色多当成渐变。",
                    "evidence": "记录能用“从___到___”表达变化方向的学生。",
                },
                "micro_steps": [
                    step(1, "打开图片，先静静看", "打开生活渐变图或教材图，给学生5秒安静观察。", "先别急着说颜色名字，看看颜色是从哪里慢慢变到哪里的。", "大屏显示三张图，每张图只保留一个箭头。", "安静看图，找一处颜色慢慢变化。", "学生能指出天空、山峦或花朵中的一处变化。", "不会说时先用手指，不要求完整句。", "提醒教师先看方向，不讲概念。", "学生眼睛能跟随箭头看变化。", "把图片减少到一张最明显的图。", "多数学生能找到一处变化后进入下一步。"),
                    step(2, "用手指出方向", "请学生用手指从起点滑到终点。", "请你用手指滑一滑，颜色从哪里开始，滑到哪里结束？", "大屏保留箭头，教师可圈起点和终点。", "用手指比划颜色变化方向。", "从深色滑到浅色；从蓝色滑到粉色。", "给起点贴一个小圆点，终点贴一个小旗。", "如果学生只说好看，提示追问从哪里到哪里。", "能指出起点和终点。", "教师示范一次手指滑动。", "至少2名学生能指出方向后进入表达。"),
                    step(3, "说一句从哪里到哪里", "让学生套用句式说一句。", "你可以这样说：我看到颜色从___变到___。", "大屏显示句式：从___到___。", "用句式说出一处变化。", "我看到颜色从蓝色变到粉色。", "句式板书保留在屏幕边角。", "给教师提示：不要纠结颜色名称是否精确。", "学生能说出完整或半完整句。", "让同桌先说，再请一名学生说。", "有学生能说出变化方向后进入比较。"),
                    step(4, "判断是不是慢慢变", "教师追问变化是否连续。", "它是一下子跳过去，还是中间一层一层慢慢变？", "大屏放大一处连续色带。", "判断“慢慢变”还是“跳过去”。", "它是一层一层变过去的。", "用“一层一层”替代“连续”术语。", "提醒教师把“颜色多”和“慢慢变”分开。", "学生能说出慢慢变的理由。", "对比一张颜色跳得很快的例子。", "学生能说慢慢变后进入概念桥接。"),
                    step(5, "轻轻引出渐变", "教师用学生语言引出“渐变”。", "这种颜色慢慢变过去，美术里可以叫渐变。今天我们就研究它。", "大屏出现课题：色彩的渐变。", "读课题，回到“颜色慢慢变过去”。", "渐变就是颜色慢慢变。", "课题旁写：渐变=慢慢变。", "提醒教师术语只出现一次，不展开理论。", "学生能把渐变和慢慢变联系起来。", "若学生记不住术语，保留慢慢变即可。", "学生理解课堂主题后进入亮暗/鲜灰辨析。"),
                ],
            },
            {
                "episode_id": "episode_02_distinguish_brightness_saturation",
                "episode_type": "概念辨析型",
                "title": "分清亮暗与鲜灰",
                "language_layers": {
                    "student_friendly": ["越来越亮", "越来越暗", "越来越鲜", "越来越灰"],
                    "teacher_professional_bridge": "亮不亮叫明度，鲜不鲜和纯度有关。",
                    "lesson_plan_expression": "引导学生用儿童化语言辨析明度与纯度变化，降低概念负荷。",
                },
                "xiaojiao_cards": {
                    "reminder": "先让学生分亮暗/鲜灰，再补明度/纯度。",
                    "probe": "你看的是亮不亮，还是鲜不鲜？",
                    "misconception": "学生可能把变浅和变灰混为一谈。",
                    "evidence": "记录能分类并说明理由的学生。",
                },
                "micro_steps": [
                    step(1, "出示两组色条", "左边放深浅色条，右边放鲜灰色条。", "这一页只看两件事：亮不亮，鲜不鲜。", "大屏左右两组色条，文字为亮暗/鲜灰。", "观察左右两组色条。", "左边越来越亮，右边越来越灰。", "用左右分区降低判断难度。", "提醒教师不要先讲定义。", "学生能看出两组不同。", "只保留一组色条先看亮暗。", "学生能说左右不同后进入分类。"),
                    step(2, "先判断亮暗", "指左侧色条，只问亮暗。", "这一组是越来越亮，还是越来越暗？", "左侧色条放大。", "举手或口头判断亮暗。", "越来越亮/越来越暗。", "给学生两个选项，不开放太多词。", "小教提示教师让学生先二选一。", "学生能用亮/暗判断。", "用黑白深浅卡替代彩色色条。", "大多数学生能判断后看鲜灰。"),
                    step(3, "再判断鲜灰", "指右侧色条，只问鲜灰。", "这一组是越来越鲜艳，还是越来越灰？", "右侧色条放大。", "判断鲜灰变化。", "越来越灰；没有那么鲜了。", "允许学生说“不鲜了”。", "提示教师接纳儿童话。", "学生能说鲜或灰。", "拿鲜艳色和灰色实物对比。", "学生能判断后进入分类活动。"),
                    step(4, "把色卡放进篮子", "请学生把色卡放到亮暗篮子或鲜灰篮子。", "这张卡更像亮暗变化，还是鲜灰变化？放到对应篮子里。", "大屏显示两个篮子：亮暗、鲜灰。", "拖动/贴卡/口头选择类别。", "这张是亮暗；这张是鲜灰。", "同桌先讨论再放。", "小教提醒教师追问选择理由。", "学生能分类并说出理由。", "不会分类时先问亮不亮，再问鲜不鲜。", "完成2-3张分类后桥接专业词。"),
                    step(5, "补专业词并收束", "教师将儿童话对应到美术词。", "美术里，亮不亮叫明度；鲜不鲜和纯度有关。我们先会看、会说就很好。", "板书：明度=亮暗；纯度=鲜灰。", "跟读关键词，不背定义。", "明度是亮暗，纯度和鲜灰有关。", "只保留等号式板书。", "提醒教师不要扩展色相等额外概念。", "学生能把专业词和儿童话连起来。", "如果学生负担大，只保留亮暗/鲜灰。", "学生会看会说后进入三格试色。"),
                ],
            },
            {
                "episode_id": "episode_03_three_step_color_trial",
                "episode_type": "示范试做型",
                "title": "三格试色",
                "language_layers": {
                    "student_friendly": ["让颜色排好队", "每次只变一点点", "第二格像第一格的朋友"],
                    "teacher_professional_bridge": "这种一格一格有规律的变化，可以形成明度或纯度渐变。",
                    "lesson_plan_expression": "通过三格小样训练学生控制渐变幅度，形成可迁移的色彩操作经验。",
                },
                "xiaojiao_cards": {
                    "reminder": "先做三格小样，不急着画完整作品。",
                    "probe": "第二格是不是一下子跑太远了？",
                    "misconception": "学生可能把三种不同颜色并排当成渐变。",
                    "evidence": "保存三格小样作为过程证据。",
                },
                "micro_steps": [
                    step(1, "拿出三格小样纸", "展示三格空框，说明今天先试一条小路。", "今天我们先不画大作品，先让颜色排好队。", "大屏显示三格空框和箭头。", "拿出三格小样纸或在学习单上找到三格。", "知道先做小样。", "三格框已印好，减少画框负担。", "提醒教师先控任务范围。", "学生找到三格位置。", "教师帮学生指认第1、2、3格。", "全班找到三格后开始第一格。"),
                    step(2, "画第一格", "示范把选好的颜色放入第一格。", "第一格先放一个你选好的颜色，别涂太厚，也别着急。", "第1格被涂上原色。", "在第一格涂色。", "第一格颜色比较稳定。", "可用彩铅/油画棒降低水分风险。", "提示教师关注材料控制。", "学生完成第一格。", "材料慢的学生可直接用色卡。", "大多数学生有第一格后进入第二格。"),
                    step(3, "画第二格", "示范第二格只做轻微变化。", "第二格不要跑太远，它要像第一格的朋友，只是亮一点或灰一点。", "第2格显示轻微变化，旁边写只变一点点。", "调出或选出第二格颜色。", "第二格比第一格略亮/略灰。", "给学生一句判断：像不像第一格的朋友？", "小教提醒教师看第二格是否跳太远。", "第二格与第一格关系接近。", "让学生把第二格调回接近第一格。", "第二格基本完成后进入第三格。"),
                    step(4, "画第三格", "示范第三格继续沿同方向变化。", "第三格继续慢慢变，不要一下子跳过去。", "第3格显示继续变化，箭头连起三格。", "完成第三格。", "三格能看出方向。", "保留箭头提醒变化方向。", "提示教师要求方向一致。", "学生三格有方向。", "让学生先说方向再改色。", "多数学生完成三格后看反例。"),
                    step(5, "对比跳色反例", "展示一组中间跳太快的三格。", "你看这一组第二格一下子跳太远了，像不像中间少了一步？", "大屏显示自然三格和跳色三格对比。", "判断哪一组更自然。", "左边更自然，右边跳太快。", "用“少了一步”解释断层。", "小教提示教师别批评学生，只说可以补一步。", "学生能识别跳色。", "让学生找哪一格需要靠近前一格。", "学生能说出问题后进入自查。"),
                    step(6, "学生试做自己的三格", "让学生独立完成一条三格路。", "现在你也试一条三格路，只要三格，先别急着画完整作品。", "大屏保留步骤：选颜色、三格、箭头。", "完成自己的三格小样。", "我做的是从___到___。", "基础做三格，进阶做五格。", "小教提示教师巡视起点、方向、中间格。", "学生有一组三格小样。", "卡住学生可用色卡排一排。", "学生完成小样后进入巡视判断。"),
                    step(7, "巡视并点拨", "教师巡视，只看三个点：起点、方向、中间是否跳。", "我先看三件事：从哪里开始，往哪里变，中间有没有跳太快。", "大屏显示三点自查。", "按三点检查自己的小样。", "能说起点、方向、中间格。", "用手指沿三格滑动检查。", "小教记录典型问题和可展示样本。", "教师能看到过程证据。", "时间不足时只保留三格和一句话。", "有可用小样后进入作品迁移。"),
                ],
            },
            {
                "episode_id": "episode_04_apply_to_artwork",
                "episode_type": "创作实践型",
                "title": "放进作品",
                "language_layers": {
                    "student_friendly": ["把颜色小路放进作品", "别人能看出方向", "不用画很复杂"],
                    "teacher_professional_bridge": "把渐变规律迁移到画面局部，形成有方向、有层次的色彩表现。",
                    "lesson_plan_expression": "引导学生将试色规律迁移到图形或小作品中，形成可见的渐变表达。",
                },
                "xiaojiao_cards": {
                    "reminder": "提醒教师分层发布任务，避免所有学生做复杂作品。",
                    "probe": "别人一眼能看出你的颜色往哪里变吗？",
                    "misconception": "学生可能追求复杂图案，忽略渐变规律。",
                    "evidence": "记录作品中能看出明确变化方向的学生样本。",
                },
                "micro_steps": [
                    step(1, "选择任务层级", "发布基础、进阶、挑战三类任务。", "你可以选适合自己的任务：色条、图形，或者小作品。今天最重要的是看得出颜色怎么变。", "大屏显示基础/进阶/挑战三栏。", "选择一个任务层级。", "我选基础/进阶/挑战。", "允许学生从基础做起。", "小教提醒教师不要让复杂图案抢走目标。", "学生能选定任务。", "选择困难时统一做基础色条。", "学生选定任务后标方向。"),
                    step(2, "先标变化方向", "要求学生先画箭头或心里确定方向。", "先别急着涂。你要先想：颜色从哪里开始，往哪里走？", "大屏显示起点、箭头、终点。", "在纸上轻轻标方向或口头说方向。", "从左到右；从里到外；从上到下。", "用箭头提示方向。", "小教提示教师先问方向再看颜色。", "学生能说出方向。", "让学生用手指在画面上滑一次。", "方向明确后迁移小样。"),
                    step(3, "把三格小样放进图形", "示范把小样规律放到一个形状里。", "刚才的小样不是结束，它是一条颜色小路。现在把这条小路放进你的图形里。", "大屏显示小样到图形的迁移箭头。", "把三格规律迁移到作品局部。", "我把渐变放在花瓣/山/圆形里。", "先放一小块，不要求整张画满。", "小教提醒教师看是否迁移了规律。", "作品中出现渐变局部。", "学生不会迁移时让他照着三格画一条色带。", "能迁移后进入创作。"),
                    step(4, "开始创作", "给学生安静创作时间，教师不频繁打断。", "现在给你一段安静时间。记住：不用画很多，先把一处渐变做清楚。", "大屏保留三点提醒：起点、方向、慢慢变。", "完成作品或局部设计。", "作品中有一处颜色慢慢变化。", "大屏提醒替代教师反复口头提醒。", "小教提示教师减少打断，保留巡视。", "学生进入持续创作。", "慢学生只完成局部即可。", "创作进行一段后巡视点拨。"),
                    step(5, "巡视抓三个点", "巡视时只看起点、方向、过渡。", "我来看看你的颜色从哪里开始，往哪里变，中间是不是太突然。", "大屏显示巡视三点。", "向教师说明自己的变化方向。", "从这里开始，往这里变。", "让学生用手指解释作品。", "小教生成个别追问：中间是不是跳太快？", "教师获得过程判断。", "如果方向不清，让学生加箭头或补一格。", "大部分作品有方向后同伴快看。"),
                    step(6, "同桌快看", "安排同桌只看一件事：方向清不清。", "同桌只帮看一件事：你能不能看出颜色往哪里变？", "大屏显示同桌提示句。", "同桌互看并指出方向。", "我看到它从___变到___。", "同伴只提一个点，避免干扰创作。", "小教提醒教师控制互评时间。", "同伴能指出或指出不清。", "看不出时让作者补一处过渡。", "同伴反馈后进入收束。"),
                    step(7, "收束到可展示样本", "选2-3个样本，不做大范围展示。", "我们先看几处颜色变化，不比谁画得最多，只看哪里变得清楚。", "大屏或实物投影展示局部。", "看样本，说出变化方向。", "这一处从___变到___。", "只展示局部，减少比较压力。", "小教记录可作为评价样本的作品。", "学生能从作品中看出渐变。", "时间不足时跳过全班展示，直接自查。", "选好样本后进入自查微修订。"),
                ],
            },
            {
                "episode_id": "episode_05_self_check_revision",
                "episode_type": "展示修订型",
                "title": "自查与微修订",
                "language_layers": {
                    "student_friendly": ["看一看", "说一说", "只改一处"],
                    "teacher_professional_bridge": "通过自评、同伴建议和微修订形成作品改进证据。",
                    "lesson_plan_expression": "组织学生依据评价要点进行自查、表达和局部修订，强化学习证据。",
                },
                "xiaojiao_cards": {
                    "reminder": "评价只抓一处微修，不做大评比。",
                    "probe": "改完以后，颜色变化更清楚了吗？",
                    "misconception": "学生可能以为评价就是重画一遍。",
                    "evidence": "记录修改前后或学习单自查勾选。",
                },
                "micro_steps": [
                    step(1, "打开三项自查", "出示自查三问。", "最后我们不急着评谁最好，先看自己有没有做到三件事。", "大屏显示：方向、慢慢变、能说清。", "看自己的小样或作品。", "能找到一处渐变。", "自查项不超过三条。", "小教提醒教师压缩评价维度。", "学生能进入自查。", "教师带全班一起读三问。", "学生知道查什么后进入同伴建议。"),
                    step(2, "同伴只提一处建议", "安排同伴用固定句式给建议。", "同桌只说一处：我看到___，我建议___。", "大屏显示同伴句式。", "给同伴一条建议。", "我看到这里变得清楚，我建议中间再浅一点。", "句式帮助学生避免泛泛说好看。", "小教提示教师控制为一条建议。", "学生能获得一条可改建议。", "如果不会说，只指出看不清的位置。", "每人收到一条建议后微修。"),
                    step(3, "选择一处微修", "要求学生只改一处。", "你只需要改一处，不用重画。让颜色变化更清楚就可以。", "大屏显示只改一处。", "选择一处修改。", "我改第二格/中间过渡/方向不清的地方。", "用圈画标出要改的位置。", "小教提醒教师防止学生重画。", "学生明确修改点。", "时间不足只口头说明要改哪里。", "学生确定修改点后动手。"),
                    step(4, "完成小修改", "给1-2分钟完成局部修改。", "改的时候想一想：它现在是不是更像慢慢变了？", "大屏保留自查三问。", "完成局部修订。", "颜色过渡更自然。", "允许很小的修改。", "小教记录典型微修案例。", "有可见修改或口头修改方案。", "材料不便时用铅笔箭头或文字说明替代。", "完成后说一说。"),
                    step(5, "说清修改并收课", "请学生说一处修改，教师连接下一课。", "你可以这样说：我改了___，因为原来___，现在___。", "大屏显示表达句式和下节课提示。", "说出修改原因。", "我改了中间一格，因为原来跳太快，现在更慢慢变了。", "用句式保护表达困难学生。", "小教记录能说清修改的学生。", "学生能说明修改与渐变有关。", "不会说完整句时只说改哪里。", "完成表达后收束到下节课“渐变的节奏”。"),
                ],
            },
        ],
        "boundary": BOUNDARY,
        "source_inputs": [rel(R93_P3_RUNBOOK)],
    }


def build_mapping(execution_map: dict) -> dict:
    rows = []
    for ep in execution_map["episodes"]:
        for micro in ep["micro_steps"]:
            rows.append(
                {
                    "episode_id": ep["episode_id"],
                    "episode_title": ep["title"],
                    "episode_type": ep["episode_type"],
                    "micro_step_order": micro["step_order"],
                    "micro_step_name": micro["step_name"],
                    "source_episode_fields": [
                        "teacher_moves",
                        "student_moves",
                        "screen_plan",
                        "student_scaffolds",
                        "xiaojiao_support",
                        "evidence",
                        "transition",
                    ],
                    "profile_fields_added": False,
                }
            )
    return {
        "stage": STAGE,
        "mapping_type": "episode_to_micro_step_execution_map",
        "micro_step_count": len(rows),
        "episode_count": len(execution_map["episodes"]),
        "profile_modified": False,
        "rows": rows,
    }


def render_md(execution_map: dict) -> str:
    parts = [
        "# 《色彩的渐变》教师课堂执行地图",
        "",
        "状态：教师审核草案；仅预览；不 formal apply。",
        "",
        "## 执行原则",
        md_list(execution_map["execution_principles"]),
    ]
    for ep_index, ep in enumerate(execution_map["episodes"], start=1):
        parts.extend([
            "",
            f"## {ep_index}. {ep['title']}（{ep['episode_type']}）",
            "",
            "### 语言三层",
            md_list([
                "学生听得懂的话：" + " / ".join(ep["language_layers"]["student_friendly"]),
                "教师补充专业词：" + ep["language_layers"]["teacher_professional_bridge"],
                "教案书面表达：" + ep["language_layers"]["lesson_plan_expression"],
            ]),
        ])
        for micro in ep["micro_steps"]:
            parts.extend([
                "",
                f"### {ep_index}.{micro['step_order']} {micro['step_name']}",
                f"- 教师动作：{micro['teacher_action']}",
                f"- 教师话术：{micro['teacher_say']}",
                f"- 大屏/材料：{micro['screen_state']}",
                f"- 学生动作：{micro['student_action']}",
                f"- 预期学生回应：{micro['expected_student_response']}",
                f"- 学生支架：{micro['student_scaffold']}",
                f"- 小教支持：{micro['xiaojiao_support']}",
                f"- 证据检查：{micro['evidence_check']}",
                f"- 卡住时：{micro['if_student_stuck']}",
                f"- 进入下一步条件：{micro['next_step_trigger']}",
            ])
    return "\n".join(parts) + "\n"


def render_talk_bank(execution_map: dict) -> str:
    parts = ["# 三年级儿童化教师话术库", "", "规则：短句、具体、可指向，先动作后概念。"]
    for ep_index, ep in enumerate(execution_map["episodes"], start=1):
        talks = [micro["teacher_say"] for micro in ep["micro_steps"]]
        parts.extend([
            "",
            f"## {ep_index}. {ep['title']}",
            "",
            "### 学生听得懂的话",
            md_list(ep["language_layers"]["student_friendly"]),
            "",
            "### 可直接说出口的话术",
            md_list(talks),
            "",
            "### 教师补充专业词",
            f"- {ep['language_layers']['teacher_professional_bridge']}",
            "",
            "### 教案书面表达",
            f"- {ep['language_layers']['lesson_plan_expression']}",
        ])
    return "\n".join(parts) + "\n"


def render_xiaojiao_cards(execution_map: dict) -> str:
    parts = ["# 小教课中支持卡", "", "小教只做提示、追问、误区提醒和证据记录建议；本轮不接真实 UI。"]
    for ep_index, ep in enumerate(execution_map["episodes"], start=1):
        cards = ep["xiaojiao_cards"]
        parts.extend([
            "",
            f"## {ep_index}. {ep['title']}",
            f"- 小教提醒：{cards['reminder']}",
            f"- 小教追问：{cards['probe']}",
            f"- 小教误区提醒：{cards['misconception']}",
            f"- 小教证据记录建议：{cards['evidence']}",
        ])
    return "\n".join(parts) + "\n"


def render_html(execution_map: dict) -> str:
    nav = "".join(
        f"<a href=\"#{esc(ep['episode_id'])}\">{i}. {esc(ep['title'])}</a>"
        for i, ep in enumerate(execution_map["episodes"], start=1)
    )
    sections = []
    for ep_index, ep in enumerate(execution_map["episodes"], start=1):
        steps_html = []
        for micro in ep["micro_steps"]:
            steps_html.append(f"""
              <section class="micro-step">
                <div class="step-heading">
                  <h3>{ep_index}.{micro['step_order']} {esc(micro['step_name'])}</h3>
                  <details>
                    <summary>大屏 / 支架 / 小教 / 证据</summary>
                    <div class="detail-body">
                  <p><b>大屏 / 材料：</b>{esc(micro['screen_state'])}</p>
                  <p><b>预期回应：</b>{esc(micro['expected_student_response'])}</p>
                  <p><b>学生支架：</b>{esc(micro['student_scaffold'])}</p>
                  <p><b>小教支持：</b>{esc(micro['xiaojiao_support'])}</p>
                  <p><b>证据检查：</b>{esc(micro['evidence_check'])}</p>
                  <p><b>卡住时：</b>{esc(micro['if_student_stuck'])}</p>
                    </div>
                </details>
                </div>
                <p class="step-line"><span class="role-icon teacher-icon">师</span>{esc(micro['teacher_action'])}</p>
                <p class="step-line talk-line"><span class="role-icon talk-icon">话</span>{esc(micro['teacher_say'])}</p>
                <p class="step-line"><span class="role-icon student-icon">生</span>{esc(micro['student_action'])}</p>
                <p class="step-line next-line"><span class="role-icon next-icon">进</span>{esc(micro['next_step_trigger'])}</p>
              </section>
            """)
        sections.append(f"""
          <article class="episode" id="{esc(ep['episode_id'])}">
            <p class="episode-type">{esc(ep['episode_type'])}</p>
            <h2>{ep_index}. {esc(ep['title'])}</h2>
            <div class="language-box">
              <p><b>学生话：</b>{esc(' / '.join(ep['language_layers']['student_friendly']))}</p>
              <p><b>教师补专业词：</b>{esc(ep['language_layers']['teacher_professional_bridge'])}</p>
            </div>
            {''.join(steps_html)}
          </article>
        """)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>《色彩的渐变》教师课堂执行地图</title>
  <style>
    :root {{
      --ink: #263238;
      --muted: #67757d;
      --line: #d9e2df;
      --paper: #fbfcfa;
      --green: #3f6f5e;
      --mint: #e4f1ec;
      --sun: #f6e8b7;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      line-height: 1.68;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 2;
      background: rgba(255,255,255,.96);
      border-bottom: 1px solid var(--line);
      padding: 22px 28px 14px;
    }}
    .head-inner, main {{ max-width: 980px; margin: 0 auto; }}
    h1 {{ margin: 0; font-size: clamp(30px, 5vw, 54px); line-height: 1.08; letter-spacing: 0; }}
    .subtitle {{ margin: 10px 0 0; color: var(--muted); }}
    nav {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 16px; }}
    nav a {{ color: var(--green); text-decoration: none; font-weight: 700; border-bottom: 2px solid #bdd7ce; }}
    main {{ padding: 28px 28px 78px; }}
    .principles {{
      border-top: 2px solid var(--ink);
      border-bottom: 1px solid var(--line);
      padding: 18px 0;
      margin-bottom: 30px;
    }}
    .principles h2 {{ margin: 0 0 8px; }}
    .principles ul {{ margin: 0; padding-left: 20px; }}
    .episode {{
      border-top: 1px solid var(--line);
      padding: 34px 0;
    }}
    .episode-type {{
      color: var(--green);
      font-weight: 700;
      margin: 0 0 6px;
    }}
    .episode h2 {{ margin: 0 0 12px; font-size: 32px; }}
    .language-box {{
      background: var(--mint);
      border: 1px solid #c6ddd5;
      padding: 14px 16px;
      margin-bottom: 18px;
    }}
    .language-box p {{ margin: 4px 0; }}
    .micro-step {{
      border-left: 3px solid var(--line);
      padding: 10px 0 10px 16px;
      margin: 8px 0;
    }}
    .step-heading {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 5px;
    }}
    .micro-step h3 {{ margin: 0; font-size: 19px; }}
    .micro-step p {{ margin: 4px 0; }}
    .step-line {{
      padding-left: 30px;
      position: relative;
    }}
    .role-icon {{
      position: absolute;
      left: 0;
      top: 1px;
      display: inline-block;
      width: 20px;
      height: 20px;
      line-height: 18px;
      text-align: center;
      border: 1px solid var(--line);
      border-radius: 50%;
      font-size: 12px;
      font-weight: 700;
      color: var(--green);
      background: #fff;
    }}
    .talk-line {{ color: var(--ink); }}
    .student-icon {{ color: #4b6f91; }}
    .next-line {{ color: var(--muted); }}
    .next-icon {{ color: #8a6a2e; }}
    details {{
      display: inline-block;
      margin: 0;
    }}
    .step-heading details[open] {{
      flex-basis: 100%;
      display: block;
    }}
    summary {{
      cursor: pointer;
      color: var(--green);
      font-weight: 700;
      font-size: 12px;
      border-bottom: 1px dotted #9dbdb1;
      list-style-position: inside;
    }}
    .detail-body {{
      margin-top: 8px;
      padding: 8px 0 4px;
      border-top: 1px dashed #c7d5d0;
    }}
    details p {{ color: var(--muted); }}
    @media (max-width: 620px) {{
      header, main {{ padding-left: 16px; padding-right: 16px; }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="head-inner">
      <h1>《色彩的渐变》教师课堂执行地图</h1>
      <p class="subtitle">从“教学过程说明书”推进到“第一步、第二步、第三步”的课堂执行手册。</p>
      <nav>{nav}</nav>
    </div>
  </header>
  <main>
    <section class="principles">
      <h2>0. 执行原则</h2>
      <ul>{ul(execution_map['execution_principles'])}</ul>
    </section>
    {''.join(sections)}
  </main>
</body>
</html>
"""


def build_quality(execution_map: dict) -> dict:
    checks = {
        "episode_count": "PASS" if len(execution_map["episodes"]) == 5 else "FAIL",
        "micro_steps_each_episode": "PASS",
        "child_language_layers": "PASS",
        "xiaojiao_embedded": "PASS",
        "teacher_action_each_step": "PASS",
        "student_action_each_step": "PASS",
        "screen_state_each_step": "PASS",
        "evidence_each_step": "PASS",
    }
    for ep in execution_map["episodes"]:
        if len(ep["micro_steps"]) < 5:
            checks["micro_steps_each_episode"] = "FAIL"
        if ep["title"] in ["三格试色", "放进作品"] and len(ep["micro_steps"]) < 7:
            checks["micro_steps_each_episode"] = "FAIL"
        if not ep.get("language_layers"):
            checks["child_language_layers"] = "FAIL"
        if not ep.get("xiaojiao_cards"):
            checks["xiaojiao_embedded"] = "FAIL"
        for micro in ep["micro_steps"]:
            if not micro.get("teacher_action") or not micro.get("teacher_say"):
                checks["teacher_action_each_step"] = "FAIL"
            if not micro.get("student_action"):
                checks["student_action_each_step"] = "FAIL"
            if not micro.get("screen_state"):
                checks["screen_state_each_step"] = "FAIL"
            if not micro.get("evidence_check"):
                checks["evidence_each_step"] = "FAIL"
    result = "BASIC_USABLE" if all(v == "PASS" for v in checks.values()) else "NEEDS_RETRY"
    return {
        "stage": STAGE,
        "quality_sentinel_version": "v1_preview",
        "result": result,
        "allowed_conclusion": "TEACHER_EXECUTION_MAP_READY",
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply": False,
        "checks": checks,
    }


def validate(execution_map: dict, quality: dict) -> dict:
    errors: list[str] = []
    required_keys = [
        "step_order",
        "step_name",
        "teacher_action",
        "teacher_say",
        "child_friendly_language_level",
        "screen_state",
        "student_action",
        "expected_student_response",
        "student_scaffold",
        "xiaojiao_support",
        "evidence_check",
        "if_student_stuck",
        "next_step_trigger",
    ]
    if len(execution_map["episodes"]) != 5:
        errors.append("episode_count_not_5")
    for ep in execution_map["episodes"]:
        count = len(ep["micro_steps"])
        if count < 5:
            errors.append(f"{ep['episode_id']}_micro_steps_less_than_5")
        if ep["title"] in ["三格试色", "放进作品"] and count < 7:
            errors.append(f"{ep['episode_id']}_core_episode_micro_steps_less_than_7")
        for micro in ep["micro_steps"]:
            missing = [key for key in required_keys if not micro.get(key)]
            if missing:
                errors.append(f"{ep['episode_id']}_{micro.get('step_order')}_missing:" + ",".join(missing))
    if quality.get("result") not in ["BASIC_USABLE", "NEEDS_RETRY", "NOT_USABLE"]:
        errors.append("invalid_quality_result")
    p3_validator = read_json(R93_P3_VALIDATOR)
    if not p3_validator.get("validator_pass"):
        errors.append("r93_p3_validator_not_pass")
    html_text = HTML_OUT.read_text(encoding="utf-8") if HTML_OUT.exists() else ""
    for phrase in ["教师课堂执行地图", "step-heading", "role-icon teacher-icon", "role-icon student-icon", "role-icon next-icon", "大屏 / 支架 / 小教 / 证据"]:
        if phrase not in html_text:
            errors.append("execution_preview_missing:" + phrase)
    if html_text.count("<section class=\"micro-step\">") < 29:
        errors.append("html_micro_step_count_too_low")
    if any(
        BOUNDARY[key]
        for key in [
            "provider_called",
            "model_called",
            "new_fields_added_to_profile",
            "profile_modified",
            "r21_modified",
            "r36_modified",
            "ui_page_connected",
            "formal_apply",
            "database_written",
            "feishu_written",
            "memory_written",
            "pptx_generated",
            "pdf_generated",
            "docx_generated",
            "printed_final_material_generated",
            "r95_executed",
            "multi_case_regression_executed",
        ]
    ):
        errors.append("boundary_violation")
    return {
        "stage": STAGE,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": "PASS" if not errors else "FAIL",
        "teacher_execution_map_ready": not errors,
        "episode_count": len(execution_map["episodes"]),
        "micro_step_count": sum(len(ep["micro_steps"]) for ep in execution_map["episodes"]),
        "quality_sentinel_v1_preview_result": quality.get("result"),
        "teacher_review_required": True,
        "preview_only": True,
        "formal_apply": False,
        "provider_called": False,
        "model_called": False,
        "new_fields_added": False,
        "profile_modified": False,
        "r21_modified": False,
        "r36_modified": False,
        "ui_page_connected": False,
        "database_written": False,
        "feishu_written": False,
        "memory_written": False,
        "pptx_generated": False,
        "pdf_generated": False,
        "docx_generated": False,
        "r95_executed": False,
        "files": {
            "schema": rel(SCHEMA_OUT),
            "map_md": rel(MAP_MD_OUT),
            "map_json": rel(MAP_JSON_OUT),
            "talk_bank": rel(TALK_BANK_OUT),
            "xiaojiao_cards": rel(XIAOJIAO_CARDS_OUT),
            "micro_step_mapping": rel(MICRO_MAPPING_OUT),
            "html": rel(HTML_OUT),
            "quality": rel(QUALITY_OUT),
        },
        "sha256": {
            "html": sha256(HTML_OUT) if HTML_OUT.exists() else None,
            "map_json": sha256(MAP_JSON_OUT) if MAP_JSON_OUT.exists() else None,
        },
        "failed_checks": errors,
        "validator_pass": not errors,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    schema = build_schema()
    execution_map = build_execution_map()
    mapping = build_mapping(execution_map)
    quality = build_quality(execution_map)
    write_json(SCHEMA_OUT, schema)
    write_json(MAP_JSON_OUT, execution_map)
    write_text(MAP_MD_OUT, render_md(execution_map))
    write_text(TALK_BANK_OUT, render_talk_bank(execution_map))
    write_text(XIAOJIAO_CARDS_OUT, render_xiaojiao_cards(execution_map))
    write_json(MICRO_MAPPING_OUT, mapping)
    write_text(HTML_OUT, render_html(execution_map))
    write_json(QUALITY_OUT, quality)
    validation = validate(execution_map, quality)
    write_json(VALIDATOR_OUT, validation)
    print(json.dumps({
        "stage": STAGE,
        "validator_pass": validation["validator_pass"],
        "quality": quality["result"],
        "episode_count": validation["episode_count"],
        "micro_step_count": validation["micro_step_count"],
        "html": str(HTML_OUT),
        "html_sha256": validation["sha256"]["html"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
