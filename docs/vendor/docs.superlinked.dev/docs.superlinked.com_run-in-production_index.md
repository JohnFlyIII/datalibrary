---
url: "https://docs.superlinked.com/run-in-production/index"
title: "Setup Superlinked Server | Superlinked Docs"
---

The Superlinked server is designed to be used by end users who want to leverage the power of Superlinked in deployable projects. With a simple command, you can run a Superlinked-powered app instance that creates REST endpoints and connects to external Vector Databases. This makes it an ideal solution for those seeking an easy-to-deploy environment for their Superlinked projects.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index\#prerequisites)    Prerequisites

Before you can use this environment, you need to have:

1. Python 3.11 or higher installed with pip and venv modules. You can download Python from [here](https://www.python.org/downloads/).

2. A Python virtual environment created and activated in a dedicated project folder of your choice.

3. Install the superlinked-server library: `pip install superlinked-server`


_Note: The following documentation uses Unix-based terminal commands. Compatibility with other operating systems has not been verified._

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index\#how-to-start-the-application)    How to start the application

To start the application follow the steps below:

1. **Create the Superlinked app folder**: Create a directory to store your Superlinked configuration files by running `mkdir superlinked_app`. For a minimal working example, copy the [app.py](https://github.com/superlinked/superlinked/blob/main/docs/run-in-production/example/app.py) into your newly created `superlinked_app` directory. For more advanced use cases, please read the next section below.

2. **Start the Superlinked server**: To start the server run the `python -m superlinked.server` command.


By default, this will start the server on port 8080 (configurable via the `SERVER_PORT` environment variable) and expose the API endpoints for use. You can verify the server is running by visiting http://localhost:8080/docs in your browser.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index\#configuring-and-customizing-your-application)    Configuring and Customizing Your Application

Once your server is running, you'll need to configure and integrate your application. There are two main aspects to focus on:

- [Application Configuration Guide](https://docs.superlinked.com/run-in-production/index/configuring-your-app) \- Learn how to structure and customize your application

- [API Integration Guide](https://docs.superlinked.com/run-in-production/index/interacting-with-app-via-api) \- Understand how to interact with your application through the REST API


Click on either link above for detailed documentation on each aspect.

## [Direct link to heading](https://docs.superlinked.com/run-in-production/index\#support)    Support

If you encounter any issues while using this environment, please open an issue in this repository and we will do our best to help you.

[PreviousOverview](https://docs.superlinked.com/run-in-production/overview) [NextConfiguring your app](https://docs.superlinked.com/run-in-production/index/configuring-your-app)

Last updated 5 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject