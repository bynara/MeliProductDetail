import unittest
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from unittest.mock import patch, MagicMock
import sys
import os
import time

# Add the parent directory to the path to import the app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    fake_user
)


class TestAuthentication(unittest.TestCase):
    """Test cases for user authentication functions."""
    
    def test_authenticate_user_valid_credentials(self):
        """Test authentication with valid credentials."""
        result = authenticate_user("testuser", "testpass")
        self.assertIsNotNone(result)
        self.assertEqual(result["username"], "testuser")
    
    def test_authenticate_user_invalid_username(self):
        """Test authentication with invalid username."""
        result = authenticate_user("wronguser", "testpass")
        self.assertIsNone(result)
    
    def test_authenticate_user_invalid_password(self):
        """Test authentication with invalid password."""
        result = authenticate_user("testuser", "wrongpass")
        self.assertIsNone(result)
    
    def test_authenticate_user_empty_credentials(self):
        """Test authentication with empty credentials."""
        result = authenticate_user("", "")
        self.assertIsNone(result)


class TestPasswordHashing(unittest.TestCase):
    """Test cases for password hashing and verification functions."""
    
    def test_hash_password_generates_hash(self):
        """Test that hash_password generates a valid hash."""
        password = "testpassword123"
        hashed = hash_password(password)
        
        self.assertIsNotNone(hashed)
        self.assertIsInstance(hashed, str)
        self.assertGreater(len(hashed), 0)
        self.assertNotEqual(hashed, password)  # Should not be the same as plain text
    
    def test_hash_password_different_hashes(self):
        """Test that the same password generates different hashes each time."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        self.assertNotEqual(hash1, hash2)  # Different salts should produce different hashes
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        hashed = hash_password(password)
        
        self.assertTrue(verify_password(password, hashed))
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = hash_password(password)
        
        self.assertFalse(verify_password(wrong_password, hashed))
    
    def test_verify_password_with_fake_user_hash(self):
        """Test password verification with the fake user's stored hash."""
        # The fake user's password is "testpass"
        self.assertTrue(verify_password("testpass", fake_user["password"]))
        self.assertFalse(verify_password("wrongpass", fake_user["password"]))


class TestTokenManagement(unittest.TestCase):
    """Test cases for JWT token creation and validation."""
    
    def test_create_access_token_basic(self):
        """Test basic token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        
        # Decode and verify the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload["sub"], "testuser")
        self.assertIn("exp", payload)
    
    def test_create_access_token_with_custom_expiry(self):
        """Test token creation with custom expiration time."""
        data = {"sub": "testuser"}
        custom_expire = timedelta(minutes=60)
        token = create_access_token(data, expires_delta=custom_expire)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        
        # Should expire in approximately 60 minutes
        time_diff = exp_time - now
        self.assertGreaterEqual(time_diff.total_seconds() / 60, 59)
        self.assertLessEqual(time_diff.total_seconds() / 60, 61)
    
    def test_create_access_token_default_expiry(self):
        """Test token creation with default expiration time."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)
        
        # Should expire in approximately ACCESS_TOKEN_EXPIRE_MINUTES
        time_diff = exp_time - now
        expected_minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        self.assertGreaterEqual(time_diff.total_seconds() / 60, expected_minutes - 1)
        self.assertLessEqual(time_diff.total_seconds() / 60, expected_minutes + 1)
    
    def test_create_access_token_preserves_data(self):
        """Test that token creation preserves all data fields."""
        data = {"sub": "testuser", "role": "admin", "permissions": ["read", "write"]}
        token = create_access_token(data)
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        self.assertEqual(payload["sub"], "testuser")
        self.assertEqual(payload["role"], "admin")
        self.assertEqual(payload["permissions"], ["read", "write"])


