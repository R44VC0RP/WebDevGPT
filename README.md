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

<img width="400" src="https://imgr.whimsical.com/thumbnails/X1iPfzEe7M53aTg8TgXapJ/L844PY5DWTUTGM6JmAh6oc">

## Technologies

- **OpenAI GPT-4-vision API**: Used by CoderAI for interpreting visual design elements and generating corresponding HTML/CSS.
- **OpenAI GPT-4 Assistants API**: Utilized by PromptAI for processing natural language inputs and generating detailed development instructions.

## Use Example:

<img width="1224" alt="Screenshot 2023-11-09 at 12 56 17 PM" src="https://github.com/R44VC0RP/WebDevGPT/assets/89211796/5d64df2b-9ec6-4a3e-9da4-4bdf6ee7f29c">

This was a non-altered fully functioning test run. Here is the website that it generated:

<img width="1224" alt="Screenshot 2023-11-09 at 12 56 17 PM" src="https://github.com/R44VC0RP/WebDevGPT/assets/89211796/3f0be013-16c5-4251-9917-f5c8b73765fa">

### Thoughts:
Overall, it works, but I still need to optimize it and make it more reliable. It also uses a decent amount of tokens. This can be fixed with prompt optemizaiton and token counting.


## Contributions

Contributions to `WebDevGPT` are welcome. You can support the project by donating at https://www.buymeacoffee.com/exonenterprise. You can also contribute by submitting a pull request or opening an issue. Any support or suggestions are GREATLY appreciated.
