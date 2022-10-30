from const import API_ENDPOINT


class SendServerClient:

    @staticmethod
    async def send_server(chat: dict, args):
        # print(chat)
        headers = {}
        id = chat["id"]
        user_id = chat["userId"]
        user_name = chat["data"]["author"]["name"]
        datetime = chat["data"]["datetime"]
        message = chat["data"]["message"]

        comment_data = {
            'id': id,
            'datetime': datetime,
            'user_id': user_id,
            'user_name': user_name,
            'message': message,
        }
        print(comment_data)
        response = args.post_json(url=f"{API_ENDPOINT}/send", headers=headers, data=comment_data)
        print(response.json())
        # response_id = response_json["id"]
        # send_text = parse_send_message(c.message)
        #
        # if send_text is None:
        #     # パースした結果全て空白だった場合送信しない
        #     print(f"[{c.datetime}] This message was not sent: {chat.author.name} {c.message}")
        #     continue
        # pass
        #
        # # 放送者判定
        # is_chat_owner = c.author.isVerified
        # # 公式バッチ持ち判定
        # is_verified = c.author.isVerified
        # # メンバーシップ判定
        # is_chat_sponsor = c.author.isVerified
        # # モデレーター判定
        # is_chat_moderator = c.author.isVerified
        #
        # user_name = replace_space_to_mcspace(c.author.name)
        # channel_name = replace_space_to_mcspace(cn)
        #
        # # Storageコマンド用Jsonを定義
        # command_data = json.dumps({
        #     'from': 'YouTube',
        #     'channel_id': cid,
        #     'channel_name': channel_name,
        #     'chat_type': c.type,
        #     'id': id,
        #     'name': user_name,
        #     'text': [send_text]
        # }, ensure_ascii=False)
        #
        # # 送信するコマンド内容を定義
        # # message = f"data modify storage mc_comment_viewer: new_comments append value {command_data}"
        # message = f"say {channel_name} [{user_name}]: {send_text}"
        #
        # # Gatewayへの送信データを定期
        # data = {"id": u_key, "dt": c.datetime, "video_id": vid, "channel_id": cid, "payload": message}
        #
        # # Gatewayへデータ送信
        # response = gw.post_json(f"{API_ENDPOINT}/", headers, data)
        # response_json = response.json()
        # response_id = response_json["id"]
        #
        # if u_key == response_id:
        #     if response.status_code == requests.codes.ok:
        #         # 成功時
        #         print(
        #             f"{response.status_code} [{c.datetime}] {u_key} {id} {c.type} {c.author.name}: {c.message} {c.amountString}")
        #     elif response.status_code == 400:
        #         # 送信したデータに異常がある
        #         print(f"{response.status_code} No send Message: {chat.author.name} / {chat.message}",
        #               file=sys.stderr)
        #     else:
        #         # サーバ上でexceptionが発生した
        #         print(f"{response.status_code} Gateway Server Error: {chat.author.name} / {chat.message}",
        #               file=sys.stderr)
        # else:
        #     # 送信したデータとレスポンスが一致していない(データ抜けの可能性)
        #     print(f"{response.status_code} Send ID is missmatch: {response_json}", file=sys.stderr)
