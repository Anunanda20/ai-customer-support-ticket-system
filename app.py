
import os

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_service import generate_support_response

load_dotenv()

app = Flask(__name__)
CORS(app)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():
    """Connect to MySQL using environment variables."""

    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, db_password, db_name]):
        raise RuntimeError(
            "Database configuration is incomplete. "
            "Check DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, and DB_NAME."
        )
    return mysql.connector.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password,
    database=db_name,
    connection_timeout=10,
    use_pure=True,
    ssl_ca=os.path.join(os.path.dirname(__file__), "ca.pem"),
    ssl_verify_cert=True,
)
    


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Customer Support</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f3f6fb;
                color: #1f2937;
            }

            header {
                background: #243b80;
                color: white;
                padding: 24px 20px;
                text-align: center;
            }

            header h1 {
                margin: 0 0 8px;
            }

            header p {
                margin: 0;
            }

            .container {
                max-width: 700px;
                margin: 35px auto;
                padding: 30px;
                background: white;
                border-radius: 14px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
            }

            label {
                display: block;
                margin-top: 18px;
                margin-bottom: 7px;
                font-weight: bold;
            }

            input, textarea, select {
                width: 100%;
                padding: 12px;
                border: 1px solid #cbd5e1;
                border-radius: 7px;
                font-size: 15px;
            }

            textarea {
                min-height: 130px;
                resize: vertical;
            }

            button {
                margin-top: 22px;
                width: 100%;
                padding: 14px;
                background: #243b80;
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #172b63;
            }

            button:disabled {
                opacity: 0.6;
                cursor: wait;
            }

            #result {
                display: none;
                margin-top: 25px;
                padding: 18px;
                border-radius: 8px;
                background: #eff6ff;
                overflow-wrap: anywhere;
                white-space: pre-wrap;
            }

            #result h3 {
                margin-top: 0;
            }

            footer {
                text-align: center;
                padding: 20px;
                color: #64748b;
                font-size: 13px;
            }
        </style>
    </head>

    <body>
        <header>
            <h1>AI Customer Support</h1>
            <p>Smart support ticket management powered by AI</p>
        </header>

        <main class="container">
            <h2>Submit a Support Ticket</h2>
            <p>Describe your issue and our AI assistant will help you.</p>

            <form id="ticketForm">
                <label for="subject">Subject</label>
                <input
                    type="text"
                    id="subject"
                    maxlength="200"
                    placeholder="Example: Unable to log in"
                    required
                >

                <label for="description">Describe your issue</label>
                <textarea
                    id="description"
                    maxlength="5000"
                    placeholder="Explain your problem here..."
                    required
                ></textarea>

                <label for="category">Category</label>
                <select id="category">
                    <option value="Technical">Technical</option>
                    <option value="Account">Account</option>
                    <option value="Billing">Billing</option>
                    <option value="General">General</option>
                </select>

                <label for="priority">Priority</label>
                <select id="priority">
                    <option value="Low">Low</option>
                    <option value="Medium" selected>Medium</option>
                    <option value="High">High</option>
                    <option value="Urgent">Urgent</option>
                </select>

                <button type="submit" id="submitButton">
                    Submit Ticket
                </button>
            </form>

            <section id="result" aria-live="polite"></section>
        </main>

        <footer>
            AI Customer Support System | Portfolio Project
        </footer>

        <script>
            const form = document.getElementById("ticketForm");
            const result = document.getElementById("result");
            const submitButton = document.getElementById("submitButton");

            form.addEventListener("submit", async function(event) {
                event.preventDefault();

                const subject =
                    document.getElementById("subject").value.trim();

                const description =
                    document.getElementById("description").value.trim();

                const category =
                    document.getElementById("category").value;

                const priority =
                    document.getElementById("priority").value;

                if (!subject || !description) {
                    alert("Please enter a subject and describe your issue.");
                    return;
                }

                submitButton.disabled = true;
                submitButton.textContent = "Submitting...";
                result.style.display = "block";
                result.textContent = "Creating your support ticket...";

                try {
                    const ticketResponse = await fetch("/tickets", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            user_id: 1,
                            subject: subject,
                            description: description,
                            category: category,
                            priority: priority
                        })
                    });

                    const ticketData = await ticketResponse.json();

                    if (!ticketResponse.ok) {
                        throw new Error(
                            ticketData.error || "Could not create the ticket."
                        );
                    }

                    result.textContent =
                        "Ticket #" + ticketData.ticket_id +
                        " created. Generating AI response...";

                    const aiResponse = await fetch(
                        "/tickets/" + ticketData.ticket_id + "/ai-response"
                    );

                    const aiData = await aiResponse.json();

                    if (!aiResponse.ok) {
                        throw new Error(
                            aiData.error ||
                            "Ticket created, but the AI response failed."
                        );
                    }

                    result.replaceChildren();

                    const heading = document.createElement("h3");
                    heading.textContent =
                        "AI Support Response — Ticket #" +
                        aiData.ticket_id;

                    const responseText = document.createElement("p");
                    responseText.textContent = aiData.ai_response;

                    result.appendChild(heading);
                    result.appendChild(responseText);

                } catch (error) {
                    result.textContent = "Error: " + error.message;
                } finally {
                    submitButton.disabled = false;
                    submitButton.textContent = "Submit Ticket";
                }
            });
        </script>
    </body>
    </html>
    """


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "AI Customer Support backend is running"
    }), 200


# ==========================================
# REGISTER USER
# ==========================================

@app.route("/register", methods=["POST"])
def register():
    conn = None
    cursor = None

    try:
        data = request.get_json(silent=True) or {}

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not all(
            isinstance(value, str) and value.strip()
            for value in (name, email, password)
        ):
            return jsonify({
                "error": "Name, email and password are required"
            }), 400

        name = name.strip()
        email = email.strip().lower()

        if len(name) > 100 or len(email) > 254 or len(password) > 128:
            return jsonify({
                "error": "One or more fields exceed the allowed length"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # NOTE: This preserves the existing database format.
        # Password hashing must be implemented before real-user deployment.
        cursor.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            """,
            (name, email, password)
        )

        conn.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except mysql.connector.IntegrityError:
        if conn:
            conn.rollback()

        return jsonify({
            "error": "This email may already be registered"
        }), 409

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Registration failed")

        return jsonify({
            "error": "Registration failed. Check server logs."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# ==========================================
# LOGIN USER
# ==========================================

@app.route("/login", methods=["POST"])
def login():
    conn = None
    cursor = None

    try:
        data = request.get_json(silent=True) or {}

        email = data.get("email")
        password = data.get("password")

        if not isinstance(email, str) or not email.strip():
            return jsonify({
                "error": "Email is required"
            }), 400

        if not isinstance(password, str) or not password:
            return jsonify({
                "error": "Password is required"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, name, email, password, role
            FROM users
            WHERE email = %s
            """,
            (email.strip().lower(),)
        )

        user = cursor.fetchone()

        # NOTE: This preserves the existing database format.
        # Replace with password-hash verification before real-user deployment.
        if not user or user["password"] != password:
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
        }), 200

    except Exception:
        app.logger.exception("Login failed")

        return jsonify({
            "error": "Login failed. Check server logs."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# ==========================================
# CREATE SUPPORT TICKET
# ==========================================

@app.route("/tickets", methods=["POST"])
def create_ticket():
    conn = None
    cursor = None

    try:
        data = request.get_json(silent=True) or {}

        user_id = data.get("user_id")
        subject = data.get("subject")
        description = data.get("description")
        category = data.get("category")
        priority = data.get("priority", "Medium")

        if not isinstance(subject, str) or not subject.strip():
            return jsonify({
                "error": "A ticket subject is required"
            }), 400

        if not isinstance(description, str) or not description.strip():
            return jsonify({
                "error": "A ticket description is required"
            }), 400

        if len(subject.strip()) > 200 or len(description.strip()) > 5000:
            return jsonify({
                "error": "Subject or description exceeds the allowed length"
            }), 400

        if isinstance(user_id, bool) or not isinstance(user_id, int) or user_id <= 0:
            return jsonify({
                "error": "A valid user ID is required"
            }), 400

        if category not in ["Technical", "Account", "Billing", "General"]:
            return jsonify({
                "error": "Invalid ticket category"
            }), 400

        if priority not in ["Low", "Medium", "High", "Urgent"]:
            return jsonify({
                "error": "Invalid priority"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO tickets
            (user_id, subject, description, category, priority)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                user_id,
                subject.strip(),
                description.strip(),
                category,
                priority
            )
        )

        ticket_id = cursor.lastrowid
        conn.commit()

        return jsonify({
            "message": "Ticket created successfully",
            "ticket_id": ticket_id
        }), 201

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Ticket creation failed")

        return jsonify({
            "error": "Could not create ticket. Check server logs."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# ==========================================
# GENERATE AI SUPPORT RESPONSE
# ==========================================

@app.route("/ai-support", methods=["POST"])
def ai_support():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message")

        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "error": "Please provide a customer message"
            }), 400

        if len(message) > 5000:
            return jsonify({
                "error": "The customer message is too long"
            }), 400

        response = generate_support_response(message.strip())

        return jsonify({
            "message": "AI response generated successfully",
            "ai_response": response
        }), 200

    except Exception:
        app.logger.exception("AI support failed")

        return jsonify({
            "error": "AI response generation failed. Check server logs."
        }), 500


# ==========================================
# GENERATE AND SAVE TICKET AI RESPONSE
# ==========================================

@app.route("/tickets/<int:ticket_id>/ai-response", methods=["GET"])
def ticket_ai_response(ticket_id):
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT subject, description, category, priority
            FROM tickets
            WHERE id = %s
            """,
            (ticket_id,)
        )

        ticket = cursor.fetchone()

        if not ticket:
            return jsonify({
                "error": "Ticket not found"
            }), 404

        customer_message = (
            f"Subject: {ticket['subject']}\n"
            f"Description: {ticket['description']}\n"
            f"Category: {ticket['category'] or 'Not specified'}\n"
            f"Priority: {ticket['priority']}\n"
        )

        response = generate_support_response(customer_message)

        cursor.execute(
            """
            UPDATE tickets
            SET ai_response = %s
            WHERE id = %s
            """,
            (response, ticket_id)
        )

        conn.commit()

        return jsonify({
            "ticket_id": ticket_id,
            "ai_response": response
        }), 200

    except Exception:
        if conn:
            conn.rollback()

        app.logger.exception("Ticket AI response failed")

        return jsonify({
            "error": "Could not process the ticket. Check server logs."
        }), 500

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
