# DeepEdit
#### Video Demo: https://youtu.be/3d2ggx4TizE
#### Description:
DeepEdit is a web-based, AI-powered photo editing application designed to provide a seamless and intuitive user experience. With a rich feature set that includes a wide variety of Instagram-style filters, advanced image enhancement capabilities, and essential editing tools like cropping and brightness adjustment, DeepEdit empowers users to transform their photos with just a few clicks.

This project was born out of a passion for both web development and the ever-evolving field of artificial intelligence, plus photo-editing. The goal was to create a tool that is not only powerful but also accessible to users of all skill levels.

## Project Overview

At its core, DeepEdit is a Flask application that leverages the power of Python for its backend and the flexibility of JavaScript for its interactive frontend. The application allows users to upload their photos, apply a variety of filters and enhancements, and then download the edited image.

The key features of DeepEdit include:

*   **A Wide Range of Filters**: DeepEdit comes with a curated collection of filters, each with its own unique aesthetic. From vintage-inspired looks to modern, vibrant styles, there's a filter for every mood and occasion.
*   **AI-Powered Image Enhancement**: This is where DeepEdit truly shines. The application integrates with state-of-the-art AI models to provide intelligent image enhancement. This feature can be used to improve the overall quality of a photo, sharpen details, and even upscale low-resolution images.
*   **Essential Editing Tools**: In addition to its advanced features, DeepEdit also provides the essential editing tools that users have come to expect. This includes the ability to crop photos to the perfect dimensions and adjust the brightness to achieve the desired look.
*   **User-Friendly Interface**: The user interface of DeepEdit has been designed with simplicity and ease of use in mind. The intuitive layout makes it easy for users to navigate the application and access all of its features.

## File-by-File Breakdown

The DeepEdit project is organized into a logical and maintainable file structure. Here's a breakdown of the most important files and directories:

*   `app.py`: This is the heart of the application. It's a Flask web server that handles all of the backend logic, including routing, file uploads, and image processing.
*   `helpers.py`: This file contains all of the image enhancement and processing functions. It's where the magic happens, with a variety of functions that leverage libraries like Pillow, OpenCV, and realesrgan to provide a wide range of enhancement options.
*   `templates/`: This directory contains all of the HTML templates that make up the user interface of the application. It includes templates for the home page, the upload page, and the editing page.
*   `static/`: This directory is home to all of the static assets, including the client-side JavaScript, CSS, and image files.

## Design Philosophy and Choices

The design of DeepEdit was guided by a few key principles:

*   **Simplicity and Ease of Use**: The primary goal was to create a tool that is both powerful and easy to use. This is reflected in the clean and intuitive user interface, as well as the straightforward workflow.
*   **Flexibility and Extensibility**: The project was designed to be flexible and extensible, allowing for the easy addition of new features and functionality in the future. The modular file structure and the use of a lightweight web framework like Flask make it easy to build upon the existing codebase.
*   **Leveraging the Best of Both Worlds**: DeepEdit combines the power of Python for its backend with the flexibility of JavaScript for its frontend. This allows for a seamless user experience, with the heavy lifting of image processing being handled by the server, while the client-side JavaScript provides a responsive and interactive user interface.

One of the key design choices was the use of multiple image processing libraries. This was done to provide a wide range of enhancement options, from simple adjustments to advanced AI-powered upscaling. By leveraging the strengths of different libraries, DeepEdit is able to offer a comprehensive set of tools that can be used to achieve a variety of different looks.

Another important design choice was the implementation of a client-side cropping feature. This was done to provide a more interactive and user-friendly experience. By allowing users to see the crop area in real-time, they are able to make more precise adjustments and achieve the exact look they are going for.

## Installation and Usage

To get started with DeepEdit, you'll need to have Python and pip installed on your machine. Once you have those prerequisites, you can follow these steps to get the project up and running:

1.  **Clone the repository**:
    ```
    git clone https://github.com/JasjeetSingh18/DeepEdit.git
    ```
2.  **Navigate to the project directory**:
    ```
    cd DeepEdit
    ```
3.  **Install the dependencies**:
    ```
    pip install -r requirements.txt
    ```
4.  **Run the application**:
    ```
    python app.py
    ```

Once the application is running, you can access it by opening your web browser. From there, you can upload a photo, apply filters and enhancements, and download the edited image.
