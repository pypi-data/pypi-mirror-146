# -*- coding: utf-8 -*-
import asyncio
import itertools
import os
import sys

from builtins import print as nprint
from keyword import kwlist
from typing import Any, AsyncIterable, Callable, Tuple

from aioconsole import aexec, ainput
from async_eval import async_eval
from colorama import Fore, Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.shortcuts import PromptSession, yes_no_dialog
from pygments.lexers.python import PythonLexer
from rich import print

keywords: Any = kwlist

session = PromptSession()


exec = aexec
eval = async_eval.async_eval
ninput = ainput

BlinkingCursor: Any = CursorShape.BLINKING_UNDERLINE


async def input(input_text: str = "", **kwargs) -> str:
    with patch_stdout():
        text = await session.prompt_async(
            input_text,
            lexer=PygmentsLexer(PythonLexer),
            auto_suggest=AutoSuggestFromHistory(),
            cursor=BlinkingCursor,
            mouse_support=True,
            **kwargs,
        )
    return text


class Input:
    def __init__(self) -> None:
        pass

    async def get_input(self) -> AsyncIterable[Tuple[int, str]]:
        for i in itertools.count():
            try:
                nprint(f"{Fore.CYAN}In [%d]{Style.RESET_ALL}: " % i, end="")
                yield i, await input(complete_in_thread=True)
            except (KeyboardInterrupt, EOFError):
                inp = yes_no_dialog(
                    "Quit",
                    text="Are you sure you wanna quit?",
                    yes_text="yes",
                    no_text="no",
                ).run()
                if inp:
                    nprint(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}", flush=True)
                    try:
                        sys.exit(0)
                    except:
                        os._exit(0)
                else:
                    nprint(f"{Fore.GREEN}Continuing...{Style.RESET_ALL}")
                    continue


class Executor:
    def __init__(self, user_globals: dict) -> None:
        self.user_globals = user_globals

    async def get(self, user_input: str) -> Callable:

        try:
            compile(user_input, "<stdin>", "eval")
        except SyntaxError:
            return exec
        return eval

    async def __call__(self, user_input: str, i: int):
        user_globals = self.user_globals.copy()
        try:
            val: Callable = await self.get(user_input)
            ret_val = (
                await val(user_input, user_globals)
                if "__await__" in dir(val) or val == exec
                else val(user_input, user_globals)
            )
        except Exception as e:
            nprint(f"{Fore.RED}{e.__class__.__name__}: {e}{Style.RESET_ALL}")
            return user_globals
        else:
            if not ret_val is None:
                format = f"{Fore.GREEN}Out [{i}]: {Style.RESET_ALL}"
                nprint(format, end="")
                print(ret_val)
                return user_globals
        return user_globals


async def main():

    user_globals = {}
    get_user_input = Input()
    async for i, user_input in get_user_input.get_input():
        if user_input == "reset":
            result = yes_no_dialog(title="Reset", text="Do you want to reset?").run()
            if result:
                user_globals = {}
                nprint(f"{Fore.GREEN}Reset Successful{Style.RESET_ALL}")
                continue
            else:
                nprint(f"{Fore.GREEN}Reset Cancelled{Style.RESET_ALL}")
                continue
        executor = Executor(user_globals)
        if not user_input:
            continue
        user_globals = await executor(user_input, i)


if __name__ == "__main__":
    asyncio.run(main())
