---
url: "https://docs.superlinked.com/tutorials/rag-hr"
title: "RAG - HR | Superlinked Docs"
---

Many companies aim to make HR documents more accessible to employees and contractors. A recent promising approach is building a RAG system on top of HR documents. This is because it

- provides a unique response to any query,

- reduces hallucinations as the answer has to be grounded in the retrieved context,

- makes the process highly scalable due to automatic question-answering.


However, this solution possesses its unique challenges. For example

- keeping the knowledgebase consistent and up-to-date,

- running LLMs efficiently,

- ensuring the generated results are correct and aligned with company communication guidelines,


In our case, we have three HR policy sources for our hypothetical company.

1. An older HR policy, which contains our maternity leave policy and details on manager responsibilities.

2. A more recent update, that contains inaccurate information on management responsibilities - but one that also contains unique information on paternity leave.

3. A newer policy document that contains updated information about management responsibilities, correcting the mistakes of the previous modernising attempt - alongside some other HR policy information.


A good system will be able to:

- provide relevant information on maternity leave (only covered in the old document),

- synthesize contradicting information and only present to us the correct ones


Regarding synthesizing information, there are contradictions between the documents pertaining to management responsibilities. We are going to use the

- creation\_date of the policy,

- and the usefulness score of each paragraph


as a proxy to know for similar documents with

- similar information but different wording, and some important parts slightly altered, or

- also talking about seemingly the same topic, but without conveying useful information


which one is more relevant to our query.

### [Direct link to heading](https://docs.superlinked.com/tutorials/rag-hr\#follow-along-in-this-colab)    Follow along in this Colab

[![Logo](https://docs.superlinked.com/~gitbook/image?url=https%3A%2F%2Fssl.gstatic.com%2Fcolaboratory-static%2Fcommon%2F30864e73efec47e27efc1f39a6579d5e%2Fimg%2Ffavicon.ico&width=20&dpr=4&quality=100&sign=223bee3d&sv=2)Google Colab](https://colab.research.google.com/github/superlinked/superlinked/blob/main/notebook/rag_hr_knowledgebase.ipynb#scrollTo=e9fb5d47-d6b9-4cdd-b2b4-80dda4eef996)

[PreviousRecSys - Ecommerce](https://docs.superlinked.com/tutorials/recsys-ecomm) [NextAnalytics - User Acquisition](https://docs.superlinked.com/tutorials/analytics-user-acquisition)

Last updated 8 months ago

Was this helpful?

This site uses cookies to deliver its service and to analyze traffic. By browsing this site, you accept the [privacy policy](https://superlinked.com/policies/privacy-policy).

AcceptReject