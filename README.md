# PASS: Presentation Automation for Slide Generation and Speech

PASS is an AI-powered pipeline designed to automate both the generation of presentation slides and their oral delivery. It can process general Word documents, not limited to research papers, and provides a comprehensive solution for creating and delivering high-quality presentations. The system generates dynamic slides and uses AI-generated voice for seamless narration.

## Overview

In today's fast-paced world, effective presentations are essential in both academic and professional settings. However, the process of creating slides, extracting key insights, and rehearsing for delivery can be time-consuming. PASS addresses these challenges by automating the generation of slides and their oral delivery, ensuring that users can create polished and engaging presentations quickly and efficiently.

PASS consists of two primary modules:

1. **Slide Generation**: Automatically extracts key information from the input document and generates a structured slide deck.
2. **Slide Presentation**: Converts the generated slide content into an AI-generated voice narration, providing a complete presentation experience.

## Architecture

The architecture of PASS comprises two main modules, each divided into several sub-modules:

![image](https://github.com/user-attachments/assets/910fc4a9-a76c-427b-81d9-55156eaa91a1)


### Slide Generation

- **Image and Text Extractor**: Separates text and images in the document.
- **Title Generator**: Generates slide titles based on the document content.
- **Content Extractor**: Extracts the most relevant content for each slide.
- **Summarizer**: Condenses extracted content into concise points for slides.
- **Image Mapping**: Maps relevant images to corresponding slides.

### Slide Presentation

- **Presenter Script Generator**: Generates the script for each slide.
- **Audio Generation**: Converts the script into speech using an AI-based Text-to-Speech model (Tacotron-2).

## Installation

To install and run PASS locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AggarwalTushar/PASS.git
   cd PASS
