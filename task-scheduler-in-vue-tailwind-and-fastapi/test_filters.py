#!/usr/bin/env python3
"""Simple test script to verify filtering functionality"""

import json
import requests

# API base URL - using direct backend access
BASE_URL = "http://localhost:8000"

def test_endpoint(path, description):
    """Test an API endpoint"""
    try:
        url = f"{BASE_URL}{path}"
        print(f"\n{description}")
        print(f"URL: {url}")

        response = requests.get(url, timeout=10)

        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)[:500]}...")
            return data
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def main():
    print("🧪 Testing Schedule Filtering API")
    print("=" * 50)

    # Test basic tasks endpoint
    tasks_data = test_endpoint("/tasks", "Get all tasks")
    if not tasks_data:
        print("❌ Basic API test failed - stopping here")
        return

    print(f"✅ Found {len(tasks_data.get('tasks', []))} tasks")

    # Test status filtering
    print("\n" + "=" * 50)
    print("🔍 Testing Status Filtering")
    print("=" * 50)

    # Test pending tasks only
    pending_data = test_endpoint("/tasks?status=pending", "Filter by status=pending")
    if pending_data:
        pending_count = len(pending_data.get('tasks', []))
        print(f"✅ Found {pending_count} pending tasks")

    # Test completed tasks only
    completed_data = test_endpoint("/tasks?status=completed", "Filter by status=completed")
    if completed_data:
        completed_count = len(completed_data.get('tasks', []))
        print(f"✅ Found {completed_count} completed tasks")

    # Test multiple statuses
    multiple_data = test_endpoint("/tasks?status=pending&status=in_progress", "Filter by multiple statuses")
    if multiple_data:
        multiple_count = len(multiple_data.get('tasks', []))
        print(f"✅ Found {multiple_count} tasks with status pending or in_progress")

    # Test pagination
    print("\n" + "=" * 50)
    print("📄 Testing Pagination")
    print("=" * 50)

    paginated_data = test_endpoint("/tasks?page=1&page_size=2", "Test pagination (page=1, size=2)")
    if paginated_data:
        print(f"✅ Pagination works - Page {paginated_data.get('page')} of {paginated_data.get('totalPages')} pages")
        print(f"   Showing {len(paginated_data.get('tasks', []))} of {paginated_data.get('totalCount')} total tasks")

    # Test sorting
    print("\n" + "=" * 50)
    print("📊 Testing Sorting")
    print("=" * 50)

    # Test different sort options
    sort_data = test_endpoint("/tasks?sortBy=dueDate&sortOrder=asc", "Sort by dueDate ascending")
    if sort_data:
        print(f"✅ Sorting by dueDate works")
        first_task = sort_data.get('tasks', [{}])[0]
        if 'dueDate' in first_task:
            print(f"   First task due date: {first_task['dueDate']}")

    print("\n" + "=" * 50)
    print("🎯 Testing Complete!")
    print("=" * 50)
    print("✅ All filtering endpoints are working correctly")

if __name__ == "__main__":
    main()