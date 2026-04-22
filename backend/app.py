from flask import Flask, request, jsonify, abort, render_template
import time
import uuid
import posixpath

app = Flask(__name__)

# ==========================================
# VULNERABLE MIDDLEWARE SIMULATOR
# ==========================================
@app.before_request
def simulate_backend_quirks():
    """
    Simulates various backend framework routing quirks (Spring Boot, IIS, etc.)
    that differ from how Nginx parses the URI.
    """
    path = request.environ.get('PATH_INFO', '')

    # Ch 8: Ghost Request (Middleware routing via Header)
    override = request.headers.get('X-Original-URL')
    if override:
        path = override

    # Ch 3: Simulate Spring Boot Matrix Variables
    # Drops anything after a ';' in a path segment
    if ';' in path:
        parts = path.split('/')
        cleaned_parts = [p.split(';')[0] for p in parts]
        path = '/'.join(cleaned_parts)

    # Ch 4: Simulate IIS / Windows Case-Insensitivity
    path = path.lower()

    # Resolve directory traversal (.../a/../b -> .../b)
    path = posixpath.normpath(path)
    
    # Update the environment so Flask routes based on the mutated path
    request.environ['PATH_INFO'] = path

# ==========================================
# LANDING PAGE ROUTE
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

# ==========================================
# CHALLENGE ROUTES
# ==========================================

@app.route('/')
def index():
    return jsonify({
        "welcome": "Welcome to the 403Override Practice Lab",
        "author": "WriteupDB Academy",
        "status": "Ready for Fuzzing"
    })

# Challenge 1: The Localhost Trust (Phase 1)
@app.route('/api/v1/admin')
def ch1_admin():
    client_ip = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    if client_ip in ['127.0.0.1', 'localhost']:
        return jsonify({"flag": "WriteupDB{phase1_header_bypass_successful}"})
    abort(403, description="Admin access requires local IP.")

# Challenge 2: The Trailing Illusion (Phase 2)
# Nginx blocks exact '/metrics'. Flask normpath turns '/metrics/' into '/metrics'
@app.route('/metrics')
def ch2_metrics():
    return jsonify({"flag": "WriteupDB{trailing_slash_illusion_broken}"})

# Challenge 3: Proxy Confusion (Phase 3)
@app.route('/api/internal/users')
def ch3_internal_users():
    return jsonify({"flag": "WriteupDB{parser_normalization_exploited}"})

# Challenge 4: The Lazy Filter (Phase 4)
# Nginx regex is case sensitive. Flask middleware lowercases everything.
@app.route('/secret-vault')
def ch4_lazy_filter():
    return jsonify({"flag": "WriteupDB{case_mutation_bypassed_waf}"})

# Challenge 5: Method Tampering
@app.route('/debug/logs', methods=['GET', 'POST', 'PUT'])
def ch5_method_tampering():
    if request.method == 'GET':
        abort(403, description="GET method not allowed for logs.")
    return jsonify({"flag": "WriteupDB{method_tampering_wins}"})

# Challenge 6: The Dynamic Trap (Test your Regex Config)
@app.route('/forbidden')
def ch6_dynamic_trap():
    return f"Access Denied. Request Time: {time.time()}", 403

# Challenge 7: The Shifting Sentinel (Phase 1 + 6)
@app.route('/api/v2/admin')
def ch7_shifting_sentinel():
    client_ip = request.headers.get('X-Real-IP', request.remote_addr)
    if client_ip in ['127.0.0.1', 'localhost']:
        return jsonify({"flag": "WriteupDB{master_of_headers_and_regex}"})
    
    tracking_id = uuid.uuid4().hex + uuid.uuid4().hex
    return f"403 Forbidden. Event logged. Trace ID: {tracking_id}", 403

# Challenge 8: The Ghost Request (Phase 1 - Header Routing)
@app.route('/system/config')
def ch8_ghost_request():
    return jsonify({"flag": "WriteupDB{phantom_routing_via_header}"})

# Challenge 9: The Double Encoding Maze (Phase 4)
# WSGI automatically URL-decodes paths. So /%76ault -> /vault
@app.route('/vault')
def ch9_double_encoding():
    return jsonify({"flag": "WriteupDB{double_decode_wizards}"})

# Custom 403 Error Handler to keep responses clean
@app.errorhandler(403)
def custom_403(error):
    return str(error.description) if error.description else "403 Forbidden - Backend Application", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)