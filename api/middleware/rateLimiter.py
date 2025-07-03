from flask import request, jsonify 
from functools import wraps
import time

rateLimitWindow = 60 # seconds 
maxRequests = 600 
requestLog = {}

def limiter(func): 
    @wraps(func) 
    def wrapper(*args, **kwargs): 
        ip = request.remote_addr 
        now = time.time()

        if ip not in requestLog:
            requestLog[ip] = []
        requestLog[ip] = [t for t in requestLog[ip] if now - t < rateLimitWindow]

        if len(requestLog[ip]) >= maxRequests:
            return jsonify({"error": "Rate limit exceeded. Versuche es spater noch einmal."}), 429

        requestLog[ip].append(now)
        return func(*args, **kwargs)
    return wrapper