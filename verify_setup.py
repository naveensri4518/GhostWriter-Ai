"""
GhostWriter AI - Verification and Testing Suite
Tests Flask endpoints, Ollama connectivity, and end-to-end horror story generation.
"""

import sys
import json
import time

def run_tests():
    print("=" * 60)
    print("RUNNING GHOSTWRITER AI TEST SUITE")
    print("=" * 60)

    try:
        from app import app, fetch_available_models, is_model_installed
    except ImportError as e:
        print(f"FAILED: Import error: {e}")
        sys.exit(1)

    client = app.test_client()

    # Test 1: Frontend Route GET /
    print("\n[Test 1] Testing GET / (Homepage)...")
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    html_text = res.get_data(as_text=True)
    assert "GHOSTWRITER" in html_text, "Missing 'GHOSTWRITER' brand in HTML"
    assert "Stories from the Other Side" in html_text, "Missing subtitle in HTML"
    assert "Ghost Stories" in html_text, "Missing category in HTML"
    assert "Terrifying" in html_text, "Missing ending in HTML"
    print("PASSED: Homepage loaded with full HTML template and configuration.")

    # Test 2: Health Endpoint GET /api/health
    print("\n[Test 2] Testing GET /api/health...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    health_data = res.get_json()
    print(f"Health Response: {json.dumps(health_data, indent=2)}")
    assert health_data.get("ollama_running") is True, "Ollama is not running!"
    assert health_data.get("model_available") is True, "Model qwen2.5:3b is not marked available!"
    assert health_data.get("configured_model") == "qwen2.5:3b", "Unexpected model name"
    print("PASSED: Health check verified Ollama is online and qwen2.5:3b is ready.")

    # Test 3: Input Validation POST /api/generate
    print("\n[Test 3] Testing POST /api/generate with empty prompt...")
    res = client.post("/api/generate", json={"prompt": ""})
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    err_data = res.get_json()
    assert err_data.get("success") is False, "Expected success: False"
    print(f"PASSED: Correctly rejected empty prompt with message: {err_data.get('error')}")

    # Test 4: Live Story Generation POST /api/generate
    print("\n[Test 4] Testing End-to-End Story Generation with Ollama...")
    test_payload = {
        "prompt": "An antique pocket watch found in an abandoned asylum begins ticking backward.",
        "category": "Supernatural",
        "ending": "Unexpected Twist"
    }
    t0 = time.time()
    res = client.post("/api/generate", json=test_payload)
    gen_time = round(time.time() - t0, 2)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.get_data(as_text=True)}"
    data = res.get_json()
    assert data.get("success") is True, "Story generation failed!"
    assert "title" in data and len(data["title"]) > 0, "Missing title in story"
    assert "story" in data and len(data["story"]) > 100, "Story content is too short or missing"
    assert data.get("category") == "Supernatural"
    assert data.get("ending") == "Unexpected Twist"
    assert data.get("model") == "qwen2.5:3b"

    print(f"\n Story Generated in {gen_time}s:")
    print(f"Title: {data['title']}")
    print(f"Category: {data['category']} | Ending: {data['ending']} | Model: {data['model']}")
    print(f"Word Count: {data['word_count']} words | Read Time: {data['reading_time_minutes']} min")
    print("-" * 60)
    print(data["story"][:350] + "...\n[Truncated for test log]")
    print("-" * 60)
    print("PASSED: End-to-end story generation succeeded with rich title and content.")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! GHOSTWRITER AI IS FULLY OPERATIONAL.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
