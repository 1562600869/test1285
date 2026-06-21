from datetime import datetime
import data_manager


def add_lawyer(lawyer_id, name, phone, specialty, status):
    data = data_manager.load_data()

    if not data_manager.validate_legal_type(specialty):
        return False, f"专长类型无效，必须是以下之一：{', '.join(data_manager.LEGAL_TYPES)}"

    if not data_manager.validate_status(status):
        return False, f"状态无效，必须是以下之一：{', '.join(data_manager.LAWYER_STATUSES)}"

    if data_manager.lawyer_exists(data, lawyer_id):
        return False, f"律师 ID {lawyer_id} 已存在"

    data["lawyers"][lawyer_id] = {
        "id": lawyer_id,
        "name": name,
        "phone": phone,
        "specialty": specialty,
        "status": status
    }

    data_manager.save_data(data)
    return True, f"成功添加律师：{name}（{lawyer_id}）"


def add_schedule(lawyer_id, date, slot):
    data = data_manager.load_data()

    if not data_manager.is_valid_date(date):
        return False, "日期格式错误，应为 YYYY-MM-DD"

    if not data_manager.validate_time_slot(slot):
        return False, f"时段无效，必须是以下之一：{', '.join(data_manager.TIME_SLOTS)}"

    if not data_manager.lawyer_exists(data, lawyer_id):
        return False, f"律师 ID {lawyer_id} 不存在"

    if not data_manager.lawyer_is_active(data, lawyer_id):
        return False, f"律师 {lawyer_id} 当前非在职状态，无法排班"

    if data_manager.has_duplicate_schedule(data, lawyer_id, date, slot):
        return False, f"该律师在 {date} {slot} 已有排班"

    if data_manager.count_same_slot_count(data, date, slot) >= 3:
        return False, f"{date} {slot} 最多只能有 3 名律师排班"

    data["schedules"].append({
        "lawyer_id": lawyer_id,
        "date": date,
        "slot": slot
    })

    data_manager.save_data(data)
    lawyer = data_manager.get_lawyer(data, lawyer_id)
    return True, f"成功排班：{lawyer['name']}（{lawyer_id}）- {date} {slot}"


def add_consult(lawyer_id, date, slot, client, phone, ctype):
    data = data_manager.load_data()

    if not data_manager.is_valid_date(date):
        return False, "日期格式错误，应为 YYYY-MM-DD"

    if not data_manager.validate_time_slot(slot):
        return False, f"时段无效，必须是以下之一：{', '.join(data_manager.TIME_SLOTS)}"

    if not data_manager.validate_legal_type(ctype):
        return False, f"咨询类型无效，必须是以下之一：{', '.join(data_manager.LEGAL_TYPES)}"

    if not data_manager.lawyer_exists(data, lawyer_id):
        return False, f"律师 ID {lawyer_id} 不存在"

    if not data_manager.has_schedule(data, lawyer_id, date, slot):
        return False, f"律师 {lawyer_id} 在 {date} {slot} 无排班，无法接受咨询"

    data["consults"].append({
        "lawyer_id": lawyer_id,
        "date": date,
        "slot": slot,
        "client": client,
        "phone": phone,
        "type": ctype
    })

    data_manager.save_data(data)
    lawyer = data_manager.get_lawyer(data, lawyer_id)
    return True, f"咨询记录已保存：{client} → {lawyer['name']}（{date} {slot}）- {ctype}"


def monthly_stats(month):
    data = data_manager.load_data()

    if not data_manager.is_valid_month(month):
        return False, "月份格式错误，应为 YYYY-MM"

    stats = {t: 0 for t in data_manager.LEGAL_TYPES}
    for c in data["consults"]:
        if c["date"].startswith(month + "-"):
            ct = c["type"]
            if ct in stats:
                stats[ct] += 1

    lines = [f"==== {month} 月咨询统计 ===="]
    for t in data_manager.LEGAL_TYPES:
        lines.append(f"{t}: {stats[t]} 次")
    total = sum(stats.values())
    lines.append(f"合计: {total} 次")

    return True, "\n".join(lines)


def lawyer_record(lawyer_id):
    data = data_manager.load_data()

    if not data_manager.lawyer_exists(data, lawyer_id):
        return False, f"律师 ID {lawyer_id} 不存在"

    now = datetime.now()
    current_month = now.strftime("%Y-%m")
    lawyer = data_manager.get_lawyer(data, lawyer_id)

    schedule_count = 0
    for s in data["schedules"]:
        if s["lawyer_id"] == lawyer_id and s["date"].startswith(current_month + "-"):
            schedule_count += 1

    consult_count = 0
    for c in data["consults"]:
        if c["lawyer_id"] == lawyer_id and c["date"].startswith(current_month + "-"):
            consult_count += 1

    lines = [f"==== {lawyer['name']}（{lawyer_id}）本月记录 ===="]
    lines.append(f"排班次数: {schedule_count} 次")
    lines.append(f"接待咨询次数: {consult_count} 次")

    return True, "\n".join(lines)
