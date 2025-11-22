import json

from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

metric = AnswerRelevancyMetric(threshold=0.7, model="gpt-4", include_reason=True)

with open("tests/test_queries.json", "r") as file:
    test_queries = json.load(file)

test_cases = []
for test in test_queries:
    query = test.get("query")
    expected = test.get("expected_answer")

    actual_answer = ""
    # PLACEHOLDER: actual_answer = run_rag_pipeline(query)

    test_case = LLMTestCase(
        input=query,
        actual_output=expected,
    )
    test_cases.append(test_case)

evaluate(test_cases=test_cases, metrics=[metric])
