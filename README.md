# WebDevGPT

Welcome to the `WebDevGPT` repository, the home of an innovative Python-based automated website development workflow that leverages the power of OpenAI's GPT-4-vision and GPT-4 Assistants API.

## Overview

`WebDevGPT` is designed to streamline the process of website development from initial user input to the final deployment. The workflow integrates PromptAI and CoderAI, two AI-driven components that work together to interpret user requirements, generate detailed coding instructions, and create a website that meets the specified criteria.

## Workflow

The development process follows a structured workflow:

1. **User Requirement Input**: Users provide their website requirements to PromptAI.
2. **Instruction Generation**: PromptAI processes the requirements and uses GPT-4 Assistants API to generate detailed instructions for the website development.
3. **Website Coding**: CoderAI, utilizing the GPT-4-vision API, interprets the instructions and begins the coding process.
4. **Website Rendering**: Upon completion, CoderAI outputs an image link to the rendered website.
5. **Evaluation**: PromptAI evaluates the rendered website against the user's requirements.
6. **Iteration**: If the website is not satisfactory, PromptAI iterates the instructions and the process repeats.
7. **User Review**: Once satisfactory, the rendered website image is presented to the user for critique.
8. **Finalization**: If the user has no further critiques, the website is finalized and deployed.

![Detailed Python Website Development Workflow](https://imgr.whimsical.com/thumbnails/X1iPfzEe7M53aTg8TgXapJ/L844PY5DWTUTGM6JmAh6oc)

## Technologies

- **OpenAI GPT-4-vision API**: Used by CoderAI for interpreting visual design elements and generating corresponding HTML/CSS.
- **OpenAI GPT-4 Assistants API**: Utilized by PromptAI for processing natural language inputs and generating detailed development instructions.

## Getting Started

To get started with `WebDevGPT`, please follow the instructions below:

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Set up your OpenAI API keys in the configuration file.
4. Run the PromptAI module to input your website requirements.
5. Follow the on-screen instructions to guide you through the development process.

## Contribution

Contributions to `WebDevGPT` are welcome. Please read
