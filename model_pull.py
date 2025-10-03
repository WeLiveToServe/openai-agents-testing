from openai import OpenAI
from openai_agents import list_models  # hypothetical call, adapt per SDK

def choose_model(models):
    print("Available models:")
    for i, m in enumerate(models, start=1):
        print(f"{i}. {m}")
    choice = int(input("Select model by number: "))
    return models[choice - 1]

def main(model_name, instructions):
    client = OpenAI()
    # Example call (replace per SDK signature)
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": instructions}],
    )
    print(response.choices[0].message.content)

if __name__ == "__main__":
    # Get models available in openai-agents
    models = list_models()  # adjust to actual SDK function
    model = choose_model(models)
    instructions = input("Enter your instructions: ")
    main(model, instructions)
