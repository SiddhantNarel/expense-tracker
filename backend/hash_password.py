#!/usr/bin/env python3
"""
Generate a Werkzeug password hash for use as the ADMIN_PASSWORD_HASH environment variable.

Usage:
    python hash_password.py <password>

Example:
    python hash_password.py mysecretpassword
"""
import sys
from werkzeug.security import generate_password_hash

if len(sys.argv) != 2:
    print(f'Usage: python {sys.argv[0]} <password>', file=sys.stderr)
    sys.exit(1)

password = sys.argv[1]
print(generate_password_hash(password))
