import argparse
import sys
import data_manager
import operations


def main():
    parser = argparse.ArgumentParser(
        description="社区法律援助站 - 律师排班与咨询记录管理工具"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    parser_add = subparsers.add_parser("add-lawyer", help="添加律师")
    parser_add.add_argument("lawyer_id", help="律师编号，如 L001")
    parser_add.add_argument("name", help="律师姓名")
    parser_add.add_argument("--phone", required=True, help="联系电话")
    parser_add.add_argument(
        "--specialty",
        required=True,
        choices=data_manager.LEGAL_TYPES,
        help=f"专长领域：{'/'.join(data_manager.LEGAL_TYPES)}"
    )
    parser_add.add_argument(
        "--status",
        required=True,
        choices=data_manager.LAWYER_STATUSES,
        help=f"在职状态：{'/'.join(data_manager.LAWYER_STATUSES)}"
    )

    parser_sched = subparsers.add_parser("schedule", help="排班")
    parser_sched.add_argument("lawyer_id", help="律师编号")
    parser_sched.add_argument("--date", required=True, help="排班日期 YYYY-MM-DD")
    parser_sched.add_argument(
        "--slot",
        required=True,
        choices=data_manager.TIME_SLOTS,
        help=f"时段：{'/'.join(data_manager.TIME_SLOTS)}"
    )

    parser_consult = subparsers.add_parser("consult", help="记录咨询")
    parser_consult.add_argument("--lawyer", required=True, dest="lawyer_id", help="律师编号")
    parser_consult.add_argument("--date", required=True, help="咨询日期 YYYY-MM-DD")
    parser_consult.add_argument(
        "--slot",
        required=True,
        choices=data_manager.TIME_SLOTS,
        help=f"时段：{'/'.join(data_manager.TIME_SLOTS)}"
    )
    parser_consult.add_argument("--client", required=True, help="当事人姓名")
    parser_consult.add_argument("--phone", required=True, help="当事人电话")
    parser_consult.add_argument(
        "--type",
        required=True,
        dest="ctype",
        choices=data_manager.LEGAL_TYPES,
        help=f"咨询类型：{'/'.join(data_manager.LEGAL_TYPES)}"
    )

    parser_stats = subparsers.add_parser("monthly-stats", help="月度咨询统计")
    parser_stats.add_argument("--month", required=True, help="统计月份 YYYY-MM")

    parser_record = subparsers.add_parser("lawyer-record", help="律师本月记录")
    parser_record.add_argument("lawyer_id", help="律师编号")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "add-lawyer":
        ok, msg = operations.add_lawyer(
            args.lawyer_id, args.name, args.phone,
            args.specialty, args.status
        )
    elif args.command == "schedule":
        ok, msg = operations.add_schedule(
            args.lawyer_id, args.date, args.slot
        )
    elif args.command == "consult":
        ok, msg = operations.add_consult(
            args.lawyer_id, args.date, args.slot,
            args.client, args.phone, args.ctype
        )
    elif args.command == "monthly-stats":
        ok, msg = operations.monthly_stats(args.month)
    elif args.command == "lawyer-record":
        ok, msg = operations.lawyer_record(args.lawyer_id)
    else:
        parser.print_help()
        sys.exit(1)

    print(msg)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
