import sys
import requests

def test_health_check_works(endpoint):
    resp = requests.get(endpoint + "/health_check")
    assert resp.status_code == 200

def test_vote_increment_and_clear_work(endpoint):
    resp = requests.post(endpoint + "/clear", data={"key":"test_key"})
    assert resp.status_code == 200

    resp = requests.get(endpoint + "/vote/test_key")
    assert "1" == resp.text, resp.text

    resp = requests.get(endpoint + "/vote/test_key")
    assert "2" == resp.text, resp.text

    resp = requests.get(endpoint + "/vote/test_key")
    assert "3" == resp.text, resp.text

def test_ping_hulu_works(endpoint):
    resp = requests.get(endpoint + "/proxy_hulu")
    assert 200 == resp.status_code

if __name__ == "__main__":
    endpoint_server = sys.argv[0]
    if not endpoint_server.startswith("http://"):
        endpoint_server = "http://127.0.0.1:5000"

    for test in [
        test_health_check_works,
        test_vote_increment_and_clear_work,
        test_ping_hulu_works
    ]:
        test(endpoint_server)
