summarize_prompt = """
You are given a slide topic and its corresponding summary. Please make the summary concise, breaking it into clear, short points that flow logically and are easy to read on a presentation slide. Try to provide the key information in 4-6 points. The summary should focus on clarity, brevity, and structure, ensuring it fits well on a slide.

Slide Topic: {title}  
Slide Summary: {content}

Format your response as a concise list of points, each being a very short sentence, following a logical flow for a presentation slide.
Don't refer to document in the response.

Example format:
Slide Topic: {title}
Summary:
- Point 1
- Point 2
...
"""

image_mapping_prompt = {
  "non_technical": """
You have created a slide deck for presenting to a non-technical audience who is primarily interested in the overall impact and value of the solution. You have been provided with the following slide topics along with the corresponding points for each topic in the following format:
Slide Topic: {title}
Summary:
- Point 1
- Point 2
...

{content}

Additionally, you have been given an image that contains relevant data, graphs, tables, or other visual information that may support one of the topics. 

Your task is to determine which slide topic is most relevant to the image based on the content provided. The image may contain various forms of data such as statistical results, graphs, or tables. Focus on matching the content of the image to the topics that involve similar technical details, results, or data points.

Either output the most relevant slide topic name from the given topics or "None", do not output anything else.

Response:

""",
  "technical": """
You have created a slide deck for presenting to a technical audience who wants to know the problem, solution, its impact, technical details, proofs, or results. You have been provided with the following slide topics along with the corresponding points for each topic in the following format:
Slide Topic: {title}
Summary:
- Point 1
- Point 2
...

{content}

Additionally, you have been given an image that contains relevant data, graphs, tables, or other visual information that may support one of the topics.

Your task is to determine which slide topic is most relevant to the image based on the content provided. The image may contain various forms of data such as statistical results, graphs, or tables. Focus on matching the content of the image to the topics that involve similar technical details, results, or data points.

Either output the most relevant slide topic name from the given topics or "None", do not output anything else.

Response:

"""
}




topic_prompts = {
 
"non_technical": """
You are given the content of the document. The goal is to present this document to a non-technical audience who is primarily interested in the overall impact and value of the solution presented in the document. They are not familiar with technical terminology related to machine learning, natural language processing, or any other complex tasks.

content: {{content}}

Please generate up to 8-10 main topics or sections that highlight the key ideas and outcomes of the document, ensuring a natural flow for a presentation. Each topic should be supported by at least 5-6 uncommon lines of content from the document, ensuring that these lines are relevant to the topic and help provide a clear understanding of the idea being presented. Topics should be concise.
Do not generate any content. Only generate the topics that have sufficient content.

Format your response as a JSON object with the following structure:
```
{
  "topics": [
    {
      "title": "Topic Name",
    },
    ...
  ]
}
```
""",

"technical" : """
You are given the content of the document. The goal is to present this document to a technical audience who is interested in understanding the problem, the proposed solution, its impact, technical details, proofs, or results. They are familiar with technical methodologies used in the field.

content: {{content}}

Please generate up to 8-10 main topics or sections that highlight the key ideas and outcomes of the document, ensuring a natural flow for a presentation. Each topic should be supported by at least 5-6 uncommon lines of content from the document, ensuring that these lines are relevant to the topic and help provide a clear understanding of the idea being presented. Topics should be concise.
Do not generate any content. Only generate the topics that have sufficient content.

Format your response as a JSON object with the following structure:
```
{
  "topics": [
    {
      "title": "Topic Name",
    },
    ...
  ]
}
```
"""
}

extract_prompts = {

    "non_technical": """
You are creating a slide deck for presenting to a non-technical audience who cares mostly about the overall impact of the solution approach in the document. They are not familiar with technical terminology related to machine learning, natural language processing, or any other complex tasks. In particular, you want to create slides for the following topics: {{list_of_topics}}. For each topic, choose the relevant sentences from the given content of the document. Each paragraph should be at least 3 lines long. Ensure that the content for one topic does not overlap with another, and provide clear, understandable paragraphs that are easy for a non-technical audience to follow.
If sufficient content is not available for a topic, that topic should not appear in the list.

content: {{content}}

Format your response as a JSON object with the following structure:
```
{
  "name_of_topic_1": "Paragraph summarizing the key points, extracted sentences related to topic_1.",
  "name_of_topic_2": "Paragraph summarizing the key points, extracted sentences related to topic_2.",
  ...
}
```
""",


    "technical" : """
You are creating a slide deck for presenting to a technical audience who wants to know the problem, solution, its impact, technical details, proofs, or results. They are familiar with technical methodologies used in the field. In particular, you want to create slides for the following topics: {{list_of_topics}}. For each topic, choose the relevant sentences from the given content of the document. Each paragraph should be at least 3 lines long. Ensure that the content for one topic does not overlap with another, and provide clear, understandable paragraphs that are easy for a non-technical audience to follow.
If sufficient content is not available for a topic, that topic should not appear in the list.

content: {{content}}

Format your response as a JSON object with the following structure:
```
{
  "name_of_topic_1": "Paragraph summarizing the key points, extracted sentences related to topic_1.",
  "name_of_topic_2": "Paragraph summarizing the key points, extracted sentences related to topic_2.",
  ...
}
```
"""
}

