import asyncio
import sys
import time
import itertools
from openai.types.shared import Reasoning
from agents import Agent, ModelSettings, Runner
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text

console = Console()

# If you have a certain reason to use Chat Completions, you can configure the model this way,
# and then you can pass the chat_completions_model to the Agent constructor.
# from openai import AsyncOpenAI
# client = AsyncOpenAI()
# from agents import OpenAIChatCompletionsModel
# chat_completions_model = OpenAIChatCompletionsModel(model="gpt-5", openai_client=client)


def record_indicator(event: asyncio.Event):
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    start_time = time.time()
    while not event.is_set(): # runs until event is set
        elapsed = time.time() - start_time
        mins, secs = divmod(elapsed, 60)
        ms = int((secs - int(secs)) * 100)
        timer = f"{int(mins)}:{int(secs):02}.{ms:02}"
        spin = next(spinner)
        msg = f"I'm infooooorencing bro... {spin}   {timer}"
        console.print(Text(msg, style="bold green"), end="\r")
        time.sleep(0.1)
    # overwrite line when done
    console.print(Text("My result is now in you", style="bold green"))

def pretty_print_response(text: str, delay: float = 0.01):
    """
    Nicely formats the agent response in green with typewriter effect.
    Uses rich to handle markdown (##, **, etc).
    """
    md = Markdown(text)

    console.print("")  # spacing before response

    # Render line by line, typewriter style
    for line in text.splitlines():
        for char in line:
            console.print(char, style="green", end="")
            sys.stdout.flush()
            time.sleep(delay)
        console.print("")  # newline after each line

    console.print("")  # final spacing 

async def main():
    print("testing: Moxon, gpt-5-nano, reasoning minimal, verbosity low"),
    agent = Agent(
        name = "Moxon", #input("what shall you call me?  "),
        instructions = input("Agent instructions? -> "),
        model = "gpt-4.1-", #input("What Model? gpt-5/o3?  ").strip(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="minimal"),
            # reasoning=Reasoning(effort=input("what level of reasoning? minimal/low/medium/high? ")),  # "minimal", "low", "medium", "high"
            verbosity=("low"),
            max_tokens = input("Token Allowance? -> "),
            # verbosity=input("what level of verbosity? low/medium/high?  "),  # "low", "medium", "high"
        ),
    )
    
    user_input = input("Prompt? -> ")
    result_ready = asyncio.Event()

    indicator_task = asyncio.create_task(
        asyncio.to_thread(record_indicator, result_ready)
    )

    result = await Runner.run(agent, user_input)
    result_ready.set() 
    await indicator_task
    pretty_print_response(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
