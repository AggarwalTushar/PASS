import json 
from vllm import LLM, SamplingParams
import argparse
import argparse, re
import numpy as np
from utils import EVAL_PROMPT


def get_llm_outputs(llm, prompts, sampling_params):
    prompts1 = [[{"role": "user", "content": prompt}] 
                for prompt in prompts]
    tokenizer = llm.get_tokenizer()
    prompts2 = [tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True) for prompt in prompts1]
    llm_outputs = llm.generate(prompts2, sampling_params)
    llm_outputs = [output.outputs[0].text.strip() for output in llm_outputs]
    llm_outputs = [output.replace(prompt, "").strip() for prompt, output in zip(prompts, llm_outputs)]

    return llm_outputs




def init_llm():
    llm = LLM("meta-llama/Meta-Llama-3-70B-Instruct", tensor_parallel_size=4, swap_space=4)
    llm_tokenizer = llm.get_tokenizer()
    sampling_params = SamplingParams(temperature=0.8, max_tokens = 256)
    sampling_params.stop = [llm_tokenizer.eos_token, "<|eot_id|>"]
    return llm, sampling_params





def main():
    global EVAL_PROMPT
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", type=str, required=True, help="Path to the json file containing the slide content")
    argparser.add_argument("--type", type=str, required=True, help="Redundancy, Coherence, or Relevance")
    args = argparser.parse_args()
    llm, sampling_params = init_llm()
    prompts = []
    EVAL_PROMPT = EVAL_PROMPT[args.type]
    with open(f"{args.file}", "r") as f:
        data = json.load(f)
    for content in data:
        prompts.append(EVAL_PROMPT.format(content = content))
    results = [get_llm_outputs(llm, prompts, sampling_params) for i in range(20)]
    results = [[float(re.findall(r'\d+\.\d+|\d+', text)[0]) for text in result] for result in results]
    results = np.array(results)
    data = np.mean(results, axis = 1)
    mean_value = np.mean(data)
    std_value = np.std(data)

    err_value = std_value / np.sqrt(len(data))

    print(args.file)
    print(f"Mean ± Standard Deviation: {mean_value} ± {std_value}")
    print(f"Mean ± Standard Error: {mean_value} ± {err_value}")

if __name__ == "__main__":
    main()