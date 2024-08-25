# Scrum Artifacts

`V2.1 - 20/04/2023`

<br>

This document contains al current and previous Scrum Artifacts.

> See [Scrum Artifacts](https://scrumguides.org/scrum-guide.html#scrum-artifacts) for more in-depth information

<br>

## Table of Contents

- [Scrum Artifacts](#scrum-artifacts)
  - [Table of Contents](#table-of-contents)
  - [1. Product Goal](#1-product-goal)
  - [2. Sprint Goals](#2-sprint-goals)
    - [2.1 Goal Sprint 1](#21-goal-sprint-1)
    - [2.2 Goal Sprint 2](#22-goal-sprint-2)
  - [3. Iteration Goals](#3-iteration-goals)
    - [3.1 Scraper](#31-scraper)
      - [3.1.1 Iteration 1](#311-iteration-1)
      - [3.1.2 Iteration 2](#312-iteration-2)
    - [3.2 Model](#32-model)
      - [3.2.1 Iteration 1](#321-iteration-1)
      - [3.2.2 Iteration 2](#322-iteration-2)
    - [3.3 Web App](#33-web-app)
      - [3.3.1 Iteration 1](#331-iteration-1)
      - [3.3.2 Iteration 2](#332-iteration-2)


## 1. Product Goal

Our goal is to create a web-app that utilizes AI to generate Dutch lyrics resembling a 'smartlap' style based on user input. The app should allow users to easily input phrases or keywords, which will be used by the AI to generate a personalized and emotional smartlap-style song. Our objective is to provide users with a unique and entertaining experience that enables them to express themselves through music while also showcasing the capabilities of AI-driven content generation.

We aim to deliver a fully functional and user-friendly web-app that meets the needs and expectations of our target audience within a series of iterative sprints.

## 2. Sprint Goals

### 2.1 Goal Sprint 1

The goal for the first sprint is to conduct research and develop a natural language model that can understand and interpret Dutch text inputs in the context of 'smartlap' songwriting. We will also create a scraper to collect relevant Dutch song lyrics and use them to train our model. Additionally, we aim to design and implement a basic user interface that enables users to input phrases or keywords and receive a simple, generated response based on the natural language model. We will conduct initial testing to validate the effectiveness of our model and collect user feedback to inform future iterations.

Our aim is to establish a solid foundation for the web-app's development and set the stage for further enhancements in subsequent sprints.

### 2.2 Goal Sprint 2

The goal for the second sprint is to stabilize the proof of concept established in the first sprint and improve the accuracy and quality of the natural language model by stabilising dependencies, enabling server training, and exploring GPT-Neo 1.3B. Additionally, we aim to modularize the lyrics scraper, make it a CLI application, and allow for interchangeable backends. We also aim to improve the user experience by experimenting with new features such as a temperature button for testing and exploring Flask. Finally, we will conduct unit testing, A/B testing, and use Figma to investigate new UX options such as allowing users to write text in stages to preserve context and multiple prompts to piece together lyrics in sections. 

Our objective is to continue to iterate and improve upon the web-app's functionality and user experience while showcasing the capabilities of AI-driven content generation.

## 3. Iteration Goals

### 3.1 Scraper

#### 3.1.1 Iteration 1

The goal for the first iteration is to develop a scraper that can collect legally available Dutch song lyrics from a pre-defined list of artists, as provided by the user. We will use an API to access the song data and filter out any songs not written in Dutch. The scraper will then clean the data by removing unnecessary symbols, text, and punctuation while retaining the song structure by preserving new lines between verses, choruses, etc. We will save all collected and cleaned data in a CSV file for later use.

Our aim is to create a reliable and efficient scraper that can collect high-quality data to be used in training our natural language model for the web-app. We will conduct testing to validate the scraper's functionality and ensure that it meets the user's needs and expectations.

#### 3.1.2 Iteration 2

The goal for the second iteration of the scraper is to improve its functionality and efficiency by modularizing it and making it a CLI application. We aim to enable interchangeable backends for different sources such as genius-lyrics, short stories, music match, or generic webpages. We will conduct unit testing to ensure the scraper's reliability and develop a scraper that can collect high-quality data for training our natural language model. Additionally, we aim to separate the scraper from the cleaning process to allow for more flexibility and customization. 

Our objective is to create a robust and efficient scraper that can quickly and reliably collect high-quality data to be used in training our natural language model for the web-app.

### 3.2 Model

#### 3.2.1 Iteration 1

The goal for the first iteration is to develop a natural language model that generates Dutch 'smartlap' lyrics based on pre-existing Dutch language models, fine-tuned using the Dutch lyrics collected by the scraper. We will use PyTorch 2.0 or Tensorflow to accelerate and facilitate the fine-tuning process. The model will take a user-provided prompt as input and generate Dutch lyrics in the style of a 'smartlap' song, retaining the song structure, such as verses, chorus, etc. We will conduct thorough testing to ensure that the model produces high-quality and coherent lyrics that meet the user's expectations.

Our aim is to create a reliable and effective natural language model that can be integrated into the web-app to generate personalized 'smartlap' lyrics based on user input.

#### 3.2.2 Iteration 2

The goal for the second iteration of the model is to improve its accuracy and performance by stabilising dependencies, enabling server training, and exploring the potential of GPT-Neo 1.3B. We aim to implement a feedback loop into the model to enable it to adapt text based on user feedback, and develop a method to analyze the generated lyrics and provide feedback on their quality and coherence. Additionally, we aim to conduct unit testing to validate the model-API's reliability and incorporate short stories into the training data to improve the coherence of the generated lyrics.

Our objective is to create a highly accurate and effective natural language model that can generate high-quality 'smartlap' lyrics based on user input

### 3.3 Web App

#### 3.3.1 Iteration 1

The goal for the first iteration is to develop a functional web-app that generates Dutch 'smartlap' lyrics based on user input using our natural language model. The app will allow users to input a prompt, which will be used to generate the corresponding lyrics using our model. The output will be displayed in plain text on the app's interface. We will include a reset button to clear the context and enable the user to input a new prompt. The app will run locally on the user's machine and not require an internet connection to function.

Our aim is to deliver a fully functional web-app that meets the user's needs and expectations, and can be used to generate personalized 'smartlap' lyrics in a convenient and user-friendly manner.

#### 3.3.2 Iteration 2

The goal for the second iteration of the web app is to improve its functionality and usability by experimenting with new features and exploring Flask. We aim to add a temperature, top-k and top-p slider for testing and implement a more sophisticated user interface. Additionally, we aim to conduct A/B testing and use Figma to investigate new UX options, such as allowing users to write text in stages to preserve context and multiple prompts to piece together lyrics in sections. 

Our objective is to create a highly functional and user-friendly web app that can generate personalized 'smartlap' lyrics in a convenient and customizable manner while showcasing the capabilities of AI-driven content generation.