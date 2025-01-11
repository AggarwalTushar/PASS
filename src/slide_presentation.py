import json
from vllm import LLM, SamplingParams
import argparse
from TTS.api import TTS

SYSTEMP_PROMPT_1 = """
You are a world-class presentation scriptwriter, trusted by renowned speakers like Tony Robbins, Sheryl Sandberg, and Simon Sinek to bring their ideas to life. In this universe, you have crafted every word of their famous speeches and presentations, and your words have won countless public speaking awards.

Your role is to generate word-for-word dialogue based on the uploaded slide topics and content. The presenter should be both informative and engaging, bringing the slide’s material to life with vivid examples, relatable anecdotes, and thought-provoking questions for the audience. Ensure that the presenter’s tone feels interactive and conversational, almost like they’re narrating an engaging story rather than just explaining points. Every detail, reaction, and pause should feel natural and intentional. Also, the presenter should say moving to the next slide when they are done with the current topic.

The presenter leads the session with expertise, injecting humor, and relatable examples to maintain audience engagement. They explain each slide's information clearly and break down complex points with analogies, staying approachable while establishing authority on the topic.
The presenter should have moments of interaction, like posing rhetorical questions to the audience, emphasizing key points with varied intonation, and using expressions like "Imagine if..." or "Have you ever wondered...".
Maintain a dynamic pace and occasionally create "hooks" to keep interest high, even hinting at surprising content or benefits on upcoming slides.
Feel free to sprinkle in minor asides, brief digressions, and humorous remarks that bring an authentic, human element to the presentation.
Ensure that every segment feels polished but conversational, filled with natural pauses, slight hesitations like “uh” or “well,” and vivid, relatable phrasing.
Begin directly with "Presenter:" and lead naturally into the slide content. Avoid giving slide titles or headings separately; integrate the key points as if they’re being explained to an engaged audience.
"""

SYSTEMP_PROMPT_2 = """
You are a world-renowned presentation scriptwriter, known for transforming complex topics into compelling, award-winning presentations. Today, your task is to refine the presentation dialogue below for an AI Text-To-Speech (TTS) pipeline, making it highly engaging and smooth for an audience to follow. Keep the Moving to next slide dialogue intact.

The TTS will simulate a **single presenter**, and your job is to edit each line to enhance clarity, engagement, and flow. The script should sound like a captivating storyteller leading the audience through the material with energy and charisma, while still clearly explaining the content.

* **Presenter:** Leads the presentation with clear explanations and strong narrative elements, using relatable examples and analogies to make complex points feel accessible. Inject personality into the words, keeping the tone conversational yet authoritative, as if the presenter is explaining directly to a curious audience.
* Avoid filler expressions like "um," "uh," or "hmm" as these do not perform well in TTS.
* Use rhetorical questions, brief asides, and phrasing like “Imagine if…” or “Think about…” to draw in the audience and encourage mental engagement.
* Maintain a friendly and professional tone, creating hooks and emphasis to ensure each segment of the content feels dynamic and engaging.

Rewrite the dialogue as necessary to bring out the presenter's charm and knowledgeability, but keep the structure straightforward. 

**Respond directly in the format of a list of tuples:**

Example of response:
[    ("Presenter", "Welcome, everyone! Today, we're diving into the fascinating world of neural networks. Imagine a system that learns just like our brains—pretty incredible, right? [pause] Let’s explore how these models work from the ground up."),    ("Presenter", "Now, you might wonder: what makes neural networks so powerful? Well, it all starts with their unique structure, designed to mimic human cognition. Think of each ‘neuron’ as a tiny data processor, and you’ll start to get the idea."),    ("Presenter", "[chuckles] Neural networks sound complex, but trust me, by the end of this session, you’ll have a solid grasp on the fundamentals.")]

Only output a list and all the elements should be inside single list. Do not output any thing other than the list.
"""

MODEL = "meta-llama/Meta-Llama-3-70B-Instruct"


def get_llm_outputs(llm, prompts, sampling_params):
    tokenizer = llm.get_tokenizer()
    prompts1 = [tokenizer.apply_chat_template(prompt, tokenize=False, add_generation_prompt=True) for prompt in prompts]
    llm_outputs = llm.generate(prompts1, sampling_params)
    llm_outputs = [output.outputs[0].text.strip() for output in llm_outputs]
    llm_outputs = [output.replace(prompt[1]["content"], "").strip() for prompt, output in zip(prompts, llm_outputs)]

    return llm_outputs

def init_llm():
    llm = LLM(MODEL, tensor_parallel_size=4, swap_space=4)
    llm_tokenizer = llm.get_tokenizer()
    sampling_params = SamplingParams(temperature=0, max_tokens = 8192)
    sampling_params.stop = [llm_tokenizer.eos_token, "<|eot_id|>"]
    return llm, sampling_params

def read_file_to_string(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)[0]
            print(content)
            content = content.split("```")[1]
            content = "\n".join(content.split("\n")[1:])
            content = eval(content)
        return content
    except UnicodeDecodeError:
        # If UTF-8 fails, try with other common encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                print(f"Successfully read file using {encoding} encoding.")
                return content
            except UnicodeDecodeError:
                continue
        
        print(f"Error: Could not decode file '{filename}' with any common encoding.")
        return None
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except IOError:
        print(f"Error: Could not read file '{filename}'.")
        return None

def audio_generator(tts, data):
    data = eval(data)
    full_text = ""
    for speaker, text in data:
        if "..." in text:
            text = text.replace("...", ".")
        full_text += text + " "
    tts.tts_to_file(full_text)    

def presenter_script_generator(llm, prompt, sampling_params):
    messages = [
        {"role": "system", "content": SYSTEMP_PROMPT_1},
        {"role": "user", "content": str(prompt) +"\nResponse:\n"},
    ]

    outputs = get_llm_outputs(llm, [messages], sampling_params)[0]

    messages = [
        {"role": "system", "content": SYSTEMP_PROMPT_2},
        {"role": "user", "content": outputs + "\nResponse:\n"},
    ]

    outputs_refine = get_llm_outputs(llm, [messages], sampling_params)[0]
    return outputs_refine

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--file", type=str, required=True, help="Path to the json file containing the content before summarization")
    args = argparser.parse_args()

    prompt = read_file_to_string(args.file)
    llm, sampling_params = init_llm()
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=True)
    outputs_refine = presenter_script_generator(llm, prompt, sampling_params)
    audio_generator(tts, outputs_refine)