EVAL_PROMPT = {
"Redundancy":"""
Evaluate the given presentation content based only on the following criteria:
Is there unnecessary repetition of information across slides in the given presentation?

### Presentation:
{content}

Provide a score from 0-10 (0 is the lowest score, 10 is the highest), followed by a brief explanation.

### Score:
""",
"Relevance":"""
Evaluate the given presentation content based only on the following criteria:
Is each slide content relevant to the specified topic in the given presentation?

### Presentation:
{content}

Provide a score from 0-10 (0 is the lowest score, 10 is the highest), followed by a brief explanation.

### Score:
""",
"Coherence":"""
Evaluate the given presentation content based only on the following criteria:
Do the slides transition logically and smoothly from one to the next in the given presentation?

### Presentation:
{content}

Provide a score from 0-10 (0 is the lowest score, 10 is the highest), followed by a brief explanation.

### Score:
"""
}


GPT_FLAT_PROMPT = """
You’re an AI assistant that will help create a presentation from a document.You will be given section heading and paragraphs in that section. Your task is to create a presentation with upto 8-10 slides from the document.For every slide, output the slide title and bullet points in the slides.Please follow the following structure in the output. Do not output slide number.
SlideTitle: The slide title
BulletPoints:
New line separated bullet points
 
Following is the document, which contains section heading and paragraphs under that heading.
———DocumentStarted———
{{content}}
———DocumentEnded———
Presentation(upto 8-10 slides):
"""

GPT_COT_PROMPT = """
You’re an AI assistant that will help create a presentation from a document. You will be given section headings and paragraphs in that section. Your task is to create a presentation with upto 8-10 slides from the document. For every slide, output the slide title and bullet points in the slides. Please follow the steps provided below:
1. Begin by thoroughly reading and understanding the document. Identify the main points, key messages, and supporting details.
2. Find relations between different paragraphs that could be presented in the same slide.
3. Create a high-level outline for your presentation. Identify the main sections or topics that you’ll cover. This will serve as the skeleton for your slides.
4. Choose the most important information from the document to include in your presentation. Focus on key messages and supporting details that align with your presentation objectives.
5. Organize the selected content into slides, maintaining a logical flow. Each slide should represent a clear point or topic, and the overall structure should make sense to your audience.
6. Make sure slides are descriptive.
7. The presentation should have upto 8-10 slides.
8. Please follow the following structure. Do not output slide numbers.
Slide Title: The slide title
Bullet Points:

New line separated bullet points
Following is the document, which contains section heading and paragraphs under that heading:

——— Document Started ———
{{content}}
——— Document Ended ———

Presentation:
"""

GPT_CONS_PROMPT = """
You’re an AI assistant that will help create a presentation from a document. You will be given section headings and paragraphs in that section. Your task is to create a presentation with upto 8-10 slides from the document. For every slide, output the slide title and bullet points in the slides. Please follow the steps provided below:
1. Begin by thoroughly reading and understanding the document. Identify the main points, key messages, and supporting details.
2. Find relations between different paragraphs that could be presented in the same slide.
3. Create a high-level outline for your presentation. Identify the main sections or topics that you’ll cover. This will serve as the skeleton for your slides.
4. Choose the most important information from the document to include in your presentation. Focus on key messages and supporting details that align with your presentation objectives.
5. Organize the selected content into slides, maintaining a logical flow. Each slide should represent a clear point or topic, and the overall structure should make sense to your audience.
6. Make sure slides are descriptive.
7. The presentation should have upto 8-10 slides.
8. Each slide should have around 5-6 bullet points. Each bullet point should have around 15 words.
9. Please follow the following structure. Do not output slide numbers.
Slide Title: The slide title
Bullet Points:
New line separated bullet points

Following is the document, which contains section headings and paragraphs under that heading: 
——— Document Started ———
{{content}}
——— Document Ended ———

Presentation:
"""
# EVAL_PROMPT = """
# On a scale of 0-10 [inclusive], rate the effectiveness, clarity, and overall quality of the following presentation, considering factors such as organization, coherence, clarity, minimal overlap between slides, and the ability to convey ideas effectively. 0 is the lowest score, 10 is the highest.

# Presentation:
# {content}

# Score:
# """


### Relevance: Is the content relevant to the specified topic?
### Clarity: Are the ideas presented in a clear and understandable way?
### Coherence: Do the slides transition logically and smoothly from one to the next?
### Completeness: Are all necessary aspects of the topic covered?