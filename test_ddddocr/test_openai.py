import os,json
import openai
import requests

from openai import OpenAI
from openai import AzureOpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential


# model_name = "gpt-4o"

# client = OpenAI(
#     base_url="https://models.inference.ai.azure.com",
#     api_key=os.environ["GITHUB_TOKEN"],
# )

os.environ["OPENAI_API_KEY"] = os.environ["GITHUB_TOKEN"]
model_name = "deepseek-chat"
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.environ["DEEP_SEEK_KEY"],
)

def openai_chat():
    # student_1_description="Emily Johnson is a sophomore majoring in computer science at Duke University. She has a 3.7 GPA. Emily is an active member of the university's Chess Club and Debate Team. She hopes to pursue a career in software engineering after graduating."

    # student_2_description = "Michael Lee is a sophomore majoring in computer science at Stanford University. He has a 3.8 GPA. Michael is known for his programming skills and is an active member of the university's Robotics Club. He hopes to pursue a career in artificial intelligence after finishing his studies."

    # prompt1 = f'''
    # Please extract the following information from the given text and return it as a JSON object:

    # name
    # major
    # school
    # grades
    # club

    # This is the body of text to extract the information from:
    # {student_1_description}
    # '''

    # prompt2 = f'''
    # Please extract the following information from the given text and return it as a JSON object:

    # name
    # major
    # school
    # grades
    # club

    # This is the body of text to extract the information from:
    # {student_2_description}'''
    
    functions = [
        {
            "name":"search_courses",
            "description":"Retrieves courses from the search index based on the parameters provided",
            "parameters":{
                "type":"object",
                "properties":{
                    "role":{
                    "type":"string",
                    "description":"The role of the learner (i.e. developer, data scientist, student, etc.)"
                    },
                    "product":{
                    "type":"string",
                    "description":"The product that the lesson is covering (i.e. Azure, Power BI, etc.)"
                    },
                    "level":{
                    "type":"string",
                    "description":"The level of experience the learner has prior to taking the course (i.e. beginner, intermediate, advanced)"
                    }
                },
                "required":[
                    "role"
                ]
            }
        }
        ]
    messages = [ {"role": "user", "content": "Find me a good course for a beginner student to learn azure."} ]
    response = client.chat.completions.create(
        # messages=[
        #     SystemMessage(content=""""""),
        #     UserMessage(content="Find me a good course for a beginner student to learn Azure."),
        # ],
        messages=messages,
        model=model_name,
        # temperature=1,
        # max_tokens=4096,
        functions=functions,
        function_call="auto",
        # top_p=1
    )
    print(response.choices[0].message.content)
    response_message = response.choices[0].message
    print(response_message)
    # Check if the model wants to call a function
    if response_message.function_call.name:
        print("Recommended Function call:")
        print(response_message.function_call.name)
        print()

        # Call the function.
        function_name = response_message.function_call.name

        available_functions = {
                "search_courses": search_courses,
        }
        function_to_call = available_functions[function_name]

        function_args = json.loads(response_message.function_call.arguments)
        function_response = function_to_call(**function_args)

        print("Output of function call:")
        print(function_response)
        print(type(function_response))


        # Add the assistant response and function response to the messages
        messages.append( # adding assistant response to messages
            {
                "role": response_message.role,
                "function_call": {
                    "name": function_name,
                    "arguments": response_message.function_call.arguments,
                },
                "content": None
            }
        )
        
        function_to_call = available_functions[function_name]

        function_args = json.loads(response_message.function_call.arguments)
        function_response = function_to_call(**function_args)
        messages.append( # adding function response to messages
            {
                "role": "function",
                "name": function_name,
                "content":function_response,
            }
        )
        print("Messages in next request:")
        print(messages)
        print()
        print("function_response:",function_response)

        second_response = client.chat.completions.create(
        messages=messages,
        model=model_name,
        function_call="auto",
        functions=functions,
        temperature=0
            )  # get a new response from GPT where it can see the function response


        print(second_response.choices[0].message.content)

def search_courses(role, product, level) ->str : 
  url = "https://learn.microsoft.com/api/catalog/"
  params = {
     "role": role,
     "product": product,
     "level": level
  }
  response = requests.get(url, params=params)
  modules = response.json()["modules"]
  results = []
  for module in modules[:5]:
     title = module["title"]
     url = module["url"]
     results.append({"title": title, "url": url})
  return str(results)

def azure():
    client = ChatCompletionsClient(
        endpoint='https://models.inference.ai.azure.com',
        credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
    )

    response = client.complete(messages=[
            SystemMessage(content=""""""),
            UserMessage(content="Find me a good course for a beginner student to learn Azure."),
        ],
        model="gpt-4o-mini",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )
    print(response.choices[0].message.content)


def text():
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            },
            {
                "role": "user",
                "content": """简要介绍和关系""",
            }
        ],
        model=model_name,
        # model = "deepseek-chat",
        temperature=1.,
        max_tokens=4096,
        top_p=1.
    )

    print(response.choices[0].message.content)

# GITHUB的token无法运行
def image_generation():
    response = openai.images.generate(model="dall-e-3",prompt="a white siamese cat",size="1024x1024",quality="standard",n=1)
    image_url = response.data[0].url
    print(image_url)



def image_genaration2():
    try:
        # Create an image by using the image generation API
        generation_response = openai.images.generate(
            prompt='Bunny on horse, holding a lollipop, on a foggy meadow where it grows daffodils',    # Enter your prompt text here
            size='1024x1024',
            n=2,
            temperature=0,
        )
        # Set the directory for the stored image
        image_dir = os.path.join(os.curdir, 'images')

        # If the directory doesn't exist, create it
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        # Initialize the image path (note the filetype should be png)
        image_path = os.path.join(image_dir, 'generated-image.png')

        # Retrieve the generated image
        image_url = generation_response["data"][0]["url"]  # extract image URL from response
        generated_image = requests.get(image_url).content  # download the image
        with open(image_path, "wb") as image_file:
            image_file.write(generated_image)

        # Display the image in the default image viewer
        image = Image.open(image_path)
        image.show()

    # catch exceptions
    except openai.InvalidRequestError as err:
        print(err)

# azure()
print("openai_chat  \n")
openai_chat()
#text()

# image_genaration2()