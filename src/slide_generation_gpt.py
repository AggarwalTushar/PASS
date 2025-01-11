from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AzureOpenAI
import json 
from utils import topic_prompts, extract_prompts, summarize_prompt
import os
from jinja2 import Template
import base64
from vllm import LLM, SamplingParams
import argparse



def get_llm_outputs(llm, prompts, image_payload = []):
    prompts1 = [[{"role": "user", "content": [{"type": "text", "text": prompt}] + image_payload}] 
                for prompt in prompts]
    responses = [llm.chat.completions.create(
                model="gpt4o", 
                messages=prompt,
                temperature=0,
                max_tokens=8192,
                ) for prompt in prompts1]
    results = [response.choices[0].message.content for response in responses]
    return results[0]




def init_llm():
    token_provider = get_bearer_token_provider(
    AzureCliCredential(), "https://cognitiveservices.azure.com/.default"
    )

    client = AzureOpenAI(
        api_version="2024-02-15-preview",
        azure_endpoint="",
        azure_ad_token_provider=token_provider
    )
    return client


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_output():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--type", type=str, required=True, help="Module Type")
    argparser.add_argument("--data_dir", type=str, required=True, help="Path to the input document file")
    argparser.add_argument("--audience_type", type=str, required=True, help="Technical or Non-Technical")
    argparser.add_argument("--model", type=str, default = "gpt-4o", help="Model Name")
    args = argparser.parse_args()
    llm = init_llm()
    with open(os.path.join(args.data_dir, "file.txt"), "r") as f:
        data = f.read()
    
    image_payload = []
    folder_name = os.path.join(args.data_dir, "images")
    for filename in os.listdir(folder_name):
        if os.path.isfile(os.path.join(folder_name, filename)) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_name, filename)
            base64_image = encode_image(image_path)
        
            image_payload.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

    model = os.path.split(args.model)[1]
    if args.type == "title_generator":
        os.makedirs(os.path.join(args.data_dir, "generations", model, "titles"), exist_ok=True)
        template = Template(topic_prompts[args.audience_type])
        prompts = [template.render(content = data)]
        result = get_llm_outputs(llm, prompts, image_payload)
        with open(os.path.join(args.data_dir, "generations", model, "titles",f"{args.audience_type}_slide_topics.json"), "w") as f:
            json.dump(result, f, indent = 4)
    elif args.type == "content_extractor":
        os.makedirs(os.path.join(args.data_dir, "generations", model, "content"), exist_ok=True)
        results = []
        topics = []
        with open(os.path.join(args.data_dir, "generations", model, "titles", f"{args.audience_type}_slide_topics.json"), "r") as f:
            item = json.load(f)
            try:
                item = item.split("```")[1]
                item = "\n".join(item.split("\n")[1:])
            except:
                start = item.find('{')
                end = item.rfind('}')
                item = item[start:end+1]
            item = eval(item)
            
            for topic in item["topics"]:
                topics.append(topic["title"])
                
        template = Template(extract_prompts[args.audience_type])
        result = get_llm_outputs(llm, [template.render(list_of_topics = topics, content = data)], image_payload)
        results.append(result)
        with open(os.path.join(args.data_dir, "generations", model, "content", f"{args.audience_type}_slide_content.json"), "w") as f:
            json.dump(results, f, indent = 4)
    elif args.type == "summarizer":
        os.makedirs(os.path.join(args.data_dir, "generations", model, "final_slides"), exist_ok=True)
        results = []
        with open(os.path.join(args.data_dir, "generations", model, "content", f"{args.audience_type}_slide_content.json"), "r") as f:
            content = json.load(f)
            for item in content:
                try:
                    item = item.split("```")[1]
                    item = "\n".join(item.split("\n")[1:])
                except:
                    start = item.find('{')
                    end = item.rfind('}')
                    item = item[start:end+1]
                item = eval(item)
                for topic, value in item.items():
                    slide_content = " ".join(value)
                    text = summarize_prompt.format(title = topic, content = slide_content)
                    result = get_llm_outputs(llm, [text])
                    results.append(result)
            with open(os.path.join(args.data_dir, "generations", model, "final_slides", f"{args.audience_type}_slides.json"), "w") as f:
                json.dump(results, f, indent = 4)
get_output()