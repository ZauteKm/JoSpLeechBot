import asyncio
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid, FloodWait
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

from tobrot.helper_funcs.torrent_search import SearchYTS, SearchAnime, Search1337x, SearchPirateBay

THUMBNAIL = "https://telegra.ph/file/4025673f818a5d0f73caf.png"

DEFAULT_SEARCH_MARKUP = [
                    [InlineKeyboardButton("Search YTS", switch_inline_query_current_chat="!yts "),
                     InlineKeyboardButton("Go Inline", switch_inline_query="!yts ")],
                    [InlineKeyboardButton("Search ThePirateBay", switch_inline_query_current_chat="!pb "),
                     InlineKeyboardButton("Go Inline", switch_inline_query="!pb ")],
                    [InlineKeyboardButton("Search 1337x", switch_inline_query_current_chat=""),
                     InlineKeyboardButton("Go Inline", switch_inline_query="")],
                    [InlineKeyboardButton("Search Anime", switch_inline_query_current_chat="!a "),
                     InlineKeyboardButton("Go Inline", switch_inline_query_current_chat="!a ")],
                    [InlineKeyboardButton("⭕ JOS Projects ⭕", url="https://t.me/JOSProjects")]
                ]

async def inline_handlers(_, inline: InlineQuery):
    search_ts = inline.query
    answers = []
    if search_ts == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Something ...",
                description="Search For Torrents ...",
                thumb_url=THUMBNAIL,
                input_message_content=InputTextMessageContent(
                    message_text="Search for Torrents from Inline!",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup(DEFAULT_SEARCH_MARKUP)
            )
        )
    elif search_ts.startswith("!pb"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!pb [text]",
                    description="Search For Torrent in ThePirateBay ...",
                    thumb_url=THUMBNAIL,
                    input_message_content=InputTextMessageContent(
                        message_text="`!pb [text]`\n\nSearch ThePirateBay Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pb ")]])
                )
            )
        else:
            torrentList = await SearchPirateBay(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found in ThePirateBay!",
                        description=f"Can't find torrents for {query} in ThePirateBay !!",
                        thumb_url=THUMBNAIL,
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Torrents Found For `{query}` in ThePirateBay !!",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pb ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}",
                            thumb_url=THUMBNAIL,
                            input_message_content=InputTextMessageContent(
                                message_text=f"`{torrentList[i]['Magnet']}`",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pb ")]])
                        )
                    )
    elif search_ts.startswith("!yts"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!yts [text]",
                    description="Search For Torrent in YTS ...",
                    thumb_url=THUMBNAIL,
                    input_message_content=InputTextMessageContent(
                        message_text="`!yts [text]`\n\nSearch YTS Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]])
                )
            )
        else:
            torrentList = await SearchYTS(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Torrents Found!",
                        description=f"Can't find YTS torrents for {query} !!",
                        thumb_url=THUMBNAIL,
                        input_message_content=InputTextMessageContent(
                            message_text=f"No YTS Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!yts ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    dl_links = "- " + "\n\n- ".join(torrentList[i]['Downloads'])
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Language: {torrentList[i]['Language']}\nLikes: {torrentList[i]['Likes']}, Rating: {torrentList[i]['Rating']}",
                            input_message_content=InputTextMessageContent(
                                message_text=f"{dl_links}",
                                parse_mode="Markdown",
                                disable_web_page_preview=True
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!yts ")]]),
                            thumb_url=torrentList[i]["Poster"]
                        )
                    )
    elif search_ts.startswith("!a"):
        query = search_ts.split(" ", 1)[-1]
        if (query == "") or (query == " "):
            answers.append(
                InlineQueryResultArticle(
                    title="!a [text]",
                    description="Search For Torrents for Anime ...",
                    thumb_url=THUMBNAIL,
                    input_message_content=InputTextMessageContent(
                        message_text="`!a [text]`\n\nSearch Anime Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!a ")]])
                )
            )
        else:
            torrentList = await SearchAnime(query)
            if not torrentList:
                answers.append(
                    InlineQueryResultArticle(
                        title="No Anime Torrents Found!",
                        description=f"Can't find Anime torrents for {query} !!",
                        thumb_url=THUMBNAIL,
                        input_message_content=InputTextMessageContent(
                            message_text=f"No Anime Torrents Found For `{query}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!a ")]])
                    )
                )
            else:
                for i in range(len(torrentList)):
                    answers.append(
                        InlineQueryResultArticle(
                            title=f"{torrentList[i]['Name']}",
                            description=f"Seeders: {torrentList[i]['Seeder']}, Leechers: {torrentList[i]['Leecher']}\nSize: {torrentList[i]['Size']}",
                            thumb_url=THUMBNAIL,
                            input_message_content=InputTextMessageContent(
                                message_text=f"`{torrentList[i]['Magnet']}`",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!a ")]]
                            )
                        )
                    )
    else:
        torrentList = await Search1337x(search_ts)
        if not torrentList:
            answers.append(
                InlineQueryResultArticle(
                    title="No Torrents Found!",
                    description=f"Can't find torrents for {search_ts} !!",
                    thumb_url=THUMBNAIL,
                    input_message_content=InputTextMessageContent(
                        message_text=f"No Torrents Found For `{search_ts}`",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="")]])
                )
            )
        else:
            for i in range(len(torrentList)):
                answers.append(
                    InlineQueryResultArticle(
                        title=f"{torrentList[i]['Name']}",
                        description=f"Seeders: {torrentList[i]['Seeders']}, Leechers: {torrentList[i]['Leechers']}\nSize: {torrentList[i]['Size']}, Downloads: {torrentList[i]['Downloads']}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"`{torrentList[i]['Magnet']}`",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]]
                        ),
                        thumb_url=THUMBNAIL
                    )
                )
    try:
        await inline.answer(
            results=answers,
            cache_time=0
        )
    except QueryIdInvalid:
        await asyncio.sleep(5)
        try:
            await inline.answer(
                results=answers,
                cache_time=0,
                switch_pm_text="Error: Search timed out!",
                switch_pm_parameter="start",
            )
        except QueryIdInvalid:
            await asyncio.sleep(5)
