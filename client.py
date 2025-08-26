from openai import OpenAI

#pip install openai
# default to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like this:
# client = OpenAI(api_key=os.environ.get("MY_CUSTOM_API_KEY"))
client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
{"role": "user", "content": "You are a virtual assistant name  jarvis skilled in general tasks like Alexa and Google Assistant."},
{"role": "user", "content": "what is coding?"}
]
)

print(completion.choices[0].message.content)