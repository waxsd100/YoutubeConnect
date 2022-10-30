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