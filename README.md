# PASS: Presentation Automation for Slide Generation and Speech

PASS is an AI-powered pipeline designed to automate both the generation of presentation slides and their oral delivery. It can process general Word documents, not limited to research papers, and provides a comprehensive solution for creating and delivering high-quality presentations. The system generates dynamic slides and uses AI-generated voice for seamless narration.

## Overview

In today's fast-paced world, effective presentations are essential in both academic and professional settings. However, the process of creating slides, extracting key insights, and rehearsing for delivery can be time-consuming. PASS addresses these challenges by automating the generation of slides and their oral delivery, ensuring that users can create polished and engaging presentations quickly and efficiently.

PASS consists of two primary modules:

1. **Slide Generation**: Automatically extracts key information from the input document and generates a structured slide deck.
2. **Slide Presentation**: Converts the generated slide content into an AI-generated voice narration, providing a complete presentation experience.

## Architecture

The architecture of PASS comprises two main modules, each divided into several sub-modules:

<img src="https://github.com/user-attachments/assets/910fc4a9-a76c-427b-81d9-55156eaa91a1" width="500" />


## Installation

To use PASS, follow these steps to set up the environment and install the required dependencies.

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AggarwalTushar/PASS.git
   cd PASS

2. **Install dependencies:**
   
    Use env.yml to create a conda environment:
   ```bash
   conda env create -f env.yml
   conda activate pass
   
3. **Execute Slide Generation Module:**
   Add your model, doc file path and audience(technical/non-technical) details in the src/run.sh file. Use the following command to run the file:
   ```bash
   bash src/run.sh
   
4. **Execute Slide Presentation Module:**
   ```bash
   python src/slide_presentation.py --file <Path to the json file containing the content before summarization - ({OUTPUT_DIR}/generations/{model}/content/{AUDIENCE_TYPE)_slide_content.json)>
   
5. **Slides Evaluation:**
   ```bash
   python src/eval.py --file <Path to the json file containing the generated slides - ({OUTPUT_DIR}/generations/{model}/content/{AUDIENCE_TYPE)_slides.json)> --type <Redundancy, Relevance, Coherence>

## Paper
The detailed paper describing PASS, its architecture, and evaluation results can be found here.

## Citation
If you use **PASS** in your research or projects, please cite the following paper:

```bash
@article{aggarwal2025pass,
  title={PASS: A Pipeline for Automated Presentation Generation and Delivery},
  author={Tushar Aggarwal, Aarohi Bhand},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