class TestGetCurrentUser(unittest.TestCase):
    """Test cases for current user extraction from tokens."""
    
    def test_get_current_user_valid_token(self):
        """Test get_current_user with a valid token."""
        # Create a valid token
        data = {"sub": "testuser"}
        token = create_access_token(data)
        
        # Mock the Depends(oauth2_scheme) to return our token
        result = get_current_user(token)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["username"], "testuser")
    
    def test_get_current_user_invalid_token(self):
        """Test get_current_user with an invalid token."""
        invalid_token = "invalid.token.here"
        
        with self.assertRaises(HTTPException) as context:
            get_current_user(invalid_token)
        
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
        self.assertEqual(context.exception.headers, {"WWW-Authenticate": "Bearer"})
    
    def test_get_current_user_expired_token(self):
        """Test get_current_user with an expired token."""
        # Create an expired token
        data = {"sub": "testuser"}
        expired_delta = timedelta(minutes=-1)  # Already expired
        expired_token = create_access_token(data, expires_delta=expired_delta)
        
        with self.assertRaises(HTTPException) as context:
            get_current_user(expired_token)
        
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
    
    def test_get_current_user_token_without_sub(self):
        """Test get_current_user with a token that doesn't have 'sub' field."""
        # Create a token without 'sub' field
        data = {"user": "testuser"}  # Wrong field name
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        
        with self.assertRaises(HTTPException) as context:
            get_current_user(token)
        
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")
    
    def test_get_current_user_wrong_secret(self):
        """Test get_current_user with a token signed with wrong secret."""
        # Create a token with wrong secret
        data = {"sub": "testuser"}
        wrong_token = jwt.encode(data, "wrong-secret", algorithm=ALGORITHM)
        
        with self.assertRaises(HTTPException) as context:
            get_current_user(wrong_token)
        
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")


class TestSecurityConstants(unittest.TestCase):
    """Test cases for security configuration constants."""
    
    def test_secret_key_exists(self):
        """Test that SECRET_KEY is defined and not empty."""
        self.assertIsNotNone(SECRET_KEY)
        self.assertIsInstance(SECRET_KEY, str)
        self.assertGreater(len(SECRET_KEY), 0)
    
    def test_algorithm_is_valid(self):
        """Test that ALGORITHM is set to a valid value."""
        self.assertEqual(ALGORITHM, "HS256")
    
    def test_access_token_expire_minutes_is_positive(self):
        """Test that ACCESS_TOKEN_EXPIRE_MINUTES is a positive integer."""
        self.assertIsInstance(ACCESS_TOKEN_EXPIRE_MINUTES, int)
        self.assertGreater(ACCESS_TOKEN_EXPIRE_MINUTES, 0)
    
    def test_fake_user_structure(self):
        """Test that fake_user has the required structure."""
        self.assertIsInstance(fake_user, dict)
        self.assertIn("username", fake_user)
        self.assertIn("password", fake_user)
        self.assertIsInstance(fake_user["username"], str)
        self.assertIsInstance(fake_user["password"], str)
        self.assertGreater(len(fake_user["username"]), 0)
        self.assertGreater(len(fake_user["password"]), 0)


class TestIntegration(unittest.TestCase):
    """Integration test cases combining multiple security functions."""
    
    def test_full_auth_flow(self):
        """Test a complete authentication flow."""
        # 1. Authenticate user
        user = authenticate_user("testuser", "testpass")
        self.assertIsNotNone(user)
        
        # 2. Create token for authenticated user
        token = create_access_token({"sub": user["username"]})
        self.assertIsNotNone(token)
        
        # 3. Verify token and get current user
        current_user = get_current_user(token)
        self.assertEqual(current_user["username"], user["username"])
    
    def test_password_hash_and_verify_cycle(self):
        """Test the complete password hashing and verification cycle."""
        original_password = "my_secure_password_123"
        
        # Hash the password
        hashed = hash_password(original_password)
        
        # Verify the password
        self.assertTrue(verify_password(original_password, hashed))
        self.assertFalse(verify_password("wrong_password", hashed))
    
    def test_token_lifecycle(self):
        """Test token creation, validation, and expiration."""
        data = {"sub": "testuser", "role": "user"}
        
        # Create token with short expiry
        short_expire = timedelta(seconds=1)
        token = create_access_token(data, expires_delta=short_expire)
        
        # Token should be valid immediately
        current_user = get_current_user(token)
        self.assertEqual(current_user["username"], "testuser")
        
        # Wait for token to expire and test
        time.sleep(2)
        
        with self.assertRaises(HTTPException) as context:
            get_current_user(token)
        
        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main(verbosity=2)
