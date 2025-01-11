from azure.identity import AzureCliCredential, get_bearer_token_provider
from openai import AzureOpenAI
import json 
from utils import topic_prompts, extract_prompts, summarize_prompt
import os
from jinja2 import Template
import base64
from vllm import LLM, SamplingParams
import argparse

def get_llm_outputs(llm, prompts, sampling_params):
    prompts1 = [[{"role": "user", "content": prompt}] 
                for prompt in prompts]
    tokenizer = llm.get_tokenizer()
    prompts2 = [tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True) for prompt in prompts1]
    #print("Entering:")
    llm_outputs = llm.generate(prompts2, sampling_params)
    #print(llm_outputs[0])
    llm_outputs = [output.outputs[0].text.strip() for output in llm_outputs]
    llm_outputs = [output.replace(prompt, "").strip() for prompt, output in zip(prompts, llm_outputs)]

    return llm_outputs[0]




def init_llm(model):
    llm = LLM(model, tensor_parallel_size=4, swap_space=4)
    llm_tokenizer = llm.get_tokenizer()
    sampling_params = SamplingParams(temperature=0, max_tokens = 8192)
    sampling_params.stop = [llm_tokenizer.eos_token, "<|eot_id|>"]
    return llm, sampling_params


def get_output():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--type", type=str, required=True, help="Module Type")
    argparser.add_argument("--data_dir", type=str, required=True, help="Path to the input document file")
    argparser.add_argument("--audience_type", type=str, required=True, help="Technical or Non-Technical")
    argparser.add_argument("--model", type=str, required=True, help="Model Name")
    args = argparser.parse_args()
    llm, sampling_params = init_llm(args.model)
    with open(os.path.join(args.data_dir, "file.txt"), "r") as f:
        data = f.read()
    model = os.path.split(args.model)[1]
    if args.type == "title_generator":
        os.makedirs(os.path.join(args.data_dir, "generations", model, "titles"), exist_ok=True)
        template = Template(topic_prompts[args.audience_type])
        prompts = [template.render(content = data)]
        result = get_llm_outputs(llm, prompts, sampling_params)
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
        result = get_llm_outputs(llm, [template.render(list_of_topics = topics, content = data)], sampling_params)
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
                    result = get_llm_outputs(llm, [text], sampling_params)
                    results.append(result)
            with open(os.path.join(args.data_dir, "generations", model, "final_slides", f"{args.audience_type}_slides.json"), "w") as f:
                json.dump(results, f, indent = 4)
get_output()