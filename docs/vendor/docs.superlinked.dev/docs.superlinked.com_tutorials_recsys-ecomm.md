---
url: "https://docs.superlinked.com/tutorials/recsys-ecomm"
title: "RecSys - Ecommerce | Superlinked Docs"
---

In this example, we are building a recommender system for an e-commerce site mainly selling clothing.

Here are the details about the products we know:

- price

- the number of reviewers

- their rating

- textual description

- name of the product (usually contains the brand name)

- category


We have two users, and each of them can be either be characterised by

- the initial choice of a product offered to them at registration.

- or more general characteristics explained in the below paragraph (price, reviews)


Users have preferences on the textual characteristics of products (description, name, category), and according to classical economics, ceteris paribus prefers products

- that cost less

- has a lot of reviews

- with higher ratings so we are going to set our spaces up to reflect that.


In the second part of the notebook, we introduce behavioral data in the form of events and their effects.

Let's imagine we first examine a cold-start setup - we try to recommend items for users we know very little of.

After introducing user behavioral data in the form of events, we look at users with some history on our site: clicked on products, bought others, etc. These are taken into account to improve the quality of the recommendations.

### [Direct link to heading](https://docs.superlinked.com/tutorials/recsys-ecomm\#follow-along-in-this-colab)    Follow along in this Colab

[![Logo](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2Fssl.gstatic.com%2Fcolaboratory-static%2Fcommon%2F817b2046193605d71a233a8db91ae991%2Fimg%2Ffavicon.ico&width=20&dpr=4&quality=100&sign=de642489&sv=2)Google Colab](https://colab.research.google.com/github/superlinked/superlinked/blob/main/notebook/recommendations_e_commerce.ipynb)

[PreviousSemantic Search - Product Images & Descriptions](https://docs.superlinked.com/tutorials/semantic-search-product-images-descriptions) [NextRAG - HR](https://docs.superlinked.com/tutorials/rag-hr)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject