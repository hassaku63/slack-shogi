
import re

from slackbot.bot import respond_to

from app.modules.shogi_input import ShogiInput
from app.modules.shogi_output import ShogiOutput
from app.slack_utils.user import User

@respond_to('start with <?@?([\d\w_-]+)>?')
def start_shogi(message, opponent_name):
    slacker = message._client.webapi
    user = User(slacker)

    channel_id = message.body["channel"]
    own_id = message.body["user"]
    opponent_id = user.username_to_id(opponent_name)
    if opponent_id is None:
        # In case of mention. In mention, slack transform username to userid like @username to <@UOIFJ83F>
        opponent_id = opponent_name

    if not user.user_in_channel(opponent_id, channel_id):
        message.reply("Error, sorry. Opponent is not found in this channel")
        return

    shogi = ShogiInput.init(channel_id=channel_id, users=[{
            "id": own_id,
            "name": user.id_to_username(own_id),
            }, {
            "id": opponent_id,
            "name": user.id_to_username(opponent_id),
        }
    ])

    if shogi is None:
        message.reply("Error, sorry")
    else:
        message.reply("Shogi started: " + shogi.id)
        board = ShogiInput.get_shogi_board(channel_id)
        board_str = ShogiOutput.make_board_emoji(board)
        message.send(board_str)

koma_names = [
    "歩",
    "歩兵",
    "と",
    "と金",
    "香",
    "香車",
    "桂",
    "桂馬",
    "銀",
    "銀将",
    "金",
    "金将",
    "角",
    "角行",
    "馬",
    "飛",
    "飛車",
    "龍",
    "王",
    "玉",
    "王将",
    "玉将",
]

koma_names += list(map(lambda n: "成"+n, koma_names))
koma_names_string_regex = "|".join(koma_names)

@respond_to("([一二三四五六七八九123456789１２３４５６７８９]{2})("+koma_names_string_regex+")([上右下左]{1,2})?(成)?")
def koma_move(message, position, koma, sub_position=None, promote=None):
    movement_str = "".join([x for x in [position, koma, sub_position, promote] if x is not None])
    channel_id = message.body["channel"]
    if not ShogiInput.exists(channel_id):
        message.reply("start withから初めてね")
        return
    own_id = message.body["user"]

    if ShogiInput.move(movement_str, channel_id, own_id):
        board = ShogiInput.get_shogi_board(channel_id)
        board_str = ShogiOutput.make_board_emoji(board)
        message.send(board_str)
    else:
        message.reply("You cannot move this!!")
        board = ShogiInput.get_shogi_board(channel_id)
        board_str = ShogiOutput.make_board_emoji(board)
        message.send(board_str)

@respond_to("今?.*の?.*状態.*を?教.*え?て?")
@respond_to("現局面.*")
@respond_to("局面.*")
@respond_to("board")
def board_info(message):
    channel_id = message.body["channel"]
    board = ShogiInput.get_shogi_board(channel_id)
    board_str = ShogiOutput.make_board_emoji(board)
    message.send(board_str)

@respond_to(".*降参.*")
@respond_to(".*resign.*")
@respond_to(".*負けました.*")
@respond_to(".*まけました.*")
@respond_to(".*まいりました.*")
@respond_to(".*参りました.*")
@respond_to(".*ありません.*")
def resign(message):
    channel_id = message.body["channel"]
    message.send("最終局面")
    board = ShogiInput.get_shogi_board(channel_id)
    board_str = ShogiOutput.make_board_emoji(board)
    message.send(board_str)
    ShogiInput.clear(channel_id)

