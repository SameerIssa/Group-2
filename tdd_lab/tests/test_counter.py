"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status
from flask import json #for test case 3

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    # ===========================
    # Test: Test Increment Counter (PUT/counter/<name>)
    # Author: Ashley Arellano
    # Date: 2025-02-03
    # Description: Ensure that when `put()` increments a given, existing 
    # counter, it produces the correct HTTP response. Otherwise, raises an
    # error. It also raises an error when there is an attempt to 
    # increment a non-existent counter.
    # ===========================
    def test_increment_counter(self,client):
        #Test case 5 when there EXISTS a counter able to be incremented
        name = '/counters/test_case_5_allowed'
        #Create counter 
        client.post(name)
        #Testing increment counter in ALLOWED case
        result = client.put(name)
        assert result.status_code == status.HTTP_200_OK

        #Test case 5 when there is a NO counter able to be incremented
        nameNotExist = '/counters/test_case_5_not_allowed'
        #Testing increment counter in NOT ALLOWED case
        result2 = client.put(nameNotExist)
        assert result2.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_delete_counter(self, client):
        """It should delete a counter"""
        # Create a counter
        client.post('/counters/foo')
        # Delete it
        result = client.delete('/counters/foo')
        # Check deletion 
        assert result.status_code == status.HTTP_204_NO_CONTENT
        # Delete again to check it passes
        result = client.delete('/counters/foo')
        # Check deletion  when counter doesn't exist
        assert result.status_code == status.HTTP_404_NOT_FOUND

