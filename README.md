\# Support Ticket Triage Assistant



A local AI prototype that helps support engineers categorize tickets,

assess priority, and identify routing and next actions.



\## Features

\- Streamlit browser interface

\- Semantic category suggestions: Authentication, Performance, Integration

\- Other / needs review outcome for weak category matches

\- Priority recommendations using explicit impact fields

\- Requests missing impact information

\- Suggested support teams and predefined next actions



\## How it works

Sentence Transformers compares a ticket with category descriptions

using a pretrained all-MiniLM-L6-v2 embedding model.



A provisional similarity threshold of 0.30 controls category abstention.

Similarity scores are not confidence percentages.



Separate Python rules recommend priority from user-selected fields:

environment, business impact, affected users, and workaround availability.



Routing and next actions come from predefined category mappings.

The app displays suggestions; a support engineer reviews them.



\## Run locally

Requires Python 3.13.



Create an environment:

`py -3.13 -m venv .venv`



Install dependencies:

`.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt`



Start the app:

`.\\.venv\\Scripts\\python.exe -m streamlit run app.py`



The first use may download the embedding model.

No paid AI API or API key is required.



\## Initial manual checks

\- Authentication, performance, and integration examples matched correctly.

\- A billing example returned Other / needs review.

\- Unknown impact fields triggered requests for more information.

\- Urgent review, High, and Normal priority examples behaved as expected.

\- An integration example displayed the expected routing and actions.



\## Limitations

\- Small manual evaluation; accuracy has not been established.

\- The threshold needs broader testing.

\- Mixed issues and unfamiliar wording may produce incorrect suggestions.

\- Impact fields are entered manually, not extracted from the ticket.

\- Priority rules and team names are illustrative.

\- No custom model training or live ticket-system integration.



\## Development

Built with AI coding assistance and manually tested using fictional tickets.



\## Next steps

\- Expand the labeled evaluation set.

\- Compare semantic categorization with a keyword baseline.

\- Test ambiguous tickets and conflicting impact information.
## Evaluation results

Evaluated on 40 fictional tickets: 20 development and 20 test
examples. No settings were changed between the two evaluations.

| Split | Keyword accuracy | Semantic accuracy | Keyword coverage | Semantic coverage |
| --- | ---: | ---: | ---: | ---: |
| Development | 80% | 90% | 75% | 85% |
| Test | 65% | 90% | 50% | 75% |

Accuracy includes correct human-review decisions. Coverage is the
fraction assigned a supported category.

Error analysis identified missed secondary issues in mixed tickets
and rejection of an indirectly worded integration issue. Results
come from a small synthetic dataset and do not establish production
accuracy or business impact.
