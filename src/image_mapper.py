from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AzureOpenAI
import json 
from utils import image_mapping_prompt
import os
from jinja2 import Template
import base64
import argparse

token_provider = get_bearer_token_provider(
    AzureCliCredential(), "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    api_version="2024-02-15-preview",
    azure_endpoint="",
    azure_ad_token_provider=token_provider
)



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--audience_type", type=str, required=True, help="Technical or Non-Technical")
    argparser.add_argument("--data_dir", type=str, required=True, help="Path to the input document file")
    argparser.add_argument("--model", type=str, required=True, help="Model Name")
    args = argparser.parse_args()
    model = os.path.split(args.model)[1]
    folder_name = os.path.join(args.data_dir, "images")
    os.makedirs(os.path.join(args.data_dir, "generations", model, "image_mapping"), exist_ok=True)
    
    results = []
    template = Template(image_mapping_prompt[args.audience_type])
    with open(os.path.join(args.data_dir, "generations", model, "final_slides", f"{args.audience_type}_slides.json"), "r") as f:
        data = f.read()
    for filename in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, filename)) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_name, filename)
            base64_image = encode_image(image_path)
            image_payload = []
        
            # Add the image payload entry
            image_payload.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

            
            
            payload = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": template.render(content = data)
                    }
                ] + image_payload
                }
            ]

            response = client.chat.completions.create(
                model="hywaygpt4o",
                messages= payload,
                max_tokens=32,
                temperature=0,
            )
            result = response.choices[0].message.content
            results.append({"image": filename, "result": result})
            print(response.choices[0].message.content)
    with open(os.path.join(args.data_dir, "generations", model, "image_mapping", f"{args.audience_type}_output.json"), "w") as f:
        json.dump(results, f, indent = 4)