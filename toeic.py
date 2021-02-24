import web_alarm as wa

json_data = wa.get_json()

wa.first_run_init(json_data)

new_board = wa.make_new_board(json_data)

if len(new_board) > 1:
    message = "새 토익알바가 올라왔습니다~ \n"
    for value, title in new_board.items():
        message += "{} : {}\n".format(value, title)
    wa.telegram_send(json_data, message)
