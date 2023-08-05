from examples.kitchen_sink.rules import will_lend
from ruleau import ApiAdapter, execute

if __name__ == "__main__":
    # Add API adapter to runner
    result = execute(
        will_lend,
        {
            "data": {
                "fico_score": 150,
                "ccjs": [],
                "kyc": "low",
                "number_of_children": 1,
                "capital": 10_000,
                "ccjs_required": True,
            }
        },
        api_adapter=ApiAdapter(
            base_url="http://127.0.0.1:8000"
        ).with_organisational_data([{"key": "Data Name", "value": None}]),
        case_id="abc",
    )
